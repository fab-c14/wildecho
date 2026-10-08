"""
Unit tests for WildEcho Expedition Field Tracker & Ecological Logger
"""

import math

import pytest

from wildecho.bioacoustics.analyzer import AcousticAnalysisResult
from wildecho.bioacoustics.catalog import CATALOG_MAP
from wildecho.intelligence.gemma_engine import NaturalistFieldReport
from wildecho.tracking.field_log import ExpeditionLogger


@pytest.fixture
def logger():
    return ExpeditionLogger(trail_name="Test Ridge Trail", habitat="dense_forest", season="autumn")


def test_waypoint_recording(logger):
    """Asserts waypoints are recorded with micro-coordinates and soundscape metrics."""
    analysis = AcousticAnalysisResult(
        ndsi=0.72,
        aci=28.4,
        peak_freq_hz=3400.0,
        spectral_centroid_hz=3100.0,
        biophony_energy=0.015,
        anthrophony_energy=0.002,
        soundscape_rating="Pristine Wilderness (High Biophony)",
    )
    sp = CATALOG_MAP["wood_thrush"]
    report = NaturalistFieldReport(
        species=sp,
        confidence=0.88,
        whisper_script="Listen to the canopy. Wood Thrush calling.",
        ecological_context="Healthy mature forest stand.",
        foraging_tip="Chanterelle indicator.",
    )

    wp = logger.record_waypoint(step=1, analysis=analysis, report=report)

    assert wp.step == 1
    assert wp.ndsi == 0.72
    assert wp.common_name == "Wood Thrush"
    assert wp.whisper_delivered is not None
    assert len(logger.waypoints) == 1


def test_shannon_diversity_index(logger):
    """Asserts Shannon-Wiener diversity calculation adheres to ecological formulas."""
    # When no species recorded, H = 0
    assert logger.calculate_shannon_diversity() == 0.0

    analysis = AcousticAnalysisResult(
        ndsi=0.6,
        aci=20.0,
        peak_freq_hz=2000.0,
        spectral_centroid_hz=2500.0,
        biophony_energy=0.01,
        anthrophony_energy=0.003,
        soundscape_rating="Serene Nature Trail",
    )

    sp1 = CATALOG_MAP["wood_thrush"]
    sp2 = CATALOG_MAP["barred_owl"]

    rep1 = NaturalistFieldReport(
        species=sp1, confidence=0.8, whisper_script="s1", ecological_context="c1", foraging_tip="f1"
    )
    rep2 = NaturalistFieldReport(
        species=sp2, confidence=0.8, whisper_script="s2", ecological_context="c2", foraging_tip="f2"
    )

    logger.record_waypoint(1, analysis, rep1)
    logger.record_waypoint(2, analysis, rep2)

    # 2 evenly distributed species -> H = - (0.5*ln(0.5) + 0.5*ln(0.5)) = ln(2) ~= 0.693
    h = logger.calculate_shannon_diversity()
    expected = round(-(0.5 * math.log(0.5) + 0.5 * math.log(0.5)), 3)
    assert abs(h - expected) < 0.01


def test_expedition_finalization(logger, tmp_path):
    """Asserts expedition summary compilation and JSON export."""
    analysis = AcousticAnalysisResult(
        ndsi=0.85,
        aci=35.0,
        peak_freq_hz=3400.0,
        spectral_centroid_hz=3200.0,
        biophony_energy=0.02,
        anthrophony_energy=0.001,
        soundscape_rating="Pristine Wilderness (High Biophony)",
    )
    sp = CATALOG_MAP["wood_thrush"]
    report = NaturalistFieldReport(
        species=sp, confidence=0.9, whisper_script="s", ecological_context="c", foraging_tip="f"
    )

    logger.record_waypoint(1, analysis, report)
    summary = logger.finalize()

    assert summary.total_waypoints == 1
    assert summary.species_detected_count == 1
    assert "wood_thrush" in summary.unique_species
    assert summary.mean_ndsi == 0.85

    saved_file = logger.save_to_disk(output_dir=tmp_path)
    assert saved_file.exists()
