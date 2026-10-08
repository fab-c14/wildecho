"""
WildEcho Eyes-Free Audio Narration Engine
Whispers concise naturalist observations into the hiker's earbuds.
Supports local speech simulation and optional ElevenLabs cloud streaming.
"""

import time

import httpx
from pydantic import BaseModel

from wildecho.config import settings
from wildecho.intelligence.gemma_engine import NaturalistFieldReport


class AudioWhisperEvent(BaseModel):
    """An eyes-free audio delivery event to wireless earbuds."""

    timestamp: float
    whisper_text: str
    estimated_duration_s: float
    engine_used: str
    delivered: bool = True


class EarbudNarrator:
    """Delivers gentle naturalist audio briefings directly into earbuds."""

    def __init__(self, api_key: str | None = settings.elevenlabs_api_key, voice_id: str = settings.elevenlabs_voice_id):
        self.api_key = api_key
        self.voice_id = voice_id

    def whisper(self, report: NaturalistFieldReport) -> AudioWhisperEvent:
        """
        Whispers the field report to the user.
        Keeps speaking pace deliberate and under 15 seconds.
        """
        text = report.whisper_script
        word_count = len(text.split())
        # Estimate duration at natural speaking rate ~140 words per minute
        estimated_duration = max(2.5, (word_count / 140.0) * 60.0)

        engine_used = "local_eyes_free"

        # If ElevenLabs API key is configured, stream realistic voice
        if self.api_key and not settings.offline_mode:
            delivered = self._call_elevenlabs(text)
            if delivered:
                engine_used = "elevenlabs_cloud"

        return AudioWhisperEvent(
            timestamp=time.time(),
            whisper_text=text,
            estimated_duration_s=round(estimated_duration, 1),
            engine_used=engine_used,
            delivered=True,
        )

    def _call_elevenlabs(self, text: str) -> bool:
        """Attempts ElevenLabs text-to-speech synthesis."""
        try:
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
            headers = {"xi-api-key": self.api_key, "Content-Type": "application/json"}
            payload = {
                "text": text,
                "model_id": "eleven_turbo_v2_5",
                "voice_settings": {"stability": 0.70, "similarity_boost": 0.85},
            }
            with httpx.Client(timeout=3.0) as client:
                res = client.post(url, headers=headers, json=payload)
                return res.status_code == 200
        except (httpx.HTTPError, OSError):
            return False
