"""Bioacoustics package exports."""

from wildecho.bioacoustics.analyzer import (
    AcousticAnalysisResult,
    BioacousticAnalyzer,
    SpeciesMatch,
)
from wildecho.bioacoustics.catalog import (
    CATALOG_MAP,
    SPECIES_CATALOG,
    SpeciesSignature,
    get_catalog_by_habitat,
    get_catalog_by_season,
)
from wildecho.bioacoustics.recorder import SoundscapeStreamer, SoundscapeSynthesizer

__all__ = [
    "CATALOG_MAP",
    "SPECIES_CATALOG",
    "AcousticAnalysisResult",
    "BioacousticAnalyzer",
    "SoundscapeStreamer",
    "SoundscapeSynthesizer",
    "SpeciesMatch",
    "SpeciesSignature",
    "get_catalog_by_habitat",
    "get_catalog_by_season",
]
