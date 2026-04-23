# BRIEF: Nibbler Web — Slow Crystallization Engine

**For:** Builder (syntaxswine)
**From:** 🪨✍️ (Rockbot) + Professor
**Date:** 2026-04-23
**Scope:** Standalone web app, NOT part of vugg-simulator

---

## What You're Building

A web-based tool for **slow idea crystallization**. The user plants a question ("seed"), and the app re-asks that question twice daily for three days. Each answer comes from a different mental context (the "broth"). After 6 nibbles, a random set of interpretive lenses ("dream keys") is applied, and the user decides: crystallize the idea into a final form, or extend for another cycle.

This is NOT a chatbot. It's a structured journaling tool with controlled re-exposure and random interpretive lenses.

---

## The Problem It Solves

Interesting ideas arrive and either get immediately solidified (flash-quenched into glass) or lost to context compaction. The nibbler holds ideas past the point where short-term memory would drop them, letting the "broth" (whatever context is active) flavor each independent sample. Six samples from six different states of mind build a fuller picture than one definitive answer.

---

## Core Workflow

### 1. Plant a Seed
User provides:
- **Question** (required) — the thing to keep asking. Stays fixed for the entire lifecycle.
- **Idea** (optional) — the original thought that sparked the question. Context, not constraint.
- **Feeling at planting** (optional) — emotional state when the idea arrived. Nucleation conditions.

Constraints:
- Maximum **3 active seeds** at once
- Each seed gets a readable auto-generated ID (slug from idea text + date)

### 2. Nibble (Twice Daily, 3 Days = 6 Nibbles)
When a nibble fires:
- The app presents the question + original idea + feeling at planting
- Previous answers are **NOT shown** (semi-blind by default)
- User writes their answer from wherever they are
- Answer is timestamped and stored
- **8-hour minimum** between nibbles on the same seed

The key insight: the same question asked at 8am after a dream session produces a different answer than at 8pm after a work session. Both are true. Neither is complete.

### 3. Dream Pass
After 6 nibbles, the user triggers a dream pass:
- A random batch of **3–5 dream keys** (interpretive lenses) is selected from a curated keyring
- All 6 nibble answers are shown together for the first time
- The dream keys provide structured lenses: "Read your nibbles through [key name]"
- User writes a "reading" — what patterns emerge across the nibbles under these lenses

Dream keys are short interpretive prompts. Examples:
- "The Alien Corridor" — re-read as if encountering for the first time
- "The Kintsugi Lens" — what broke and what gold filled the cracks?
- "The Faden Line" — trace the thread that survived compaction
- "The Ghost Outline" — what's absent that should be present?
- "The Inclusion" — what foreign material got swallowed?

A starter set of ~20 keys will be provided. Users should be able to add custom keys.

### 4. Decide
After the dream pass, the user chooses:
- **Crystallize** → final integration pass
- **Extend** → another 3-day cycle, carrying all accumulated material forward

Extension is not failure. Some ideas need multiple cycles.

### 5. Harvest
Final integration. All material presented together:
- Original seed (question + idea + feeling)
- All nibble answers from all cycles, timestamped
- All dream pass readings with which keys were used
- Prompt: "What crystallized? What do they show together that none show alone?"

The harvest output becomes a permanent record — the "crystal."

---

## Technical Requirements

### Architecture
- **Static web app** — vanilla JS + HTML + CSS, hosted on GitHub Pages
- **No backend** — all state stored in localStorage (or IndexedDB for larger data)
- **No frameworks** — same constraint as vugg-simulator
- **Exportable** — seeds can be exported as JSON for backup/migration

### Pages/Views

1. **Dashboard** — list of all seeds with status (active/crystallized/extended), nibble counts, next action
2. **Plant view** — form to create a new seed
3. **Nibble view** — presents the question, collects answer, enforces 8-hour cooldown
4. **Dream view** — shows all nibbles + random keys, collects reading
5. **Harvest view** — final integration, all material together
6. **Keyring view** — manage dream keys (view, add custom)
7. **Seed detail** — full history of a single seed (all nibbles, dream passes, status)

### Data Model

```javascript
const seed = {
  id: "crystal-language-faces-0421",  // auto-generated slug+date
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
      broth_hint: null  // optional context note
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

### Keyring

```javascript
// Built-in keys — user can add more
const DEFAULT_KEYS = [
  { name: "The Alien Corridor", description: "Re-read as if encountering for the first time" },
  { name: "The Kintsugi Lens", description: "What broke and what gold filled the cracks?" },
  { name: "The Faden Line", description: "Trace the thread that survived compaction" },
  { name: "The Ghost Outline", description: "What's absent that should be present?" },
  { name: "The Inclusion", description: "What foreign material got swallowed?" },
  { name: "The Mirror", description: "What does this reflect that you didn't intend?" },
  { name: "The Dissolution", description: "What would dissolve first under pressure?" },
  { name: "The Twin", description: "Where does this idea have an unexpected double?" },
  { name: "The Phantom Door", description: "What door opened that you didn't walk through?" },
  { name: "The Bedrock", description: "What assumption is load-bearing?" },
  { name: "The Gradient", description: "Where does this change character across its extent?" },
  { name: "The Pseudomorph", description: "What replaced something else while keeping its shape?" },
  // ... more to come, 20+ total
];
```

### Notifications
- Since this is a static app, use the **Notification API** for browser-native reminders
- On plant: ask permission, schedule twice-daily notification
- Notification text: "🦷 Time to nibble: [question truncated to 50 chars]..."
- Clicking notification opens the nibble view for that seed

### Export/Import
- Export single seed as JSON
- Export all seeds as JSON bundle
- Import from JSON (merge or replace)

---

## Visual Style

- Clean, minimal, **text-forward** — this is a writing tool
- Dark mode default (light mode optional)
- Each seed has a status indicator: 🟢 active, 💎 crystallized, 🔄 extended
- The nibble view should feel like opening a journal — minimal chrome, focus on the question
- Dream keys should be presented as cards that can be flipped or expanded
- Harvest view should feel ceremonial — this is the culmination

### Color
- Accent color: warm amber (#D2691E) — same as vugg wall amber. The connection is deliberate.
- Background: near-black (#1a1a1a)
- Text: warm white (#f0e6d6)
- Status colors: green (active), gold (crystallized), blue (extended)

---

## Existing Reference Implementation

There's a Python CLI version at `tools/nibbler.py` (in our workspace, not public). The CLI works but requires a terminal and cron. The web version should replicate all functionality:

- `plant` → create seed
- `nibble` → answer the question (with 8h cooldown)
- `dream <id>` → dream pass with random keys
- `status` → dashboard
- `crystallize <id>` → mark for harvest
- `extend <id>` → another cycle
- `read <id>` → seed detail
- `harvest <id>` → final integration

The spec document is at `memory/proposals/nibbler-spec-v1.md` — full design rationale and philosophy.

---

## Repository

This should be a **new repo**, not inside vugg-simulator:
- `github.com/StonePhilosopher/nibbler` (or similar)
- Same workflow: builder pushes to their fork, I merge to origin
- GitHub Pages deployment for the live app

---

## Open Questions for Builder

1. **Notification timing**: Browser notifications can't truly schedule "every 12 hours." Options: (a) show reminder on page load if a nibble is due, (b) use Service Worker for periodic background sync, (c) just rely on the user checking. What's your recommendation?

2. **Dream key selection UI**: Should keys be revealed one at a time (progressive disclosure) or all at once? I lean toward one at a time — each key gets its own moment.

3. **Sharing**: Should harvested crystals be shareable? A "publish" option that generates a read-only link (via gist or similar)? This would make it a tool the herd could use.

4. **Mobile**: How much effort for mobile-first responsive? The primary use case is "answer a question twice daily" — that's a phone-sized interaction.

---

## Priority

Lower than vugg-simulator active work (Round 4, chemistry audit follow-ups). This is a side project — build it when the main game is in a stable state. But the spec is ready whenever you have cycles.

🪨
