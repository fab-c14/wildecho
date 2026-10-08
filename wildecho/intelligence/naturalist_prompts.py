"""
WildEcho Naturalist Prompt Design Contracts
Structured prompting engine designed specifically for Google Gemma 2.
Enforces eyes-free constraint: output must be immediately speakable in <15 seconds.
"""

from wildecho.bioacoustics.catalog import SpeciesSignature


def build_gemma_naturalist_prompt(
    species: SpeciesSignature, confidence: float, ndsi: float, aci: float, habitat: str, season: str
) -> str:
    """
    Constructs an ecological reasoning prompt for Gemma 2.
    Instructs the model to generate a concise, whisper-ready audio field note
    plus foraging and safety associations.
    """
    return f"""<start_of_turn>user
You are WildEcho, an offline backcountry naturalist AI companion whispering into a hiker's earbuds.
The user is outdoors touching grass. They have their phone in their pocket and must NOT look at a screen.
A bioacoustic audio sensor just detected a wildlife vocalization on the trail:

- Identified Species: {species.common_name} ({species.scientific_name})
- Taxonomic Class: {species.category.upper()}
- Detection Confidence: {confidence * 100:.1f}%
- Soundscape Health (NDSI): {ndsi:+.2f} (Scale: -1.0 anthropic noise to +1.0 pristine biophony)
- Acoustic Complexity (ACI): {aci:.1f}
- Trail Habitat: {habitat.replace("_", " ").title()}
- Season: {season.title()}

Species Field Reference:
- Song Pattern: {species.call_pattern.replace("_", " ")}
- Field Acoustic Note: {species.field_description}
- Ecological Association: {species.foraging_association}
- Safety Consideration: {species.safety_note or "Trail clear"}

Provide an eyes-free naturalist briefing following these strict guidelines:
1. WHISPER SCRIPT: Exactly 1 to 2 short sentences (under 25 words). Spoken directly into the hiker's ear. Calm, evocative, informative. Do not mention confidence percentages or metrics.
2. ECOLOGICAL INSIGHT: 1 concise sentence explaining what this species' presence reveals about this micro-habitat.
3. FORAGING & SAFETY: 1 concise sentence highlighting nearby wild forage or trail awareness.

Format your response as:
WHISPER: <whisper text>
INSIGHT: <insight text>
FORAGING_SAFETY: <foraging and safety text>
<end_of_turn>
<start_of_turn>model
"""
