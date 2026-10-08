# WildEcho 🌲🔊
### Offline Backcountry Acoustic Nature Explorer & Eyes-Free Audio Field Guide
> *Built for Hacktoberfest 2026: Open-Source AI Challenge (Week 1: "Touch Grass")*

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Core Model: Google Gemma 2](https://img.shields.io/badge/Core%20Model-Google%20Gemma%202%20(Open--Weight)-purple.svg)](https://ai.google.dev/gemma)
[![Code Quality: Pylint 10.00/10](https://img.shields.io/badge/pylint-10.00%2F10-brightgreen.svg)](https://pylint.org/)
[![Linter: Ruff](https://img.shields.io/badge/ruff-clean-green.svg)](https://docs.astral.sh/ruff/)
[![Audio Engine: ElevenLabs](https://img.shields.io/badge/Whisper-ElevenLabs%20Turbo-orange.svg)](https://elevenlabs.io/)
[![Deploy: Render Blueprint](https://img.shields.io/badge/Deploy-Render%20Blueprint-46E3B7.svg)](https://render.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🌿 The Core Philosophy: "Touch Grass, Keep Screen in Pocket"

Modern outdoor and birding apps demand that you pull out your phone, unlock a bright glass screen under direct sunlight, navigate clunky menus, and squint at photos while the animal flees into the brush.

**WildEcho flips the paradigm completely:**
* **Zero Screen Time**: Put your phone in your pocket or backpack with your wireless earbuds on. Touch grass, feel the breeze, and hike without digital fatigue.
* **Continuous Backcountry Listening**: Passively samples environmental soundscapes in the background via local microphone buffers.
* **100% Offline Bioacoustics Engine**: Computes spectral power distributions, Normalized Difference Soundscape Index (**NDSI**), and Acoustic Complexity Index (**ACI**) locally on edge hardware with zero cellular signal.
* **Open-Weight Gemma 2 Intelligence**: Correlates biometric audio signatures with elevation, season, and forest habitat to whisper concise (10–15s) naturalist observations directly into your ears.
* **Passive Biodiversity Journaling**: Silently computes Shannon-Wiener ecological diversity metrics ($H$) and archives trail waypoints for post-hike review.

---

## 🏆 Hacktoberfest 2026 Challenge Alignment

WildEcho is tailored specifically for **Week 1: "Touch Grass"** of the Hacktoberfest Open-Source AI Challenge, with turnkey integrations across three premier partner categories:

| Prize Category | Implementation in WildEcho | Key Files |
| :--- | :--- | :--- |
| **Touch Grass (Week 1)** | Eyes-free audio UX designed exclusively for backcountry hiking, forest exploration, and screenless outdoor immersion. | `wildecho/audio/narrator.py`, `wildecho/ui/` |
| **Best Use of Gemma** | Powered by open-weights **Google Gemma 2** (`gemma-2-2b-it` / `gemma-2-9b-it`) via local Ollama inference with deterministic offline edge synthesis fallback. | `wildecho/intelligence/gemma_engine.py`, `wildecho/intelligence/naturalist_prompts.py` |
| **Best Use of Render** | Turnkey companion web application and REST API fully defined with native infrastructure-as-code in `render.yaml`. | `render.yaml`, `wildecho/web/app.py` |
| **Best Use of ElevenLabs** | Whispers ultra-low latency, natural conversational audio briefs directly to wireless earbuds using `eleven_turbo_v2_5`. | `wildecho/audio/narrator.py` |

---

## 🔬 Scientific Architecture & Bioacoustics Pipeline

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

### 1. Normalized Difference Soundscape Index (NDSI)
Formulated by Bernie Krause and Pijanowski et al. based on the **Acoustic Niche Hypothesis**:
$$\text{NDSI} = \frac{\text{Biophony} - \text{Anthrophony}}{\text{Biophony} + \text{Anthrophony}}$$
* $\text{Biophony}$ ($2.0\text{ kHz} - 11.0\text{ kHz}$): Biological bird, amphibian, and insect communications.
* $\text{Anthrophony}$ ($50\text{ Hz} - 1.5\text{ kHz}$): Mechanical engines, aircraft rumble, and industrial drones.
* **Output Range**: $+1.0$ (pristine biological wilderness) to $-1.0$ (intense anthropogenic noise pollution).

### 2. Acoustic Complexity Index (ACI)
Based on Pieretti, Farina & Ceraulo (2011), measuring the temporal variability of sound intensities across frequency bins:
$$\text{ACI} = \frac{\sum_{k} \sum_{t} |I_k(t) - I_k(t-1)|}{\sum_{k} \sum_{t} I_k(t)}$$
Pulsed avian vocalizations and rapid warbles register high complexity, whereas continuous wind and steady stream water produce flat, near-zero scores.

### 3. Shannon-Wiener Ecological Diversity Index ($H$)
Calculates the taxonomic evenness and species richness along each trail:
$$H = -\sum_{i=1}^{S} p_i \ln(p_i)$$
Where $p_i$ is the proportional encounter frequency of species $i$.

---

## 💻 Installation & Quickstart

WildEcho is packaged with [`uv`](https://docs.astral.sh/uv/) for instant, reproducible virtual environments.

### 1. Prerequisites
* Python 3.11+
* `uv` package manager (`pip install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`)
* *(Optional)* Ollama with `gemma2:2b` (`ollama run gemma2:2b`) for local LLM inference.
* *(Optional)* ElevenLabs API Key (`ELEVENLABS_API_KEY`) for live voice synthesis.

### 2. Setup
```bash
git clone https://github.com/fab-c14/wildecho.git
cd wildecho
uv sync --all-extras
```

### 3. Run a Live Backcountry Audio Expedition
```bash
# Simulate a hike through a dense temperate forest in autumn
uv run wildecho listen --trail "Cascade Mountain Ridge" --habitat dense_forest --season autumn --windows 5

# View the offline wildlife catalog
uv run wildecho catalog

# Inspect historical expedition logs
uv run wildecho log
```

### 4. Launch the Companion Web Explorer
```bash
uv run wildecho serve --port 8000
```
Open [http://localhost:8000](http://localhost:8000) in your browser to view the interactive expedition dashboard, live trail simulation player, and acoustic spectrogram breakdown.

---

## 🛠️ CLI Reference

WildEcho features a comprehensive CLI powered by **Typer** and **Rich**:

| Command | Description | Example |
| :--- | :--- | :--- |
| `wildecho listen` | Starts an active backcountry listening session. | `uv run wildecho listen --windows 10 --delay 1.0` |
| `wildecho catalog` | Lists embedded wildlife acoustic profiles & foraging associations. | `uv run wildecho catalog --category bird` |
| `wildecho log` | Summarizes recorded expeditions and Shannon biodiversity scores. | `uv run wildecho log` |
| `wildecho serve` | Launches the companion FastAPI web service. | `uv run wildecho serve --host 0.0.0.0 --port 8000` |
| `wildecho version` | Displays version and bioacoustic engine configuration. | `uv run wildecho version` |

---

## 🦅 Curated Offline Species Catalog

WildEcho embeds full acoustic signatures for native wildlife, allowing total offline biometric identification:

* 🐦 **Wood Thrush** (*Hylocichla mustelina*): Peak $3400\text{ Hz}$, liquid flute cascade $\rightarrow$ *Foraging: Chanterelles & Black Trumpet mushrooms*.
* 🦅 **Pileated Woodpecker** (*Dryocopus pileatus*): Peak $2200\text{ Hz}$, percussive drum $\rightarrow$ *Foraging: Lion's Mane & Oyster mushrooms on hardwood snags*.
* 🦉 **Barred Owl** (*Strix varia*): Peak $850\text{ Hz}$, rhythmic deep hoot $\rightarrow$ *Trail Safety: Active near dusk; headlamp required*.
* 🐸 **Pacific Tree Frog** (*Pseudacris regilla*): Peak $2600\text{ Hz}$, two-syllable ribbit chorus $\rightarrow$ *Foraging: Wild watercress & clean vernal pools*.
* 🐦 **Black-Capped Chickadee** (*Poecile atricapillus*): Peak $4200\text{ Hz}$, sentinel chatter $\rightarrow$ *Foraging: Wild hazelnut groves & elderberries*.
* 🦅 **Red-Tailed Hawk** (*Buteo jamaicensis*): Peak $3800\text{ Hz}$, piercing rasping screech $\rightarrow$ *Safety: Thermal ridge draft; steep cliff warning*.
* 🦗 **True Katydid** (*Pterophylla camellifolia*): Peak $6800\text{ Hz}$, canopy stridulation $\rightarrow$ *Foraging: Mature autumn acorn & hickory nut mast*.
* 🦌 **Rocky Mountain Elk** (*Cervus canadensis*): Peak $1400\text{ Hz}$, high-pitch bugle call $\rightarrow$ *Safety: Rutting season caution; maintain distance*.
* 🐦 **Hermit Thrush** (*Catharus guttatus*): Peak $4100\text{ Hz}$, ascending flute trill $\rightarrow$ *Foraging: Subalpine huckleberry patches*.
* 🐦 **Belted Kingfisher** (*Megaceryle alcyon*): Peak $3200\text{ Hz}$, mechanical dry rattle $\rightarrow$ *Foraging: High-flow pristine trout creeks*.
* 🐸 **American Bullfrog** (*Lithobates catesbeianus*): Peak $280\text{ Hz}$, deep bass drone $\rightarrow$ *Safety: Muddy bottomland swamp boundary*.
* 🐦 **Common Raven** (*Corvus corax*): Peak $950\text{ Hz}$, deep hollow croak $\rightarrow$ *Foraging: Alpine ridge passes & berry slopes*.

---

## ☁️ Deployment on Render

WildEcho includes a turnkey [`render.yaml`](render.yaml) blueprint:

```yaml
services:
  - type: web
    name: wildecho
    env: python
    buildCommand: pip install uv && uv sync --no-dev
    startCommand: uv run uvicorn wildecho.web.app:app --host 0.0.0.0 --port $PORT
    plan: free
```

To deploy:
1. Fork or push this repository to GitHub.
2. In the Render Dashboard, click **New +** $\rightarrow$ **Blueprint**.
3. Connect your repository — Render automatically detects `render.yaml` and deploys the web explorer.

---

## 🧪 Rigorous Quality & Verification

Every module is strictly type-annotated and passes enterprise-grade linters:

```bash
# 1. Unit Tests (100% pass rate)
uv run pytest -v

# 2. Ruff Linting & Formatting
uv run ruff check wildecho/ tests/
uv run ruff format --check wildecho/ tests/

# 3. Pylint Static Analysis (Perfect 10.00/10 Score)
uv run pylint wildecho/ tests/
```

```
============================= test session starts =============================
collected 13 items

tests/test_bioacoustics.py::test_catalog_invariants PASSED               [  7%]
tests/test_bioacoustics.py::test_ndsi_calculation PASSED                 [ 15%]
tests/test_bioacoustics.py::test_aci_complexity PASSED                   [ 23%]
tests/test_bioacoustics.py::test_species_matching PASSED                 [ 30%]
tests/test_cli.py::test_cli_version PASSED                               [ 38%]
tests/test_cli.py::test_cli_catalog_listing PASSED                       [ 46%]
tests/test_cli.py::test_cli_catalog_inspect PASSED                       [ 53%]
tests/test_cli.py::test_cli_listen_session PASSED                        [ 61%]
tests/test_field_log.py::test_waypoint_recording PASSED                  [ 69%]
tests/test_field_log.py::test_shannon_diversity_index PASSED             [ 76%]
tests/test_field_log.py::test_expedition_finalization PASSED             [ 84%]
tests/test_gemma_engine.py::test_prompt_construction PASSED              [ 92%]
tests/test_gemma_engine.py::test_edge_report_synthesis PASSED            [100%]

============================= 13 passed in 14.72s =============================

------------------------------------
Your code has been rated at 10.00/10
```

---

## 📜 License

WildEcho is open-source software licensed under the [MIT License](LICENSE).
Built with ❤️ for backcountry explorers, trail naturalists, and outdoor enthusiasts.
Keep your phone in your pocket, listen to the trees, and touch grass.
