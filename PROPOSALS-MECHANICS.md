# PROPOSAL: Nucleation Affinity & Epitaxy System

**Date:** 2026-04-23
**Status:** Research proposal — needs prototyping
**Priority:** Mechanics layer, after current rounds complete

---

## The Idea (Professor's insight)

Minerals don't nucleate in isolation. The probability of a crystal forming depends on what's already on the wall — both structurally (epitaxy) and chemically (paragenetic context). Minerals that co-occur in nature get bonuses; minerals that compete for the same broth get penalties (or possibly bonuses, if the first mineral concentrates what the second needs).

## Mechanic: `nucleation_affinity`

Each mineral declares affinity modifiers — how the presence of other minerals affects its nucleation probability:

```json
"nucleation_affinity": {
  "epitaxy": {
    "on_quartz": {"bonus": +0.2, "reason": "structural_match"},
    "on_albite": {"bonus": +0.3, "reason": "lattice_match"},
    "on_feldspar": {"bonus": +0.25, "reason": "framework_silicate_kinship"}
  },
  "competition": {
    "vs_pyrite": {"modifier": -0.1, "reason": "shared_Fe_S"},
    "vs_galena": {"modifier": -0.3, "reason": "strong_broth_overlap"}
  },
  "symbiosis": {
    "after_tourmaline": {"bonus": +0.2, "reason": "topographic_shelter"},
    "after_malachite": {"bonus": +0.15, "reason": "Cu_concentrated_surface"}
  }
}
```

Three categories of affinity:
1. **Epitaxy** — structural/lattice match. Quartz on feldspar, albite on tourmaline. Lowers nucleation energy barrier.
2. **Competition** — shared broth ingredients. Negative modifier when both want the same stuff.
3. **Symbiosis** — sequential paragenesis. One mineral's residue enables the next.

## Open Research Questions

1. **Does competition concentrate or starve?** A mineral consuming Cu might starve its neighbor, OR it might create a Cu-rich surface that enables nucleation. Likely depends on the specific pair. Needs systematic research per mineral pair.

2. **What's the right magnitude?** Affinity bonuses should be significant enough to notice but not so strong that they override broth chemistry. Start with ±0.1–0.3 range and tune.

3. **Is this per-cell or per-vug?** Affinity could apply at the cell level (a crystal grows next to another crystal on the wall) or at the vug level (the overall mineral assemblage affects all nucleation). Cell-level is more realistic but more complex.

---

# PROPOSAL: Broth Residue Cascades

**Date:** 2026-04-23
**Status:** Research proposal
**Priority:** Mechanics layer, complementary with nucleation affinity

---

## The Idea

When mineral A crystallizes, it doesn't just consume ingredients — it changes what's left behind. The residue is chemically different from the original broth, and that difference can ENABLE the next mineral. "The first mineral's exhaust is the second mineral's fuel."

## Mechanic: `residue_effects`

Each mineral declares what its crystallization leaves behind — how it shifts the broth composition beyond simple consumption:

```json
"residue_effects": {
  "azurite": {
    "consumes": {"Cu": -3, "CO3": -2},
    "residue_shift": {"pH": +0.3, "CO2_activity": -0.4},
    "enables": ["malachite"],
    "narrative": "Azurite pulls CO₂ aggressively. The residue is Cu-rich but CO₂-poor — malachite territory."
  },
  "chalcopyrite": {
    "consumes": {"Cu": -1, "Fe": -1, "S": -2},
    "residue_shift": {"Cu_Fe_ratio": +0.5},
    "enables": ["bornite"],
    "narrative": "Chalcopyrite takes 1:1 Cu:Fe. Residual fluid drifts toward higher Cu:Fe — bornite conditions."
  },
  "sphalerite": {
    "consumes": {"Zn": -1, "S": -1},
    "residue_shift": {"relative_Pb": +0.3},
    "enables": ["galena"],
    "narrative": "Sphalerite removes Zn. Pb becomes relatively enriched. Galena follows."
  }
}
```

## Classic Cascade Sequences

**Supergene copper:** chalcopyrite → chalcocite → cuprite → azurite → malachite
Each step changes the oxidation state and residue chemistry.

**MVT sequence:** sphalerite (high T) → galena (lower T) → fluorite → calcite → dolomite
Thermal partitioning + residue enrichment.

**Tsumeb sequence:** primary sulfides → oxidation zone → arsenate zone
O₂ rises, each mineral's exhaust shifts conditions for the next.

## Relationship to Existing Code

This is already happening IMPLICITLY — when quartz consumes SiO₂, everything else is relatively enriched. The proposal makes it EXPLICIT: each mineral declares its residue signature, and the nucleation engine reads it as context for subsequent crystallization.

---

# PROPOSAL: Pseudomorph System

**Date:** 2026-04-23
**Status:** Research proposal
**Priority:** Visual/mechanics layer

---

## The Idea

A crystal that replaces another crystal in-place, keeping the original shape but changing the chemistry. "Goethite (after Pyrite)" — a cube that used to be pyrite.

## Mechanic: `pseudomorph_after`

When conditions shift (typically oxidation), a mineral can undergo in-place replacement:

```json
"pseudomorph": {
  "replaces": "pyrite",
  "trigger": "O2 > 0.5 and pH < 6",
  "preserves": ["habit", "shape", "twin_laws"],
  "changes": ["color", "chemistry", "class"],
  "display_name": "Goethite (after Pyrite)",
  "narrative": "The pyrite couldn't survive the oxygen. But its shape did."
}
```

The crystal keeps its external geometry (cube, octahedron, whatever pyrite grew) but the rendering changes — color shifts from brass-yellow to brown, the luster goes from metallic to earthy. The ghost of the original mineral is visible in the shape.

## Known Pseudomorph Pairs

- Pyrite → Goethite (most common pseudomorph in nature)
- Aragonite → Calcite (over geological time)
- Siderite → Goethite (oxidation, already in game data)
- Azurite → Malachite (partial, common in Bisbee specimens)
- Fluorite → Quartz (rare but dramatic)
- Barite → Quartz (common in some deposits)
- Calcite → Quartz (silicification of fossils = same mechanic)
- Gypsum → Barite (especially desert rose forms)
- Wood → Opal/Chalcedony (petrified wood — mineraloid pseudomorph of organic material)

## Visual Implications

Pseudomorphs are among the most visually interesting specimens because they show TWO stories — the shape tells you what WAS, the material tells you what IS. The display name "Goethite (after Pyrite)" is the mineralogical equivalent of a palimpsest.

---

# PROPOSAL: Mineral Overgrowth & Crystal-on-Crystal Growth

**Date:** 2026-04-23
**Status:** Research proposal
**Priority:** Visual/mechanics layer
**Source:** Professor's request — "more minerals growing on other minerals"

---

## The Idea

In nature, crystals don't just nucleate on bare wall. They grow ON other crystals. The visual result — tourmaline sticking out of albite, quartz coating pyrite, calcite perched on galena — is what makes mineral specimens beautiful.

## Mechanic: `overgrowth_target`

Minerals declare which other minerals they commonly grow on (or in):

```json
"overgrowth": {
  "commonly_on": ["albite", "quartz", "feldspar"],
  "commonly_with": ["muscovite", "lepidolite"],
  "orientation": "radiating_from_matrix",
  "narrative": "Tourmaline needles radiate from albite matrix like a mineral sunburst."
}
```

## Rendering Implications

When mineral A has an overgrowth relationship with mineral B, the renderer should:
1. Place A's crystals emerging FROM B's crystal faces, not from bare wall
2. Orient them according to the declared pattern (radiating, parallel, random, perpendicular)
3. Optionally show a thin contact zone where the two meet

## Classic Overgrowth Assemblages

- **Tourmaline on albite** (pegmatite classic)
- **Quartz on pyrite** (coating/perching)
- **Calcite on galena** (MVT specimens)
- **Azurite/malachite on cuprite** (supergene copper)
- **Wulfenite on mimetite** (oxidized lead zones)
- **Epidote on feldspar** (metamorphic veins)
- **Apophyllite on stilbite** (Deccan Traps — Professor's TN498 context)
- **Fluorite on quartz** (hydrothermal veneer)

---

# PROPOSAL: Zoning & Color Banding

**Date:** 2026-04-23
**Status:** Research proposal
**Priority:** Visual — high payoff for relatively low complexity

---

## The Idea

Each growth band should be colored based on what the broth chemistry was at that moment. Rhodochrosite buttons with pink/white alternating bands. Fluorite with blue/green/purple zones. Amethyst with clear-to-purple gradients.

## Mechanic: `zone_color_from_broth`

When a crystal adds a growth band, the color of that band is determined by the current broth state:

```json
"zoning": {
  "enabled": true,
  "color_source": "broth_snapshot",
  "bands": [
    {"condition": "Mn > 5", "color": "rose_pink"},
    {"condition": "Mn < 2 and Ca > 10", "color": "white"},
    {"condition": "Mn > 5 and Fe > 1", "color": "salmon"}
  ]
}
```

## Classic Zoned Minerals

- **Rhodochrosite** — pink/white button banding (Mn/Ca alternation)
- **Fluorite** — blue/green/purple/clear zones (varying activators)
- **Amethyst** — clear → purple → clear (radiation pulses)
- **Tourmaline** — watermelon (pink core, green rim — Li/Fe shift during growth)
- **Garnet** — growth zoning visible in thin section
- **Calcite** — amber/clear banding (Mn²⁺ fluorescence zones)

## Why This Matters

Zoned crystals are among the most photographed specimens in any collection. The visual payoff per implementation hour is enormous. A rhodochrosite button with alternating pink and white bands would be one of the most beautiful things in the game.

---

# PROPOSAL: Inclusion Rendering

**Date:** 2026-04-23
**Status:** Research proposal
**Priority:** Visual — high rock-shop appeal

---

## The Idea

Minerals trap things during growth. Fluid inclusions (bubbles), mineral inclusions (needles, flakes, crystals), and even color zoning from changing broth chemistry. These inclusions are what make specimens like rutilated quartz and included amethyst among the most popular at rock shops.

## Mechanic: `visible_inclusions`

When mineral A is growing and mineral B is present in the vug, A can trap B as an inclusion:

```json
"inclusions": {
  "trappable": {
    "rutile": {"form": "needles", "frequency": 0.15, "color": "golden"},
    "tourmaline": {"form": "needles", "frequency": 0.1, "color": "black"},
    "hematite": {"form": "flakes", "frequency": 0.2, "color": "red"},
    "fluid": {"form": "bubbles", "frequency": 0.3, "color": "clear"}
  },
  "display_name_overrides": {
    "rutile": "Rutilated Quartz",
    "tourmaline": "Tourmalinated Quartz",
    "hematite": "Strawberry Quartz"
  }
}
```

## Classic Included Minerals

- **Rutilated quartz** — golden needles of rutile in clear quartz
- **Tourmalinated quartz** — black tourmaline needles
- **Strawberry quartz** — hematite flakes in quartz
- **Included amethyst** — goethite needles, creating "cactus quartz"
- **Emerald with jardim** — pyrite/calcite inclusions in emerald
- **Sapphire with silk** — rutile needles creating asterism

---

# PROPOSAL: Display Name Variants

**Date:** 2026-04-23
**Status:** Ready for implementation (simple)
**Priority:** Polish — ties into all other proposals

---

## The Idea

When color_rules trigger, the display name changes. Same mineral, different face. Applied to all color-variant minerals:

```json
"color_rules": {
  "clear": {"default": true, "display_name": "Quartz"},
  "smoky": {"trigger": "radiation_damage > 0.3", "display_name": "Smoky Quartz"},
  "amethyst": {"trigger": "Fe > 2 and radiation_damage > 0.1", "display_name": "Amethyst"},
  "citrine": {"trigger": "heated_amethyst", "display_name": "Citrine"}
}
```

Applied to:
- **Quartz:** clear, smoky, amethyst, citrine, rose (Ti)
- **Beryl:** emerald (Cr/V), aquamarine (Fe²⁺), heliodor (Fe³⁺), morganite (Mn), bixbite (Mn red)
- **Corundum:** ruby (Cr), sapphire (Fe+Ti), padparadscha (Cr+Fe)
- **Spodumene:** kunzite (Mn pink), hiddenite (Cr green)
- **Feldspar:** labradorite, moonstone, sunstone
- **Gypsum/selenite:** desert rose, satin spar, alabaster

Pseudomorph display names follow the same pattern: "Goethite (after Pyrite)"

---

# PROPOSAL: Composite Mineral Assemblages (Rocks)

**Date:** 2026-04-23
**Status:** Research proposal — new game mechanic
**Priority:** After individual minerals are solid

---

## The Idea

Some culturally-named "minerals" are actually rocks — aggregates of multiple minerals. When the right combination nucleates together in the same vug, the game recognizes the composite:

```json
"composite": {
  "name": "Lapis Lazuli",
  "requires": ["lazurite", "calcite", "pyrite"],
  "window_ticks": 10,
  "all_must_be_present": true,
  "display_override": "Lapis Lazuli — blue lazurite with white calcite veining and gold pyrite specks"
}
```

## Extensible Composites

- **Lapis Lazuli** — lazurite + calcite + pyrite
- **Granite** — quartz + feldspar + mica (needs mica first)
- **Unakite** — epidote + feldspar + quartz
- **Eilat Stone** — chrysocolla + turquoise + malachite
- **Petrified Wood** — chalcedony/quartz replacing organic structure

---

🪨
