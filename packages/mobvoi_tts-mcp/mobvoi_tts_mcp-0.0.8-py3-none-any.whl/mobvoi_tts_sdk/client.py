import typing
import json
import re
import os
import httpx

from typing import Iterator, Optional
from .text_to_speech import TextToSpeechClient

DEFAULT_SPAEKER = "xiaoyi_meet"

class MobvoiTTS:
    def __init__(
        self,
        *,
        app_key: typing.Optional[str] = None,
        app_secret: typing.Optional[str] = None,
        httpx_client: typing.Optional[httpx.Client] = None
    ):
        self.text_to_speech = TextToSpeechClient(app_key=app_key, app_secret=app_secret, text2speech_client=httpx_client)
    
    def generate(
        self,
        *,
        text: str,
        speaker: typing.Optional[str] = DEFAULT_SPAEKER,
        audio_type: Optional[str] = "mp3",
        speed: Optional[float] = 1.0,
        rate: Optional[int] = 24000,
        volume: Optional[float] = 1.0,
        pitch: Optional[float] = 0,
        streaming: Optional[bool] = False,
    ):
        return self.text_to_speech.convert_with_timestamps(
            text=text,
            speaker=speaker,
            audio_type=audio_type,
            speed=speed,
            rate=rate,
            volume=volume,
            pitch=pitch,
            streaming=streaming
        )