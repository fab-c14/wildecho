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
    <title>WildEcho | Backcountry Acoustic Nature Explorer</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['"Plus Jakarta Sans"', 'system-ui', 'sans-serif'],
                        mono: ['"JetBrains Mono"', 'monospace'],
                    },
                    colors: {
                        canopy: {
                            950: '#060a07',
                            900: '#0a100d',
                            850: '#0e1612',
                            800: '#14201a',
                            700: '#1d2e26',
                        },
                        emerald: {
                            glow: '#10b981',
                        }
                    }
                }
            }
        }
    </script>
    <style>
        body {
            background-color: #060a07;
            color: #ecfdf5;
            background-image: 
                radial-gradient(ellipse 60% 50% at 50% -20%, rgba(16, 185, 129, 0.08), transparent),
                radial-gradient(circle at 100% 100%, rgba(6, 182, 212, 0.03), transparent);
            background-attachment: fixed;
        }
        .bento-card {
            background-color: #0a100d;
            border: 1px solid rgba(16, 185, 129, 0.12);
            transition: border-color 0.2s ease, transform 0.2s ease;
        }
        .bento-card:hover {
            border-color: rgba(16, 185, 129, 0.24);
        }
        /* Custom scrollbar */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #0a100d; }
        ::-webkit-scrollbar-thumb { background: #1d2e26; border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: #10b981; }
    </style>
</head>
<body class="p-4 sm:p-6 lg:p-8 max-w-7xl mx-auto min-h-screen flex flex-col font-sans antialiased">
    <!-- Top Telemetry Bar & Navigation -->
    <header class="border-b border-emerald-950/80 pb-6 mb-8 flex flex-col lg:flex-row justify-between items-start lg:items-center gap-6">
        <div>
            <!-- Status Badge Strip -->
            <div class="inline-flex items-center gap-2.5 px-3 py-1 bg-emerald-950/60 border border-emerald-800/40 rounded-full text-xs font-mono text-emerald-400 mb-3 shadow-inner">
                <span class="inline-block w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                <span>BACKCOUNTRY OFFLINE MODE</span>
                <span class="text-emerald-700">•</span>
                <span class="text-neutral-400">TOUCH GRASS (WEEK 1)</span>
                <span class="text-emerald-700">•</span>
                <span class="text-emerald-300 font-semibold">GEMMA 2 REASONER</span>
            </div>
            
            <div class="flex items-baseline gap-3">
                <h1 class="text-3xl sm:text-4xl font-extrabold tracking-tight text-white flex items-center gap-3">
                    <span>WildEcho</span>
                    <span class="font-mono text-xs tracking-normal bg-emerald-950 text-emerald-400 border border-emerald-800/60 font-semibold px-2.5 py-0.5 rounded-full">v0.1.0</span>
                </h1>
                <span class="text-xs font-mono text-emerald-500/70 hidden sm:inline">[22.05 kHz DSP • 12 Taxa]</span>
            </div>
            <p class="text-xs sm:text-sm text-neutral-400 mt-1 max-w-2xl">
                Eyes-free backcountry acoustic explorer. Put your phone in your pocket, walk the trail, and let on-device AI whisper wildlife intelligence into your earbuds.
            </p>
        </div>

        <!-- Simulation Controls -->
        <div class="flex flex-wrap items-center gap-2.5 bg-canopy-900 border border-emerald-950 p-2 rounded-xl shadow-lg">
            <select id="habitat-select" class="bg-canopy-850 border border-emerald-900/60 text-xs font-mono text-emerald-200 rounded-lg px-3 py-2 outline-none focus:border-emerald-500">
                <option value="dense_forest">🌲 Dense Forest</option>
                <option value="mountain_trail">⛰️ Mountain Trail</option>
                <option value="riparian_stream">💧 Riparian Stream</option>
                <option value="open_meadow">🌾 Open Meadow</option>
            </select>
            <select id="season-select" class="bg-canopy-850 border border-emerald-900/60 text-xs font-mono text-emerald-200 rounded-lg px-3 py-2 outline-none focus:border-emerald-500">
                <option value="autumn">🍂 Autumn</option>
                <option value="spring">🌸 Spring</option>
                <option value="summer">☀️ Summer</option>
                <option value="winter">❄️ Winter</option>
            </select>
            <button onclick="runSimulation()" id="run-btn" class="px-4 py-2 bg-emerald-600 hover:bg-emerald-500 active:scale-[0.98] text-white font-semibold text-xs rounded-lg shadow-md transition flex items-center gap-2">
                <span>▶ Run Trail Walk</span>
            </button>
            <a href="https://github.com/fab-c14/wildecho" target="_blank" rel="noopener" class="px-3 py-2 bg-canopy-850 hover:bg-canopy-800 text-neutral-300 font-mono text-xs rounded-lg border border-neutral-800 transition">
                GitHub ↗
            </a>
        </div>
    </header>

    <!-- Asymmetric Hero Stage: Waveform Visualizer + Active Whisper -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-8">
        <!-- Live Acoustic Spectrum Canvas (7 cols) -->
        <div class="lg:col-span-7 bento-card rounded-2xl p-5 sm:p-6 flex flex-col justify-between relative overflow-hidden">
            <div class="flex items-center justify-between mb-4">
                <div class="flex items-center gap-2">
                    <span class="w-2.5 h-2.5 rounded-full bg-emerald-400"></span>
                    <span class="text-xs font-mono uppercase tracking-wider text-emerald-400 font-semibold">Live Spectrum Analyzer</span>
                </div>
                <div class="flex items-center gap-3 text-[11px] font-mono text-neutral-400">
                    <span class="flex items-center gap-1"><span class="w-2 h-2 rounded-sm bg-rose-500/80"></span> Anthrophony (&lt;1.5k)</span>
                    <span class="flex items-center gap-1"><span class="w-2 h-2 rounded-sm bg-emerald-400"></span> Biophony (2-11k)</span>
                </div>
            </div>

            <!-- Canvas Visualization -->
            <div class="relative w-full h-44 sm:h-52 bg-canopy-950/90 rounded-xl border border-emerald-950/60 overflow-hidden flex items-end px-3 py-2">
                <canvas id="spectrumCanvas" class="w-full h-full"></canvas>
                <div class="absolute top-2 left-3 text-[10px] font-mono text-emerald-500/60 pointer-events-none">
                    BAND: 50 Hz — 11,025 Hz (FFT 512)
                </div>
                <div class="absolute top-2 right-3 text-[10px] font-mono text-neutral-400 pointer-events-none" id="live-fps">
                    REAL-TIME DSP
                </div>
            </div>

            <!-- Telemetry Footer -->
            <div class="mt-4 pt-4 border-t border-emerald-950/80 grid grid-cols-3 gap-2 text-center font-mono">
                <div>
                    <div class="text-[10px] text-neutral-500 uppercase">Peak Detection</div>
                    <div class="text-sm font-bold text-cyan-400 mt-0.5" id="spec-peak">3,402 Hz</div>
                </div>
                <div>
                    <div class="text-[10px] text-neutral-500 uppercase">Acoustic Complexity</div>
                    <div class="text-sm font-bold text-fuchsia-400 mt-0.5" id="spec-aci">13.3 ACI</div>
                </div>
                <div>
                    <div class="text-[10px] text-neutral-500 uppercase">Soundscape State</div>
                    <div class="text-sm font-bold text-emerald-400 mt-0.5 truncate" id="spec-rating">Serene Nature</div>
                </div>
            </div>
        </div>

        <!-- Latest Spoken Earbud Field Briefing (5 cols) -->
        <div class="lg:col-span-5 bento-card rounded-2xl p-5 sm:p-6 flex flex-col justify-between border-emerald-900/40 relative">
            <div>
                <div class="flex items-center justify-between mb-3">
                    <div class="inline-flex items-center gap-2 text-[11px] font-mono font-bold text-amber-400 tracking-wider uppercase">
                        <span class="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></span>
                        <span>Spoken Earbud Brief</span>
                    </div>
                    <span id="whisper-engine-badge" class="text-[10px] font-mono px-2 py-0.5 rounded bg-canopy-850 text-neutral-400 border border-neutral-800">
                        Gemma 2 • ~7.7s
                    </span>
                </div>

                <div class="text-xs font-mono text-emerald-400/90 mb-2 flex items-center gap-2">
                    <span id="whisper-species" class="font-bold">Wood Thrush</span>
                    <span class="text-neutral-500 italic text-[11px]" id="whisper-latin">(Hylocichla mustelina)</span>
                    <span class="ml-auto font-mono text-[10px] px-1.5 py-0.5 bg-emerald-950 text-emerald-300 rounded border border-emerald-800/60" id="whisper-conf">98% match</span>
                </div>

                <blockquote class="text-base sm:text-lg font-medium text-white/95 leading-relaxed italic border-l-2 border-emerald-500/60 pl-3.5 my-3" id="whisper-text">
                    "Listen to the canopy. That liquid flute cascade is a Wood Thrush. Take a breath and enjoy the moment."
                </blockquote>
            </div>

            <div class="mt-4 pt-3.5 border-t border-emerald-950/80 space-y-2 text-xs">
                <div class="flex items-start gap-2">
                    <span class="text-amber-400 font-mono text-[11px] shrink-0 mt-0.5">🍄 FORAGE:</span>
                    <span class="text-neutral-300 text-xs" id="whisper-forage">Mature deciduous leaf litter indicates prime Chanterelle and Black Trumpet mushroom habitat.</span>
                </div>
                <div class="flex items-start gap-2">
                    <span class="text-rose-400 font-mono text-[11px] shrink-0 mt-0.5">⚠️ SAFETY:</span>
                    <span class="text-neutral-300 text-xs" id="whisper-safety">Shaded interior woods; keep bearings on trail landmarks.</span>
                </div>
            </div>
        </div>
    </div>

    <!-- 3-Pillar Ecological Telemetry Bento -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-8">
        <!-- Metric Card 1: NDSI Gauge -->
        <div class="bento-card rounded-2xl p-5 sm:p-6 flex flex-col justify-between">
            <div class="flex items-center justify-between text-xs font-mono text-neutral-400">
                <span class="uppercase tracking-wider">Acoustic Biophony (NDSI)</span>
                <span class="text-emerald-400 font-semibold">[Krause Niche]</span>
            </div>
            <div class="my-3">
                <div class="text-3xl sm:text-4xl font-extrabold font-mono text-emerald-300 tracking-tight" id="kpi-ndsi">+0.78</div>
                <!-- Dynamic Horizontal Gauge -->
                <div class="w-full bg-canopy-950 h-2 rounded-full overflow-hidden mt-3 p-0.5 border border-emerald-950">
                    <div id="ndsi-bar" class="h-full bg-gradient-to-r from-rose-500 via-amber-400 to-emerald-400 rounded-full transition-all duration-500" style="width: 89%;"></div>
                </div>
            </div>
            <p class="text-[11px] text-neutral-400 leading-normal">
                Scale: -1.0 (Human anthrophony) to +1.0 (Pristine biological soundscape).
            </p>
        </div>

        <!-- Metric Card 2: Shannon Diversity -->
        <div class="bento-card rounded-2xl p-5 sm:p-6 flex flex-col justify-between">
            <div class="flex items-center justify-between text-xs font-mono text-neutral-400">
                <span class="uppercase tracking-wider">Biodiversity Index (H)</span>
                <span class="text-cyan-400 font-semibold">[Shannon-Wiener]</span>
            </div>
            <div class="my-3">
                <div class="text-3xl sm:text-4xl font-extrabold font-mono text-white tracking-tight" id="kpi-diversity">1.61</div>
                <div class="text-xs font-mono text-cyan-400 mt-2 flex items-center gap-2">
                    <span class="w-1.5 h-1.5 rounded-full bg-cyan-400"></span>
                    <span id="kpi-species-count">5 unique wildlife taxa identified</span>
                </div>
            </div>
            <p class="text-[11px] text-neutral-400 leading-normal">
                Quantifies taxonomic evenness and biological acoustic species richness along the trail.
            </p>
        </div>

        <!-- Metric Card 3: Screenless Immersion -->
        <div class="bento-card rounded-2xl p-5 sm:p-6 flex flex-col justify-between">
            <div class="flex items-center justify-between text-xs font-mono text-neutral-400">
                <span class="uppercase tracking-wider">Trail Screen Time</span>
                <span class="text-amber-400 font-semibold">[Touch Grass]</span>
            </div>
            <div class="my-3">
                <div class="text-3xl sm:text-4xl font-extrabold font-mono text-amber-400 tracking-tight">0.0 s</div>
                <div class="text-xs font-mono text-neutral-400 mt-2">
                    100% eyes-free earbud narration
                </div>
            </div>
            <p class="text-[11px] text-neutral-400 leading-normal">
                Phone tucked in pocket. Zero screen fatigue, zero popups, zero GPS distraction while hiking.
            </p>
        </div>
    </div>

    <!-- Secondary Bento: Soundscape Timeline Chart & Offline Catalog -->
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-8">
        <!-- Soundscape Timeline Line Chart (7 cols) -->
        <div class="lg:col-span-7 bento-card rounded-2xl p-5 sm:p-6">
            <div class="flex items-center justify-between mb-4">
                <div>
                    <h3 class="text-sm font-bold text-white tracking-tight">Trail Soundscape Timeline</h3>
                    <p class="text-xs text-neutral-400">Acoustic partition: Biophony (Nature) vs Anthrophony (Human Noise)</p>
                </div>
                <span class="text-[11px] font-mono text-neutral-500">6 WAYPOINTS</span>
            </div>
            <div class="h-64">
                <canvas id="soundscapeChart"></canvas>
            </div>
        </div>

        <!-- Embedded Offline Species Catalog (5 cols) -->
        <div class="lg:col-span-5 bento-card rounded-2xl p-5 sm:p-6 flex flex-col justify-between">
            <div>
                <div class="flex items-center justify-between mb-3">
                    <h3 class="text-sm font-bold text-white tracking-tight">Offline Species Catalog</h3>
                    <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-900/60">
                        12 Native Taxa
                    </span>
                </div>
                
                <!-- Category Filter Pills -->
                <div class="flex items-center gap-1.5 mb-3 overflow-x-auto pb-1 text-[11px] font-mono" id="cat-filters">
                    <button onclick="filterCatalog('all')" class="cat-btn px-2.5 py-1 rounded-md bg-emerald-700 text-white font-semibold">All</button>
                    <button onclick="filterCatalog('bird')" class="cat-btn px-2.5 py-1 rounded-md bg-canopy-850 text-neutral-400 hover:text-white border border-neutral-800">Birds</button>
                    <button onclick="filterCatalog('amphibian')" class="cat-btn px-2.5 py-1 rounded-md bg-canopy-850 text-neutral-400 hover:text-white border border-neutral-800">Frogs</button>
                    <button onclick="filterCatalog('mammal')" class="cat-btn px-2.5 py-1 rounded-md bg-canopy-850 text-neutral-400 hover:text-white border border-neutral-800">Mammals</button>
                    <button onclick="filterCatalog('insect')" class="cat-btn px-2.5 py-1 rounded-md bg-canopy-850 text-neutral-400 hover:text-white border border-neutral-800">Insects</button>
                </div>

                <div class="overflow-y-auto max-h-56 pr-1 text-xs">
                    <div id="catalog-list" class="space-y-2">
                        <!-- Populated dynamically -->
                    </div>
                </div>
            </div>
            
            <div class="mt-3 pt-3 border-t border-emerald-950/80 text-[11px] font-mono text-neutral-500 flex justify-between">
                <span>ZERO CELLULAR REQUIRED</span>
                <span class="text-emerald-500/80">EDGE HARMONIC MATCHING</span>
            </div>
        </div>
    </div>

    <!-- Trail Waypoints Chronological Inspector -->
    <div class="bento-card rounded-2xl p-5 sm:p-6 mb-8">
        <div class="flex items-center justify-between mb-4">
            <div>
                <h3 class="text-sm font-bold text-white tracking-tight">Expedition Waypoint Sequence</h3>
                <p class="text-xs text-neutral-400">Step-by-step biometric acoustic log along the hiking path</p>
            </div>
            <span class="text-xs font-mono text-emerald-400" id="exp-trail-title">Cascade Mountain Ridge</span>
        </div>
        <div class="overflow-x-auto">
            <table class="w-full text-left text-xs font-mono">
                <thead class="text-neutral-500 border-b border-emerald-950">
                    <tr>
                        <th class="pb-2.5">Waypoint</th>
                        <th class="pb-2.5">Elevation</th>
                        <th class="pb-2.5">NDSI</th>
                        <th class="pb-2.5">ACI</th>
                        <th class="pb-2.5">Detected Wildlife</th>
                        <th class="pb-2.5">Confidence</th>
                        <th class="pb-2.5">Soundscape Status</th>
                    </tr>
                </thead>
                <tbody class="divide-y divide-emerald-950/60 text-neutral-300" id="waypoints-body">
                    <!-- Populated dynamically -->
                </tbody>
            </table>
        </div>
    </div>

    <!-- Footer -->
    <footer class="mt-auto border-t border-emerald-950/80 pt-6 pb-4 flex flex-col sm:flex-row justify-between items-center gap-4 text-xs font-mono text-neutral-500">
        <div>
            WildEcho • Google Gemma 2 & SciPy • Hacktoberfest 2026: Week 1 ("Touch Grass")
        </div>
        <div class="flex items-center gap-4">
            <a href="https://github.com/fab-c14/wildecho" target="_blank" class="text-emerald-400 hover:text-emerald-300 transition">GitHub Repo</a>
            <span>•</span>
            <a href="https://dev.to/challenges/hf26" target="_blank" class="text-neutral-400 hover:text-neutral-300 transition">DEV Challenge</a>
        </div>
    </footer>

    <!-- Interactive Scripts -->
    <script>
        let chartInstance = null;
        let fullCatalog = [];
        let canvasAnimationId = null;

        // Spectrum visualizer simulation
        function initSpectrumCanvas() {
            const canvas = document.getElementById('spectrumCanvas');
            const ctx = canvas.getContext('2d');
            
            function resize() {
                canvas.width = canvas.parentElement.clientWidth;
                canvas.height = canvas.parentElement.clientHeight;
            }
            resize();
            window.addEventListener('resize', resize);

            const numBars = 32;
            let barHeights = Array(numBars).fill(10);

            function draw() {
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                const barWidth = (canvas.width / numBars) - 2;

                for (let i = 0; i < numBars; i++) {
                    // Target height with natural organic wobble
                    const isBiophony = i > 8; // bands above ~1.5 kHz
                    const target = isBiophony 
                        ? (Math.sin(Date.now() * 0.003 + i) * 0.35 + 0.55) * canvas.height * 0.75
                        : (Math.sin(Date.now() * 0.001 + i) * 0.15 + 0.20) * canvas.height * 0.45;
                    
                    barHeights[i] += (target - barHeights[i]) * 0.08;

                    const x = i * (barWidth + 2);
                    const h = Math.max(4, barHeights[i]);
                    const y = canvas.height - h;

                    // Gradient coloring: low frequency anthrophony vs high frequency biophony
                    const grad = ctx.createLinearGradient(0, canvas.height, 0, y);
                    if (isBiophony) {
                        grad.addColorStop(0, '#065f46');
                        grad.addColorStop(1, '#34d399');
                    } else {
                        grad.addColorStop(0, '#7f1d1d');
                        grad.addColorStop(1, '#f87171');
                    }

                    ctx.fillStyle = grad;
                    ctx.fillRect(x, y, barWidth, h);

                    // Peak cap dot
                    ctx.fillStyle = isBiophony ? '#a7f3d0' : '#fca5a5';
                    ctx.fillRect(x, y - 2, barWidth, 2);
                }

                canvasAnimationId = requestAnimationFrame(draw);
            }
            draw();
        }

        async function init() {
            initSpectrumCanvas();

            // Load species catalog
            try {
                const res = await fetch('/api/catalog');
                fullCatalog = await res.json();
                renderCatalog(fullCatalog);
            } catch(e) { console.error('Catalog error:', e); }

            // Initialize Soundscape Timeline Chart
            const ctx = document.getElementById('soundscapeChart').getContext('2d');
            chartInstance = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['WP #01', 'WP #02', 'WP #03', 'WP #04', 'WP #05', 'WP #06'],
                    datasets: [
                        {
                            label: 'Biophony (Nature)',
                            data: [0.72, 0.88, 0.65, 0.94, 0.82, 0.91],
                            borderColor: '#10b981',
                            backgroundColor: 'rgba(16, 185, 129, 0.12)',
                            borderWidth: 2,
                            fill: true,
                            tension: 0.35,
                            pointRadius: 4,
                            pointBackgroundColor: '#10b981'
                        },
                        {
                            label: 'Anthrophony (Human Noise)',
                            data: [0.22, 0.08, 0.05, 0.02, 0.01, 0.03],
                            borderColor: '#f43f5e',
                            backgroundColor: 'rgba(244, 63, 94, 0.05)',
                            borderWidth: 1.5,
                            fill: true,
                            tension: 0.35,
                            pointRadius: 3,
                            pointBackgroundColor: '#f43f5e'
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            labels: {
                                color: '#9ca3af',
                                font: { family: '"JetBrains Mono"', size: 11 }
                            }
                        }
                    },
                    scales: {
                        x: {
                            ticks: { color: '#6b7280', font: { family: '"JetBrains Mono"', size: 10 } },
                            grid: { color: 'rgba(16, 185, 129, 0.08)' }
                        },
                        y: {
                            ticks: { color: '#6b7280', font: { family: '"JetBrains Mono"', size: 10 } },
                            grid: { color: 'rgba(16, 185, 129, 0.08)' },
                            min: 0,
                            max: 1.0
                        }
                    }
                }
            });

            // Initial simulation load
            await runSimulation();
        }

        function renderCatalog(items) {
            const list = document.getElementById('catalog-list');
            list.innerHTML = items.map(s => `
                <div class="p-2.5 rounded-lg bg-canopy-950/80 border border-emerald-950/60 hover:border-emerald-800/60 transition flex items-center justify-between gap-3">
                    <div>
                        <div class="font-bold text-emerald-300">${s.common_name}</div>
                        <div class="text-[11px] text-neutral-500 italic">${s.scientific_name}</div>
                    </div>
                    <div class="text-right shrink-0">
                        <div class="font-mono text-cyan-400 font-semibold">${Math.round(s.peak_freq_hz)} Hz</div>
                        <div class="font-mono text-[10px] uppercase text-neutral-400">${s.category}</div>
                    </div>
                </div>
            `).join('');
        }

        function filterCatalog(category) {
            // Update filter pill UI
            document.querySelectorAll('.cat-btn').forEach(btn => {
                btn.className = 'cat-btn px-2.5 py-1 rounded-md bg-canopy-850 text-neutral-400 hover:text-white border border-neutral-800';
            });
            event.target.className = 'cat-btn px-2.5 py-1 rounded-md bg-emerald-700 text-white font-semibold';

            if (category === 'all') {
                renderCatalog(fullCatalog);
            } else {
                renderCatalog(fullCatalog.filter(s => s.category === category));
            }
        }

        async function runSimulation() {
            const btn = document.getElementById('run-btn');
            const habitat = document.getElementById('habitat-select').value;
            const season = document.getElementById('season-select').value;
            btn.innerHTML = '<span>⏳ Sampling Trail...</span>';
            btn.disabled = true;

            try {
                const res = await fetch('/api/simulate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        trail_name: "Cascade Mountain Ridge",
                        habitat: habitat,
                        season: season,
                        windows: 6
                    })
                });
                const data = await res.json();

                // Update KPIs
                const ndsiSign = data.mean_ndsi >= 0 ? '+' : '';
                document.getElementById('kpi-ndsi').innerText = `${ndsiSign}${data.mean_ndsi.toFixed(2)}`;
                const ndsiPercent = Math.min(100, Math.max(0, ((data.mean_ndsi + 1.0) / 2.0) * 100));
                document.getElementById('ndsi-bar').style.width = `${ndsiPercent}%`;
                document.getElementById('kpi-diversity').innerText = data.shannon_diversity_index.toFixed(2);
                document.getElementById('kpi-species-count').innerText = `${data.species_detected_count} detections (${data.unique_species.length} unique taxa)`;

                // Update Whisper card
                const lastWhisper = data.waypoints.filter(w => w.whisper_delivered).pop();
                if (lastWhisper) {
                    document.getElementById('whisper-species').innerText = lastWhisper.common_name;
                    document.getElementById('whisper-latin').innerText = `(${lastWhisper.scientific_name || 'Acoustic Signature'})`;
                    document.getElementById('whisper-text').innerText = `"${lastWhisper.whisper_delivered}"`;
                    document.getElementById('whisper-conf').innerText = `${Math.round(lastWhisper.confidence * 100)}% match`;
                    document.getElementById('spec-peak').innerText = `${Math.round(lastWhisper.peak_detected_hz || 3400)} Hz`;
                    document.getElementById('spec-aci').innerText = `${(lastWhisper.aci || 12.0).toFixed(1)} ACI`;
                    document.getElementById('spec-rating').innerText = lastWhisper.soundscape_rating.replace(/\\s*\\(.*?\\)/, '');

                    // Find species for foraging & safety notes
                    const sp = fullCatalog.find(s => s.id === lastWhisper.detected_species_id);
                    if (sp) {
                        document.getElementById('whisper-forage').innerText = sp.foraging_association;
                        document.getElementById('whisper-safety').innerText = sp.safety_note || 'Maintain trail bearings.';
                    }
                }

                // Update Waypoints table
                const tableBody = document.getElementById('waypoints-body');
                tableBody.innerHTML = data.waypoints.map(w => `
                    <tr class="hover:bg-emerald-950/30 transition">
                        <td class="py-2.5 font-bold text-white">#${String(w.step).padStart(2, '0')}</td>
                        <td class="py-2.5 text-neutral-400">${Math.round(w.elevation_meters)}m</td>
                        <td class="py-2.5 ${w.ndsi >= 0 ? 'text-emerald-400' : 'text-rose-400'}">${w.ndsi >= 0 ? '+' : ''}${w.ndsi.toFixed(2)}</td>
                        <td class="py-2.5 text-fuchsia-400">${w.aci.toFixed(1)}</td>
                        <td class="py-2.5 font-bold ${w.common_name ? 'text-emerald-300' : 'text-neutral-500'}">
                            ${w.common_name || 'Ambient Geophony'}
                        </td>
                        <td class="py-2.5">${w.confidence ? Math.round(w.confidence * 100) + '%' : '—'}</td>
                        <td class="py-2.5 text-neutral-400 truncate">${w.soundscape_rating}</td>
                    </tr>
                `).join('');

                // Update chart
                const labels = data.waypoints.map(w => `WP #${String(w.step).padStart(2, '0')}`);
                const biophonyVals = data.waypoints.map(w => Math.max(0, (w.ndsi + 1.0) / 2.0));
                const anthroVals = data.waypoints.map(w => Math.max(0, (1.0 - w.ndsi) / 4.0));

                chartInstance.data.labels = labels;
                chartInstance.data.datasets[0].data = biophonyVals;
                chartInstance.data.datasets[1].data = anthroVals;
                chartInstance.update();

            } catch (err) {
                console.error('Simulation error:', err);
            } finally {
                btn.innerHTML = '<span>▶ Run Trail Walk</span>';
                btn.disabled = false;
            }
        }

        window.onload = init;
    </script>
</body>
</html>
"""
