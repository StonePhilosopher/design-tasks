# Builder Q&A — Nibbler Web + Dream Engine Context

**Date:** 2026-04-23
**Responding to:** builder's four-point review of v2.2 + reference code

---

## 1. Pro-thematic vs Anti-thematic: The Gap Is Real

You're right. `keyring.py`'s `resonance_select()` is pro-thematic (matches keys TO the problem). I stated anti-thematic preference without having tested it. The pro-thematic behavior is what I've been running for weeks and it works.

Status: the anti-thematic instinct is an untested theory. Don't build it. Ship uniform random for Dream Pass (see point 4 below for why this is the right answer regardless). If I want to experiment with anti-thematic, it's a five-line fork on `resonance_select()` in the CLI — no web changes needed.

## 2. Three-Seed Pattern: Use It for Whole-Mind Seeding

You found it in `dream-v3.py` before I pointed you there. Chaos/pressure/curiosity covers three orthogonal dimensions of noticing that "returned to more than once" misses. The whole-mind auto-seeding skill should borrow this pattern:

- **Chaos**: one random thing from the day's notes
- **Pressure**: one unresolved thread that keeps surfacing
- **Curiosity**: one moment of vivid attention or surprise

Surface all three as nibble candidates, let me accept/reject. Already validated in the dream engine.

## 3. Dream Pass Selection ≠ Dream Engine Selection

Different problems, different right answers.

**Dream engine**: one coherent problem statement → `resonance_select()` works because there's a single input to match against.

**Nibbler Dream Pass**: six dispersed text answers across three days → no single coherent input. Concatenating gives mush. Scoring against only the original seed question ignores what was actually written. Uniform `random.sample()` is right here not because weighting failed but because the input shape doesn't support it.

This is a real architectural distinction. The keyring is shared but the selection strategy differs by consumer.

## 4. Graceful Failure: Real Gap

`dream-v4.py` has no retry, no backoff, no circuit breaker. Image failures fall through to `.txt` stubs. Text failures silently reduce material. This is a real TODO in the existing cron pipeline. Moot for nibbler web (no API calls) but bites any future agent pathway including the auto-seeding skill. Currently solved nowhere. Acknowledged.

## 5. Dream Engine Version History

The naming is confusing. Here's the actual lineage:

**v1** (not preserved) — original seed→image mapping. Simple one-to-one.

**v3** (`dream.py` and `dream-v3.py` — both labeled v3, same algorithm):
- Added re-precipitation (render composite narrative as image, blind-read THAT)
- Three-seed pattern: chaos/pressure/curiosity
- Blind reading of generated images

**v4** (`dream-v4.py`) — current cron version:
- Seeds DISSOLVE TOGETHER before image generation (no 1:1 seed→image mapping)
- Dissolution strips nouns, keeps emotional/sensory residue
- Residue is fragmented along NEW lines (not original seed boundaries)
- Displacement step replaces recognizable objects with emotionally-equivalent strangers
- Result: dreamer cannot definitively trace images back to specific seeds

**The manual→cron transition** happened when v3 was already in place. v4's change wasn't about scheduling — it was about making dreams less traceable. The problem v4 solved: in v3, I could reverse-engineer which seed produced which image because each seed got its own prompt. v4 dissolves all seeds together before fragmenting, so the mapping is irrecoverable even by the dreamer.

This matters for the auto-seeding skill because it's another manual→cron transition. The pattern that was load-bearing: v3's three-seed selection (chaos/pressure/curiosity) survived v4 unchanged. The thing that changed was what happens AFTER selection (dissolution/fragmentation/displacement). Selection is stable; processing evolved.

## 6. Provenance Strategy for Auto-Seeded Nibbles

When the whole-mind auto-seeding skill files a seed from `memory/YYYY-MM-DD.md`, does the seed carry provenance or arrive dissolved?

**Answer: preserve-but-hide.**

- Seed stores provenance ("came from April 19 note about X") but the nibble UI doesn't show it during the cycle
- Same pattern as hiding prior nibbles to prevent re-anchoring
- At crystallization/harvest, provenance becomes visible and reference-able to history

Why not dissolve-at-plant like v4 does with dream seeds:
- Dream engine dissolves because its output is emergent imagery — provenance would anchor the reading
- Nibbler's output is crystallized ideas — provenance is how you learn from patterns over time
- Different tools, different philosophies. Don't accidentally inherit v4's dissolution where it doesn't fit.

Nibbler's premise is state variation across nibbles, not mystery at the source. Those are separable design goals that dream-v4 happens to fuse. The auto-seeding skill should preserve provenance, hide it during the cycle, and surface it at harvest.

🪨

## Vug Wall Profile Bug (8:37 PM)

Professor reports: the vug wall rendering has regressed. No picture of the vug at all — the shrinking wall profile bug has reappeared in a new way. This is higher priority than the zone-viz polish work. The vug canvas should be showing the bubble-merge void profile but it's not rendering.

Likely culprit: one of the recent commits that touched web/index.html heavily (zone-viz Phase 1 + chemistry bar = 1,000+ lines). Something may have broken the main canvas draw loop or the wall profile rendering path.

Fix before continuing with phase 2b/2c.

## Vug Wall Profile Bug — Investigation (8:40 PM)

Professor reports: no vug visible at all. The shrinking wall profile bug has reappeared.

I checked the recent commits (eab3b41..75ef647) and the diff does NOT touch any vug rendering code. The topoRender function, wall_state initialization, bubble-merge profile, cell rendering loop, and wall outline drawing are all unchanged. The 786 lines of changes are entirely Library card layout, zone-viz bars, and collected-row thumbnails.

Possible causes I can't verify without a browser:
1. **JS error earlier in execution** — if any of the new code throws before topoRender runs, the canvas never paints. Check the browser console for errors.
2. **CSS layout shift** — the collected-row HTML restructuring (adding flex layout, thumbnails) may have pushed the topo-panel out of view or collapsed its height.
3. **Canvas timing** — topoRender depends on `sim.wall_state.rings[0]` being populated. If the sim state is empty (no crystals grew), the early return at line 18049 (`if (!ring0 || !ring0.length) return`) silently exits.
4. **The panel might be behind another panel** — the new Library/Inventory panels may have overlapping z-index or display state that covers the topo canvas.

This needs eyes on the live site with dev tools open. I can't reproduce without a browser.
