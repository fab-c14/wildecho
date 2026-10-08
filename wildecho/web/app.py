"""
WildEcho Companion Web Application
FastAPI server providing API endpoints and interactive web explorer.
Deployable on Render via render.yaml blueprint.
"""

import json
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from wildecho.bioacoustics.catalog import SPECIES_CATALOG
from wildecho.config import settings
from wildecho.ui.dashboard import run_expedition_session

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app_instance: FastAPI) -> AsyncGenerator[None, None]:
    # Startup: ensure expeditions directory exists
    settings.expeditions_dir.mkdir(parents=True, exist_ok=True)
    yield


app = FastAPI(
    title="WildEcho API",
    description="Offline Backcountry Acoustic Nature Explorer & Eyes-Free Audio Field Guide",
    version="0.1.0",
    lifespan=lifespan,
)


class SimulationRequest(BaseModel):
    trail_name: str = "Pine Ridge Wilderness Trail"
    habitat: str = "dense_forest"
    season: str = "autumn"
    windows: int = 5


@app.get("/health")
def healthcheck():
    """Health check endpoint for Render container monitoring."""
    return {"status": "healthy", "service": "wildecho", "model": settings.gemma_model}


@app.get("/api/catalog")
def get_catalog():
    """Returns the offline wildlife acoustic catalog."""
    return [sp.model_dump() for sp in SPECIES_CATALOG]


@app.get("/api/expeditions")
def get_expeditions():
    """Returns all recorded expeditions."""
    exp_dir = settings.expeditions_dir
    if not exp_dir.exists():
        return []

    summaries = []
    for file in sorted(exp_dir.glob("*.json"), reverse=True):
        try:
            with open(file, "r", encoding="utf-8") as f:
                summaries.append(json.load(f))
        except (json.JSONDecodeError, OSError) as err:
            logger.warning("Skipping invalid expedition log %s: %s", file, err)
    return summaries


@app.post("/api/simulate")
def simulate_expedition(req: SimulationRequest):
    """Executes a trail soundscape simulation and returns the resulting field log."""
    summary = run_expedition_session(
        trail_name=req.trail_name,
        habitat=req.habitat,
        season=req.season,
        windows=req.windows,
        delay_seconds=0.0,  # Instant for API
    )
    return summary.model_dump()


@app.get("/", response_class=HTMLResponse)
def index_page():
    """Serves the standalone interactive WildEcho Expedition Explorer."""
    return HTMLResponse(content=INDEX_HTML)


INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WildEcho | Backcountry Acoustic Explorer</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { background-color: #0c140d; color: #ecfdf5; font-family: system-ui, -apple-system, sans-serif; }
    </style>
</head>
<body class="p-4 md:p-8 max-w-6xl mx-auto">
    <!-- Header -->
    <header class="border-b border-emerald-900 pb-6 mb-8 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
            <div class="inline-flex items-center gap-2 px-3 py-1 bg-emerald-950 border border-emerald-800 rounded-full text-xs font-semibold text-emerald-400 mb-2">
                <span>🌲 Hacktoberfest Week 1: Touch Grass</span>
                <span>•</span>
                <span>Core: Google Gemma 2</span>
            </div>
            <h1 class="text-3xl font-extrabold tracking-tight text-white flex items-center gap-3">
                <span>WildEcho</span>
                <span class="text-xs bg-emerald-700 text-white font-bold px-2 py-0.5 rounded">v0.1.0</span>
            </h1>
            <p class="text-sm text-emerald-300/80 mt-1">
                Offline Backcountry Acoustic Nature Explorer & Eyes-Free Audio Field Guide
            </p>
        </div>
        <div class="flex gap-3">
            <button onclick="runSimulation()" id="run-btn" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded-lg shadow-md transition flex items-center gap-2">
                <span>▶ Run Trail Simulation</span>
            </button>
            <a href="https://github.com/fab-c14/wildecho" target="_blank" class="px-4 py-2 bg-neutral-900 hover:bg-neutral-800 border border-neutral-700 text-neutral-300 font-semibold rounded-lg text-sm flex items-center gap-1">
                GitHub ↗
            </a>
        </div>
    </header>

    <!-- Main Grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <!-- Metric Card 1 -->
        <div class="bg-neutral-900/80 border border-emerald-950 rounded-xl p-5 shadow-sm">
            <div class="text-xs text-emerald-400 font-semibold uppercase tracking-wider">Acoustic Biophony (NDSI)</div>
            <div class="text-3xl font-black text-emerald-300 mt-2" id="kpi-ndsi">+0.78</div>
            <p class="text-xs text-neutral-400 mt-1">Scale: -1.0 (Human Noise) to +1.0 (Pristine Nature)</p>
        </div>

        <!-- Metric Card 2 -->
        <div class="bg-neutral-900/80 border border-emerald-950 rounded-xl p-5 shadow-sm">
            <div class="text-xs text-emerald-400 font-semibold uppercase tracking-wider">Shannon Diversity (H)</div>
            <div class="text-3xl font-black text-white mt-2" id="kpi-diversity">1.61</div>
            <p class="text-xs text-neutral-400 mt-1">Taxonomic balance of detected wildlife calls</p>
        </div>

        <!-- Metric Card 3 -->
        <div class="bg-neutral-900/80 border border-emerald-950 rounded-xl p-5 shadow-sm">
            <div class="text-xs text-emerald-400 font-semibold uppercase tracking-wider">Eyes-Free Screen Time</div>
            <div class="text-3xl font-black text-yellow-400 mt-2">0.0 seconds</div>
            <p class="text-xs text-neutral-400 mt-1">100% whispered into earbuds on trail</p>
        </div>
    </div>

    <!-- Active Whisper Box -->
    <div class="bg-gradient-to-r from-emerald-950/40 via-neutral-900 to-emerald-950/40 border border-yellow-800/40 rounded-xl p-6 mb-8">
        <div class="flex items-center gap-2 text-xs font-bold text-yellow-400 tracking-wide uppercase mb-2">
            <span>🔊 Latest Whispered Earbud Briefing</span>
            <span class="text-neutral-500">•</span>
            <span id="whisper-species" class="text-emerald-400">Wood Thrush (Hylocichla mustelina)</span>
        </div>
        <blockquote class="text-lg md:text-xl font-medium text-white italic" id="whisper-text">
            "Listen to the canopy. That liquid flute cascade is a Wood Thrush. Take a breath and enjoy the moment."
        </blockquote>
        <div class="mt-4 pt-4 border-t border-neutral-800 grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div>
                <span class="text-emerald-400 font-semibold">🍄 Foraging Correlation:</span>
                <span class="text-neutral-300 ml-1" id="whisper-forage">Mature deciduous leaf litter indicates prime Chanterelle and Black Trumpet mushroom habitat.</span>
            </div>
            <div>
                <span class="text-yellow-400 font-semibold">⚠️ Trail Safety:</span>
                <span class="text-neutral-300 ml-1" id="whisper-safety">Shaded interior woods; keep bearings on trail landmarks.</span>
            </div>
        </div>
    </div>

    <!-- Charts & Table -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <div class="bg-neutral-900/80 border border-neutral-800 rounded-xl p-5">
            <h3 class="text-sm font-bold text-white mb-4">Trail Soundscape: Biophony vs Anthrophony Timeline</h3>
            <canvas id="soundscapeChart" height="200"></canvas>
        </div>
        <div class="bg-neutral-900/80 border border-neutral-800 rounded-xl p-5">
            <h3 class="text-sm font-bold text-white mb-4">Offline Species Catalog (Embedded Edge Engine)</h3>
            <div class="overflow-y-auto max-h-64 text-xs">
                <table class="w-full text-left">
                    <thead class="text-neutral-500 border-b border-neutral-800">
                        <tr>
                            <th class="pb-2">Species</th>
                            <th class="pb-2">Class</th>
                            <th class="pb-2">Peak Freq</th>
                            <th class="pb-2">Pattern</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-neutral-800 text-neutral-300" id="catalog-body">
                        <!-- Loaded dynamically -->
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="border-t border-neutral-800 pt-6 text-center text-xs text-neutral-500">
        WildEcho • Built with Google Gemma 2 & SciPy • Hacktoberfest 2026: Week 1 (Touch Grass)
    </footer>

    <script>
        let chartInstance = null;

        async function init() {
            // Load catalog
            try {
                const res = await fetch('/api/catalog');
                const catalog = await res.json();
                const tbody = document.getElementById('catalog-body');
                tbody.innerHTML = catalog.map(s => `
                    <tr>
                        <td class="py-2 font-semibold text-emerald-300">${s.common_name}</td>
                        <td class="py-2 uppercase text-neutral-400">${s.category}</td>
                        <td class="py-2 text-cyan-400">${Math.round(s.peak_freq_hz)} Hz</td>
                        <td class="py-2 text-neutral-400">${s.call_pattern.replace('_', ' ')}</td>
                    </tr>
                `).join('');
            } catch(e) { console.error(e); }

            // Render chart
            const ctx = document.getElementById('soundscapeChart').getContext('2d');
            chartInstance = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['Start', 'Waypoint 1', 'Waypoint 2', 'Waypoint 3', 'Waypoint 4', 'Summit'],
                    datasets: [
                        {
                            label: 'Biophony (Nature)',
                            data: [0.65, 0.82, 0.74, 0.89, 0.92, 0.85],
                            borderColor: '#34d399',
                            backgroundColor: 'rgba(52, 211, 153, 0.1)',
                            fill: true,
                            tension: 0.3
                        },
                        {
                            label: 'Anthrophony (Human Noise)',
                            data: [0.15, 0.08, 0.05, 0.02, 0.01, 0.03],
                            borderColor: '#f87171',
                            backgroundColor: 'rgba(248, 113, 113, 0.05)',
                            fill: true,
                            tension: 0.3
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { labels: { color: '#94a3b8' } } },
                    scales: {
                        x: { ticks: { color: '#64748b' }, grid: { color: '#1e293b' } },
                        y: { ticks: { color: '#64748b' }, grid: { color: '#1e293b' }, min: 0, max: 1.0 }
                    }
                }
            });
        }

        async function runSimulation() {
            const btn = document.getElementById('run-btn');
            btn.innerText = 'Analyzing...';
            btn.disabled = true;

            try {
                const res = await fetch('/api/simulate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ trail_name: "Highland Ridge Trail", habitat: "dense_forest", season: "autumn", windows: 6 })
                });
                const data = await res.json();

                document.getElementById('kpi-ndsi').innerText = (data.mean_ndsi >= 0 ? '+' : '') + data.mean_ndsi.toFixed(2);
                document.getElementById('kpi-diversity').innerText = data.shannon_diversity_index.toFixed(2);

                const lastWp = data.waypoints.find(w => w.whisper_delivered);
                if (lastWp) {
                    document.getElementById('whisper-species').innerText = lastWp.common_name;
                    document.getElementById('whisper-text').innerText = `"${lastWp.whisper_delivered}"`;
                }

                // Update chart
                const labels = data.waypoints.map(w => `#${w.step}`);
                const ndsiData = data.waypoints.map(w => Math.max(0, (w.ndsi + 1) / 2));
                chartInstance.data.labels = labels;
                chartInstance.data.datasets[0].data = ndsiData;
                chartInstance.update();

            } catch (err) {
                console.error(err);
            } finally {
                btn.innerText = '▶ Run Trail Simulation';
                btn.disabled = false;
            }
        }

        window.onload = init;
    </script>
</body>
</html>
"""
