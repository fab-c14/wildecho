"""
WildEcho CLI Entrypoint
Built with Typer and Rich for a colorful, professional developer experience.
"""

import json

import typer
from rich.table import Table

from wildecho import __version__
from wildecho.bioacoustics.catalog import CATALOG_MAP, SPECIES_CATALOG
from wildecho.config import settings
from wildecho.ui.console import console
from wildecho.ui.dashboard import run_expedition_session
from wildecho.ui.panels import expedition_summary_panel, species_card_panel

app = typer.Typer(
    name="wildecho",
    help="WildEcho: Offline Backcountry Acoustic Nature Explorer & Eyes-Free Audio Field Guide",
    add_completion=False,
)


@app.command()
def listen(
    trail: str = typer.Option("Highland Ridge Old Growth Trail", "--trail", "-t", help="Name of the backcountry trail"),
    habitat: str = typer.Option(
        "dense_forest",
        "--habitat",
        "-h",
        help="Habitat type (dense_forest, riparian_stream, mountain_trail, open_meadow)",
    ),
    season: str = typer.Option("autumn", "--season", "-s", help="Season (spring, summer, autumn, winter)"),
    windows: int = typer.Option(5, "--windows", "-w", help="Number of soundscape sampling windows to evaluate"),
    delay: float = typer.Option(0.3, "--delay", "-d", help="Inter-window delay in seconds for simulation"),
):
    """
    Start an eyes-free backcountry acoustic listening expedition.
    Samples soundscapes, identifies wildlife biometric signatures, whispers naturalist notes into earbuds,
    and logs the trail biodiversity track.
    """
    run_expedition_session(trail_name=trail, habitat=habitat, season=season, windows=windows, delay_seconds=delay)


@app.command()
def catalog(
    habitat: str | None = typer.Option(None, "--habitat", "-h", help="Filter by habitat"),
    season: str | None = typer.Option(None, "--season", "-s", help="Filter by season"),
    species_id: str | None = typer.Option(None, "--inspect", "-i", help="Inspect a specific species ID"),
):
    """
    Inspect the embedded offline wildlife acoustic signature catalog.
    """
    if species_id:
        if species_id in CATALOG_MAP:
            sp = CATALOG_MAP[species_id]
            from wildecho.bioacoustics.analyzer import SpeciesMatch

            mock_match = SpeciesMatch(species=sp, confidence=0.92, peak_detected_hz=sp.peak_freq_hz, snr_db=18.4)
            console.print(species_card_panel(mock_match))
            return
        console.print(f"[bold red]Error:[/bold red] Species '{species_id}' not found in catalog.")
        return

    table = Table(title="WildEcho: Embedded Offline Wildlife Acoustic Catalog", show_lines=True)
    table.add_column("ID", style="cyan", width=18)
    table.add_column("Common Name", style="bold green")
    table.add_column("Scientific Name", style="italic white")
    table.add_column("Class", style="yellow")
    table.add_column("Peak Freq", justify="right")
    table.add_column("Call Pattern", style="dim white")
    table.add_column("Foraging & Forest Indicator", style="dim green")

    for sp in SPECIES_CATALOG:
        if habitat and habitat not in sp.habitats:
            continue
        if season and season not in sp.seasons:
            continue

        table.add_row(
            sp.id,
            sp.common_name,
            sp.scientific_name,
            str(sp.category).upper(),
            f"{sp.peak_freq_hz:.0f} Hz",
            sp.call_pattern.replace("_", " ").title(),
            sp.foraging_association[:55] + "...",
        )

    console.print()
    console.print(table)
    console.print()


@app.command()
def log(expedition_id: str | None = typer.Option(None, "--id", help="Specific expedition ID to view")):
    """
    View saved backcountry expedition field logs and biodiversity reports.
    """
    exp_dir = settings.expeditions_dir
    if not exp_dir.exists():
        console.print("[yellow]No expeditions logged yet. Run `wildecho listen` to start an expedition.[/yellow]")
        return

    files = sorted(exp_dir.glob("*.json"), reverse=True)
    if not files:
        console.print("[yellow]No saved expeditions found in 'expeditions/'.[/yellow]")
        return

    target_file = files[0]
    if expedition_id:
        custom_file = exp_dir / f"{expedition_id}.json"
        if custom_file.exists():
            target_file = custom_file
        else:
            console.print(f"[red]Expedition '{expedition_id}' not found.[/red]")
            return

    with open(target_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    from wildecho.tracking.field_log import ExpeditionSummary

    summary = ExpeditionSummary(**data)

    console.print()
    console.print(expedition_summary_panel(summary))
    console.print()

    from wildecho.ui.charts import waypoints_timeline_table

    console.print(waypoints_timeline_table(summary.waypoints))
    console.print()


@app.command()
def serve(
    host: str = typer.Option("127.0.0.1", "--host", help="Host interface to bind to"),
    port: int = typer.Option(8000, "--port", "-p", help="Port number for companion web server"),
):
    """
    Launch the interactive companion Web Expedition Explorer (FastAPI).
    """
    import uvicorn

    from wildecho.web.app import app as web_app

    console.print(f"\n[bold green]Launching WildEcho Web Explorer on http://{host}:{port}[/bold green]\n")
    uvicorn.run(web_app, host=host, port=port)


@app.command()
def version():
    """Display WildEcho version and core AI model architecture."""
    console.print(f"[bold green]WildEcho[/bold green] v{__version__}")
    console.print("Core Reasoning: [cyan]Google Gemma 2 (gemma-2-2b-it)[/cyan]")
    console.print("Bioacoustics:   [magenta]NumPy/SciPy Signal Processing (NDSI & ACI)[/magenta]")
    console.print("Hardware Mode:  [yellow]100% Offline Edge (Zero Screen Backcountry)[/yellow]")


if __name__ == "__main__":
    app()
