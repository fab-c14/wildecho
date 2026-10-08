"""
WildEcho Configuration Module
Powered by Pydantic Settings for type-safe offline edge settings.
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class WildEchoSettings(BaseSettings):
    """Configuration settings for WildEcho bioacoustics and edge reasoning."""

    model_config = SettingsConfigDict(env_prefix="WILDECHO_", env_file=".env", extra="ignore")

    # Audio Signal Processing Parameters
    sample_rate: int = 22050
    analysis_window_seconds: float = 3.0
    biophony_low_hz: float = 2000.0
    biophony_high_hz: float = 8000.0
    anthrophony_low_hz: float = 200.0
    anthrophony_high_hz: float = 2000.0

    # Detection & Matching Thresholds
    confidence_threshold: float = 0.55
    min_biophony_ratio: float = 0.15

    # Edge AI (Google Gemma 2 Core)
    gemma_model: str = "gemma-2-2b-it"
    gemma_temperature: float = 0.3
    offline_mode: bool = True
    ollama_endpoint: str = "http://localhost:11434"

    # Eyes-Free Audio Narration
    tts_engine: str = "local_naturalist"
    elevenlabs_api_key: str | None = None
    elevenlabs_voice_id: str = "pNInz6obpgDQGcFmaJgB"  # Naturalist voice
    whisper_speed: float = 1.0

    # Expedition Storage
    expeditions_dir: Path = Path("expeditions")
    data_dir: Path = Path("data")


settings = WildEchoSettings()
