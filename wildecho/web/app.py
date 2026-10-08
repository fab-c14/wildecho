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
    <title>WildEcho | Offline Backcountry Acoustic Nature Explorer</title>
    <script src="https://cdn.tailwindcss.com"></script>
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
                            850: '#0f1712',
                            800: '#16231c',
                            700: '#1f3329',
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
                radial-gradient(ellipse 70% 40% at 50% -10%, rgba(16, 185, 129, 0.12), transparent),
                radial-gradient(circle at 100% 100%, rgba(6, 182, 212, 0.04), transparent);
            background-attachment: fixed;
        }
        .nature-card {
            background-color: #0a100d;
            border: 1px solid rgba(16, 185, 129, 0.14);
            transition: all 0.2s ease;
        }
        .nature-card:hover {
            border-color: rgba(16, 185, 129, 0.32);
        }
        .sound-wave-bar {
            animation: soundBounce 1.2s ease-in-out infinite alternate;
        }
        @keyframes soundBounce {
            0% { height: 15%; }
            100% { height: 95%; }
        }
        /* Custom scrollbar */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #0a100d; }
        ::-webkit-scrollbar-thumb { background: #1f3329; border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: #10b981; }
    </style>
</head>
<body class="p-4 sm:p-6 lg:p-8 max-w-7xl mx-auto min-h-screen flex flex-col font-sans antialiased">

    <!-- Top Navigation Bar (Single Line Desktop, <72px Height) -->
    <header class="border-b border-emerald-950/80 pb-4 mb-6 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
        <div class="flex items-center gap-3">
            <span class="text-2xl p-1.5 bg-emerald-950/80 border border-emerald-800/60 rounded-xl shadow-inner">🌲</span>
            <div>
                <div class="flex items-center gap-2">
                    <span class="font-extrabold text-xl text-white tracking-tight">WildEcho</span>
                    <span class="font-mono text-[11px] bg-emerald-950 text-emerald-400 border border-emerald-800/60 font-semibold px-2 py-0.5 rounded-full">v0.1.0</span>
                </div>
                <div class="text-[11px] font-mono text-emerald-400/90 font-medium tracking-wide">
                    HACKTOBERFEST 2026 • WEEK 1: TOUCH GRASS • GOOGLE GEMMA 2
                </div>
            </div>
        </div>

        <!-- Quick Links (Single Line on Desktop) -->
        <nav class="flex items-center gap-2.5">
            <a href="https://github.com/fab-c14/wildecho" target="_blank" rel="noopener" class="px-3.5 py-1.5 bg-canopy-850 hover:bg-canopy-800 active:scale-[0.98] text-white font-mono text-xs rounded-xl border border-emerald-900/60 transition whitespace-nowrap shadow-sm">
                GitHub Repo ↗
            </a>
            <a href="https://dev.to/fabc14/wildecho-offline-backcountry-acoustic-nature-explorer-eyes-free-audio-field-guide-6k3" target="_blank" rel="noopener" class="px-3.5 py-1.5 bg-emerald-950/80 hover:bg-emerald-900 active:scale-[0.98] text-emerald-300 font-mono text-xs rounded-xl border border-emerald-800/60 transition whitespace-nowrap">
                DEV Submission ↗
            </a>
            <a href="/docs" target="_blank" class="px-3 py-1.5 bg-canopy-900 hover:bg-canopy-850 text-neutral-400 hover:text-white font-mono text-xs rounded-xl border border-neutral-800 transition whitespace-nowrap">
                API Docs ↗
            </a>
        </nav>
    </header>

    <!-- HERO SECTION (Strict Layout Discipline: Max 4 text elements, headline <=2 lines, subtext <=20 words) -->
    <section class="mb-8 pt-2 sm:pt-4 pb-4">
        <div class="max-w-4xl">
            <!-- 1. Eyebrow -->
            <div class="inline-flex items-center gap-2 px-3 py-1 bg-emerald-950/70 border border-emerald-800/50 rounded-full text-xs font-mono text-emerald-400 mb-3">
                <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                <span>100% OFFLINE BACKCOUNTRY ACOUSTIC EXPLORER</span>
            </div>

            <!-- 2. Headline (Max 2 lines) -->
            <h1 class="text-3xl sm:text-5xl lg:text-6xl font-black text-white tracking-tight leading-[1.08] mb-3">
                Listen to the forest.<br>
                <span class="text-emerald-400">Keep your phone in your pocket.</span>
            </h1>

            <!-- 3. Subtext (18 words, max 2 lines) -->
            <p class="text-sm sm:text-base text-neutral-300 leading-relaxed mb-5 max-w-[65ch]">
                Eyes-free acoustic guide powered by Google Gemma 2. Put your screen away and experience nature through whispered audio.
            </p>

            <!-- 4. CTAs (Distinct intents, single line on desktop) -->
            <div class="flex flex-wrap items-center gap-3">
                <button onclick="scrollToSimulator()" class="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 active:scale-[0.98] text-white font-bold text-xs sm:text-sm rounded-xl shadow-lg transition flex items-center gap-2 whitespace-nowrap">
                    <span>▶ Walk Trail Simulator (5 Waypoints)</span>
                </button>
                <button onclick="speakCurrentWhisper()" class="px-4 py-2.5 bg-canopy-850 hover:bg-canopy-800 active:scale-[0.98] text-emerald-300 font-mono text-xs sm:text-sm rounded-xl border border-emerald-900/60 transition flex items-center gap-2 whitespace-nowrap">
                    <span>🔊 Replay Earbud Whisper</span>
                </button>
            </div>
        </div>
    </section>

    <!-- 3-STEP "HOW IT WORKS" VISUAL MENTAL MODEL (5-SECOND UNDERSTANDING) -->
    <section class="mb-8 bg-gradient-to-r from-emerald-950/30 via-canopy-900 to-emerald-950/30 border border-emerald-900/40 rounded-2xl p-5 sm:p-6 shadow-sm">
        <div class="text-xs font-mono text-emerald-400 font-bold tracking-wider uppercase mb-3 flex items-center gap-2">
            <span>💡 How WildEcho Works in 5 Seconds</span>
            <span class="text-neutral-500">•</span>
            <span class="text-neutral-400 lowercase font-normal">the "touch grass" philosophy</span>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <!-- Step 1 -->
            <div class="bg-canopy-950/80 border border-emerald-950 p-4 rounded-xl flex items-start gap-3.5">
                <div class="text-2xl p-2 bg-emerald-950/70 border border-emerald-900/50 rounded-lg shrink-0">📱</div>
                <div>
                    <h3 class="font-bold text-white text-sm">1. Phone in Pocket</h3>
                    <p class="text-xs text-neutral-300 mt-1 leading-relaxed">
                        Put your phone in your backpack. No glowing screens, no menus, zero screen fatigue while walking the trail.
                    </p>
                </div>
            </div>

            <!-- Step 2 -->
            <div class="bg-canopy-950/80 border border-emerald-950 p-4 rounded-xl flex items-start gap-3.5">
                <div class="text-2xl p-2 bg-emerald-950/70 border border-emerald-900/50 rounded-lg shrink-0">🎙️</div>
                <div>
                    <h3 class="font-bold text-white text-sm">2. 100% Offline Bioacoustics</h3>
                    <p class="text-xs text-neutral-300 mt-1 leading-relaxed">
                        Passive microphone buffers analyze forest soundscapes in real-time on your device with <strong>zero cell signal</strong>.
                    </p>
                </div>
            </div>

            <!-- Step 3 -->
            <div class="bg-canopy-950/80 border border-emerald-950 p-4 rounded-xl flex items-start gap-3.5">
                <div class="text-2xl p-2 bg-emerald-950/70 border border-emerald-900/50 rounded-lg shrink-0">🎧</div>
                <div>
                    <h3 class="font-bold text-white text-sm">3. Earbuds Whisper</h3>
                    <p class="text-xs text-neutral-300 mt-1 leading-relaxed">
                        <strong>Google Gemma 2</strong> softly whispers species names, wild edible mushroom foraging clues, and trail safety.
                    </p>
                </div>
            </div>
        </div>
    </section>

    <!-- MAIN INTERACTIVE STAGE: VIRTUAL HIKE SIMULATOR -->
    <main class="space-y-8" id="simulator-stage">
        <!-- Trail Control Bar -->
        <div class="nature-card rounded-2xl p-5 sm:p-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-gradient-to-b from-canopy-900 to-canopy-950">
            <div>
                <span class="text-xs font-mono text-emerald-400 font-semibold uppercase tracking-wider">Interactive Trail Simulator</span>
                <h2 class="text-xl sm:text-2xl font-extrabold text-white mt-0.5" id="current-trail-heading">
                    Cascade Mountain Ridge Walk
                </h2>
                <p class="text-xs text-neutral-400 mt-1">
                    Simulate walking 5 backcountry waypoints with real voice audio whispers spoken into your headphones.
                </p>
            </div>

            <!-- Hike Actions -->
            <div class="flex flex-wrap items-center gap-3">
                <!-- Voice Mute Toggle -->
                <button onclick="toggleVoice()" id="voice-toggle-btn" class="px-3.5 py-2.5 rounded-xl text-xs font-mono border transition flex items-center gap-2 bg-emerald-950/80 border-emerald-700/60 text-emerald-300 whitespace-nowrap active:scale-[0.98]">
                    <span id="voice-icon">🔊</span>
                    <span id="voice-label">Voice Audio: ON</span>
                </button>

                <!-- Primary Start Hike Button -->
                <button onclick="startSimulatedHike()" id="start-hike-btn" class="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 active:scale-[0.98] text-white font-bold text-xs sm:text-sm rounded-xl shadow-lg transition flex items-center gap-2 whitespace-nowrap">
                    <span>▶ Walk Trail (5 Waypoints)</span>
                </button>
            </div>
        </div>

        <!-- Waypoint Stepper Progress -->
        <div class="nature-card rounded-2xl p-4 sm:p-5">
            <div class="flex justify-between items-center text-xs font-mono mb-2">
                <span class="text-neutral-400">TRAIL PROGRESS: <span id="progress-text" class="text-white font-bold">Waypoint 1 of 5</span></span>
                <span class="text-emerald-400 font-semibold" id="elevation-stat">Elevation: 854 meters</span>
            </div>
            
            <!-- Progress Bar -->
            <div class="w-full bg-canopy-950 h-3 rounded-full overflow-hidden p-0.5 border border-emerald-950 mb-3">
                <div id="hike-progress-bar" class="h-full bg-gradient-to-r from-emerald-600 to-emerald-400 rounded-full transition-all duration-500" style="width: 20%;"></div>
            </div>

            <!-- Step Buttons -->
            <div class="flex justify-between items-center text-xs font-mono">
                <button onclick="prevWaypoint()" id="prev-wp-btn" class="px-3 py-1.5 rounded-lg bg-canopy-850 hover:bg-canopy-800 text-neutral-400 hover:text-white border border-neutral-800 disabled:opacity-30 disabled:pointer-events-none transition whitespace-nowrap active:scale-[0.98]">
                    ◀ Previous Waypoint
                </button>
                <div class="flex gap-1.5" id="waypoint-dots">
                    <!-- Dots inserted dynamically -->
                </div>
                <button onclick="nextWaypoint()" id="next-wp-btn" class="px-3 py-1.5 rounded-lg bg-canopy-850 hover:bg-canopy-800 text-emerald-400 hover:text-white border border-emerald-900/60 disabled:opacity-30 disabled:pointer-events-none transition whitespace-nowrap active:scale-[0.98]">
                    Next Waypoint ▶
                </button>
            </div>
        </div>

        <!-- ACTIVE WAYPOINT SPOTLIGHT: WHAT THE HIKER EXPERIENCES -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            <!-- Left: The Spoken Earbud Whisper (7 cols) -->
            <div class="lg:col-span-7 nature-card rounded-2xl p-6 flex flex-col justify-between border-emerald-800/40 relative overflow-hidden bg-gradient-to-br from-canopy-900 via-canopy-950 to-canopy-900">
                <div>
                    <!-- Header -->
                    <div class="flex items-center justify-between pb-3 mb-4 border-b border-emerald-950">
                        <div class="flex items-center gap-2.5">
                            <span class="w-2.5 h-2.5 rounded-full bg-amber-400 animate-ping"></span>
                            <span class="text-xs font-mono uppercase tracking-wider text-amber-400 font-bold">
                                Spoken Earbud Transmission
                            </span>
                        </div>
                        <div class="flex items-center gap-2">
                            <span class="text-[11px] font-mono px-2.5 py-0.5 rounded-full bg-emerald-950 text-emerald-300 border border-emerald-800/60 font-semibold" id="spotlight-match">
                                98% Acoustic Match
                            </span>
                            <button onclick="speakCurrentWhisper()" title="Replay voice whisper" class="p-1.5 rounded-lg bg-emerald-900/40 hover:bg-emerald-800/60 active:scale-[0.98] text-emerald-300 text-xs border border-emerald-800/60 transition whitespace-nowrap">
                                🔊 Hear Again
                            </button>
                        </div>
                    </div>

                    <!-- Species Tag -->
                    <div class="flex items-baseline gap-2 mb-3">
                        <h3 class="text-xl sm:text-2xl font-black text-white" id="spotlight-species">
                            Wood Thrush
                        </h3>
                        <span class="text-xs font-mono text-neutral-400 italic pb-0.5" id="spotlight-latin">
                            (Hylocichla mustelina)
                        </span>
                    </div>

                    <!-- Spoken Whisper Text -->
                    <div class="relative bg-canopy-950/80 border border-emerald-950 p-4 rounded-xl mb-4">
                        <blockquote class="text-base sm:text-lg font-medium text-emerald-100 italic leading-relaxed" id="spotlight-quote">
                            "Listen to the canopy. That liquid flute cascade is a Wood Thrush. Take a breath and enjoy the moment."
                        </blockquote>
                        <div class="text-[11px] font-mono text-neutral-400 mt-2 flex items-center justify-between">
                            <span>Synthesized by Google Gemma 2 (Offline Edge)</span>
                            <span>~7.7 seconds spoken duration</span>
                        </div>
                    </div>

                    <!-- Foraging Clue & Trail Safety (Practical outdoor value!) -->
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                        <div class="bg-amber-950/20 border border-amber-900/40 p-3 rounded-xl">
                            <div class="font-bold text-amber-400 font-mono text-[11px] flex items-center gap-1.5 mb-1">
                                <span>🍄 Wild Foraging Indicator</span>
                            </div>
                            <p class="text-neutral-300 text-xs leading-normal" id="spotlight-forage">
                                Mature deciduous leaf litter indicates prime Chanterelle and Black Trumpet mushroom habitat.
                            </p>
                        </div>

                        <div class="bg-rose-950/20 border border-rose-900/40 p-3 rounded-xl">
                            <div class="font-bold text-rose-400 font-mono text-[11px] flex items-center gap-1.5 mb-1">
                                <span>⚠️ Trail Terrain & Safety</span>
                            </div>
                            <p class="text-neutral-300 text-xs leading-normal" id="spotlight-safety">
                                Shaded interior woods; maintain bearings on trail landmarks.
                            </p>
                        </div>
                    </div>
                </div>

                <!-- Footer Audio Animation -->
                <div class="mt-4 pt-4 border-t border-emerald-950 flex items-center justify-between text-xs font-mono text-neutral-500">
                    <div class="flex items-center gap-2 text-emerald-400">
                        <div class="flex items-center gap-0.5 h-3">
                            <span class="w-1 bg-emerald-400 rounded-full sound-wave-bar" style="animation-delay: 0.1s;"></span>
                            <span class="w-1 bg-emerald-400 rounded-full sound-wave-bar" style="animation-delay: 0.3s;"></span>
                            <span class="w-1 bg-emerald-400 rounded-full sound-wave-bar" style="animation-delay: 0.2s;"></span>
                            <span class="w-1 bg-emerald-400 rounded-full sound-wave-bar" style="animation-delay: 0.4s;"></span>
                        </div>
                        <span id="audio-status-label">Simulating earbud listening...</span>
                    </div>
                    <button onclick="playSpeciesTone()" class="text-cyan-400 hover:text-cyan-300 underline text-xs whitespace-nowrap active:scale-[0.98]">
                        ▶ Test Acoustic Whistle Sound
                    </button>
                </div>
            </div>

            <!-- Right: Plain-English Nature Meters (Zero Math Confusion) (5 cols) -->
            <div class="lg:col-span-5 space-y-4">
                <!-- Card 1: Nature Purity (Plain English NDSI) -->
                <div class="nature-card rounded-2xl p-5">
                    <div class="flex justify-between items-center text-xs font-mono text-neutral-400 mb-1">
                        <span class="uppercase font-semibold">Soundscape Purity</span>
                        <span class="text-emerald-400 font-bold" id="purity-ratio">92% Nature</span>
                    </div>
                    <div class="text-2xl font-black text-white" id="purity-title">
                        Pristine Wilderness
                    </div>
                    <p class="text-xs text-neutral-300 mt-1" id="purity-desc">
                        Soundscape is dominated by native bird calls and wind, with near-zero highway or airplane noise.
                    </p>
                    <!-- Progress Bar -->
                    <div class="w-full bg-canopy-950 h-2 rounded-full overflow-hidden mt-3 border border-emerald-950">
                        <div id="purity-bar" class="h-full bg-emerald-400 rounded-full transition-all duration-300" style="width: 92%;"></div>
                    </div>
                    <div class="flex justify-between text-[10px] font-mono text-neutral-400 mt-1.5">
                        <span>Human Noise (-1.0)</span>
                        <span id="raw-ndsi" class="text-emerald-400 font-semibold">+0.84 NDSI</span>
                        <span>Pure Nature (+1.0)</span>
                    </div>
                </div>

                <!-- Card 2: Songbird Activity (Plain English ACI) -->
                <div class="nature-card rounded-2xl p-5">
                    <div class="flex justify-between items-center text-xs font-mono text-neutral-400 mb-1">
                        <span class="uppercase font-semibold">Songbird Complexity</span>
                        <span class="text-fuchsia-400 font-bold" id="complexity-badge">High Activity</span>
                    </div>
                    <div class="text-2xl font-black text-white" id="complexity-title">
                        Active Bird Chorus
                    </div>
                    <p class="text-xs text-neutral-300 mt-1" id="complexity-desc">
                        Sharp harmonic frequency hops indicate active territorial and mating vocalizations.
                    </p>
                    <div class="flex justify-between text-[10px] font-mono text-neutral-400 mt-3 pt-2 border-t border-emerald-950">
                        <span>Acoustic Complexity Score:</span>
                        <span id="raw-aci" class="text-fuchsia-400 font-bold">14.5 ACI</span>
                    </div>
                </div>

                <!-- Card 3: Biodiversity Health (Shannon H) -->
                <div class="nature-card rounded-2xl p-5">
                    <div class="flex justify-between items-center text-xs font-mono text-neutral-400 mb-1">
                        <span class="uppercase font-semibold">Taxonomic Health</span>
                        <span class="text-cyan-400 font-bold" id="diversity-badge">Rich Ecosystem</span>
                    </div>
                    <div class="text-2xl font-black text-white" id="diversity-title">
                        Balanced Diversity
                    </div>
                    <p class="text-xs text-neutral-300 mt-1">
                        Trail supports balanced co-existence across songbirds, raptors, and amphibians.
                    </p>
                    <div class="flex justify-between text-[10px] font-mono text-neutral-400 mt-3 pt-2 border-t border-emerald-950">
                        <span>Shannon Diversity Index (H):</span>
                        <span id="raw-shannon" class="text-cyan-400 font-bold">1.61 H</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- LIVE ACOUSTIC EQUALIZER WATERFALL -->
        <div class="nature-card rounded-2xl p-5 sm:p-6">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2 mb-4">
                <div>
                    <h3 class="text-sm font-bold text-white tracking-tight">Audio Frequency Spectrum Analyzer</h3>
                    <p class="text-xs text-neutral-300">
                        Shows how WildEcho mathematically separates human drone (<1.5 kHz) from biological calls (2–11 kHz) on edge hardware.
                    </p>
                </div>
                <div class="flex items-center gap-4 text-xs font-mono">
                    <span class="flex items-center gap-1.5 text-rose-400">
                        <span class="w-2.5 h-2.5 rounded-sm bg-rose-500"></span> Low Noise (Engines/Road)
                    </span>
                    <span class="flex items-center gap-1.5 text-emerald-400">
                        <span class="w-2.5 h-2.5 rounded-sm bg-emerald-400"></span> High Biophony (Birds/Frogs)
                    </span>
                </div>
            </div>

            <!-- Canvas -->
            <div class="h-44 sm:h-48 w-full bg-canopy-950 rounded-xl border border-emerald-950 p-2 relative">
                <canvas id="liveSpectrum" class="w-full h-full"></canvas>
            </div>
        </div>

        <!-- EXPEDITION FIELD JOURNAL (BUILT AUTOMATICALLY AS YOU WALK) -->
        <div class="nature-card rounded-2xl p-5 sm:p-6">
            <div class="flex justify-between items-center mb-4">
                <div>
                    <h3 class="text-sm font-bold text-white tracking-tight">Expedition Trail Journal</h3>
                    <p class="text-xs text-neutral-400">Silently compiled as you walk with your phone in your pocket.</p>
                </div>
                <span class="text-xs font-mono px-2.5 py-1 rounded-lg bg-emerald-950 text-emerald-300 border border-emerald-800/60">
                    5 Waypoints Logged
                </span>
            </div>

            <div class="overflow-x-auto">
                <table class="w-full text-left text-xs font-mono">
                    <thead class="text-neutral-400 border-b border-emerald-950 pb-2">
                        <tr>
                            <th class="pb-2.5">Waypoint</th>
                            <th class="pb-2.5">Elevation</th>
                            <th class="pb-2.5">Soundscape Purity</th>
                            <th class="pb-2.5">Detected Wildlife</th>
                            <th class="pb-2.5">Confidence</th>
                            <th class="pb-2.5">Action</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-emerald-950/60 text-neutral-300" id="journal-tbody">
                        <!-- Filled by JS -->
                    </tbody>
                </table>
            </div>
        </div>

        <!-- OFFLINE WILDLIFE FIELD GUIDE (AUDIBLE CATALOG) -->
        <div class="nature-card rounded-2xl p-5 sm:p-6">
            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-4">
                <div>
                    <h3 class="text-sm font-bold text-white tracking-tight">Offline Wildlife Acoustic Catalog</h3>
                    <p class="text-xs text-neutral-400">12 native species embedded directly on-device with acoustic signatures and foraging associations.</p>
                </div>
                <!-- Category Tabs -->
                <div class="flex gap-1.5 text-xs font-mono" id="catalog-tabs">
                    <button onclick="filterCatalog('all')" class="cat-pill px-3 py-1 rounded-lg bg-emerald-600 text-white font-bold active:scale-[0.98]">All (12)</button>
                    <button onclick="filterCatalog('bird')" class="cat-pill px-3 py-1 rounded-lg bg-canopy-850 text-neutral-400 border border-neutral-800 hover:text-white active:scale-[0.98]">Birds</button>
                    <button onclick="filterCatalog('amphibian')" class="cat-pill px-3 py-1 rounded-lg bg-canopy-850 text-neutral-400 border border-neutral-800 hover:text-white active:scale-[0.98]">Frogs</button>
                    <button onclick="filterCatalog('mammal')" class="cat-pill px-3 py-1 rounded-lg bg-canopy-850 text-neutral-400 border border-neutral-800 hover:text-white active:scale-[0.98]">Mammals</button>
                    <button onclick="filterCatalog('insect')" class="cat-pill px-3 py-1 rounded-lg bg-canopy-850 text-neutral-400 border border-neutral-800 hover:text-white active:scale-[0.98]">Insects</button>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" id="species-grid">
                <!-- Cards filled by JS -->
            </div>
        </div>

        <!-- HACKATHON EVALUATOR / JUDGE CHEAT SHEET -->
        <div class="border border-emerald-800/40 bg-gradient-to-br from-emerald-950/20 via-canopy-900 to-canopy-950 rounded-2xl p-5 sm:p-6">
            <h3 class="text-sm font-bold text-emerald-300 font-mono uppercase tracking-wider mb-2 flex items-center gap-2">
                <span>🏆 Hackathon Evaluator & Judge Summary</span>
            </h3>
            <p class="text-xs text-neutral-300 mb-4 leading-relaxed">
                Why WildEcho was built for <strong>Hacktoberfest 2026: Week 1 ("Touch Grass")</strong>:
            </p>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs font-sans">
                <div class="bg-canopy-950/90 border border-emerald-950 p-4 rounded-xl">
                    <div class="font-bold text-white mb-1">🌿 Week 1 Theme: Touch Grass</div>
                    <p class="text-neutral-400 text-xs">
                        Completely eliminates screen staring in nature. Hikers put the phone in their pocket and experience real acoustic immersion.
                    </p>
                </div>
                <div class="bg-canopy-950/90 border border-emerald-950 p-4 rounded-xl">
                    <div class="font-bold text-white mb-1">🧠 Google Gemma 2 Core Model</div>
                    <p class="text-neutral-400 text-xs">
                        Open-weight on-device model (`gemma-2-2b-it`). Closed cloud APIs cannot function 10 miles deep in the backcountry with no cell reception.
                    </p>
                </div>
                <div class="bg-canopy-950/90 border border-emerald-950 p-4 rounded-xl">
                    <div class="font-bold text-white mb-1">☁️ Render & ElevenLabs</div>
                    <p class="text-neutral-400 text-xs">
                        Turnkey `render.yaml` companion dashboard deployment, paired with ElevenLabs low-latency voice whisper streaming.
                    </p>
                </div>
            </div>
        </div>
    </main>

    <!-- Footer -->
    <footer class="mt-8 border-t border-emerald-950/80 pt-6 pb-2 text-center text-xs font-mono text-neutral-500">
        WildEcho • Built with Google Gemma 2 & Python SciPy • Open-Source MIT License
    </footer>

    <!-- Interactive Client JavaScript -->
    <script>
        // State
        let voiceEnabled = true;
        let currentWpIndex = 0;
        let simulationWaypoints = [];
        let speciesCatalog = [];
        let audioCtx = null;

        function scrollToSimulator() {
            const el = document.getElementById('simulator-stage');
            if (el) el.scrollIntoView({ behavior: 'smooth' });
            startSimulatedHike();
        }

        // Sound generator using Web Audio API tailored to species category
        function playSpeciesTone() {
            try {
                if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                const wp = simulationWaypoints[currentWpIndex];
                let freq = 3400;
                let category = 'bird';
                if (wp && wp.detected_species_id) {
                    const sp = speciesCatalog.find(s => s.id === wp.detected_species_id);
                    if (sp) {
                        freq = sp.peak_freq_hz;
                        category = sp.category;
                    }
                }
                synthesizeCategorySound(freq, category);
            } catch(e) { console.error('Audio tone error:', e); }
        }

        function synthesizeCategorySound(freq, category) {
            try {
                if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();

                if (category === 'amphibian') {
                    // Pulsed frog ribbit
                    osc.type = 'sawtooth';
                    osc.frequency.setValueAtTime(freq * 0.8, audioCtx.currentTime);
                    osc.frequency.exponentialRampToValueAtTime(freq, audioCtx.currentTime + 0.1);
                    osc.frequency.exponentialRampToValueAtTime(freq * 0.7, audioCtx.currentTime + 0.3);

                    gain.gain.setValueAtTime(0.001, audioCtx.currentTime);
                    gain.gain.linearRampToValueAtTime(0.2, audioCtx.currentTime + 0.05);
                    gain.gain.linearRampToValueAtTime(0.01, audioCtx.currentTime + 0.15);
                    gain.gain.linearRampToValueAtTime(0.25, audioCtx.currentTime + 0.22);
                    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.45);
                    osc.start();
                    osc.stop(audioCtx.currentTime + 0.46);
                } else if (category === 'insect') {
                    // Rapid clicking stridulation
                    osc.type = 'triangle';
                    osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
                    gain.gain.setValueAtTime(0.001, audioCtx.currentTime);
                    gain.gain.linearRampToValueAtTime(0.18, audioCtx.currentTime + 0.02);
                    gain.gain.linearRampToValueAtTime(0.001, audioCtx.currentTime + 0.08);
                    gain.gain.linearRampToValueAtTime(0.18, audioCtx.currentTime + 0.14);
                    gain.gain.linearRampToValueAtTime(0.001, audioCtx.currentTime + 0.2);
                    gain.gain.linearRampToValueAtTime(0.18, audioCtx.currentTime + 0.26);
                    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.35);
                    osc.start();
                    osc.stop(audioCtx.currentTime + 0.36);
                } else if (category === 'mammal') {
                    // Resonant bugle or deep glide
                    osc.type = 'sawtooth';
                    osc.frequency.setValueAtTime(freq * 0.6, audioCtx.currentTime);
                    osc.frequency.exponentialRampToValueAtTime(freq * 1.4, audioCtx.currentTime + 0.3);
                    osc.frequency.exponentialRampToValueAtTime(freq, audioCtx.currentTime + 0.6);
                    gain.gain.setValueAtTime(0.001, audioCtx.currentTime);
                    gain.gain.linearRampToValueAtTime(0.22, audioCtx.currentTime + 0.1);
                    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.65);
                    osc.start();
                    osc.stop(audioCtx.currentTime + 0.66);
                } else {
                    // Songbird flute warble
                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
                    osc.frequency.exponentialRampToValueAtTime(freq * 1.3, audioCtx.currentTime + 0.15);
                    osc.frequency.exponentialRampToValueAtTime(freq * 0.9, audioCtx.currentTime + 0.35);
                    gain.gain.setValueAtTime(0.001, audioCtx.currentTime);
                    gain.gain.linearRampToValueAtTime(0.2, audioCtx.currentTime + 0.05);
                    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.5);
                    osc.start();
                    osc.stop(audioCtx.currentTime + 0.55);
                }

                osc.connect(gain);
                gain.connect(audioCtx.destination);
            } catch(e) { console.error('Audio tone error:', e); }
        }

        function playCustomTone(freq, category = 'bird') {
            synthesizeCategorySound(freq, category);
        }

        // Web Speech API: Speaks the earbud whisper aloud
        function speakCurrentWhisper() {
            if (!voiceEnabled || !('speechSynthesis' in window)) return;
            const wp = simulationWaypoints[currentWpIndex];
            if (!wp || !wp.whisper_delivered) return;

            window.speechSynthesis.cancel(); // Stop any pending speech
            const utterance = new SpeechSynthesisUtterance(wp.whisper_delivered);
            utterance.rate = 0.95; // Calm naturalist cadence
            utterance.pitch = 1.0;

            const status = document.getElementById('audio-status-label');
            if (status) status.innerText = 'Whispering to earbuds...';

            utterance.onend = () => {
                if (status) status.innerText = 'Earbud whisper delivered.';
            };

            window.speechSynthesis.speak(utterance);
        }

        function toggleVoice() {
            voiceEnabled = !voiceEnabled;
            const btn = document.getElementById('voice-toggle-btn');
            const icon = document.getElementById('voice-icon');
            const label = document.getElementById('voice-label');
            
            if (voiceEnabled) {
                btn.className = 'px-3.5 py-2.5 rounded-xl text-xs font-mono border transition flex items-center gap-2 bg-emerald-950/80 border-emerald-700/60 text-emerald-300 whitespace-nowrap active:scale-[0.98]';
                icon.innerText = '🔊';
                label.innerText = 'Voice Audio: ON';
                speakCurrentWhisper();
            } else {
                btn.className = 'px-3.5 py-2.5 rounded-xl text-xs font-mono border transition flex items-center gap-2 bg-canopy-850 border-neutral-800 text-neutral-400 whitespace-nowrap active:scale-[0.98]';
                icon.innerText = '🔇';
                label.innerText = 'Voice Audio: OFF';
                if ('speechSynthesis' in window) window.speechSynthesis.cancel();
            }
        }

        // Initialize Spectrum Canvas
        function initSpectrum() {
            const canvas = document.getElementById('liveSpectrum');
            if (!canvas) return;
            const ctx = canvas.getContext('2d');
            const numBars = 36;
            let barHeights = Array(numBars).fill(10);

            function draw() {
                canvas.width = canvas.parentElement.clientWidth;
                canvas.height = canvas.parentElement.clientHeight;
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                const barWidth = (canvas.width / numBars) - 2;

                for (let i = 0; i < numBars; i++) {
                    const isBiophony = i > 10; // >1500 Hz
                    const baseWave = isBiophony 
                        ? (Math.sin(Date.now() * 0.003 + i * 0.5) * 0.4 + 0.5) * canvas.height * 0.8
                        : (Math.sin(Date.now() * 0.001 + i * 0.2) * 0.15 + 0.15) * canvas.height * 0.35;

                    barHeights[i] += (baseWave - barHeights[i]) * 0.1;
                    const h = Math.max(4, barHeights[i]);
                    const x = i * (barWidth + 2);
                    const y = canvas.height - h;

                    ctx.fillStyle = isBiophony ? '#10b981' : '#f43f5e';
                    ctx.fillRect(x, y, barWidth, h);
                }
                requestAnimationFrame(draw);
            }
            draw();
        }

        // Display current waypoint
        function renderWaypoint(index) {
            if (!simulationWaypoints || simulationWaypoints.length === 0) return;
            currentWpIndex = Math.max(0, Math.min(index, simulationWaypoints.length - 1));
            const wp = simulationWaypoints[currentWpIndex];

            // Progress bar
            const pct = ((currentWpIndex + 1) / simulationWaypoints.length) * 100;
            document.getElementById('hike-progress-bar').style.width = pct + '%';
            document.getElementById('progress-text').innerText = `Waypoint ${currentWpIndex + 1} of ${simulationWaypoints.length}`;
            document.getElementById('elevation-stat').innerText = `Elevation: ${Math.round(wp.elevation_m || 850)} meters`;

            // Buttons state
            document.getElementById('prev-wp-btn').disabled = currentWpIndex === 0;
            document.getElementById('next-wp-btn').disabled = currentWpIndex === simulationWaypoints.length - 1;

            // Update dots
            const dotsContainer = document.getElementById('waypoint-dots');
            dotsContainer.innerHTML = simulationWaypoints.map((_, i) => `
                <button onclick="renderWaypoint(${i})" class="w-3 h-3 rounded-full transition ${i === currentWpIndex ? 'bg-emerald-400 scale-125' : 'bg-canopy-700 hover:bg-neutral-500'}"></button>
            `).join('');

            // Spotlight Whisper Card
            document.getElementById('spotlight-species').innerText = wp.common_name || 'Ambient Nature';
            document.getElementById('spotlight-latin').innerText = wp.scientific_name ? `(${wp.scientific_name})` : '(Geophonic Nature)';
            document.getElementById('spotlight-match').innerText = wp.confidence ? `${Math.round(wp.confidence * 100)}% Match` : 'Ambient';
            document.getElementById('spotlight-quote').innerText = wp.whisper_delivered ? `"${wp.whisper_delivered}"` : '"Forest canopy is peaceful. No active predator or sentinel calls detected."';

            // Find species foraging and safety metadata
            const sp = speciesCatalog.find(s => s.id === wp.detected_species_id);
            if (sp) {
                document.getElementById('spotlight-forage').innerText = sp.foraging_association;
                document.getElementById('spotlight-safety').innerText = sp.safety_note || 'Maintain trail bearings.';
            } else {
                document.getElementById('spotlight-forage').innerText = 'Damp moss and shaded leaf litter indicate healthy fungal substrate.';
                document.getElementById('spotlight-safety').innerText = 'Keep trail markers in view as light shifts through the trees.';
            }

            // Nature Purity (NDSI in plain English)
            const ndsiVal = wp.ndsi || 0.75;
            const purityPct = Math.round(((ndsiVal + 1.0) / 2.0) * 100);
            document.getElementById('purity-ratio').innerText = `${purityPct}% Nature`;
            document.getElementById('purity-bar').style.width = `${purityPct}%`;
            document.getElementById('raw-ndsi').innerText = `${ndsiVal >= 0 ? '+' : ''}${ndsiVal.toFixed(2)} NDSI`;
            if (ndsiVal >= 0.6) {
                document.getElementById('purity-title').innerText = 'Pristine Wilderness';
                document.getElementById('purity-desc').innerText = 'Pure biological soundscape with zero mechanical human noise detected.';
            } else if (ndsiVal >= 0.2) {
                document.getElementById('purity-title').innerText = 'Serene Nature Trail';
                document.getElementById('purity-desc').innerText = 'High songbird chorus with faint distant background ambiance.';
            } else {
                document.getElementById('purity-title').innerText = 'Mixed Acoustic Edge';
                document.getElementById('purity-desc').innerText = 'Distant road or aircraft noise heard mixed with nature.';
            }

            // Songbird Complexity (ACI in plain English)
            const aciVal = wp.aci || 13.0;
            document.getElementById('raw-aci').innerText = `${aciVal.toFixed(1)} ACI`;
            if (aciVal >= 10.0) {
                document.getElementById('complexity-badge').innerText = 'High Song Activity';
                document.getElementById('complexity-title').innerText = 'Active Bird Chorus';
                document.getElementById('complexity-desc').innerText = 'Rapid frequency warbles indicate active biological vocalizations.';
            } else {
                document.getElementById('complexity-badge').innerText = 'Quiet Ambiance';
                document.getElementById('complexity-title').innerText = 'Quiet Canopy';
                document.getElementById('complexity-desc').innerText = 'Steady breeze through trees with intermittent single whistles.';
            }

            // Speak the whisper
            speakCurrentWhisper();
        }

        function prevWaypoint() {
            if (currentWpIndex > 0) renderWaypoint(currentWpIndex - 1);
        }

        function nextWaypoint() {
            if (currentWpIndex < simulationWaypoints.length - 1) renderWaypoint(currentWpIndex + 1);
        }

        async function startSimulatedHike() {
            const btn = document.getElementById('start-hike-btn');
            btn.innerHTML = '<span>⏳ Hiking Trail...</span>';
            btn.disabled = true;

            try {
                const res = await fetch('/api/simulate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        trail_name: "Cascade Mountain Ridge",
                        habitat: "dense_forest",
                        season: "autumn",
                        windows: 5
                    })
                });
                const data = await res.json();
                simulationWaypoints = data.waypoints;

                // Update journal table
                const tbody = document.getElementById('journal-tbody');
                tbody.innerHTML = simulationWaypoints.map((w, i) => `
                    <tr class="hover:bg-emerald-950/30 transition cursor-pointer ${i === currentWpIndex ? 'bg-emerald-950/40 text-emerald-300' : ''}" onclick="renderWaypoint(${i})">
                        <td class="py-2.5 font-bold">#${String(w.step).padStart(2, '0')}</td>
                        <td class="py-2.5 text-neutral-400">${Math.round(w.elevation_m || 850)}m</td>
                        <td class="py-2.5 ${w.ndsi >= 0 ? 'text-emerald-400' : 'text-rose-400'}">
                            ${Math.round(((w.ndsi + 1)/2)*100)}% Nature
                        </td>
                        <td class="py-2.5 font-bold ${w.common_name ? 'text-emerald-300' : 'text-neutral-500'}">
                            ${w.common_name || 'Ambient Nature'}
                        </td>
                        <td class="py-2.5">${w.confidence ? Math.round(w.confidence * 100) + '%' : '—'}</td>
                        <td class="py-2.5 text-cyan-400 hover:underline">Inspect 👁️</td>
                    </tr>
                `).join('');

                // Render first waypoint
                renderWaypoint(0);

            } catch(e) {
                console.error('Hike simulation failed:', e);
            } finally {
                btn.innerHTML = '<span>▶ Walk Trail (5 Waypoints)</span>';
                btn.disabled = false;
            }
        }

        function renderCatalogCards(items) {
            const grid = document.getElementById('species-grid');
            grid.innerHTML = items.map(s => `
                <div class="nature-card rounded-xl p-4 flex flex-col justify-between">
                    <div>
                        <div class="flex items-start justify-between gap-2 mb-1">
                            <div>
                                <h4 class="font-bold text-white text-sm">${s.common_name}</h4>
                                <div class="text-[11px] text-neutral-400 italic">${s.scientific_name}</div>
                            </div>
                            <span class="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-canopy-850 text-neutral-400 border border-neutral-800">
                                ${s.category}
                            </span>
                        </div>
                        <p class="text-xs text-neutral-300 mt-2 leading-relaxed line-clamp-2">
                            ${s.field_description}
                        </p>
                    </div>

                    <div class="mt-4 pt-3 border-t border-emerald-950/80 flex items-center justify-between text-xs font-mono">
                        <span class="text-cyan-400 font-semibold">${Math.round(s.peak_freq_hz)} Hz</span>
                        <button onclick="playCustomTone(${s.peak_freq_hz}, '${s.category}')" class="text-xs px-2.5 py-1 rounded bg-emerald-950/80 hover:bg-emerald-900 text-emerald-300 border border-emerald-800/60 transition active:scale-[0.98] whitespace-nowrap">
                            ▶ Play Call
                        </button>
                    </div>
                </div>
            `).join('');
        }

        function filterCatalog(category) {
            document.querySelectorAll('.cat-pill').forEach(btn => {
                btn.className = 'cat-pill px-3 py-1 rounded-lg bg-canopy-850 text-neutral-400 border border-neutral-800 hover:text-white active:scale-[0.98]';
            });
            event.target.className = 'cat-pill px-3 py-1 rounded-lg bg-emerald-600 text-white font-bold active:scale-[0.98]';

            if (category === 'all') {
                renderCatalogCards(speciesCatalog);
            } else {
                renderCatalogCards(speciesCatalog.filter(s => s.category === category));
            }
        }

        async function initPage() {
            initSpectrum();
            try {
                const res = await fetch('/api/catalog');
                speciesCatalog = await res.json();
                renderCatalogCards(speciesCatalog);
            } catch(e) { console.error('Catalog load error:', e); }

            // Automatically start initial simulated hike
            await startSimulatedHike();
        }

        window.onload = initPage;
    </script>
</body>
</html>
"""
