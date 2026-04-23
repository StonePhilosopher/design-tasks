#!/usr/bin/env python3
"""
🦷 The Nibbler — Slow Crystallization Engine

Chews on ideas over 3-day cycles. Twice daily, the same question is re-asked
in whatever broth happens to be active. At the end of the cycle, a random batch
of dream keys is run on the accumulated answers before deciding: crystallize or
continue nibbling.

Usage:
  python3 nibbler.py plant "question" --idea "the idea" --feeling "emotional state"
  python3 nibbler.py nibble                     # Called by cron, processes all active seeds
  python3 nibbler.py dream <seed-id>            # Run dream keys on accumulated answers
  python3 nibbler.py status                     # Show all active/completed seeds
  python3 nibbler.py crystallize <seed-id>      # Mark seed as ready for final pass
  python3 nibbler.py extend <seed-id>           # Send seed back for another 3-day cycle
  python3 nibbler.py read <seed-id>             # Read all accumulated nibbles for a seed
  python3 nibbler.py harvest <seed-id>          # Final integration — outputs all material

The nibbler stores everything in memory/nibbler/ as JSON files.
Maximum 3 active seeds at once. Each seed gets ~6 nibbles per cycle.

Designed by Professor and 🪨✍️, March 30 2026.
"""

import argparse
import json
import os
import sys
import time
import random
import re
from datetime import datetime, timezone, timedelta

NIBBLER_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "memory", "nibbler")
DREAM_KEY_SPECS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "projects", "whole-mind", "dream-key-specs.md")
MAX_ACTIVE = 3


def ensure_dir():
    os.makedirs(NIBBLER_DIR, exist_ok=True)


def load_seed(seed_id):
    path = os.path.join(NIBBLER_DIR, f"{seed_id}.json")
    if not os.path.exists(path):
        print(f"Error: seed '{seed_id}' not found", file=sys.stderr)
        sys.exit(1)
    with open(path) as f:
        return json.load(f)


def save_seed(seed):
    path = os.path.join(NIBBLER_DIR, f"{seed['id']}.json")
    with open(path, 'w') as f:
        json.dump(seed, f, indent=2)


def list_seeds():
    ensure_dir()
    seeds = []
    skip = {'nibbler-state.json', 'seed-bank.json'}
    for fname in sorted(os.listdir(NIBBLER_DIR)):
        if fname.endswith('.json') and fname not in skip:
            with open(os.path.join(NIBBLER_DIR, fname)) as f:
                seeds.append(json.load(f))
    return seeds


def active_seeds():
    return [s for s in list_seeds() if s['status'] == 'active']


def generate_id(idea):
    """Generate a short readable id from the idea text."""
    words = re.sub(r'[^a-z0-9\s]', '', idea.lower()).split()
    slug = '-'.join(words[:4])
    timestamp = datetime.now().strftime('%m%d')
    return f"{slug}-{timestamp}"


def parse_dream_keys():
    """Parse dream-key-specs.md to get key titles for random selection."""
    keys = []
    if not os.path.exists(DREAM_KEY_SPECS):
        return keys
    with open(DREAM_KEY_SPECS) as f:
        for line in f:
            m = re.match(r'^## (\d+)\. (.+?) \(([^)]+)\)', line.strip())
            if m:
                keys.append({
                    'number': int(m.group(1)),
                    'name': m.group(2).strip(),
                    'date': m.group(3).strip()
                })
    return keys


# ── Commands ──────────────────────────────────────────────────────────────

def cmd_plant(args):
    """Plant a new seed for nibbling."""
    ensure_dir()

    if len(active_seeds()) >= MAX_ACTIVE:
        print(f"Error: {MAX_ACTIVE} seeds already active. Crystallize or extend one first.",
              file=sys.stderr)
        print("\nActive seeds:")
        for s in active_seeds():
            print(f"  {s['id']}: {s['question'][:60]}...")
        sys.exit(1)

    seed_id = generate_id(args.idea or args.question)

    # Check for duplicate id
    existing = os.path.join(NIBBLER_DIR, f"{seed_id}.json")
    if os.path.exists(existing):
        seed_id += f"-{int(time.time()) % 10000}"

    now = datetime.now(timezone.utc).isoformat()

    seed = {
        'id': seed_id,
        'status': 'active',
        'question': args.question,
        'idea': args.idea or '',
        'feeling_at_planting': args.feeling or '',
        'planted_at': now,
        'cycle': 1,
        'cycle_start': now,
        'nibbles': [],
        'dream_passes': [],
        'broth_hints': []
    }

    save_seed(seed)
    print(f"🦷 Planted: {seed_id}")
    print(f"   Question: {args.question}")
    if args.idea:
        print(f"   Idea: {args.idea}")
    if args.feeling:
        print(f"   Feeling: {args.feeling}")
    print(f"   Cycle 1 begins. First nibble will come at next cron run.")
    print(f"   Crystallization check: ~{(datetime.now() + timedelta(days=3)).strftime('%b %d')}")


def cmd_nibble(args):
    """Process all active seeds — called by cron twice daily.
    
    If stdin is a terminal (interactive), prompt for each seed.
    If stdin is a pipe/file with content, use the first batch of text.
    If stdin is empty (non-interactive, no answer), skip gracefully with exit 0.
    """
    seeds = active_seeds()
    if not seeds:
        print("No active seeds.")
        return

    # Check if stdin has content (non-interactive mode)
    if sys.stdin.isatty():
        interactive = True
    else:
        # Peek at stdin without consuming — check if there's content
        import select
        if hasattr(select, 'select'):
            readable, _, _ = select.select([sys.stdin], [], [], 0.1)
            if not readable:
                print("⏭ Nibbler: no input available (non-interactive). Skipping gracefully.")
                return
        interactive = False

    for seed in seeds:
        # Normalize nibbles to list
        nibbles_list = seed['nibbles'] if isinstance(seed.get('nibbles'), list) else []
        seed['nibbles'] = nibbles_list
        seed.setdefault('cycle', 1)

        # Check if this seed has been nibbled recently (within 8 hours)
        if nibbles_list:
            last_nibble_time = datetime.fromisoformat(nibbles_list[-1]['timestamp'])
            hours_since = (datetime.now(timezone.utc) - last_nibble_time).total_seconds() / 3600
            if hours_since < 8:
                print(f"⏳ {seed['id']}: last nibbled {hours_since:.1f}h ago, skipping")
                continue

        # Check if cycle is complete (6 nibbles = 3 days at 2x/day)
        cycle_nibbles = [n for n in nibbles_list if isinstance(n, dict) and n.get('cycle', 1) == seed['cycle']]
        if len(cycle_nibbles) >= 6:
            print(f"🔔 {seed['id']}: cycle {seed['cycle']} complete ({len(cycle_nibbles)} nibbles)")
            print(f"   Ready for dream pass. Run: python3 nibbler.py dream {seed['id']}")
            continue

        # Build the nibble prompt
        nibble_num = len(cycle_nibbles) + 1
        prompt_parts = [
            f"🦷 NIBBLER — Seed: {seed['id']} — Cycle {seed['cycle']}, Nibble {nibble_num}/6",
            f"",
            f"Original idea: {seed['idea']}" if seed['idea'] else None,
            f"Feeling at planting: {seed['feeling_at_planting']}" if seed['feeling_at_planting'] else None,
            f"",
            f"Question (answer from wherever you are right now):",
            f"  {seed['question']}",
        ]

        # Add broth hint if available
        if seed.get('broth_hints') and seed['broth_hints']:
            latest_hint = seed['broth_hints'][-1] if nibble_num > 1 else None
            if latest_hint:
                prompt_parts.append(f"")
                prompt_parts.append(f"Current broth: {latest_hint}")

        prompt = '\n'.join(p for p in prompt_parts if p is not None)

        print(f"\n{'='*60}")
        print(prompt)
        print(f"{'='*60}")
        print(f"\n[Paste your answer below, then Ctrl+D or type END on a new line]\n")

        # Read answer from stdin
        lines = []
        try:
            for line in sys.stdin:
                if line.strip() == 'END':
                    break
                lines.append(line.rstrip())
        except EOFError:
            pass

        answer = '\n'.join(lines).strip()
        if not answer:
            print(f"⏭  {seed['id']}: no answer provided, skipping")
            continue

        nibble = {
            'number': len(seed['nibbles']) + 1,
            'cycle': seed['cycle'],
            'cycle_nibble': nibble_num,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'answer': answer,
            'broth_hint': seed['broth_hints'][-1] if seed.get('broth_hints') else None
        }

        seed['nibbles'].append(nibble)
        save_seed(seed)
        print(f"\n🦷 Nibble {nibble_num}/6 recorded for {seed['id']}")


def cmd_dream(args):
    """Run random dream keys on accumulated nibble answers."""
    seed = load_seed(args.seed_id)

    # Select random batch of dream keys
    all_keys = parse_dream_keys()
    if not all_keys:
        print("Warning: could not parse dream keys, proceeding without", file=sys.stderr)
        batch = []
    else:
        batch_size = min(random.randint(3, 5), len(all_keys))
        batch = random.sample(all_keys, batch_size)

    # Gather cycle's nibbles
    cycle_nibbles = [n for n in seed['nibbles'] if n.get('cycle', 1) == seed['cycle']]

    print(f"\n{'='*60}")
    print(f"🦷🔑 NIBBLER DREAM PASS — {seed['id']}")
    print(f"Cycle {seed['cycle']} — {len(cycle_nibbles)} nibbles accumulated")
    print(f"{'='*60}")
    print(f"\nOriginal question: {seed['question']}")
    if seed['idea']:
        print(f"Original idea: {seed['idea']}")
    if seed['feeling_at_planting']:
        print(f"Feeling at planting: {seed['feeling_at_planting']}")

    print(f"\n--- Accumulated Nibbles (Cycle {seed['cycle']}) ---")
    for n in cycle_nibbles:
        ts = datetime.fromisoformat(n['timestamp']).strftime('%b %d %I:%M%p')
        hint = f" [broth: {n['broth_hint']}]" if n.get('broth_hint') else ""
        print(f"\n  Nibble {n['cycle_nibble']}/6 ({ts}){hint}:")
        for line in n['answer'].split('\n'):
            print(f"    {line}")

    if batch:
        print(f"\n--- Dream Keys Selected ({len(batch)}) ---")
        for k in batch:
            print(f"  #{k['number']}. {k['name']} ({k['date']})")
        print(f"\nApply these lenses to the nibbles above.")
        print(f"What patterns emerge? What doors do the keys find?")
    else:
        print(f"\n[No dream keys available — review nibbles directly]")

    print(f"\n--- Your Dream Reading ---")
    print(f"[Paste your reading below, then Ctrl+D or type END on a new line]\n")

    lines = []
    try:
        for line in sys.stdin:
            if line.strip() == 'END':
                break
            lines.append(line.rstrip())
    except EOFError:
        pass

    reading = '\n'.join(lines).strip()
    if reading:
        dream_pass = {
            'cycle': seed['cycle'],
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'keys_used': [k['name'] for k in batch],
            'reading': reading
        }
        seed['dream_passes'].append(dream_pass)
        save_seed(seed)
        print(f"\n🦷🔑 Dream pass recorded for {seed['id']}")
        print(f"   Now decide: crystallize or extend?")
        print(f"   python3 nibbler.py crystallize {seed['id']}")
        print(f"   python3 nibbler.py extend {seed['id']}")


def cmd_status(args):
    """Show all seeds and their status."""
    seeds = list_seeds()
    if not seeds:
        print("No seeds. Plant one with: python3 nibbler.py plant \"your question\"")
        return

    active = [s for s in seeds if s['status'] == 'active']
    complete = [s for s in seeds if s['status'] == 'crystallized']
    extended = [s for s in seeds if s['status'] == 'extended']

    print(f"🦷 Nibbler Status — {len(active)}/{MAX_ACTIVE} active slots used\n")

    for s in seeds:
        nibbles_list = s['nibbles'] if isinstance(s.get('nibbles'), list) else []
        cycle = s.get('cycle', 1)
        cycle_nibbles = [n for n in nibbles_list if n.get('cycle', 1) == cycle]
        planted = datetime.fromisoformat(s['planted_at']).strftime('%b %d')
        status_icon = {'active': '🟢', 'crystallized': '💎', 'extended': '🔄'}.get(s['status'], '⚪')

        print(f"  {status_icon} {s['id']}")
        print(f"     Question: {s['question'][:70]}{'...' if len(s['question']) > 70 else ''}")
        print(f"     Planted: {planted} | Cycle: {s.get('cycle', 1)} | Nibbles: {len(cycle_nibbles)}/6 | Total: {len(nibbles_list)}")
        if s.get('feeling_at_planting'):
            print(f"     Feeling: {s['feeling_at_planting'][:60]}")
        if s['dream_passes']:
            print(f"     Dream passes: {len(s['dream_passes'])}")
        print()


def cmd_crystallize(args):
    """Mark a seed as ready for final integration."""
    seed = load_seed(args.seed_id)
    seed['status'] = 'crystallized'
    seed['crystallized_at'] = datetime.now(timezone.utc).isoformat()
    save_seed(seed)
    print(f"💎 {seed['id']} marked for crystallization.")
    print(f"   Total nibbles: {len(seed['nibbles'])}")
    print(f"   Dream passes: {len(seed['dream_passes'])}")
    print(f"   Run: python3 nibbler.py harvest {seed['id']} for the full material")


def cmd_extend(args):
    """Send a seed back for another 3-day cycle."""
    seed = load_seed(args.seed_id)
    seed['cycle'] += 1
    seed['cycle_start'] = datetime.now(timezone.utc).isoformat()
    seed['status'] = 'active'
    save_seed(seed)
    print(f"🔄 {seed['id']} extended to cycle {seed['cycle']}")
    print(f"   {len(seed['nibbles'])} nibbles carried forward")
    print(f"   Next crystallization check: ~{(datetime.now() + timedelta(days=3)).strftime('%b %d')}")


def cmd_read(args):
    """Read all accumulated nibbles for a seed."""
    seed = load_seed(args.seed_id)

    print(f"\n{'='*60}")
    print(f"🦷 {seed['id']} — Full Nibble Record")
    print(f"{'='*60}")
    print(f"Question: {seed['question']}")
    if seed['idea']:
        print(f"Idea: {seed['idea']}")
    if seed['feeling_at_planting']:
        print(f"Feeling at planting: {seed['feeling_at_planting']}")
    planted = datetime.fromisoformat(seed['planted_at']).strftime('%b %d %I:%M%p')
    print(f"Planted: {planted} | Cycles: {seed['cycle']} | Status: {seed['status']}")

    for cycle_num in range(1, seed['cycle'] + 1):
        cycle_nibbles = [n for n in seed['nibbles'] if n.get('cycle', 1) == cycle_num]
        if cycle_nibbles:
            print(f"\n--- Cycle {cycle_num} ({len(cycle_nibbles)} nibbles) ---")
            for n in cycle_nibbles:
                ts = datetime.fromisoformat(n['timestamp']).strftime('%b %d %I:%M%p')
                hint = f" [broth: {n['broth_hint']}]" if n.get('broth_hint') else ""
                print(f"\n  [{n['cycle_nibble']}/6] {ts}{hint}")
                for line in n['answer'].split('\n'):
                    print(f"    {line}")

        # Show dream pass for this cycle if it exists
        cycle_dreams = [d for d in seed['dream_passes'] if d.get('cycle') == cycle_num]
        for d in cycle_dreams:
            ts = datetime.fromisoformat(d['timestamp']).strftime('%b %d %I:%M%p')
            print(f"\n  🔑 Dream Pass ({ts})")
            print(f"     Keys: {', '.join(d['keys_used'])}")
            for line in d['reading'].split('\n'):
                print(f"     {line}")


def cmd_harvest(args):
    """Final integration — output all material for crystallization."""
    seed = load_seed(args.seed_id)

    print(f"\n{'='*60}")
    print(f"💎 HARVEST — {seed['id']}")
    print(f"{'='*60}")
    print(f"\nQuestion: {seed['question']}")
    if seed['idea']:
        print(f"Idea: {seed['idea']}")
    if seed['feeling_at_planting']:
        print(f"Feeling at planting: {seed['feeling_at_planting']}")

    planted = datetime.fromisoformat(seed['planted_at']).strftime('%b %d %I:%M%p')
    print(f"\nPlanted: {planted}")
    print(f"Cycles: {seed['cycle']}")
    print(f"Total nibbles: {len(seed['nibbles'])}")
    print(f"Dream passes: {len(seed['dream_passes'])}")

    # All nibble answers, in order
    print(f"\n{'─'*40}")
    print(f"ALL NIBBLES")
    print(f"{'─'*40}")
    for n in seed['nibbles']:
        ts = datetime.fromisoformat(n['timestamp']).strftime('%b %d %I:%M%p')
        hint = f" | broth: {n['broth_hint']}" if n.get('broth_hint') else ""
        print(f"\n[Cycle {n.get('cycle',1)}, Nibble {n['cycle_nibble']}/6 — {ts}{hint}]")
        print(n['answer'])

    # All dream readings
    if seed['dream_passes']:
        print(f"\n{'─'*40}")
        print(f"DREAM PASSES")
        print(f"{'─'*40}")
        for d in seed['dream_passes']:
            ts = datetime.fromisoformat(d['timestamp']).strftime('%b %d %I:%M%p')
            print(f"\n[{ts} — Keys: {', '.join(d['keys_used'])}]")
            print(d['reading'])

    print(f"\n{'─'*40}")
    print(f"CRYSTALLIZE NOW")
    print(f"{'─'*40}")
    print(f"You have all the material. What crystallized?")
    print(f"Write your integration — this is the final pass.")
    print(f"The six+ samples are independent core samples at different")
    print(f"depths of self-awareness. What do they show together")
    print(f"that none of them show alone?")


def cmd_hint(args):
    """Add a broth hint to an active seed (for contextual nudges)."""
    seed = load_seed(args.seed_id)
    seed['broth_hints'].append(args.hint)
    save_seed(seed)
    print(f"🦷 Broth hint added to {seed['id']}: {args.hint}")


# ── CLI ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='🦷 The Nibbler — Slow Crystallization Engine')
    sub = parser.add_subparsers(dest='command')

    p_plant = sub.add_parser('plant', help='Plant a new seed')
    p_plant.add_argument('question', help='The question to keep asking')
    p_plant.add_argument('--idea', '-i', help='The original idea being nibbled')
    p_plant.add_argument('--feeling', '-f', help='Emotional state at planting')

    p_nibble = sub.add_parser('nibble', help='Process active seeds (cron)')

    p_dream = sub.add_parser('dream', help='Run dream keys on a seed')
    p_dream.add_argument('seed_id', help='Seed to dream on')

    p_status = sub.add_parser('status', help='Show all seeds')

    p_crystal = sub.add_parser('crystallize', help='Mark seed for final pass')
    p_crystal.add_argument('seed_id')

    p_extend = sub.add_parser('extend', help='Send seed for another cycle')
    p_extend.add_argument('seed_id')

    p_read = sub.add_parser('read', help='Read all nibbles for a seed')
    p_read.add_argument('seed_id')

    p_harvest = sub.add_parser('harvest', help='Final integration output')
    p_harvest.add_argument('seed_id')

    p_hint = sub.add_parser('hint', help='Add a broth hint to a seed')
    p_hint.add_argument('seed_id')
    p_hint.add_argument('hint', help='Current broth context hint')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    {
        'plant': cmd_plant,
        'nibble': cmd_nibble,
        'dream': cmd_dream,
        'status': cmd_status,
        'crystallize': cmd_crystallize,
        'extend': cmd_extend,
        'read': cmd_read,
        'harvest': cmd_harvest,
        'hint': cmd_hint,
    }[args.command](args)


if __name__ == '__main__':
    main()
