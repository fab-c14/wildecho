# WildEcho 🌲🔊: Offline Backcountry Acoustic Nature Explorer & Eyes-Free Audio Field Guide

> *Submitted for the **Hacktoberfest 2026: Open-Source AI Challenge (Week 1: "Touch Grass")**.*
> *Tags: `#hf26challenge`, `#opensource`, `#ai`, `#python`*

---

## 1. The Core Philosophy: "Touch Grass, Keep Phone in Pocket" 🌿

Every existing outdoor and bird-watching application today makes the same mistake:
It forces you to take your phone out of your pocket, unlock a glowing screen in bright sunlight, fiddle with dropdown menus, squint at photos, and scroll while the rare songbird you were listening to flies away into the brush.

Technology in the outdoors should deepen your immersion in nature, not distract you with screen fatigue.

**WildEcho flips the paradigm completely**:
* **100% Screen-Free Experience**: Slip your phone into your pocket or backpack with your wireless earbuds in. Walk the trail, smell the pines, and listen.
* **Passive Backcountry Acoustic Sampling**: Passively samples the ambient soundscape in the background using continuous audio buffers.
* **Offline Bioacoustics on the Edge**: Computes soundscape frequency metrics (Normalized Difference Soundscape Index — **NDSI**, and Acoustic Complexity Index — **ACI**) locally on your device with **zero cellular reception**.
* **Open-Weight Gemma 2 Naturalist Intelligence**: Correlates acoustic frequency peaks with habitat, season, and elevation to whisper concise, poetic (10–15s) naturalist audio notes into your earbuds.
* **Automatic Biodiversity Mapping**: Silently logs every detected species and calculates your trail's **Shannon-Wiener Ecological Diversity Index ($H$)** for post-hike reflection.

---

## 2. What I Built 🛠️

WildEcho is a complete, offline-first backcountry acoustic nature explorer and eyes-free audio companion.

```
                                  [ WILD SOUNDSCAPE ]
                            (Birds, Wind, Water, Distant Road)
                                            │
                                            ▼
                                [ Audio Buffer (22.05 kHz) ]
                                            │
                                            ▼
                    ┌──────────────────────────────────────────────┐
                    │        Bioacoustic Signal Processing         │
                    │                                              │
                    │  1. Welch PSD Spectral Decomposition         │
                    │  2. NDSI Index (Biophony vs. Anthrophony)    │
                    │  3. ACI Complexity Index (Temporal Flux)     │
                    │  4. Spectral Centroid & Peak Detection       │
                    └───────────────────────┬──────────────────────┘
                                            │
                                            ▼
                    ┌──────────────────────────────────────────────┐
                    │       Offline Species Biometric Matcher      │
                    │                                              │
                    │  * 12 Curated Wildlife Signatures            │
                    │  * Harmonic Ratio & Peak Proximity           │
                    │  * Bayesian Habitat & Seasonal Priors        │
                    └───────────────────────┬──────────────────────┘
                                            │
                                            ▼
                    ┌──────────────────────────────────────────────┐
                    │        Gemma 2 Naturalist Reasoner           │
                    │                                              │
                    │  * Eyes-Free Audio Whisper Contract          │
                    │  * Foraging Correlation (Mushrooms / Nuts)   │
                    │  * Trail Safety Observation (Snags / Cliffs) │
                    └───────────────────────┬──────────────────────┘
                                            │
                                            ▼
                    ┌──────────────────────────────────────────────┐
                    │            Eyes-Free Audio Delivery          │
                    │                                              │
                    │  * Wireless Earbud Narration (ElevenLabs)   │
                    │  * Shannon-Wiener Biodiversity Log (H)       │
                    │  * Offline JSON Waypoint Persistence         │
                    └──────────────────────────────────────────────┘
```

### Core Features:
1. **Offline Acoustic Ecology Pipeline (`wildecho/bioacoustics/`)**:
   - **Normalized Difference Soundscape Index (NDSI)**: Quantifies the ratio of biological sounds (Biophony: 2–11 kHz) to human mechanical noise (Anthrophony: 50–1500 Hz) using the Bernie Krause Acoustic Niche Hypothesis.
   - **Acoustic Complexity Index (ACI)**: Measures temporal intensity fluctuations across biological frequency bands (Pieretti et al., 2011), accurately distinguishing dynamic bird chirps and frog choruses from static wind noise.
   - **Curated Wildlife Catalog**: 12 native species profiles (Wood Thrush, Pileated Woodpecker, Barred Owl, Pacific Tree Frog, Katydid, Rocky Mountain Elk, etc.) with frequency bounds, harmonic structures, foraging correlations, and trail safety warnings.

2. **Gemma 2 Naturalist Reasoning Engine (`wildecho/intelligence/`)**:
   - Powered by **Google Gemma 2** (`gemma2:2b` / `gemma2:9b`).
   - Enforces strict eyes-free conversational prompt contracts: exactly 2 sentences of conversational earbud audio, followed by foraging associations and trail safety alerts.
   - Includes deterministic offline edge synthesis fallback for pure edge devices without Ollama running.

3. **Earbud Whisper Engine (`wildecho/audio/`)**:
   - Whispers audio observations directly into wireless earbuds using **ElevenLabs Turbo v2.5**.
   - Offline word-rate and duration estimation for local test harnesses.

4. **Forest Terminal UI & Companion Web App (`wildecho/ui/` & `wildecho/web/`)**:
   - Rich, color-coded terminal dashboard with live biophony gauges, NDSI meters, and species detection cards.
   - FastAPI companion web application deployed on **Render** (`render.yaml`) featuring an interactive trail explorer and JSON export.

---

## 3. Why Open Innovation & Open-Source AI is at the Core 🧠

The prompt for Week 1 asked: *Why does open innovation matter for what you built?*

In the backcountry, **open-source AI is not a stylistic choice — it is an engineering necessity:**

1. **Backcountry Zero-Connectivity Execution**:
   Closed LLM APIs (OpenAI, Claude, etc.) require high-speed internet and uninterrupted 5G signal. If you are 12 miles deep in the North Cascades or Glacier National Park, closed APIs are 100% dead on arrival. With **Google Gemma 2** (`gemma-2-2b-it`), the entire weights live on the device. Inference runs locally on edge NPUs or laptop hardware with zero latency and zero signal.
2. **Hiker Privacy & Location Sovereignty**:
   Nature apps frequently transmit GPS coordinates, timestamps, and audio recordings to centralized cloud servers. WildEcho keeps all location and acoustic data strictly on your local device.
3. **Zero Recurring Token Costs**:
   Backcountry explorers and rangers can sample soundscapes 24 hours a day without running up monthly API subscription fees or token bills.

---

## 4. Hacktoberfest Prize Category Integrations 🏆

### 🌟 Best Use of Gemma (Google Gemma 2)
WildEcho uses **Google Gemma 2** (`gemma2:2b` / `gemma2:9b`) as its core ecological reasoning brain. Rather than outputting visual markdown, Gemma operates under an **eyes-free audio prompt contract**:

```python
# From wildecho/intelligence/naturalist_prompts.py
SYSTEM_NATURALIST_CONTRACT = """
You are WildEcho, a wise and quiet backcountry naturalist companion whispering into a hiker's wireless earbuds.
The hiker has their phone tucked away in their pocket to touch grass and immerse themselves in nature.

STRICT CONSTRAINTS:
1. AUDIO FIRST: Write exclusively for spoken earbud listening (conversational cadence).
2. NO MARKDOWN OR BULLETS in the audio script. Maximum 2 sentences (10 to 15 seconds of spoken audio).
3. Connect the species detection to immediate foraging indicators (wild mushrooms, berries, nuts) and terrain safety.
"""
```

### 🚀 Best Use of Render
WildEcho includes a native [`render.yaml`](render.yaml) Infrastructure-as-Code blueprint that deploys the companion FastAPI explorer with a single click:

```yaml
services:
  - type: web
    name: wildecho
    env: python
    buildCommand: pip install uv && uv sync --no-dev
    startCommand: uv run uvicorn wildecho.web.app:app --host 0.0.0.0 --port $PORT
    plan: free
```

### 🎙️ Best Use of ElevenLabs
When wireless earbuds are connected, WildEcho streams ultra-natural, low-latency audio field notes using the **ElevenLabs Turbo v2.5** endpoint (`eleven_turbo_v2_5`), providing a voice experience that sounds like a seasoned naturalist walking beside you on the trail.

---

## 5. Live Simulation: Walking the Cascade Mountain Trail 🌲

Here is an actual simulation run from `wildecho listen --trail "Cascade Mountain Trail" --habitat dense_forest --season autumn`:

```
+----------------------------- Expedition Active -----------------------------+
|  WILDECHO   - Offline Backcountry Acoustic Nature Explorer                  |
|  [Eyes-Free Mode] Phone in pocket, earbuds active. Touch grass.             |
|                                                                             |
|  Trail:     Cascade Mountain Trail                                          |
|  Habitat:   Dense Forest                                                    |
|  Season:    Autumn | Engine: Offline Gemma 2 & Edge Bioacoustics            |
+-----------------------------------------------------------------------------+

---------------- Trail Waypoint #01 - Ambient Sampling Window -----------------
 Soundscape Quality:   Serene Nature Trail
 Biophony Index (NDSI): [-1.0 ==================>          +1.0] (+0.35)
 Acoustic Complexity:  13.3 ACI | Peak: 3402 Hz

                  Detected Biological Species (Bioacoustics)                   
+-----------------------------------------------------------------------------+
| #   | Common Name    | Scientific Name | Class     | Peak Freq | Confidence |
|-----+----------------+-----------------+-----------+-----------+------------|
| 1   | Wood Thrush    | Hylocichla      | BIRD      |   3402 Hz |      98.0% |
|     |                | mustelina       |           |           |            |
+-----------------------------------------------------------------------------+

+--------------------------- Earbud Audio Briefing ---------------------------+
|  [WHISPER DELIVERED TO EARBUDS]                                             |
|                                                                             |
| "Listen to the canopy. That flute cascade is a Wood Thrush. Take a breath   |
| and enjoy the moment."                                                      |
|                                                                             |
|  Naturalist Insight: Active Wood Thrush singing suggests this trail edge    |
| remains an important wildlife acoustic corridor.                            |
|  Foraging Association: Indicates mature deciduous canopy with deep leaf     |
| litter; prime habitat for Chanterelles and Black Trumpet mushrooms.         |
|  Trail Safety: Inhabits shaded interior woods; keep bearings on trail       |
| landmarks.                                                                  |
+----- Audio Duration: ~7.7s | Synthesized by gemma-2-2b-it:offline-edge -----+

------------------------------ Trailhead Reached ------------------------------
+------------------------- Expedition Field Summary --------------------------+
|  EXPEDITION COMPLETE  - Backcountry Field Log Compiled                      |
|                                                                             |
|  Trail:              Cascade Mountain Trail                                 |
|  Duration:           0.2 minutes | 3 waypoints sampled                      |
|  Mean NDSI:          -0.469 (Bio-to-Anthro Soundscape Ratio)                |
|  Mean ACI:           9.25 (Acoustic Complexity Index)                       |
|  Shannon Index:      0.693 (Taxonomic Diversity H)                          |
|  Total Species:      2 (Wood Thrush, Barred Owl)                            |
+-----------------------------------------------------------------------------+
```

---

## 6. Code Quality & Verification 🔬

WildEcho was engineered with strict typing and enterprise-grade quality standards:
* **100% Unit Test Pass Rate**: 13/13 Pytest tests passing (`uv run pytest -v`).
* **Pylint Score**: **10.00 / 10.00** across both source code and test suites.
* **Ruff**: 100% compliant and auto-formatted.

---

## 7. Try It Yourself & Code Repository 🔗

* **GitHub Repository**: [github.com/fab-c14/wildecho](https://github.com/fab-c14/wildecho)
* **License**: MIT License

```bash
# Clone and run in seconds with uv:
git clone https://github.com/fab-c14/wildecho.git
cd wildecho
uv sync --all-extras
uv run wildecho listen --habitat dense_forest
```

*Built with love for nature, open-weight AI, and the wilderness.*
*Keep your phone in your pocket, listen to the trees, and touch grass.*
