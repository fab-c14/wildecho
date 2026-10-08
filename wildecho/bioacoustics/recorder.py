"""
WildEcho Soundscape Recorder & Synthesizer Harness
Captures real-time audio or synthesizes backcountry soundscapes for offline evaluation.
Enables field testing without requiring physical outdoor hardware connected.
"""

from collections.abc import Generator

import numpy as np

from wildecho.bioacoustics.catalog import SPECIES_CATALOG, SpeciesSignature
from wildecho.config import settings


class SoundscapeSynthesizer:
    """Generates physically modeled backcountry audio buffers for testing."""

    def __init__(self, sample_rate: int = settings.sample_rate):
        self.sample_rate = sample_rate

    def generate_wind_and_stream(self, duration_s: float, intensity: float = 0.15) -> np.ndarray:
        """Generates geophony backdrop: low-frequency wind and stream noise.

        In acoustic ecology (Pijanowski et al. 2011), geophony (wind, water)
        concentrates below ~1.5 kHz, leaving the biophony band (2–11 kHz) clean
        for wildlife vocalizations. A 4th-order Butterworth low-pass at 1200 Hz
        enforces this physical constraint so ACI correctly ranks wildlife calls
        above flat ambient noise.
        """
        from scipy import signal as scipy_signal

        samples = int(self.sample_rate * duration_s)
        # White noise base
        white = np.random.normal(0, 1, samples)
        # Pink the noise with the classic IIR shaping filter
        b_pink = [0.049922035, -0.095993537, 0.050612699, -0.004408786]
        a_pink = [1, -2.494956002, 2.017265875, -0.522189400]
        pink = scipy_signal.lfilter(b_pink, a_pink, white)
        # Apply geophony low-pass: strict cutoff at 1200 Hz (well below biophony floor)
        nyq = self.sample_rate / 2.0
        sos = scipy_signal.butter(4, 1200.0 / nyq, btype="low", output="sos")
        geo = scipy_signal.sosfilt(sos, pink)
        return (geo / (np.max(np.abs(geo)) + 1e-9)) * intensity

    def generate_species_call(self, species: SpeciesSignature, duration_s: float) -> np.ndarray:
        """Synthesizes harmonic bioacoustic call matching a species profile."""
        samples = int(self.sample_rate * duration_s)
        t = np.linspace(0, duration_s, samples, endpoint=False)
        audio = np.zeros(samples)

        # Base cadence envelope
        cadence = max(0.5, species.typical_cadence_hz)
        envelope = np.maximum(0.0, np.sin(2.0 * np.pi * cadence * t)) ** 3

        # Fundamental frequency with proper instantaneous phase integration (vibrato)
        f0 = species.peak_freq_hz
        base_phase = 2.0 * np.pi * f0 * t + 0.5 * np.sin(2.0 * np.pi * 3.5 * t)

        # Add fundamental and harmonics
        for h in range(1, species.harmonic_count + 1):
            h_amp = (1.0 / h) * 0.4
            audio += h_amp * np.sin(base_phase * h)

        return audio * envelope

    def generate_soundscape_scene(
        self, duration_s: float = 3.0, species_ids: list[str] | None = None, anthro_noise_level: float = 0.0
    ) -> np.ndarray:
        """Combines ambient stream/canopy noise with specific wildlife vocalizations."""
        samples = int(self.sample_rate * duration_s)
        audio = self.generate_wind_and_stream(duration_s, intensity=0.10)

        # Add human mechanical anthrophony rumble (e.g. distant road) if specified
        if anthro_noise_level > 0.0:
            t = np.linspace(0, duration_s, samples, endpoint=False)
            low_drone = np.sin(2.0 * np.pi * 320.0 * t) * anthro_noise_level
            audio += low_drone

        # Inject species calls
        if species_ids:
            for sp_id in species_ids:
                matching = [s for s in SPECIES_CATALOG if s.id == sp_id]
                if matching:
                    sp_audio = self.generate_species_call(matching[0], duration_s)
                    audio += sp_audio * 0.60

        # Normalize to prevent digital clipping
        peak = np.max(np.abs(audio))
        if peak > 0.95:
            audio = audio / peak * 0.95

        return audio


class SoundscapeStreamer:
    """Streams continuous audio windows for real-time field evaluation."""

    def __init__(self, sample_rate: int = settings.sample_rate):
        self.sample_rate = sample_rate
        self.synthesizer = SoundscapeSynthesizer(sample_rate)

    def stream_windows(
        self, habitat: str = "dense_forest", season: str = "autumn", steps: int = 5
    ) -> Generator[tuple[int, np.ndarray, list[str]], None, None]:
        """
        Yields simulated audio windows representing a walk along a nature trail.
        Each window simulates ambient shifts and intermittent wildlife encounters.
        """
        # Habitat-specific species pools
        habitat_species = {
            "dense_forest": ["wood_thrush", "pileated_woodpecker", "barred_owl", "katydid"],
            "riparian_stream": ["pacific_tree_frog", "belted_kingfisher", "american_bullfrog"],
            "mountain_trail": ["hermit_thrush", "rocky_mountain_elk", "common_raven", "red_tailed_hawk"],
            "open_meadow": ["black_capped_chickadee", "red_tailed_hawk", "katydid"],
        }

        active_pool = habitat_species.get(habitat, ["wood_thrush", "black_capped_chickadee"])

        for step in range(1, steps + 1):
            # Select species for this window (some windows are quiet nature)
            if step % 2 == 1 and active_pool:
                chosen_species = [active_pool[(step - 1) % len(active_pool)]]
            elif step % 4 == 0:
                # Occasional two-species chorus
                chosen_species = active_pool[:2]
            else:
                chosen_species = []

            # Occasional distant anthrophony near trailheads (step 1)
            anthro_level = 0.08 if step == 1 else 0.0

            audio = self.synthesizer.generate_soundscape_scene(
                duration_s=settings.analysis_window_seconds, species_ids=chosen_species, anthro_noise_level=anthro_level
            )
            yield step, audio, chosen_species
