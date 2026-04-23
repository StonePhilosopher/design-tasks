# PROPOSAL: Geological Seasons — Event Regimes for Long Games

**Date:** 2026-04-23
**Status:** Backlog — low priority, future work
**Source:** Professor's insight on warming/cooling cycles and tectonic grouping

---

## The Problem

Currently, rare events (twins, phantoms, inclusions, dissolution episodes) fire as random per-step rolls. This causes two bugs:

1. **Per-step accumulation**: a twin probability of 8% per zone means a 30-zone crystal has a 91.6% chance of twinning. Every crystal twins. (Current state of selenite, cerussite.)
2. **No narrative structure**: events are a slot machine, not a story. Long games feel like noise instead of geology.

## The Idea: Seasons

The Earth doesn't do random per-step rolls. It does **regimes** — long stretches where one flavor of event dominates, with causal chains linking one season to the next.

### Season Types

| Season | What Happens | Crystal Signatures |
|--------|-------------|-------------------|
| **Tectonic pulse** | Fracturing, pressure swings, new vein opening | Twins, deformation, phantom boundaries cluster together |
| **Thermal stability** | Slow steady growth, no disturbances | Large clean crystals, few twins, maybe one inclusion |
| **Oxidation front** | O₂ rises through the vug | Pseudomorphs cascade, sulfides → oxides → carbonates |
| **Hydrothermal flush** | Rapid injection of hot fluid | Flash growth, dendrites, hopper forms, turbulent inclusions |
| **Quiescent doldrums** | Nothing grows | Dissolution etches sharpest points, Gibbs-Thompson sculpting |
| **Evaporitic concentration** | Fluid slowly concentrates | Halite, gypsum, selenite bloom; twins from growth stress |
| **Metamorphic overprint** | Temperature/pressure regime shift | Recrystallization, new mineral suite overprints old |

### Causal Chaining

Seasons aren't independent — one season *seeds* the next:

- Tectonic pulse → fracturing → pressure drop → rapid boiling → flash deposition (hydrothermal flush)
- Hydrothermal flush → deposits sulfides → exhausts fluid → quiescent doldrums
- Quiescent doldrums → slow cooling → O₂ diffuses in → oxidation front advances
- Oxidation front → dissolves sulfides → enriches fluid in metals → next flush carries different chemistry

This is the **residue cascade at the vug scale** — the same mechanic we're building for broth chemistry, but applied to the event timeline.

### Implementation Sketch

Instead of per-step random rolls for rare events:

1. **Season generator**: at scenario start, generate a timeline of seasons with start/end steps, intensity, and type. Each scenario has a characteristic season sequence (Bisbee: hydrothermal → tectonic → oxidation; MVT: thermal → quiescent → flush → quiescent).
2. **Season modifiers**: during a season, modify probabilities:
   - Twin probability: base × season_multiplier (0 during stability, 3x during tectonic pulse)
   - Growth rate: modified by season type
   - Dissolution: active during doldrums, suppressed during flush
   - Inclusions: more likely during turbulent seasons
3. **One roll per crystal**: twin determination happens at nucleation, modified by the current season. Born during a tectonic pulse? Higher twin chance. Born during stability? Almost never.
4. **Crystal diary**: each zone records which season was active. The crystal's growth history becomes a geological diary — "this phantom boundary was the tectonic pulse at step 200."

### Why This Matters

- **Fixes the twin bug** structurally instead of with a band-aid
- **Makes long games readable**: you can look at a crystal and see *why* things happened
- **Enables storytelling**: scenarios become narratives, not random noise
- **Connects to zone-viz**: the growth bands inside crystal shapes would show season boundaries as color shifts or markers
- **Residue cascade at macro scale**: the same principle (one mineral's exhaust is the next mineral's fuel) applied to the event timeline

### Twin Bug Fix (Immediate)

While seasons are backlog, the per-step twin roll needs a quick fix: move twin determination to nucleation time (one roll when crystal is born), not per-zone. This is a one-line change per mineral engine. The 22 twin rolls in the codebase should each fire once at crystal creation, not every growth step.

---

🪨
