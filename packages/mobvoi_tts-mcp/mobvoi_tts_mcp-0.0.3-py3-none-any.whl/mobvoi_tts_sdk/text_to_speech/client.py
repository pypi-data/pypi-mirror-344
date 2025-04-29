import os, sys
import typing
import httpx
import json
import time
import hashlib

class TextToSpeechClient:
    def __init__(self, *, app_key: str, app_secret: str, text2speech_client: httpx.Client):
        self._client = text2speech_client
        self._timestamp = str(int(time.time()))
        self._app_key = app_key
        self._app_secret = app_secret
        message = '+'.join([self._app_key, self._app_secret, self._timestamp])
        m = hashlib.md5()
        m.update(message.encode("utf8"))
        self._signature = m.hexdigest()
        
    def convert_with_timestamps(
        self,
        *,
        text: str,
        speaker: typing.Optional[str] = None,
        audio_type: typing.Optional[str] = None,
        speed: typing.Optional[str] = None,
        rate: typing.Optional[int] = 24000,
        volume: typing.Optional[float] = 1.0,
        pitch: typing.Optional[float] = 0,
        streaming: typing.Optional[bool] = False,
    ):
        request_data = {
            'text': text,
            'speaker': speaker,
            'audio_type': audio_type,
            'speed': speed,
            'rate': rate,
            'volume': volume,
            'pitch': pitch,
            'streaming': streaming,
            'gen_srt': False,
            'appkey': self._app_key,
            'timestamp': self._timestamp,
            'signature': self._signature,
            
        }
        print(f"request_data: {request_data}")
        _response = self._client.request(
            method="POST",
            url="https://open.mobvoi.com/api/tts/v1",    
            headers={
                "content-type": "application/json",
            },
            data= json.dumps(request_data)
        )
        
        return _response.content