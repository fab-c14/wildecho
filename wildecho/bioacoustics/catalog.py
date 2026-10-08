"""
WildEcho Bioacoustics Catalog
Embedded offline acoustic signature database of North American and European wildlife.
Enables instant offline biometric identification in backcountry settings with zero signal.
"""

from pydantic import BaseModel, Field


class SpeciesSignature(BaseModel):
    """Acoustic and ecological profile for offline biometric matching."""

    id: str
    common_name: str
    scientific_name: str
    category: str = Field(description="bird, amphibian, mammal, or insect")
    habitats: list[str] = Field(default_factory=list)
    seasons: list[str] = Field(default_factory=list)
    min_freq_hz: float
    max_freq_hz: float
    peak_freq_hz: float
    harmonic_count: int = 1
    call_pattern: str = "melodic_whistle"
    typical_cadence_hz: float = 1.0
    field_description: str
    foraging_association: str
    safety_note: str | None = None


# Comprehensive offline species catalog curated for temperate forests, mountains, and wetlands
SPECIES_CATALOG: list[SpeciesSignature] = [
    SpeciesSignature(
        id="wood_thrush",
        common_name="Wood Thrush",
        scientific_name="Hylocichla mustelina",
        category="bird",
        habitats=["dense_forest", "riparian_stream", "mixed_woodland"],
        seasons=["spring", "summer", "autumn"],
        min_freq_hz=2100.0,
        max_freq_hz=4800.0,
        peak_freq_hz=3400.0,
        harmonic_count=3,
        call_pattern="flute_cascade",
        typical_cadence_hz=0.8,
        field_description="Liquid, flute-like ethereal three-part song ending in a rapid trill.",
        foraging_association="Indicates mature deciduous canopy with deep leaf litter; prime habitat for Chanterelles and Black Trumpet mushrooms.",
        safety_note="Inhabits shaded interior woods; keep bearings on trail landmarks.",
    ),
    SpeciesSignature(
        id="pileated_woodpecker",
        common_name="Pileated Woodpecker",
        scientific_name="Dryocopus pileatus",
        category="bird",
        habitats=["dense_forest", "old_growth", "mountain_trail"],
        seasons=["spring", "summer", "autumn", "winter"],
        min_freq_hz=1400.0,
        max_freq_hz=3200.0,
        peak_freq_hz=2200.0,
        harmonic_count=2,
        call_pattern="percussive_drum",
        typical_cadence_hz=1.8,
        field_description="Loud, resonant, descending laugh 'cuk-cuk-cuk' and heavy deep wood hammer drumming.",
        foraging_association="Excavates dead and dying standing hardwoods; high probability of wild Lion's Mane (Hericium) and Oyster mushrooms on nearby snags.",
        safety_note="Watch overhead for loose falling dead branches near standing snags.",
    ),
    SpeciesSignature(
        id="barred_owl",
        common_name="Barred Owl",
        scientific_name="Strix varia",
        category="bird",
        habitats=["dense_forest", "riparian_stream", "wetland_marsh"],
        seasons=["spring", "summer", "autumn", "winter"],
        min_freq_hz=450.0,
        max_freq_hz=1800.0,
        peak_freq_hz=850.0,
        harmonic_count=4,
        call_pattern="deep_hoot",
        typical_cadence_hz=0.5,
        field_description="Rhythmic, eight-note cadence: 'Who cooks for you? Who cooks for you-all?'",
        foraging_association="Prefers mature swamp borders and bottomlands with abundant moss; look for wild ramps in spring and rich damp soils.",
        safety_note="Active near dusk; ensure headlamp is packed before venturing deeper.",
    ),
    SpeciesSignature(
        id="pacific_tree_frog",
        common_name="Pacific Tree Frog",
        scientific_name="Pseudacris regilla",
        category="amphibian",
        habitats=["riparian_stream", "wetland_marsh", "mountain_trail"],
        seasons=["spring", "summer", "autumn"],
        min_freq_hz=1800.0,
        max_freq_hz=3600.0,
        peak_freq_hz=2600.0,
        harmonic_count=2,
        call_pattern="ribbit_chorus",
        typical_cadence_hz=2.2,
        field_description="Loud two-syllable 'krek-ek' or 'rib-bit', often calling in synchronized acoustic choruses.",
        foraging_association="Marks clean, unpolluted seasonal vernal pools; wild watercress and stinging nettles often flank nearby damp banks.",
        safety_note="Sign of muddy or slippery embankments; watch footing near water edges.",
    ),
    SpeciesSignature(
        id="black_capped_chickadee",
        common_name="Black-Capped Chickadee",
        scientific_name="Poecile atricapillus",
        category="bird",
        habitats=["dense_forest", "mixed_woodland", "open_meadow", "mountain_trail"],
        seasons=["spring", "summer", "autumn", "winter"],
        min_freq_hz=3200.0,
        max_freq_hz=7500.0,
        peak_freq_hz=4200.0,
        harmonic_count=2,
        call_pattern="rapid_chatter",
        typical_cadence_hz=2.5,
        field_description="Clear two-note whistling 'fee-bee' or buzzy flock sentinel 'chick-a-dee-dee-dee'.",
        foraging_association="Forages in birch, willow, and conifer edges; frequent companion to wild hazelnut groves and elderberry thickets.",
        safety_note="Harmless sentinel; increased 'dee' notes warn of nearby predators or large animals.",
    ),
    SpeciesSignature(
        id="red_tailed_hawk",
        common_name="Red-Tailed Hawk",
        scientific_name="Buteo jamaicensis",
        category="bird",
        habitats=["open_meadow", "mountain_trail", "mixed_woodland"],
        seasons=["spring", "summer", "autumn", "winter"],
        min_freq_hz=2500.0,
        max_freq_hz=5200.0,
        peak_freq_hz=3800.0,
        harmonic_count=2,
        call_pattern="piercing_screech",
        typical_cadence_hz=0.4,
        field_description="Piercing, raspy, descending 2-second raptor scream: 'kreeee-aaaarrr'.",
        foraging_association="Circles sunny south-facing open ridge thermal zones; open clearings frequently host wild blueberries, rosehips, and sumac.",
        safety_note="Thermals indicate steep cliffs or open exposure; be mindful of wind and hydration.",
    ),
    SpeciesSignature(
        id="katydid",
        common_name="True Katydid",
        scientific_name="Pterophylla camellifolia",
        category="insect",
        habitats=["dense_forest", "mixed_woodland"],
        seasons=["summer", "autumn"],
        min_freq_hz=4500.0,
        max_freq_hz=11000.0,
        peak_freq_hz=6800.0,
        harmonic_count=1,
        call_pattern="stridulation_rasp",
        typical_cadence_hz=3.0,
        field_description="Loud, mechanical, pulsating 3-pulsed rasp: 'Katy-did, Katy-didn't' from high canopy.",
        foraging_association="Calls from mature oak and hickory treetops; indicator of heavy autumn acorn and hickory nut mast drops.",
        safety_note="Sign of warm late-summer/autumn evenings; temperature drops rapidly after dusk.",
    ),
    SpeciesSignature(
        id="common_raven",
        common_name="Common Raven",
        scientific_name="Corvus corax",
        category="bird",
        habitats=["mountain_trail", "old_growth", "open_meadow"],
        seasons=["spring", "summer", "autumn", "winter"],
        min_freq_hz=600.0,
        max_freq_hz=2100.0,
        peak_freq_hz=1100.0,
        harmonic_count=3,
        call_pattern="deep_croak",
        typical_cadence_hz=0.7,
        field_description="Deep, resonant, guttural wooden croak 'grrruk' and hollow bell-like knocking.",
        foraging_association="Intelligent opportunist; scavenges along game trails and subalpine meadows with wild currants and juniper berries.",
        safety_note="Repeated agitated raven calls often indicate large predators (bears, cougars) near carrion.",
    ),
    SpeciesSignature(
        id="hermit_thrush",
        common_name="Hermit Thrush",
        scientific_name="Catharus guttatus",
        category="bird",
        habitats=["dense_forest", "mountain_trail"],
        seasons=["spring", "summer", "autumn"],
        min_freq_hz=2400.0,
        max_freq_hz=6100.0,
        peak_freq_hz=4100.0,
        harmonic_count=4,
        call_pattern="ethereal_chords",
        typical_cadence_hz=0.6,
        field_description="Opens with a clear pure fluted note followed by ethereal, echoing minor chords.",
        foraging_association="Inhabits subalpine fir and hemlock forests with damp moss carpets; prime territory for King Bolete (Porcini).",
        safety_note="High altitude indicator; prepare for sudden mountain temperature shifts.",
    ),
    SpeciesSignature(
        id="american_bullfrog",
        common_name="American Bullfrog",
        scientific_name="Lithobates catesbeianus",
        category="amphibian",
        habitats=["wetland_marsh", "riparian_stream"],
        seasons=["spring", "summer"],
        min_freq_hz=180.0,
        max_freq_hz=950.0,
        peak_freq_hz=420.0,
        harmonic_count=3,
        call_pattern="deep_drone",
        typical_cadence_hz=0.5,
        field_description="Deep, resonant, low-pitch foghorn drone 'jug-o-rum' echoing across open still water.",
        foraging_association="Lurks in still oxbows and cattail marshes; rich foraging grounds for wild cattail shoots and duck potato (arrowhead).",
        safety_note="Soft deep marsh sediment; do not wade without testing bottom firmness.",
    ),
    SpeciesSignature(
        id="rocky_mountain_elk",
        common_name="Rocky Mountain Elk",
        scientific_name="Cervus canadensis nelsoni",
        category="mammal",
        habitats=["mountain_trail", "open_meadow", "dense_forest"],
        seasons=["autumn"],
        min_freq_hz=700.0,
        max_freq_hz=4200.0,
        peak_freq_hz=2800.0,
        harmonic_count=3,
        call_pattern="piercing_bugle",
        typical_cadence_hz=0.3,
        field_description="High-pitched, piercing, haunting autumnal rut bugle transitioning to deep guttural grunts.",
        foraging_association="Grazes in subalpine aspen groves and grassy glades; aspen stands host wild Leccinum mushrooms.",
        safety_note="CAUTION: Bull elk during autumn rut are highly aggressive. Maintain at least 50 yards distance.",
    ),
    SpeciesSignature(
        id="belted_kingfisher",
        common_name="Belted Kingfisher",
        scientific_name="Megaceryle alcyon",
        category="bird",
        habitats=["riparian_stream", "wetland_marsh"],
        seasons=["spring", "summer", "autumn"],
        min_freq_hz=1600.0,
        max_freq_hz=4800.0,
        peak_freq_hz=3100.0,
        harmonic_count=2,
        call_pattern="mechanical_rattle",
        typical_cadence_hz=3.5,
        field_description="Loud, harsh, mechanical ungreased-spool fishing reel chatter patrol rattle.",
        foraging_association="Patrols clear gravel-bottom streams with active minnow pools; stream sandbars frequently feature wild mint.",
        safety_note="Steep eroded earthen riverbanks can give way suddenly; watch your step.",
    ),
]

CATALOG_MAP: dict[str, SpeciesSignature] = {s.id: s for s in SPECIES_CATALOG}


def get_catalog_by_habitat(habitat: str) -> list[SpeciesSignature]:
    """Filters species by habitat type."""
    return [s for s in SPECIES_CATALOG if habitat in s.habitats]


def get_catalog_by_season(season: str) -> list[SpeciesSignature]:
    """Filters species by seasonal presence."""
    return [s for s in SPECIES_CATALOG if season in s.seasons]
