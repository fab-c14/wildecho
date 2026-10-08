"""
WildEcho Bioacoustics Signal Processing Engine
Fast, offline mathematical soundscape analysis powered by NumPy and SciPy.
Computes NDSI, ACI, spectral centroid, and matches wildlife acoustic fingerprints.
"""

import numpy as np
from pydantic import BaseModel, Field
from scipy import signal

from wildecho.bioacoustics.catalog import SPECIES_CATALOG, SpeciesSignature
from wildecho.config import settings


class SpeciesMatch(BaseModel):
    """Biometric match of a detected species in the soundscape."""

    species: SpeciesSignature
    confidence: float = Field(ge=0.0, le=1.0)
    peak_detected_hz: float
    snr_db: float


class AcousticAnalysisResult(BaseModel):
    """Structured result of an offline soundscape window analysis."""

    ndsi: float = Field(description="Normalized Difference Soundscape Index (-1.0 to +1.0)")
    aci: float = Field(description="Acoustic Complexity Index")
    peak_freq_hz: float
    spectral_centroid_hz: float
    biophony_energy: float
    anthrophony_energy: float
    soundscape_rating: str
    matches: list[SpeciesMatch] = Field(default_factory=list)


class BioacousticAnalyzer:
    """Offline soundscape and biological acoustic analysis engine."""

    def __init__(self, sample_rate: int = settings.sample_rate):
        self.sample_rate = sample_rate

    def compute_spectrum(self, audio_data: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Computes Power Spectral Density using Welch's method."""
        if len(audio_data) < 256:
            audio_data = np.pad(audio_data, (0, 256 - len(audio_data)))

        freqs, psd = signal.welch(
            audio_data, fs=self.sample_rate, nperseg=min(1024, len(audio_data)), scaling="density"
        )
        return freqs, psd

    def calculate_ndsi(self, freqs: np.ndarray, psd: np.ndarray) -> tuple[float, float, float]:
        """
        Calculates Normalized Difference Soundscape Index (NDSI).
        NDSI = (Biophony - Anthrophony) / (Biophony + Anthrophony)
        +1.0 = Pristine pure biological soundscape
        -1.0 = Dominant mechanical anthrophony
        """
        # Anthrophony band: 200 Hz - 2000 Hz
        anthro_mask = (freqs >= settings.anthrophony_low_hz) & (freqs < settings.anthrophony_high_hz)
        # Biophony band: 2000 Hz - 8000 Hz
        bio_mask = (freqs >= settings.biophony_low_hz) & (freqs <= settings.biophony_high_hz)

        anthro_energy = float(np.sum(psd[anthro_mask]))
        bio_energy = float(np.sum(psd[bio_mask]))

        total = bio_energy + anthro_energy
        if total <= 1e-12:
            return 0.0, bio_energy, anthro_energy

        ndsi = (bio_energy - anthro_energy) / total
        return float(np.clip(ndsi, -1.0, 1.0)), bio_energy, anthro_energy

    def calculate_aci(self, audio_data: np.ndarray) -> float:
        """
        Calculates Acoustic Complexity Index (ACI).
        Quantifies variability of sound intensities across frequency bins over time.
        High ACI = rich animal vocalizations with dynamic frequency hops.
        Low ACI = flat wind, constant drone, or static.
        """
        if len(audio_data) < 1024:
            return 0.0

        # Compute spectrogram
        f, _t, sxx = signal.spectrogram(audio_data, fs=self.sample_rate, nperseg=512, noverlap=256)

        # Restrict to biophony frequency range
        bio_mask = (f >= settings.biophony_low_hz) & (f <= settings.biophony_high_hz)
        if not np.any(bio_mask) or sxx.shape[1] < 2:
            return 0.0

        bio_sxx = sxx[bio_mask, :]
        # Absolute difference between adjacent temporal frames
        diff = np.abs(np.diff(bio_sxx, axis=1))
        sum_intensity = np.sum(bio_sxx, axis=1)

        # Require minimum biophony intensity per frequency bin (rejects stopband numerical noise)
        valid = sum_intensity > 1e-5
        if not np.any(valid):
            return 0.0

        aci_per_bin = np.sum(diff[valid, :], axis=1) / sum_intensity[valid]
        return float(np.mean(aci_per_bin) * 100.0)

    def calculate_spectral_centroid(self, freqs: np.ndarray, psd: np.ndarray) -> float:
        """Calculates the center of mass of the frequency spectrum."""
        total_energy = np.sum(psd)
        if total_energy <= 1e-12:
            return 0.0
        return float(np.sum(freqs * psd) / total_energy)

    def match_species(
        self,
        freqs: np.ndarray,
        psd: np.ndarray,
        aci: float,
        current_habitat: str | None = None,
        current_season: str | None = None,
    ) -> list[SpeciesMatch]:
        """
        Matches detected acoustic energy peaks against offline species database.
        Applies habitat & seasonal Bayesian priors when available.
        """
        matches: list[SpeciesMatch] = []
        if len(psd) == 0:
            return matches

        # Baseline noise floor and global peak estimate
        noise_floor = np.median(psd)
        if noise_floor <= 1e-12:
            noise_floor = 1e-9

        global_peak_power = float(np.max(psd))
        global_peak_freq = float(freqs[np.argmax(psd)])

        for sp in SPECIES_CATALOG:
            # Check frequency window
            band_mask = (freqs >= sp.min_freq_hz) & (freqs <= sp.max_freq_hz)
            if not np.any(band_mask):
                continue

            band_psd = psd[band_mask]
            band_freqs = freqs[band_mask]

            max_val = float(np.max(band_psd))
            peak_freq = float(band_freqs[np.argmax(band_psd)])

            # Relative power dominance compared to global peak
            dominance = max_val / (global_peak_power + 1e-12)

            # Signal-to-noise ratio in species band
            snr = max_val / noise_floor
            snr_db = float(10.0 * np.log10(max(snr, 1.0)))

            # Frequency proximity to species signature peak
            freq_diff = abs(peak_freq - sp.peak_freq_hz)
            freq_tolerance = (sp.max_freq_hz - sp.min_freq_hz) * 0.5
            freq_score = max(0.0, 1.0 - (freq_diff / freq_tolerance))

            # Fundamental alignment: bonus if global soundscape peak is within this species' band
            fundamental_bonus = 1.25 if (sp.min_freq_hz <= global_peak_freq <= sp.max_freq_hz) else 0.80

            # ACI modulation score (complex calls vs steady noise)
            aci_score = min(1.0, aci / 40.0) if aci > 5.0 else 0.3

            # Environmental priors
            prior = 1.0
            if current_habitat and current_habitat in sp.habitats:
                prior += 0.25
            if current_season and current_season in sp.seasons:
                prior += 0.20

            # Combined confidence score weighted by power dominance
            raw_score = freq_score * 0.40 + min(snr_db / 20.0, 1.0) * 0.25 + dominance * 0.20 + aci_score * 0.15
            confidence = raw_score * fundamental_bonus * (prior / 1.45)
            confidence = float(np.clip(confidence, 0.0, 0.98))

            if confidence >= settings.confidence_threshold:
                matches.append(
                    SpeciesMatch(
                        species=sp,
                        confidence=round(confidence, 3),
                        peak_detected_hz=round(float(peak_freq), 1),
                        snr_db=round(snr_db, 1),
                    )
                )

        # Sort matches by descending confidence
        matches.sort(key=lambda m: m.confidence, reverse=True)
        return matches

    def analyze_audio_window(
        self, audio_data: np.ndarray, habitat: str | None = None, season: str | None = None
    ) -> AcousticAnalysisResult:
        """Executes full acoustic pipeline on an audio sample buffer."""
        freqs, psd = self.compute_spectrum(audio_data)
        ndsi, bio_energy, anthro_energy = self.calculate_ndsi(freqs, psd)
        aci = self.calculate_aci(audio_data)
        centroid = self.calculate_spectral_centroid(freqs, psd)
        peak_freq = float(freqs[np.argmax(psd)]) if len(psd) > 0 else 0.0

        matches = self.match_species(freqs, psd, aci, current_habitat=habitat, current_season=season)

        # Rating categorization
        if ndsi >= 0.65 and aci >= 15.0:
            rating = "Pristine Wilderness (High Biophony)"
        elif ndsi >= 0.25:
            rating = "Serene Nature Trail"
        elif ndsi >= -0.20:
            rating = "Mixed Acoustic Edge"
        else:
            rating = "Elevated Anthrophony (Human Noise)"

        return AcousticAnalysisResult(
            ndsi=round(ndsi, 3),
            aci=round(aci, 2),
            peak_freq_hz=round(peak_freq, 1),
            spectral_centroid_hz=round(centroid, 1),
            biophony_energy=float(round(bio_energy, 5)),
            anthrophony_energy=float(round(anthro_energy, 5)),
            soundscape_rating=rating,
            matches=matches,
        )
