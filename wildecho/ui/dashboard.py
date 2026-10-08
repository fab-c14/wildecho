"""
WildEcho Expedition Dashboard & Live Listening Runner
Coordinates live soundscape sampling, offline Gemma reasoning,
eyes-free earbud whispers, and silent field logging.
"""

import time

from rich.rule import Rule

from wildecho.audio.narrator import EarbudNarrator
from wildecho.bioacoustics.analyzer import BioacousticAnalyzer
from wildecho.bioacoustics.recorder import SoundscapeStreamer
from wildecho.intelligence.gemma_engine import GemmaEcologicalEngine
from wildecho.tracking.field_log import ExpeditionLogger, ExpeditionSummary
from wildecho.ui.charts import (
    biophony_energy_bars,
    ndsi_gauge,
    species_detection_table,
    waypoints_timeline_table,
)
from wildecho.ui.console import console
from wildecho.ui.panels import (
    expedition_summary_panel,
    header_panel,
    whisper_panel,
)


def run_expedition_session(
    trail_name: str = "Great Smoky Mountain Ridge Trail",
    habitat: str = "dense_forest",
    season: str = "autumn",
    windows: int = 5,
    delay_seconds: float = 0.5,
) -> ExpeditionSummary:
    """
    Executes a complete backcountry acoustic expedition session.
    Walks through trail soundscape windows, performs offline biometric matching,
    synthesizes Gemma 2 eyes-free audio whispers, and compiles field logs.
    """
    console.print()
    console.print(header_panel(trail_name, habitat, season))
    console.print()

    analyzer = BioacousticAnalyzer()
    gemma = GemmaEcologicalEngine()
    narrator = EarbudNarrator()
    streamer = SoundscapeStreamer()
    logger = ExpeditionLogger(trail_name=trail_name, habitat=habitat, season=season)

    for step, audio_buf, _target_species in streamer.stream_windows(habitat=habitat, season=season, steps=windows):
        console.print(
            Rule(f"[bold green]Trail Waypoint #{step:02d}[/bold green] - Ambient Sampling Window", style="green")
        )

        # 1. Analyze soundscape window
        result = analyzer.analyze_audio_window(audio_buf, habitat=habitat, season=season)

        # Print soundscape status
        console.print(f" Soundscape Quality:   [bold]{result.soundscape_rating}[/bold]")
        console.print(f" Biophony Index (NDSI): {ndsi_gauge(result.ndsi).markup}")
        console.print(
            f" Acoustic Complexity:  [magenta]{result.aci:.1f} ACI[/magenta] | Peak: [cyan]{result.peak_freq_hz:.0f} Hz[/cyan]"
        )
        console.print()
        console.print(biophony_energy_bars(result.biophony_energy, result.anthrophony_energy))

        # 2. Check for detected species
        report = None
        if result.matches:
            top_match = result.matches[0]
            console.print()
            console.print(species_detection_table(result.matches))

            # 3. Generate Gemma 2 ecological reasoning report
            report = gemma.generate_report(
                species=top_match.species,
                confidence=top_match.confidence,
                ndsi=result.ndsi,
                aci=result.aci,
                habitat=habitat,
                season=season,
            )

            # 4. Whisper briefing into earbuds
            whisper_event = narrator.whisper(report)

            console.print()
            console.print(whisper_panel(report, whisper_event.estimated_duration_s))

        # 5. Silently record waypoint
        logger.record_waypoint(step=step, analysis=result, report=report)

        console.print()
        if delay_seconds > 0 and step < windows:
            time.sleep(delay_seconds)

    # Finalize expedition
    summary = logger.finalize()
    saved_path = logger.save_to_disk()

    console.print(Rule("[bold green]Trailhead Reached[/bold green]", style="green"))
    console.print(expedition_summary_panel(summary))
    console.print()
    console.print(waypoints_timeline_table(summary.waypoints))
    console.print()
    console.print(f"[bold green][OK][/bold green] Field journal saved to: [cyan]{saved_path}[/cyan]\n")

    return summary
