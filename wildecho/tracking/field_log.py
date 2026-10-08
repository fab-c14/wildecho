"""
WildEcho Expedition Field Tracker & Ecological Logger
Silently maps trail biodiversity metrics and logs acoustic species encounters
for post-expedition review once you return from the backcountry.
"""

import json
import math
import time
from collections import Counter
from pathlib import Path

from pydantic import BaseModel, Field

from wildecho.bioacoustics.analyzer import AcousticAnalysisResult
from wildecho.config import settings
from wildecho.intelligence.gemma_engine import NaturalistFieldReport


class TrailWaypoint(BaseModel):
    """An acoustic observation waypoint along the trail."""

    step: int
    timestamp: float
    latitude: float
    longitude: float
    elevation_m: float
    ndsi: float
    aci: float
    soundscape_rating: str
    detected_species_id: str | None = None
    common_name: str | None = None
    confidence: float | None = None
    whisper_delivered: str | None = None


class ExpeditionSummary(BaseModel):
    """High-level ecological and acoustic summary of an expedition."""

    expedition_id: str
    trail_name: str
    habitat: str
    season: str
    start_time: float
    end_time: float
    duration_minutes: float
    total_waypoints: int
    species_detected_count: int
    unique_species: list[str]
    shannon_diversity_index: float
    mean_ndsi: float
    mean_aci: float
    pristine_soundscape_ratio: float
    waypoints: list[TrailWaypoint] = Field(default_factory=list)


class ExpeditionLogger:
    """Manages active backcountry tracking and persists field logs."""

    def __init__(
        self,
        trail_name: str = "Pine Ridge Wilderness Trail",
        habitat: str = "dense_forest",
        season: str = "autumn",
        base_lat: float = 35.6120,
        base_lon: float = -83.5180,
        base_elevation: float = 850.0,
    ):
        self.expedition_id = f"exp_{int(time.time())}"
        self.trail_name = trail_name
        self.habitat = habitat
        self.season = season
        self.base_lat = base_lat
        self.base_lon = base_lon
        self.base_elevation = base_elevation

        self.start_time = time.time()
        self.waypoints: list[TrailWaypoint] = []
        self.reports: list[NaturalistFieldReport] = []

    def record_waypoint(
        self, step: int, analysis: AcousticAnalysisResult, report: NaturalistFieldReport | None = None
    ) -> TrailWaypoint:
        """Records an acoustic window waypoint along the trail."""
        # Simulated trail progression (~60 meters per window)
        lat = self.base_lat + (step * 0.00045)
        lon = self.base_lon + (step * 0.00030)
        elevation = self.base_elevation + (step * 3.5)

        sp_id = report.species.id if report else None
        c_name = report.species.common_name if report else None
        conf = report.confidence if report else None
        whisper = report.whisper_script if report else None

        waypoint = TrailWaypoint(
            step=step,
            timestamp=time.time(),
            latitude=round(lat, 5),
            longitude=round(lon, 5),
            elevation_m=round(elevation, 1),
            ndsi=analysis.ndsi,
            aci=analysis.aci,
            soundscape_rating=analysis.soundscape_rating,
            detected_species_id=sp_id,
            common_name=c_name,
            confidence=conf,
            whisper_delivered=whisper,
        )

        self.waypoints.append(waypoint)
        if report:
            self.reports.append(report)

        return waypoint

    def calculate_shannon_diversity(self) -> float:
        """
        Calculates Shannon-Wiener Biodiversity Index (H) from detected taxa.
        H = -sum(p_i * ln(p_i))
        Higher score = richer, more balanced ecological community.
        """
        species_list = [w.detected_species_id for w in self.waypoints if w.detected_species_id]
        if not species_list:
            return 0.0

        counts = Counter(species_list)
        total = len(species_list)
        shannon = 0.0
        for count in counts.values():
            p = count / total
            shannon -= p * math.log(p)

        return round(shannon, 3)

    def finalize(self) -> ExpeditionSummary:
        """Finalizes the expedition and compiles comprehensive ecological summary."""
        end_time = time.time()
        duration_min = max(0.1, (end_time - self.start_time) / 60.0)

        species_ids = [w.detected_species_id for w in self.waypoints if w.detected_species_id]
        unique_sp = sorted(set(species_ids))

        ndsi_values = [w.ndsi for w in self.waypoints]
        mean_ndsi = float(round(sum(ndsi_values) / len(ndsi_values), 3)) if ndsi_values else 0.0

        aci_values = [w.aci for w in self.waypoints]
        mean_aci = float(round(sum(aci_values) / len(aci_values), 2)) if aci_values else 0.0

        pristine_count = sum(1 for w in self.waypoints if w.ndsi >= 0.5)
        pristine_ratio = round(pristine_count / len(self.waypoints), 3) if self.waypoints else 0.0

        return ExpeditionSummary(
            expedition_id=self.expedition_id,
            trail_name=self.trail_name,
            habitat=self.habitat,
            season=self.season,
            start_time=self.start_time,
            end_time=end_time,
            duration_minutes=round(duration_min, 1),
            total_waypoints=len(self.waypoints),
            species_detected_count=len(species_ids),
            unique_species=unique_sp,
            shannon_diversity_index=self.calculate_shannon_diversity(),
            mean_ndsi=mean_ndsi,
            mean_aci=mean_aci,
            pristine_soundscape_ratio=pristine_ratio,
            waypoints=self.waypoints,
        )

    def save_to_disk(self, output_dir: Path = settings.expeditions_dir) -> Path:
        """Saves expedition data as a structured JSON file."""
        output_dir.mkdir(parents=True, exist_ok=True)
        summary = self.finalize()
        filepath = output_dir / f"{self.expedition_id}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(summary.model_dump(), f, indent=2)
        return filepath
