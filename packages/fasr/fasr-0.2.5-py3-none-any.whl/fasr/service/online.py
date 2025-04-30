from asyncio import Queue
from pathlib import Path
import time
import asyncio
import traceback
from urllib.parse import parse_qs
from typing import Literal

from funasr import AutoModel
from loguru import logger
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from pydantic import BaseModel, Field, ConfigDict

from fasr.config import registry
from fasr.data import Waveform
from fasr.models.stream_asr.base import StreamASRModel
from .schema import AudioChunk, TranscriptionResponse


class RealtimeASRService(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True, validate_assignment=True, extra="ignore"
    )

    host: str = Field("127.0.0.1", description="服务地址")
    port: int = Field(27000, description="服务端口")
    device: Literal["cpu", "cuda", "mps"] = Field("cpu", description="设备")
    asr_model_name: Literal["stream_sensevoice", "stream_paraformer"] = Field(
        "stream_paraformer", description="流式asr模型"
    )
    asr_checkpoint_dir: str | Path | None = Field(
        None,
        description="asr模型路径",
    )
    asr_model: StreamASRModel = Field(None, description="asr模型")
    vad_model: AutoModel = Field(None, description="vad模型")
    vad_chunk_size_ms: int = Field(100, description="音频分片大小")
    vad_end_silence_ms: int = Field(200, description="vad判定音频片段结束最大静音时间")
    sample_rate: int = Field(16000, description="音频采样率")
    bit_depth: int = Field(16, description="音频位深")
    channels: int = Field(1, description="音频通道数")

    def setup(self):
        app = FastAPI()
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        logger.info(
            f"Start online ASR Service on {self.host}:{self.port}, device: {self.device}"
        )

        self.asr_model = registry.stream_asr_models.get(self.asr_model_name)()
        self.asr_model.from_checkpoint(
            checkpoint_dir=self.asr_checkpoint_dir,
            device=self.device,
        )

        self.vad_model = AutoModel(
            model=str(Path(__file__).parent.parent / "asset" / "fsmn-vad"),
            disable_update=True,
            disable_log=True,
            disable_pbar=True,
            max_end_silence_time=self.vad_end_silence_ms,
        )

        @app.websocket("/asr/realtime")
        async def transcribe(ws: WebSocket):
            try:
                # 解析请求参数
                await ws.accept()
                query_params = parse_qs(ws.scope["query_string"].decode())
                itn = query_params.get("itn", ["false"])[0].lower() == "true"
                model = query_params.get("model", ["paraformer"])[0].lower()
                chunk_size = int(self.vad_chunk_size_ms * self.sample_rate / 1000)
                logger.info(f"itn: {itn}, chunk_size: {chunk_size}, model: {model}")
                waveform_queue = Queue()
                tasks = []
                tasks.append(
                    asyncio.create_task(
                        self.vad_task(ws, waveform_queue=waveform_queue)
                    )
                )
                tasks.append(
                    asyncio.create_task(
                        self.asr_task(ws=ws, waveform_queue=waveform_queue)
                    )
                )
                await asyncio.gather(
                    *tasks,
                )
            except WebSocketDisconnect:
                logger.info("WebSocket disconnected")
            except Exception as e:
                logger.error(
                    f"Unexpected error: {e}\nCall stack:\n{traceback.format_exc()}"
                )
                await ws.close()
            finally:
                logger.info("Cleaned up resources after WebSocket disconnect")

        uvicorn.run(app, host=self.host, port=self.port, ws="wsproto")

    async def vad_task(self, ws: WebSocket, waveform_queue: Queue):
        chunk_size = int(self.vad_chunk_size_ms * self.sample_rate / 1000)
        cache: dict = {}
        bytes_buffer = b""
        audio_buffer = np.array([], dtype=np.float32)
        audio_data = np.array([], dtype=np.float32)
        offset = 0
        is_detected = False
        while True:
            try:
                raw_data = await ws.receive()
            except Exception as e:
                logger.error(f"Error receiving data: {e}")
                break
            bytes_data = raw_data.get("bytes", None)
            if bytes_data is None:
                logger.warning("No data received")
                continue
            bytes_buffer += bytes_data
            if len(bytes_buffer) < 2:
                continue
            valid_len = len(bytes_buffer) - (len(bytes_buffer) % 2)
            audio_buffer = np.append(
                audio_buffer,
                np.frombuffer(
                    bytes_buffer[:valid_len],
                    dtype=np.int16,
                ).astype(np.float32)
                / 32767.0,
            )
            bytes_buffer = bytes_buffer[valid_len:]
            while len(audio_buffer) >= chunk_size:
                chunk = audio_buffer[:chunk_size]
                audio_buffer = audio_buffer[chunk_size:]
                audio_data = np.append(audio_data, chunk)
                start = time.perf_counter()
                segments = self.vad_model.generate(
                    input=chunk,
                    cache=cache,
                    fs=self.sample_rate,
                    is_final=False,
                    chunk_size=self.vad_chunk_size_ms,
                )[0]["value"]
                end = time.perf_counter()
                if len(segments) > 0:
                    logger.info(f"segments: {segments}, time: {round(end - start, 3)}s")
                    start, end = segments[0]
                    if start != -1 and end == -1:
                        is_detected = True
                        start_idx = start * self.sample_rate // 1000
                        end_idx = offset + len(chunk)
                        waveform = Waveform(
                            data=audio_data[start_idx:end_idx],
                            sample_rate=self.sample_rate,
                        )
                        await self.send_response("", ws, "segment_start")
                        await waveform_queue.put((waveform, "segment_start"))
                        logger.info("vad state: segment_start")

                    if start == -1 and end != -1:
                        is_detected = False
                        start_idx = offset
                        end_idx = end * self.sample_rate // 1000

                        waveform = Waveform(
                            data=audio_data[start_idx:end_idx],
                            sample_rate=self.sample_rate,
                        )
                        await self.send_response("", ws, "segment_end")
                        await waveform_queue.put((waveform, "segment_end"))
                        logger.info("vad state: segment_end")

                else:
                    if is_detected:
                        waveform = Waveform(data=chunk, sample_rate=self.sample_rate)
                        await waveform_queue.put((waveform, "segment_mid"))
                        # logger.info("vad state: segment_mid")

                offset += len(chunk)

    async def asr_task(self, waveform_queue: Queue, ws: WebSocket):
        cache = {}
        while True:
            waveform, vad_state = await waveform_queue.get()
            if waveform is None:
                break
            is_last = vad_state == "segment_end"
            if is_last:
                final_text = ""
                for span in self.asr_model.transcribe_chunk(
                    waveform=waveform, is_last=True, state=cache
                ):
                    final_text += span.text

                await self.send_response(final_text, ws, "final_transcript")
                logger.info(f"asr state: final_transcript, text: {final_text}")
            else:
                for span in self.asr_model.transcribe_chunk(
                    waveform=waveform, is_last=False, state=cache
                ):
                    await self.send_response(span.text, ws, "interim_transcript")
                    logger.info(f"asr state: interim_transcript, text: {span.text}")
            waveform_queue.task_done()

    async def send_response(self, text: str, ws: WebSocket, state: str):
        response = TranscriptionResponse(data=AudioChunk(text=text, state=state))
        await ws.send_json(response.model_dump())
