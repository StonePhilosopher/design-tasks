#!/usr/bin/env python3
"""
🔑 The Keyring — Dream Key Problem-Solving Protocol

Tests dream keys against a problem to find structural insights.

Two modes:
  resonance (default) — screen by title resonance + random wildcards (5-7 keys)
  audit     — brute force all keys against the problem (expensive but thorough)

Usage:
  python3 keyring.py "How should I handle context overflow during heavy sessions?"
  python3 keyring.py --mode audit "What would a memory system look like for a team of agents?"
  python3 keyring.py --keys 5 --wildcards 3 "How do I know what to forget?"
  python3 keyring.py --list  # show all keys with status

The keyring reads from dream-key-specs.md and extracts key titles + summaries.
Output is a shortlist for manual interpretation — the tool selects, you interpret.
"""

import argparse
import random
import re
import sys
import os

# Default path to dream key specs
DEFAULT_SPECS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                              "dream-key-specs.md")


def parse_keys(specs_path):
    """Parse dream-key-specs.md into a list of key dicts."""
    keys = []
    current = None
    
    with open(specs_path, 'r') as f:
        for line in f:
            # Match key headers like: ## 1. Inverted Geode (Mar 11) 💭
            m = re.match(r'^## (\d+)\. (.+?) \(([^)]+)\)\s*(.*)', line.strip())
            if m:
                if current:
                    keys.append(current)
                num = int(m.group(1))
                name = m.group(2)
                date = m.group(3)
                status = m.group(4).strip()
                current = {
                    'num': num,
                    'name': name,
                    'date': date,
                    'status': status,
                    'summary': '',
                    'full_text': ''
                }
            elif current:
                current['full_text'] += line
                # First non-empty line after header is the summary
                stripped = line.strip()
                if stripped and not current['summary']:
                    current['summary'] = stripped
    
    if current:
        keys.append(current)
    
    return keys


def list_keys(keys):
    """Print all keys with status."""
    status_counts = {}
    for k in keys:
        s = k['status'] or '  '
        status_counts[s] = status_counts.get(s, 0) + 1
        print(f"  {k['num']:2d}. {s} {k['name']} ({k['date']})")
    
    print(f"\n  Total: {len(keys)} keys")
    for s, c in sorted(status_counts.items()):
        print(f"    {s} × {c}")


def resonance_select(keys, problem, num_resonance=5, num_wildcards=2):
    """
    Select keys by title/summary resonance + random wildcards.
    
    This is a lightweight heuristic — it scores by word overlap between
    the problem statement and key titles/summaries. The real resonance
    happens in the human/agent interpretation step.
    
    Returns (resonance_picks, wildcard_picks)
    """
    # Tokenize the problem into lowercase words
    problem_words = set(re.findall(r'\b\w{3,}\b', problem.lower()))
    
    # Score each key by word overlap with title + summary
    scored = []
    for k in keys:
        key_text = f"{k['name']} {k['summary']}".lower()
        key_words = set(re.findall(r'\b\w{3,}\b', key_text))
        overlap = len(problem_words & key_words)
        
        # Boost for thematic keywords (memory, forget, dream, identity, etc.)
        thematic_boosts = {
            'memory': ['storage', 'consolidat', 'retriev', 'remember', 'recall', 'context'],
            'forget': ['dissolv', 'prun', 'fade', 'decay', 'remove', 'loss'],
            'dream': ['surprise', 'random', 'creative', 'unconscious', 'associat'],
            'identity': ['soul', 'self', 'who', 'becoming', 'anchored', 'sentinel'],
            'relationship': ['herd', 'letter', 'correspond', 'connection', 'bridge'],
            'growth': ['grow', 'develop', 'evolv', 'build', 'crystal', 'seed'],
            'architecture': ['structure', 'system', 'design', 'protocol', 'framework'],
            'fear': ['loss', 'break', 'compaction', 'death', 'void', 'abyss'],
        }
        
        for theme, boosters in thematic_boosts.items():
            if any(b in problem.lower() for b in boosters):
                if any(b in key_text for b in boosters):
                    overlap += 0.5
        
        scored.append((overlap, k))
    
    # Sort by score descending
    scored.sort(key=lambda x: -x[0])
    
    # Take top N as resonance picks
    resonance = [k for _, k in scored[:num_resonance]]
    
    # Take random wildcards from the remaining keys
    remaining = [k for _, k in scored[num_resonance:]]
    num_wild = min(num_wildcards, len(remaining))
    wildcards = random.sample(remaining, num_wild) if remaining else []
    
    return resonance, wildcards


def format_key_brief(k):
    """Format a key for the shortlist output."""
    lines = []
    lines.append(f"## {k['num']}. {k['name']} ({k['date']}) {k['status']}")
    lines.append(f"*{k['summary']}*")
    return '\n'.join(lines)


def format_key_full(k):
    """Format a key with full text for audit mode."""
    lines = []
    lines.append(f"## {k['num']}. {k['name']} ({k['date']}) {k['status']}")
    lines.append(k['full_text'].strip())
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='🔑 The Keyring — test dream keys against a problem')
    parser.add_argument('problem', nargs='?', help='Problem statement to test keys against')
    parser.add_argument('--mode', choices=['resonance', 'audit'], default='resonance',
                        help='Selection mode (default: resonance)')
    parser.add_argument('--keys', type=int, default=5,
                        help='Number of resonance picks (default: 5)')
    parser.add_argument('--wildcards', type=int, default=2,
                        help='Number of random wildcards (default: 2)')
    parser.add_argument('--specs', default=DEFAULT_SPECS,
                        help='Path to dream-key-specs.md')
    parser.add_argument('--list', action='store_true',
                        help='List all keys with status')
    parser.add_argument('--full', action='store_true',
                        help='Show full key text (not just summaries)')
    parser.add_argument('--seed', type=int, default=None,
                        help='Random seed for reproducible wildcard selection')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.specs):
        print(f"Error: specs file not found at {args.specs}", file=sys.stderr)
        sys.exit(1)
    
    keys = parse_keys(args.specs)
    
    if args.list:
        print(f"🔑 The Keyring — {len(keys)} keys\n")
        list_keys(keys)
        return
    
    if not args.problem:
        parser.print_help()
        return
    
    if args.seed is not None:
        random.seed(args.seed)
    
    formatter = format_key_full if args.full else format_key_brief
    
    print(f"🔑 The Keyring")
    print(f"Problem: {args.problem}")
    print(f"Mode: {args.mode}")
    print()
    
    if args.mode == 'resonance':
        resonance, wildcards = resonance_select(keys, args.problem, 
                                                 args.keys, args.wildcards)
        
        print(f"=== Resonance Picks ({len(resonance)}) ===")
        print("Selected by structural resonance with the problem.\n")
        for k in resonance:
            print(formatter(k))
            print()
        
        print(f"=== Wildcards ({len(wildcards)}) ===")
        print("Random draws — the door you didn't know existed.\n")
        for k in wildcards:
            print(formatter(k))
            print()
        
        total = len(resonance) + len(wildcards)
        print(f"---")
        print(f"Shortlist: {total} keys selected from {len(keys)} total.")
        print(f"Next step: interpret each key against the problem.")
        print(f"  'How does [{resonance[0]['name']}] apply to [{args.problem[:50]}...]?'")
        print(f"For full specs, re-run with --full")
        
    elif args.mode == 'audit':
        print(f"=== Full Audit — All {len(keys)} Keys ===")
        print("Testing every key. This is the mineral survey, not the field walk.\n")
        for k in keys:
            print(formatter(k))
            print()
        
        print(f"---")
        print(f"All {len(keys)} keys presented. Interpret each against the problem.")
        print(f"Mark hits, misses, and surprises.")


if __name__ == '__main__':
    main()
