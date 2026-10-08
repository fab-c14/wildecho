"""
Unit tests for WildEcho Bioacoustics Signal Processing
"""

import numpy as np
import pytest

from wildecho.bioacoustics.analyzer import BioacousticAnalyzer
from wildecho.bioacoustics.catalog import SPECIES_CATALOG
from wildecho.bioacoustics.recorder import SoundscapeSynthesizer


@pytest.fixture
def analyzer():
    return BioacousticAnalyzer(sample_rate=22050)


@pytest.fixture
def synthesizer():
    return SoundscapeSynthesizer(sample_rate=22050)


def test_catalog_invariants():
    """Asserts that all species in catalog have valid physical frequency bounds."""
    assert len(SPECIES_CATALOG) >= 10
    for sp in SPECIES_CATALOG:
        assert sp.min_freq_hz > 0
        assert sp.max_freq_hz > sp.min_freq_hz
        assert sp.min_freq_hz <= sp.peak_freq_hz <= sp.max_freq_hz
        assert sp.harmonic_count >= 1
        assert len(sp.habitats) > 0
        assert len(sp.seasons) > 0


def test_ndsi_calculation(analyzer):
    """Asserts NDSI accurately distinguishes pure biophony vs pure anthrophony."""
    freqs = np.linspace(0, 11025, 1024)

    # Pure high-frequency biophony (3500 Hz peak)
    bio_psd = np.exp(-0.5 * ((freqs - 3500) / 200) ** 2)
    ndsi_bio, bio_e, anthro_e = analyzer.calculate_ndsi(freqs, bio_psd)
    assert ndsi_bio > 0.80
    assert bio_e > anthro_e

    # Pure low-frequency anthrophony (300 Hz engine rumble)
    anthro_psd = np.exp(-0.5 * ((freqs - 300) / 50) ** 2)
    ndsi_anthro, bio_e2, anthro_e2 = analyzer.calculate_ndsi(freqs, anthro_psd)
    assert ndsi_anthro < -0.80
    assert anthro_e2 > bio_e2


def test_aci_complexity(analyzer, synthesizer):
    """Asserts that dynamic bird vocalizations have higher ACI than static noise."""
    flat_noise = synthesizer.generate_wind_and_stream(duration_s=2.0, intensity=0.2)
    wood_thrush = next(s for s in SPECIES_CATALOG if s.id == "wood_thrush")
    call = synthesizer.generate_species_call(wood_thrush, duration_s=2.0)

    aci_noise = analyzer.calculate_aci(flat_noise)
    aci_call = analyzer.calculate_aci(call)

    assert aci_call > aci_noise


def test_species_matching(analyzer, synthesizer):
    """Asserts that synthesizing a Wood Thrush call matches the Wood Thrush signature."""
    audio = synthesizer.generate_soundscape_scene(duration_s=3.0, species_ids=["wood_thrush"], anthro_noise_level=0.0)

    result = analyzer.analyze_audio_window(audio, habitat="dense_forest", season="autumn")
    assert result.ndsi > 0.20
    assert len(result.matches) > 0
    top_match = result.matches[0]
    assert top_match.species.id == "wood_thrush"
    assert top_match.confidence >= 0.60
