"""
WildEcho UI Panels
Rich panels for eyes-free notifications, species cards, and trail headers.
"""

from rich import box
from rich.panel import Panel
from rich.text import Text

from wildecho.bioacoustics.analyzer import SpeciesMatch
from wildecho.intelligence.gemma_engine import NaturalistFieldReport
from wildecho.tracking.field_log import ExpeditionSummary


def header_panel(trail_name: str, habitat: str, season: str) -> Panel:
    """Renders expedition kickoff panel."""
    content = Text()
    content.append(" WILDECHO  ", style="bold green on dark_green")
    content.append(" - Offline Backcountry Acoustic Nature Explorer\n", style="bold white")
    content.append(" [Eyes-Free Mode] Phone in pocket, earbuds active. Touch grass.\n\n", style="italic green")
    content.append(f" Trail:     {trail_name}\n", style="white")
    content.append(f" Habitat:   {habitat.replace('_', ' ').title()}\n", style="cyan")
    content.append(f" Season:    {season.title()} | Engine: Offline Gemma 2 & Edge Bioacoustics\n", style="dim white")

    return Panel(content, title="[bold green]Expedition Active[/bold green]", border_style="green", box=box.ROUNDED)


def whisper_panel(report: NaturalistFieldReport, duration_s: float) -> Panel:
    """Displays what is whispered into the hiker's earbuds."""
    content = Text()
    content.append(" [WHISPER DELIVERED TO EARBUDS] \n\n", style="bold yellow")
    content.append(f'"{report.whisper_script}"\n\n', style="bold bright_white")

    content.append(" Naturalist Insight: ", style="bold cyan")
    content.append(f"{report.ecological_context}\n", style="white")

    content.append(" Foraging Association: ", style="bold green")
    content.append(f"{report.foraging_tip}\n", style="white")

    if report.safety_alert:
        content.append(" Trail Safety: ", style="bold red")
        content.append(f"{report.safety_alert}\n", style="yellow")

    footer = f"Audio Duration: ~{duration_s:.1f}s | Synthesized by {report.generated_by}"

    return Panel(
        content,
        title="[bold yellow]Earbud Audio Briefing[/bold yellow]",
        subtitle=f"[dim]{footer}[/dim]",
        border_style="yellow",
        box=box.ROUNDED,
    )


def species_card_panel(match: SpeciesMatch) -> Panel:
    """Displays detailed species biometric identification card."""
    sp = match.species
    content = Text()
    content.append(f"{sp.common_name} ", style="bold green")
    content.append(f"({sp.scientific_name})\n", style="italic dim white")
    content.append(
        f"Taxonomic Class: {sp.category.upper()} | Confidence: {match.confidence * 100:.1f}%\n\n", style="cyan"
    )

    content.append("Acoustic Signature:\n", style="bold white")
    content.append(
        f"  * Detected Peak: {match.peak_detected_hz:.1f} Hz (Signature: {sp.peak_freq_hz:.1f} Hz)\n", style="white"
    )
    content.append(f"  * Call Pattern:  {sp.call_pattern.replace('_', ' ').title()}\n", style="white")
    content.append(f"  * Signal SNR:    +{match.snr_db:.1f} dB above baseline noise\n\n", style="white")

    content.append("Field Acoustic Notes:\n", style="bold white")
    content.append(f"  {sp.field_description}\n\n", style="dim white")

    content.append("Foraging Correlation:\n", style="bold green")
    content.append(f"  {sp.foraging_association}\n", style="white")

    return Panel(
        content,
        title=f"[bold green]Species Identification: {sp.common_name}[/bold green]",
        border_style="green",
        box=box.ROUNDED,
    )


def expedition_summary_panel(summary: ExpeditionSummary) -> Panel:
    """Displays comprehensive post-hike celebration card."""
    content = Text()
    content.append(" EXPEDITION COMPLETE  - Backcountry Field Log Compiled\n\n", style="bold green")

    content.append(f" Trail:              {summary.trail_name}\n", style="white")
    content.append(
        f" Habitat & Season:   {summary.habitat.replace('_', ' ').title()} ({summary.season.title()})\n", style="white"
    )
    content.append(
        f" Duration:           {summary.duration_minutes:.1f} minutes | {summary.total_waypoints} waypoints sampled\n\n",
        style="white",
    )

    content.append(" Ecological Soundscape Indices:\n", style="bold cyan")
    content.append(
        f"  * Mean NDSI:       {summary.mean_ndsi:+.3f} (Bio-to-Anthro Soundscape Ratio)\n",
        style="green" if summary.mean_ndsi >= 0.4 else "yellow",
    )
    content.append(f"  * Mean ACI:        {summary.mean_aci:.2f} (Acoustic Complexity Index)\n", style="magenta")
    content.append(
        f"  * Shannon Index:   {summary.shannon_diversity_index:.3f} (Taxonomic Diversity H)\n", style="cyan"
    )
    content.append(
        f"  * Pristine Ratio:  {summary.pristine_soundscape_ratio * 100:.1f}% of trail in high-biophony zone\n\n",
        style="green",
    )

    content.append(
        f" Total Species Detected: {summary.species_detected_count} ({len(summary.unique_species)} unique taxa)\n",
        style="bold white",
    )
    if summary.unique_species:
        for sp_id in summary.unique_species:
            content.append(f"   + {sp_id.replace('_', ' ').title()}\n", style="green")

    return Panel(
        content, title="[bold green]Expedition Field Summary[/bold green]", border_style="green", box=box.ROUNDED
    )
