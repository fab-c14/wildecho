"""
WildEcho Terminal Visualizations & Charts
Renders ASCII/Rich soundscape meters, NDSI gauges, and species tables.
"""

from rich import box
from rich.table import Table
from rich.text import Text

from wildecho.bioacoustics.analyzer import SpeciesMatch
from wildecho.tracking.field_log import TrailWaypoint


def ndsi_gauge(ndsi: float, width: int = 28) -> Text:
    """
    Renders an ASCII gauge for NDSI from -1.0 (Anthro) to +1.0 (Bio).
    Example: [-1.0 |========>            | +1.0] (+0.42)
    """
    normalized = (ndsi + 1.0) / 2.0  # 0.0 to 1.0
    pos = int(normalized * width)
    pos = max(0, min(pos, width))

    gauge = Text()
    gauge.append("[-1.0 ", style="dim")
    for i in range(width):
        if i == pos:
            gauge.append(">", style="bold green" if ndsi >= 0 else "bold red")
        elif i < pos:
            gauge.append("=", style="green" if ndsi >= 0 else "red")
        else:
            gauge.append(" ", style="dim")
    gauge.append(" +1.0] ", style="dim")

    color = "bold green" if ndsi >= 0.5 else ("green" if ndsi >= 0.2 else ("yellow" if ndsi >= -0.2 else "red"))
    gauge.append(f"({ndsi:+.2f})", style=color)
    return gauge


def biophony_energy_bars(bio_energy: float, anthro_energy: float, max_width: int = 20) -> Table:
    """Renders side-by-side relative energy bars for biophony and anthrophony."""
    table = Table(box=box.SIMPLE_HEAD, show_edge=False, pad_edge=False)
    table.add_column("Acoustic Band", style="bold white", width=14)
    table.add_column("Relative Energy", width=max_width + 4)
    table.add_column("Energy Value", justify="right", style="cyan")

    total = max(bio_energy + anthro_energy, 1e-9)
    bio_ratio = bio_energy / total
    anthro_ratio = anthro_energy / total

    bio_bars = int(bio_ratio * max_width)
    anthro_bars = int(anthro_ratio * max_width)

    b_text = Text()
    b_text.append("[" + "=" * bio_bars + ">" + " " * (max_width - bio_bars) + "]", style="green")

    a_text = Text()
    a_text.append("[" + "=" * anthro_bars + ">" + " " * (max_width - anthro_bars) + "]", style="red")

    table.add_row("Biophony (Nature)", b_text, f"{bio_energy:.4f}")
    table.add_row("Anthrophony (Noise)", a_text, f"{anthro_energy:.4f}")

    return table


def species_detection_table(matches: list[SpeciesMatch]) -> Table:
    """Renders a clean table of detected biological species in the window."""
    table = Table(title="Detected Biological Species (Bioacoustics)", box=box.ROUNDED)
    table.add_column("#", style="dim", width=3)
    table.add_column("Common Name", style="bold green")
    table.add_column("Scientific Name", style="italic white")
    table.add_column("Class", style="cyan")
    table.add_column("Peak Freq", justify="right")
    table.add_column("Confidence", justify="right", style="bold green")

    for idx, m in enumerate(matches, start=1):
        sp = m.species
        conf_style = "bold green" if m.confidence >= 0.75 else "green"
        table.add_row(
            str(idx),
            sp.common_name,
            sp.scientific_name,
            sp.category.upper(),
            f"{m.peak_detected_hz:.0f} Hz",
            f"[{conf_style}]{m.confidence * 100:.1f}%[/{conf_style}]",
        )

    return table


def waypoints_timeline_table(waypoints: list[TrailWaypoint]) -> Table:
    """Renders the step-by-step expedition log table."""
    table = Table(title="Trail Expedition Acoustic Timeline", box=box.ROUNDED)
    table.add_column("Step", style="dim", justify="right", width=4)
    table.add_column("Elevation", justify="right", style="white")
    table.add_column("NDSI", justify="right")
    table.add_column("ACI", justify="right", style="magenta")
    table.add_column("Detected Species", style="bold green")
    table.add_column("Confidence", justify="right")
    table.add_column("Soundscape Rating", style="dim white")

    for w in waypoints:
        ndsi_style = "green" if w.ndsi >= 0.3 else ("yellow" if w.ndsi >= -0.2 else "red")
        species_str = w.common_name or "[dim]Ambient Nature[/dim]"
        conf_str = f"{w.confidence * 100:.0f}%" if w.confidence else "-"

        table.add_row(
            f"#{w.step}",
            f"{w.elevation_m:.0f}m",
            f"[{ndsi_style}]{w.ndsi:+.2f}[/{ndsi_style}]",
            f"{w.aci:.1f}",
            species_str,
            conf_str,
            w.soundscape_rating,
        )

    return table
