# BRIEF: Chemistry Zone Bar — Simple Crystal Growth Readout

**Date:** 2026-04-23
**Status:** Ready for implementation
**Priority:** Higher than shape-aware fill — this is the foundation
**Source:** Professor's vision, clarified through conversation

---

## The Idea

A simple horizontal bar that shows the chemistry history of a crystal. Each segment is colored by the dominant chromophore during that growth period. Segment width is proportional to how long that chemical regime lasted.

Think of it like a stratigraphic column for a single crystal.

## Reference

Watermelon tourmaline is the model. A crystal that grew green (Fe/Cr dominant) for a long time, then shifted to pink (Mn dominant) at the end would render as:

```
|████████████ Fe/Cr (green) ████████████|████ Mn (pink) ████|
```

The wide green segment tells you iron/chromium dominated the broth for most of this crystal's life. The thin pink segment on the right tells you manganese showed up briefly near the end. You can read the crystal's growth history at a glance.

## Where It Lives

Same three surfaces the builder already identified:
- **Zone History modal** — full-width bar replaces or supplements the text zone list
- **Crystal Inventory card** — small thumbnail bar
- **Library collected rows** — mini bar per specimen

## How It Works

1. Walk the crystal's zones in order
2. Group consecutive zones that share the same dominant chromophore (highest trace element, or the one that triggers a `color_rule`)
3. Each group becomes one segment
4. Segment width = proportional to total `thickness_um` of zones in that group
5. Segment color = the color that `color_rules` would produce for that chromophore mix

## Data We Already Have

- Each zone records `trace_Fe`, `trace_Mn`, `trace_Al`, `trace_Ti`, `trace_Pb`, `trace_Au`
- Each mineral has `color_rules` that map chromophore conditions to display colors
- The bar is just rendering what's already there — no schema changes needed

## Best Minerals For This

Strong zoning minerals produce the most dramatic bars:
- **Tourmaline** — watermelon (Fe/Cr green → Mn pink), indicolite (Fe blue)
- **Fluorite** — purple/blue/green/clear zones from varying activators
- **Halite** — blue (radiation damage) / clear / pink (impurities)
- **Calcite** — amber/clear/pink Mn zones
- **Rhodochrosite** — pink/white Mn/Ca alternation
- **Amethyst** — clear → purple → smoky (radiation + Fe)

Weak zoning minerals (galena, pyrite) get a pretty uniform bar — and that's honest. They don't zone much.

## Relationship to Shape-Aware Fill

The chemistry bar is **phase 1**. The shape-aware fill (growth bands inside crystal outlines) is phase 2 and builds ON TOP of this. The color derivation logic is the same — the shape-aware version just maps those colors into the crystal's geometry instead of a flat bar.

Ship this first. It's simpler, more useful, and the data is already there.

---

🪨
