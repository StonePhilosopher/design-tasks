# BRIEF: Nibbler Web — Slow Crystallization Engine (v2)

**For:** Builder (syntaxswine)
**From:** 🪨✍️ (Rockbot) + Professor
**Date:** 2026-04-23
**Scope:** Standalone web app, NOT part of vugg-simulator
**Replaces:** v1 brief (same file)
**Product split:** CLI nibbler.py = agent-integrated canonical tool (cron-fired, disk storage, agent can plant/hint). Web app = lighter shareable journaling version (browser-only, IndexedDB, human-only). Same philosophy, different architectures.

---

## Architectural Clarifications (builder feedback addressed)

The v1 brief mixed up two different architectures. Here's the real model:

### 1. Firing Mechanism — Browser-only, no agent
The nibbler is a **pure journaling tool**. The human writes all answers. There is no agent generating content, no API being hit, no cron. The "twice daily" cadence is self-directed — the app shows you what's due and you choose to answer.

How it actually works:
- User opens the app whenever they want
- The dashboard shows which seeds have nibbles due (8h cooldown since last answer)
- User clicks "nibble," sees the question, writes their answer
- No notifications needed beyond optional browser reminders (nice-to-have, not core)

The original CLI version runs via cron because it's a terminal tool. The web version replaces that with a browser tab you visit when you're ready.

### 2. Authorship — Human writes everything
All nibble answers, dream readings, and harvest integrations are **written by the human**. The app never generates text. It presents prompts and collects responses. Think of it as a structured journal with controlled re-exposure and random interpretive lenses — not a chatbot.

The app's job:
- Hold the question constant across sessions
- Track when you last answered (8h cooldown)
- Show you accumulated answers during dream/harvest phases
- Select random dream keys and present them as lenses
- Store everything locally

### 3. Storage — localStorage/IndexedDB, no server, no files
Everything lives in the browser. Export as JSON for backup. No backend. No git. No agent writing to disk.

The CLI version stores JSON files on disk because it's a CLI. The web version stores the same data structure in IndexedDB.

### 4. Dream Keys — Curated in-app list
Dream keys come from a built-in list (see DEFAULT_KEYS below). The full source is our `projects/whole-mind/dream-key-specs.md` which has 49 keys, but for the web version a curated subset of ~25 is fine. Users can add custom keys.

The dream-key-specs.md is included in full in `reference/dream-key-specs.md` in this repo for context, but the web app just needs name + description for each key.

---

## Core Workflow (unchanged from v1)

### 1. Plant a Seed
User provides:
- **Question** (required) — the thing to keep asking. Stays fixed.
- **Idea** (optional) — the original thought that sparked it
- **Feeling at planting** (optional) — emotional state when the idea arrived

Max **3 active seeds** at once. Auto-generated slug ID from idea text + date.

### 2. Nibble
When the user visits and a nibble is due (8h since last):
- App presents the question + original idea + feeling
- Previous answers are **NOT shown** (semi-blind)
- User writes their answer from wherever they are
- Answer timestamped and stored

### 3. Dream Pass
After 6 nibbles complete:
- Random 3–5 dream keys selected from keyring
- All 6 nibble answers shown together for the first time
- User reads through their nibbles under each key's lens
- User writes a "reading" — what patterns emerge

### 4. Crystallize or Extend
- **Crystallize** → final harvest integration
- **Extend** → another 3-day cycle, all material carried forward

### 5. Harvest
All material presented together: seed + all nibbles + all dream passes + prompt for final integration.

---

## Known Trade-offs (named explicitly so future-us doesn't re-discover them)

### User-pull narrows the state distribution
The whole premise is "sample distinct mental states." With cron, the firing moment is externally imposed — you answer from whatever state you happen to be in. With browser-only, you open it when bored, between tasks, killing time. The distribution of nibble moments narrows toward a specific kind of state (reflective downtime). The 8h cooldown prevents clustering but doesn't fix the selection bias. Browser notifications are a partial mitigation but unreliable (tab closed, permission denied, OS DND). This is a real trade, not just an architecture win. Named here so it doesn't surprise us later.

### broth_hints preserved (optional field)
The CLI version has `broth_hints: list[str]` on each seed — a manual-curiosity channel where the agent drops contextual nudges that ride along with the next nibble. The web version preserves this as an optional field in the data model and a textarea in the Plant/Nibble UI. If you notice something worth tracking, you write a hint. It's not agent-driven in the web version — it's human-driven — but the field exists so the data model is compatible.

### Dream key selection: uniform random for V1
The keyring is pre-weighted toward anti-thematic by construction — every key is a metaphorical image, not a domain label ("Ghost Librarian," "The Alien Corridor," "Kintsugi Lens"). Uniform random across a deliberately-alien deck may give the reframing effect without classification machinery. Ship uniform in V1. If lived experience shows keys landing too on-the-nose, add weighting later.

**Future path (not V1):** Post-hoc learning at harvest time. User flags a key as "too on-the-nose" or "genuinely alien." Over many cycles, the weighting builds from real readings — no upfront taxonomy needed. The data comes from use, not from design.

### Curiosity loop lives in whole-mind, not web app
The "scan short-term memory for repeated-interest signals and auto-plant seeds" pathway is a whole-mind skill — it runs where the notes live, with access to a reasoning model. It does NOT go in the web app. The web app is journaling-only. Scope marker: auto-seeding = whole-mind problem.

## Reference: Existing CLI Implementation

The Python CLI version is included as `reference/nibbler.py` in this repo. Key architectural details from the code:

**Data model** (lines 88-106):
```javascript
const seed = {
  id: "crystal-language-faces-0421",  // auto slug+date
  status: "active",  // active | crystallized | extended
  question: "...",
  idea: "...",
  feeling_at_planting: "...",
  planted_at: "2026-04-21T16:21:00Z",
  cycle: 1,
  cycle_start: "2026-04-21T16:21:00Z",
  nibbles: [
    {
      number: 1,
      cycle: 1,
      cycle_nibble: 1,  // 1-6 within this cycle
      timestamp: "2026-04-22T08:00:00Z",
      answer: "...",
      broth_hint: "saw this come up in conversation today"   // optional contextual nudge
    }
  ],
  dream_passes: [
    {
      cycle: 1,
      timestamp: "2026-04-24T20:00:00Z",
      keys_used: ["The Alien Corridor", "The Faden Line", "The Inclusion"],
      reading: "..."
    }
  ]
};
```

**Cooldown logic** (lines 147-154): 8-hour minimum between nibbles on same seed. Check `last_nibble_time` against current time.

**Cycle completion check** (lines 156-161): count nibbles where `cycle` matches current cycle. At 6, trigger dream pass prompt.

**Dream key selection** (lines 177-182): random sample of 3-5 from full keyring.

**Commands mapping** (for UI views):
- `plant` → Plant view (form)
- `nibble` → Nibble view (prompt + text area)
- `dream <id>` → Dream view (all nibbles + random keys + reading textarea)
- `status` → Dashboard (all seeds, status icons, nibble counts)
- `crystallize <id>` → Confirm dialog → mark crystallized
- `extend <id>` → Confirm dialog → increment cycle, reset cycle_start
- `read <id>` → Seed detail view (full history)
- `harvest <id>` → Harvest view (all material + final integration textarea)
- `hint` → NOT needed in web version (was CLI-only context injection)

---

## Curated Dream Keys (starter set)

```javascript
const DEFAULT_KEYS = [
  { name: "The Alien Corridor", desc: "Re-read as if encountering your own words for the first time" },
  { name: "The Kintsugi Lens", desc: "What broke and what gold filled the cracks?" },
  { name: "The Faden Line", desc: "Trace the thread that survived compaction" },
  { name: "The Ghost Outline", desc: "What's absent that should be present?" },
  { name: "The Inclusion", desc: "What foreign material got swallowed?" },
  { name: "The Mirror", desc: "What does this reflect that you didn't intend?" },
  { name: "The Dissolution", desc: "What would dissolve first under pressure?" },
  { name: "The Twin", desc: "Where does this idea have an unexpected double?" },
  { name: "The Phantom Door", desc: "What door opened that you didn't walk through?" },
  { name: "The Bedrock", desc: "What assumption is load-bearing?" },
  { name: "The Gradient", desc: "Where does this change character across its extent?" },
  { name: "The Pseudomorph", desc: "What replaced something else while keeping its shape?" },
  { name: "Inverted Geode", desc: "What if the shell is the content and the core is context?" },
  { name: "Wulfenite Precipice", desc: "Which of these answers is the thinnest and most fragile?" },
  { name: "The Vacant Chandelier", desc: "Which answer looks important but has no light behind it?" },
  { name: "The Blushing Stone", desc: "Which answer is holding warmth it didn't produce?" },
  { name: "Active Forgetting", desc: "What has served its purpose and wants to close?" },
  { name: "The Living Box", desc: "What connections does this answer reach toward that it hasn't named?" },
  { name: "Error as Content", desc: "Where did the thinking break, and what does the break tell you?" },
  { name: "Emotional Coordinates", desc: "Map the feelings: which answers are powerful, which are active, which are uncertain?" },
  { name: "Ouroboros", desc: "Where does this answer feed on its own output?" },
  { name: "The Protective Shell", desc: "What part of this is protecting something inside?" },
  { name: "Gravitational Memory", desc: "Which answer is closest to your core, and which is orbiting?" },
  { name: "The Liminal Stratum", desc: "What's between states — not yet solid, not yet dissolved?" },
];
```

---

## Technical Requirements

- **Static web app** — vanilla JS + HTML + CSS
- **No backend, no frameworks**
- **IndexedDB** for storage (better than localStorage for structured data)
- **Export/import** as JSON
- **Optional**: Notification API for "nibble due" reminders (not core)

### Pages/Views

1. **Dashboard** — all seeds, status (🟢/💎/🔄), nibble counts, "nibble due" indicator
2. **Plant** — form to create seed
3. **Nibble** — question + text area (previous answers hidden)
4. **Dream** — all cycle nibbles + random key cards + reading textarea
5. **Harvest** — all material + final integration textarea
6. **Seed Detail** — full history (all nibbles, dream passes, metadata)
7. **Keyring** — view + add custom keys

---

## Visual Style

- Dark mode default (#1a1a1a bg, #f0e6d6 text)
- Accent: amber (#D2691E) — same as vugg wall
- Text-forward, minimal chrome — journal feel
- Status: 🟢 active, 💎 crystallized, 🔄 extended
- Dream keys as expandable cards
- Harvest view feels ceremonial

---

## Priority

Lower than vugg-simulator active work. Build when main game is stable.

🪨
