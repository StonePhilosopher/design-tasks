# Mineral Implementation Status — 2026-04-23

**62 minerals implemented. Zero drift.** 

## Remaining from Rounds 3-6 (17 minerals)

### Round 3: Carbonates ✅ DONE
All four implemented (aragonite, siderite, rhodochrosite, dolomite)

### Round 4: Sulfates + Halide — 2 remaining
- ✅ Barite (done in Round 5)
- ✅ Celestine (done in Round 5)
- ❌ **Gypsum** — merge into existing `selenite` (decision: gypsum habits expand selenite)
- ❌ **Halite** — NaCl, needs Cl broth field

### Round 5: Oxides + Phosphate — 4 remaining
- ❌ **Corundum** — Al₂O₃ (ruby/sapphire)
- ❌ **Rutile** — TiO₂ (needs Ti broth field)
- ❌ **Franklinite** — (Zn,Mn,Fe)(Fe,Mn)₂O₄ (Franklin NJ specific)
- ❌ **Apatite** — Ca₅(PO₄)₃(F,Cl,OH) (needs P broth field)

### Round 6: Silicates — 11 remaining
- ❌ **Orthoclase/Microcline** — expand existing `feldspar` (decision: not new entry)
- ❌ **Garnet** — X₃Z₂(SiO₄)₃ (almandine/grossular/spessartine)
- ❌ **Staurolite** — Fe₂Al₉Si₄O₂₂(OH)₂
- ❌ **Diopside** — CaMgSi₂O₆
- ❌ **Epidote** — Ca₂(Al,Fe³⁺)₃(SiO₄)₃(OH)
- ❌ **Titanite** — CaTiSiO₅
- ❌ **Prehnite** — Ca₂Al₂Si₃O₁₀(OH)₂
- ❌ **Stilbite** — NaCa₄Al₉Si₂₇O₇₂·28H₂O
- ❌ **Heulandite** — (Ca,Na)₂₋₃Al₃(Al,Si)₂Si₁₃O₃₆·12H₂O
- ❌ **Willemite** — Zn₂SiO₄

## Merge decisions (no new entry needed)
- **Gypsum → selenite**: gypsum habits (desert rose, satin spar) expand the existing selenite entry
- **Orthoclase/Microcline → feldspar**: expand existing feldspar with twinning mechanics

## New broth fields needed
- **Ti** (rutile, titanite)
- **P** (apatite)
- **Cl** (halite, apatite)
- **Co** (already added in Round 2)
- **Ni** (already added in Round 2)

## Full spec
`proposals/MINERALS-ROUNDS-3-6.md` in vugg-simulator repo
