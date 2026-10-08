"""
Unit tests for Google Gemma 2 Ecological Reasoning Engine
"""

from wildecho.bioacoustics.catalog import CATALOG_MAP
from wildecho.intelligence.gemma_engine import GemmaEcologicalEngine
from wildecho.intelligence.naturalist_prompts import build_gemma_naturalist_prompt


def test_prompt_construction():
    """Asserts prompt follows Gemma 2 turn formatting and contains ecological markers."""
    sp = CATALOG_MAP["wood_thrush"]
    prompt = build_gemma_naturalist_prompt(
        species=sp, confidence=0.88, ndsi=0.75, aci=32.4, habitat="dense_forest", season="autumn"
    )

    assert "<start_of_turn>user" in prompt
    assert "<start_of_turn>model" in prompt
    assert "Wood Thrush" in prompt
    assert "WHISPER:" in prompt
    assert "INSIGHT:" in prompt
    assert "FORAGING_SAFETY:" in prompt


def test_edge_report_synthesis():
    """Asserts offline edge reasoning produces concise whisper and ecological intelligence."""
    engine = GemmaEcologicalEngine()
    sp = CATALOG_MAP["pileated_woodpecker"]

    report = engine.generate_report(
        species=sp, confidence=0.82, ndsi=0.68, aci=24.5, habitat="dense_forest", season="autumn"
    )

    assert report.species.id == "pileated_woodpecker"
    assert len(report.whisper_script.split()) <= 35
    assert "Pileated Woodpecker" in report.whisper_script
    assert len(report.ecological_context) > 0
    assert len(report.foraging_tip) > 0
    assert report.safety_alert is not None
