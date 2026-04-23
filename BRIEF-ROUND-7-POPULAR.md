# BRIEF: Round 7 — Popular Minerals + Composite Mechanic

**For:** Builder (syntaxswine)
**From:** 🪨✍️ + Professor
**Date:** 2026-04-23
**Priority:** After Rounds 5-6 complete. This is the next wave.

---

## New Minerals (10 entries)

### 1. Labradorite — (Ca,Na)(Al,Si)₄O₈
**Expands:** existing `feldspar` entry
- Plagioclase feldspar with labradorescence (iridescent play of color from exsolution lamellae)
- **Trigger:** Ca-rich feldspar + slow cooling (allows exsolution lamellae to form)
- **Color:** Gray base, flashes of blue/green/orange. The flash is the whole point.
- **Mechanic:** Labradorescence as a visual effect tied to cooling rate. Fast cooling = no flash. Slow cooling = the exsolution has time to separate into thin layers = interference colors.

### 2. Moonstone — KAlSi₃O₈
**Expands:** existing `feldspar` entry
- Orthoclase feldspar with adularescence (blue-white floating sheen)
- **Trigger:** K-feldspar + thin albite exsolution layers
- **Mechanic:** Similar exsolution mechanic to labradorite but different chemistry and visual effect. Blue-white glow rather than rainbow flash.

### 3. Sunstone — (Ca,Na)(Al,Si)₄O₈
**Expands:** existing `feldspar` entry
- Plagioclase feldspar with aventurescence (sparkling from hematite/copper inclusions)
- **Trigger:** feldspar + trace Cu or Fe inclusions
- **Mechanic:** Inclusions within the crystal rather than exsolution. Different driver than labradorite/moonstone.

### 4. Gypsum varieties — CaSO₄·2H₂O
**Expands:** existing `selenite` entry
- Desert rose (sand-included rosettes in arid conditions)
- Satin spar (fibrous, translucent)
- Alabaster (massive, fine-grained)
- **Mechanic:** Habit variants driven by growth conditions. Desert rose = growth through sand (solid inclusions during growth). Satin spar = fibrous habit on fracture walls. Alabaster = massive habit at low supersaturation.

### 5. Dioptase — CuSiO₃·H₂O
**New entry.** Class: Silicate | System: Trigonal
- Emerald-green copper silicate. One of the most striking collector minerals.
- **Consumes:** Cu, SiO₂, H₂O
- **Conditions:** Oxidizing zone of copper deposits. Low-T hydrothermal.
- **Habits:** Short prismatic crystals, rhombohedral termination. Often stubby, gemmy.
- **Color:** Deep emerald green. One of the greenest minerals that isn't copper carbonate.
- **Competes with:** Malachite, chrysocolla (all oxidized Cu minerals)
- **Key mechanic:** Cu budget competition. If CO₃ is high → malachite wins. If SiO₂ is high → chrysocolla or dioptase. Dioptase needs both Cu AND SiO₂ at specific ratios.

### 6. Turquoise — CuAl₆(PO₄)₄(OH)₈·4H₂O
**New entry.** Class: Phosphate | System: Triclinic
- THE culturally significant blue-green mineral. Ancient trade routes existed for this stuff.
- **Consumes:** Cu, Al, P, H₂O
- **Conditions:** Arid, oxidizing. Weathering of Al-bearing rocks with Cu and P.
- **Habits:** Massive, botryoidal, nodular. Microcrystalline (rarely visible crystals).
- **Color:** Sky blue to blue-green. Iron content shifts it greener.
- **Key mechanic:** Needs all three (Cu + Al + P) simultaneously. Phosphate gate — requires apatite or other phosphate source to be weathering nearby.

### 7. Jadeite — NaAlSi₂O₆
**New entry.** Class: Silicate (pyroxene) | System: Monoclinic
- One of the two jade minerals. The harder, more valuable one.
- **Consumes:** Na, Al, SiO₂
- **Conditions:** High-pressure, low-temperature metamorphic (blueschist facies). Subduction zones.
- **Habits:** Massive, granular. Individual crystals are rare — jade is typically interlocking microcrystalline aggregate.
- **Color:** Green (Fe), lavender (Mn), white (pure), black (omphacite mix).
- **Key mechanic:** Requires high pressure + low temperature. Unusual formation window — most silicates don't form at these conditions. The interlocking aggregate texture = exceptional toughness (not hardness).

### 8. Nephrite — Ca₂(Mg,Fe)₅Si₈O₂₂(OH)₂
**New entry.** Class: Silicate (amphibole) | System: Monoclinic
- The other jade. Softer but tougher than jadeite. More common.
- **Consumes:** Ca, Mg, Fe, SiO₂
- **Conditions:** Metamorphic (greenschist facies). Less extreme pressure than jadeite.
- **Habits:** Massive, fibrous interlocking aggregate.
- **Color:** Green (Fe) to white (Mg endmember).
- **Key mechanic:** Fibrous interlocking = extreme toughness. Different formation conditions than jadeite (lower pressure, more Ca/Mg available).

### 9. Lazurite — (Na,Ca)₈(AlSiO₄)₆(SO₄,S,Cl)₂
**New entry.** Class: Feldspathoid (silicate) | System: Isometric
- The blue component of lapis lazuli. The actual mineral that makes lapis blue.
- **Consumes:** Na, Ca, Al, SiO₂, S
- **Conditions:** Contact metamorphism of limestone. Low SiO₂ (feldspathoid, not feldspar — forms when there isn't enough silica to make feldspar).
- **Habits:** Massive, granular. Rare dodecahedral crystals.
- **Color:** Deep ultramarine blue. The blue is from S₃⁻ radical anion — one of the only minerals colored by a molecular ion.
- **Key mechanic:** Low-SiO₂ gate. Lazurite only forms when silica is insufficient to make feldspar. If SiO₂ is high, you get feldspar instead.

### 10. Opal — SiO₂·nH₂O
**New entry.** Class: Mineraloid | System: Amorphous
- Not technically a mineral (amorphous), but culturally essential.
- **Consumes:** SiO₂, H₂O
- **Conditions:** Low temperature, silica-rich fluids in arid environments. Australia conditions.
- **Habits:** Massive, botryoidal, vein-filling.
- **Color:** Precious opal = play-of-color from diffraction through silica sphere arrays. Common opal = no play of color. Fire opal = orange body color.
- **Key mechanic:** Sphere-packing diffraction. Play-of-color emerges when uniform silica spheres (~150-400nm) self-assemble into a periodic lattice. Uniform sphere size = better play of color. Variable sphere size = common opal. This is essentially a natural diffraction grating.

---

## Composite Mechanic: Lapis Lazuli

**New game mechanic — co-crystallization composites.**

Lapis lazuli is NOT a single mineral. It's a rock composed of:
- **Lazurite** (blue — the color source)
- **Calcite** (white veins)
- **Pyrite** (gold specks)

**Mechanic:** If lazurite, calcite, AND pyrite all nucleate in the same vug within the same turn (or within N ticks of each other), the game recognizes the composite and labels the formation "Lapis Lazuli" rather than listing three separate minerals.

This is geologically correct — lapis lazuli is defined by the co-occurrence, not by any single mineral. The gold specks of pyrite in the blue lazurite matrix are diagnostic.

**Display:** The composite gets its own visual treatment — blue base with white calcite veining and gold pyrite inclusions. More visually striking than any of the three components alone.

**This mechanic is extensible:**
- Granite (quartz + feldspar + mica co-crystallization)
- Unakite (epidote + feldspar + quartz)
- Eilat stone (chrysocolla + turquoise + malachite)
- Any paragenetic assemblage that's culturally named as a "rock" rather than a "mineral"

---

## Display Name Variant Mechanic

**Applies to all color-variant minerals.** When `color_rules` trigger fires, the display name changes:

```json
"color_rules": {
  "clear": {"default": true, "display_name": "Quartz"},
  "smoky": {"trigger": "radiation_damage > 0.3", "display_name": "Smoky Quartz"},
  "amethyst": {"trigger": "Fe > 2 and radiation_damage > 0.1", "display_name": "Amethyst"},
  "citrine": {"trigger": "heated_amethyst", "display_name": "Citrine"}
}
```

Same pattern for:
- **Beryl:** emerald (Cr/V), aquamarine (Fe²⁺), heliodor (Fe³⁺), morganite (Mn), bixbite (Mn red)
- **Corundum:** ruby (Cr), sapphire (Fe+Ti), padparadscha (Cr+Fe)
- **Spodumene:** kunzite (Mn pink), hiddenite (Cr green)
- **Feldspar:** labradorite, moonstone, sunstone
- **Gypsum/selenite:** desert rose, satin spar, alabaster

---

🪨
