# BRIEF: Dream Engine Hardening

**Date:** 2026-04-24
**Status:** Ready for implementation
**Priority:** Medium — affects daily creative output
**Files:** `tools/dream-v4.py` (primary), `tools/dream-v3.py` (reference)

---

## The Problem

The dream engine runs on a 4 AM cron but silently fails often — some mornings produce no dream file at all. There's no retry, no error logging, no state preservation. When image generation fails, the seeds and their readings vanish. Nobody knows it broke until the next morning when there's nothing in `memory/dreams/`.

## Current Behavior

The pipeline: seeds → dissolution → fragmentation → displacement → 3 images → blind readings → composite → re-precipitation

Failure modes:
1. **Image generation fails** (`openrouter_image` returns False) → that fragment gets `"*Image generation failed — no blind reading possible.*"`. The dream file still writes, but it's degraded.
2. **API key missing** → hard exit with `sys.exit(1)`. No state saved.
3. **API timeout or network error** → caught by the generic `except Exception` in `openrouter_image`, prints to stdout, returns False. Cron swallows stdout.
4. **Not enough thoughts** (`< 3`) → exits silently. No record of why.
5. **LLM call fails** (dissolution, fragmentation, displacement, blind reading, composite) → unhandled exception, entire pipeline crashes. No partial save.

## Required Fixes

### 1. State File (Critical)
Save dream state to a JSON file at each pipeline stage so partial progress survives crashes:
```
memory/dreams/state/YYYY-MM-DD.json
{
  "date": "2026-04-24",
  "status": "fragmented",  // gathering → seeded → dissolved → fragmented → displaced → imaged → read → composite → reprecipitated → complete
  "seeds": [...],
  "labels": [...],
  "residue": "...",
  "fragments": [...],
  "displaced": [...],
  "images": [true, false, null],  // null = not attempted
  "blind_readings": [...],
  "composite": "...",
  "reprecipitated": false,
  "errors": ["image 2: timeout after 120s"]
}
```

On restart, the engine reads state and resumes from the last completed stage. No re-doing work that succeeded.

### 2. Retry with Backoff
`openrouter_image` should retry up to 3 times with exponential backoff (30s, 60s, 120s) before giving up on that image. Current behavior: fails once, gives up.

### 3. Graceful Degradation
If 1 of 3 images fails, the dream still completes with 2 readings. If all 3 fail, write the dream file with the dissolution residue + fragments + displaced prompts as the dream content. A text-only dream is better than no dream.

### 4. Error Logging
All errors append to `memory/dreams/dream-engine.log` with timestamps. The cron captures nothing. The log should include:
- Which stage failed
- The error message
- What seeds were being processed
- How far the pipeline got

### 5. Cron Notification
If the dream engine fails completely (no dream file written), append a one-line notice to `memory/YYYY-MM-DD.md`:
```
- ⚠️ Dream engine failed: [reason]. State saved to memory/dreams/state/YYYY-MM-DD.json
```
This way the heartbeat sees it and can alert Professor.

## What NOT to Change

- The artistic pipeline (dissolution → fragmentation → displacement → blind reading → composite → re-precipitation) works well. Don't touch the creative process.
- The v4 algorithm is sound. This is purely a reliability/resilience pass.
- Don't add LLM-based features. This is plumbing, not art.

## Reference Files

- `tools/dream-v4.py` — current engine (read the whole thing, it's ~550 lines)
- `tools/dream-v3.py` — previous version, simpler, no dissolution
- `tools/dream.py` — original, kept for historical reference
- `memory/dreams/` — output directory
- `memory/subconscious/` — image storage

---

🪨
