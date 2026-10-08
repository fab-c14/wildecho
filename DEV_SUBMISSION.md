*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 1: Touch Grass](https://dev.to/challenges/hacktoberfest-week1-2026-10-05)*

# WildEcho 🌲🔊: Offline Backcountry Acoustic Nature Explorer & Eyes-Free Audio Field Guide

## What I Built

Most outdoor and birding apps make the same mistake: they force you to pull a phone from your pocket, squint at a bright screen in midday sun, scroll through dropdowns, and tap buttons while the rare songbird you were listening to flutters away into the brush.

**WildEcho flips the paradigm completely.**

It is an eyes-free, 100% offline backcountry nature explorer designed around a single guiding principle:
> *"Slip your phone into your pocket, put on your earbuds, and listen to the forest. Touch grass without screen fatigue."*

```
                              [ WILD FOREST SOUNDSCAPE ]
                         (Songbirds, Wind, Water, Distant Road)
                                          │
                                          ▼
                             [ Continuous Audio Buffer ]
                                          │
                                          ▼
                 ┌──────────────────────────────────────────────────┐
                 │       Offline Bioacoustic Signal Processing      │
                 │                                                  │
                 │  • Welch Power Spectral Density (PSD)            │
                 │  • NDSI Index (Biophony 2–11kHz vs Anthrophony)  │
                 │  • ACI Complexity Index (Harmonic Temporal Flux) │
                 │  • Spectral Centroid & Resonance Peaks           │
                 └────────────────────────┬─────────────────────────┘
                                          │
                                          ▼
                 ┌──────────────────────────────────────────────────┐
                 │        Offline Wildlife Biometric Matcher        │
                 │                                                  │
                 │  • 12 Embedded Native Species Signatures         │
                 │  • Harmonic Proximity & Peak Tracking            │
                 │  • Habitat (Forest/Wetland) & Seasonal Priors    │
                 └────────────────────────┬─────────────────────────┘
                                          │
                                          ▼
                 ┌──────────────────────────────────────────────────┐
                 │      Google Gemma 2 Naturalist Reasoning Brain   │
                 │                                                  │
                 │  • Eyes-Free Spoken Whisper Prompt Contract      │
                 │  • Wild Foraging Clues (Chanterelles, Morels)    │
                 │  • Backcountry Trail Safety (Snags, Shaded Ledges│
                 └────────────────────────┬─────────────────────────┘
                                          │
                                          ▼
                 ┌──────────────────────────────────────────────────┐
                 │             Eyes-Free Audio Delivery             │
                 │                                                  │
                 │  • ElevenLabs Turbo v2.5 / Web Speech API Audio  │
                 │  • Shannon-Wiener Ecological Diversity Index (H) │
                 │  • Silent Offline JSON Waypoint Field Journal    │
                 └──────────────────────────────────────────────────┘
```

### 🌿 The Core Backcountry Experience:
1. **📱 Phone in Pocket**: Tuck your device away in your backpack or hip pocket. No screen glare, no menus, zero notification anxiety.
2. **🎙️ 100% Offline Bioacoustics**: Edge DSP algorithms compute soundscape purity (**NDSI** — Normalized Difference Soundscape Index) and songbird complexity (**ACI** — Acoustic Complexity Index) locally with **zero cellular reception**.
3. **🎧 Google Gemma 2 Earbud Whispers**: On-device open-weight LLM whispers concise, poetic audio notes (species name, foraging associations, and trail safety) into your wireless earbuds.
4. **📊 Automatic Biodiversity Journal**: Silently logs every waypoint encounter and calculates your trail's **Shannon-Wiener Ecological Diversity Index ($H$)** for review once you return home.

---

## Demo

- 🌐 **Interactive Trail Explorer & Audio Simulator**: Run locally via `uv run wildecho serve --port 8000` (FastAPI + Tailwind + Web Speech API + Web Audio API frequency synthesizer).
- 🌲 **Terminal Eyes-Free Expedition Mode**:
  ```bash
  uv run wildecho listen --trail "Cascade Mountain Ridge" --habitat dense_forest --season autumn
  ```

### Live Simulation Output:
```text
+----------------------------- Expedition Active -----------------------------+
|  WILDECHO   - Offline Backcountry Acoustic Nature Explorer                  |
|  [Eyes-Free Mode] Phone in pocket, earbuds active. Touch grass.             |
|                                                                             |
|  Trail:     Cascade Mountain Ridge Walk                                     |
|  Habitat:   Dense Forest                                                    |
|  Season:    Autumn | Engine: Offline Gemma 2 & Edge Bioacoustics            |
+-----------------------------------------------------------------------------+

---------------- Trail Waypoint #01 - Ambient Sampling Window -----------------
 Soundscape Quality:   Pristine Wilderness (92% Pure Nature)
 Biophony Index (NDSI): [-1.0 ==================>          +1.0] (+0.84)
 Acoustic Complexity:  14.5 ACI | Peak: 3402 Hz

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
| "Listen to the canopy. That liquid flute cascade is a Wood Thrush. Take a   |
| breath and enjoy the moment."                                               |
|                                                                             |
|  🍄 Foraging Clue: Mature deciduous canopy with deep leaf litter; prime     |
|     habitat for Chanterelles and Black Trumpet mushrooms.                   |
|  ⚠️ Trail Safety: Inhabits shaded interior woods; keep bearings on trail    |
|     landmarks.                                                              |
+----- Audio Duration: ~7.7s | Synthesized by Google Gemma 2 Edge ------------+
```

---

## Code

WildEcho is 100% open-source under the MIT license:

{% github fab-c14/wildecho %}

🔗 **GitHub Repository:** [https://github.com/fab-c14/wildecho](https://github.com/fab-c14/wildecho)

---

## How I Built It

WildEcho unites mathematical bioacoustic signal processing, local on-device LLM reasoning, and modern web audio architecture:

### 1. 🔬 Bioacoustic Signal Processing Pipeline (`wildecho/bioacoustics/`)
- **Normalized Difference Soundscape Index (NDSI)**: Implements Bernie Krause's Acoustic Niche Hypothesis to separate human drone (Anthrophony: 50–1500 Hz) from biological calls (Biophony: 2000–11000 Hz):
  $$\text{NDSI} = \frac{\text{Biophony} - \text{Anthrophony}}{\text{Biophony} + \text{Anthrophony}}$$
- **Acoustic Complexity Index (ACI)**: Implemented based on Pieretti et al. (2011), tracking rapid sound intensity fluctuations across spectrogram bins to detect songbirds without being fooled by steady wind.
- **Embedded Wildlife Catalog**: 12 native species across Birds, Amphibians, Mammals, and Insects with acoustic frequency profiles, harmonic ratios, and ecological associations.

### 2. 🧠 Google Gemma 2 Naturalist Reasoning Engine (`wildecho/intelligence/`)
- Powered by **Google Gemma 2** (`google/gemma-2-2b-it`).
- Uses a strict **Eyes-Free Audio Prompt Contract** restricting responses to 2 conversational spoken sentences without markdown, plus wild edible foraging correlations and terrain safety advisories.
- Fallback edge generation ensures 100% operation even on ultra-low-power edge hardware.

### 3. 🎧 Earbud Whisper Streaming (`wildecho/audio/` & Web UI)
- Streams lifelike naturalist narration into wireless earbuds via **ElevenLabs Turbo v2.5** when online.
- In the companion web explorer, leverages native browser **Web Speech API (`window.speechSynthesis`)** and **Web Audio API (`AudioContext`)** to speak whispers and synthesize species sound calls directly in judges' headphones.

### 4. ☁️ Turnkey Deployment on Render (`render.yaml`)
- Declared as an Infrastructure-as-Code service in `render.yaml` for automatic zero-downtime deployment on **Render**:
```yaml
services:
  - type: web
    name: wildecho
    env: python
    buildCommand: pip install uv && uv sync --no-dev
    startCommand: uv run uvicorn wildecho.web.app:app --host 0.0.0.0 --port $PORT
    plan: free
```

---

## Why Does Open Innovation Matter?

In backcountry wilderness, **open-source AI is not an aesthetic preference — it is an absolute necessity:**

1. **Backcountry Zero-Connectivity Execution**: Closed APIs (OpenAI, Claude) require continuous internet. 10 miles deep in a national park with zero cellular towers, closed cloud models are completely dead. Open-weight models like **Google Gemma 2** run locally on the hiker's device with zero latency and zero signal.
2. **Hiker Privacy & Location Sovereignty**: Closed apps frequently beam GPS telemetry, timestamps, and audio to central clouds. WildEcho keeps 100% of location data, trail paths, and audio buffers local.
3. **Zero Cost & Free Public Science**: Outdoor adventurers, conservation volunteers, and national park visitors shouldn't have to pay subscription token fees to learn about their local forest ecosystem.

---

## Prize Categories

### 🌟 Featured Categories:
- **Best Use of Gemma ($200 USD):** WildEcho runs **Google Gemma 2** (`gemma-2-2b-it`) as its core ecological intelligence engine, translating acoustic frequency metrics into eyes-free naturalist field notes and foraging hints.
- **Best Use of Render ($200 USD):** The companion explorer is declared via `render.yaml`, providing a one-click deployment blueprint for Render web services with automatic health monitoring.

### 🤝 Partner Categories:
- **Best Use of ElevenLabs ($100 USD):** Powers the eyes-free earbud voice streaming pipeline using ElevenLabs Turbo v2.5 (`eleven_turbo_v2_5`) for natural, low-latency audio briefings.

---

## Try It Yourself

```bash
# Clone and explore with uv in seconds:
git clone https://github.com/fab-c14/wildecho.git
cd wildecho
uv sync --all-extras
uv run wildecho listen --habitat dense_forest
# Or launch the interactive web companion:
uv run wildecho serve --port 8000
```

*Built with love for nature, open-weight AI, and the wilderness.*  
*Keep your phone in your pocket, listen to the trees, and touch grass! 🌲🎧*
