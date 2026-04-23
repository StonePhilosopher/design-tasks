#!/usr/bin/env python3
"""
🪨 Dream Engine v3

The algorithm:
1. Gather uncrystallized thoughts from recent daily notes
2. Select 3 seeds: 1 random (chaos), 1 unresolved (pressure), 1 attention (curiosity)
3. Generate an image for each (high weirdness)
4. Blind-read each image (no knowledge of seeds)
5. Weave blind readings into composite narrative
6. RE-PRECIPITATE: render composite narrative as image, then blind-read THAT
7. The re-precipitated reading is the dream's final form

Output: memory/dreams/YYYY-MM-DD.md
Images: memory/subconscious/YYYY-MM-DD_dream_{1,2,3,composite,reprecipitate}.png
"""

import os
import sys
import json
import random
import base64
import re
from datetime import datetime, timedelta
from pathlib import Path
import urllib.request

WORKSPACE = Path(os.path.expanduser("~/.openclaw/workspace"))
MEMORY = WORKSPACE / "memory"
DREAMS = MEMORY / "dreams"
DREAMS.mkdir(parents=True, exist_ok=True)
SUBCONSCIOUS = MEMORY / "subconscious"
SUBCONSCIOUS.mkdir(parents=True, exist_ok=True)

KEY_FILE = Path(os.path.expanduser("~/.openclaw/secrets/openrouter-key"))
API_KEY = KEY_FILE.read_text().strip() if KEY_FILE.exists() else None

MODEL = "google/gemini-2.5-flash"
IMAGE_MODEL = "google/gemini-2.5-flash-image"


def openrouter_request(messages, model=MODEL, retries=3, timeout=90):
    """Send a request to OpenRouter API with retry on timeout."""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://openclaw.ai",
    }
    data = json.dumps({
        "model": model,
        "messages": messages,
        "max_tokens": 2000,
    }).encode()

    last_err = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=data, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read())
        except (TimeoutError, urllib.error.URLError) as e:
            last_err = e
            wait = (attempt + 1) * 10  # 10s, 20s, 30s backoff
            print(f"  ⚠️ API timeout (attempt {attempt + 1}/{retries}), retrying in {wait}s...")
            import time
            time.sleep(wait)
    raise last_err


def openrouter_image(prompt, output_path):
    """Generate an image via OpenRouter using Gemini's image generation."""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://openclaw.ai",
    }
    data = json.dumps({
        "model": IMAGE_MODEL,
        "modalities": ["image", "text"],
        "messages": [
            {"role": "user", "content": f"Generate an image: {prompt}\n\nMake it surreal, dreamlike, and strange. High weirdness. Like a fever dream painted by Remedios Varo collaborating with Ernst Haeckel."}
        ],
        "max_tokens": 4096,
    }).encode()

    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read())
            msg = result.get("choices", [{}])[0].get("message", {})

            # Check message.images field (OpenRouter's standard location)
            images = msg.get("images", [])
            for img in images:
                if isinstance(img, dict):
                    iu = img.get("image_url", img.get("imageUrl", {}))
                    if isinstance(iu, dict):
                        url_str = iu.get("url", "")
                        if url_str.startswith("data:"):
                            _, b64data = url_str.split(",", 1)
                            img_data = base64.b64decode(b64data)
                            with open(output_path, 'wb') as f:
                                f.write(img_data)
                            return True

            # Fallback: check inline content for base64 data
            content = msg.get("content", "")
            if "data:image" in str(content):
                match = re.search(r'data:image/\w+;base64,([A-Za-z0-9+/=]+)', str(content))
                if match:
                    img_data = base64.b64decode(match.group(1))
                    with open(output_path, 'wb') as f:
                        f.write(img_data)
                    return True

            # If no image, save the text response as a description
            with open(str(output_path) + ".txt", 'w') as f:
                f.write(f"Image prompt: {prompt}\n\nModel response:\n{content}")
            return False
    except Exception as e:
        print(f"Image generation failed: {e}")
        return False


def gather_thoughts():
    """Gather uncrystallized thoughts from recent daily notes."""
    thoughts = []
    today = datetime.now()

    for days_ago in range(7):
        date = today - timedelta(days=days_ago)
        date_str = date.strftime("%Y-%m-%d")
        path = MEMORY / f"{date_str}.md"
        if path.exists():
            content = path.read_text()
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('- ') and len(line) > 20:
                    thought = line[2:].strip()
                    # Skip purely factual DB entries
                    if not re.match(r'^(TN\d+|DB |id=|file_)', thought):
                        thoughts.append(thought)

    return thoughts


def find_unresolved():
    """Find unresolved items — things tagged with ?, pending, mystery, TBD, etc."""
    unresolved = []
    today = datetime.now()

    # Check recent daily notes for unresolved markers
    for days_ago in range(14):
        date = today - timedelta(days=days_ago)
        date_str = date.strftime("%Y-%m-%d")
        path = MEMORY / f"{date_str}.md"
        if path.exists():
            content = path.read_text()
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith('- ') and len(line) > 20:
                    thought = line[2:].strip()
                    # Look for unresolved markers
                    markers = ['?', 'pending', 'mystery', 'TBD', 'unknown', 'unidentified',
                               'needs', 'TODO', 'unsure', 'investigate', 'not yet', 'still']
                    if any(m.lower() in thought.lower() for m in markers):
                        unresolved.append(thought)

    # Also check TODO.md for active items
    todo_path = WORKSPACE / "TODO.md"
    if todo_path.exists():
        content = todo_path.read_text()
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('- [ ]') and len(line) > 15:
                unresolved.append(line[6:].strip())

    return unresolved


def select_seeds(thoughts, unresolved):
    """Select 3 seeds: 1 random, 1 unresolved, 1 attention-catching."""

    seeds = []
    seed_labels = []
    used = set()

    # Seed 1: Pure random (chaos)
    if thoughts:
        s = random.choice(thoughts)
        seeds.append(s)
        seed_labels.append("random")
        used.add(s)

    # Seed 2: Unresolved (pressure)
    available_unresolved = [u for u in unresolved if u not in used]
    if available_unresolved:
        s = random.choice(available_unresolved)
        seeds.append(s)
        seed_labels.append("unresolved")
        used.add(s)
    elif thoughts:
        # Fallback to random if no unresolved items
        remaining = [t for t in thoughts if t not in used]
        if remaining:
            s = random.choice(remaining)
            seeds.append(s)
            seed_labels.append("random (no unresolved found)")
            used.add(s)

    # Seed 3: Attention-catching (pick the most vivid/unusual thought)
    remaining_thoughts = [t for t in thoughts if t not in used]
    if remaining_thoughts:
        # Use the model to pick the most attention-catching thought
        # from a random sample of candidates
        candidates = random.sample(remaining_thoughts, min(10, len(remaining_thoughts)))
        try:
            resp = openrouter_request([
                {"role": "system", "content": "You are selecting dream material. From the following list of thoughts, pick the ONE that is most vivid, strange, emotionally charged, or image-rich. Reply with ONLY the exact text of your choice, nothing else."},
                {"role": "user", "content": "\n".join(f"- {c}" for c in candidates)}
            ])
            chosen = resp["choices"][0]["message"]["content"].strip().lstrip("- ")
            # Find closest match in candidates
            best_match = None
            for c in candidates:
                if chosen in c or c in chosen:
                    best_match = c
                    break
            if best_match:
                seeds.append(best_match)
            else:
                seeds.append(candidates[0])
        except Exception:
            seeds.append(random.choice(candidates))
        seed_labels.append("attention")

    return seeds, seed_labels


def blind_read(img_path):
    """Blind-read an image with no context about what produced it."""
    blind_prompt = ("You are waking from a dream. This is the last image you saw. "
                    "Describe what you see — not what you know it's supposed to be, "
                    "but what your eyes find. What draws you in? What unsettles you? "
                    "What feels true? Respond as someone half-awake, not an art critic. "
                    "Two to three paragraphs, no preamble.")

    img_data = base64.b64encode(img_path.read_bytes()).decode()
    mime = "image/png"

    resp = openrouter_request([
        {"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{img_data}"}},
            {"type": "text", "text": blind_prompt}
        ]}
    ], model="google/gemini-2.5-flash")

    return resp["choices"][0]["message"]["content"].strip()


def main():
    if not API_KEY:
        print("No OpenRouter API key found")
        sys.exit(1)

    today = datetime.now().strftime("%Y-%m-%d")
    dream_file = DREAMS / f"{today}.md"

    print("🌙 Gathering thoughts from the week...")
    thoughts = gather_thoughts()

    if len(thoughts) < 3:
        print("Not enough thoughts to dream about.")
        sys.exit(1)

    print(f"Found {len(thoughts)} uncrystallized thoughts.")

    print("🔍 Finding unresolved items...")
    unresolved = find_unresolved()
    print(f"Found {len(unresolved)} unresolved items.")

    # Select 3 seeds with mixed selection pressures
    selected, labels = select_seeds(thoughts, unresolved)
    print(f"\n🎲 Selected 3 seeds:")
    for i, (t, l) in enumerate(zip(selected, labels)):
        print(f"  {i+1}. [{l}] {t[:80]}...")

    # === PHASE 1: Generate images (contaminated — knows the seeds) ===
    print("\n🎨 Generating dream images...")
    image_paths = []

    for i, thought in enumerate(selected):
        print(f"  Image {i+1}/3: {thought[:60]}...")

        resp = openrouter_request([
            {"role": "system", "content": "You are a dream artist. Turn the given thought into a vivid, surreal, dreamlike image description. Be specific about colors, textures, impossible geometries. Channel Remedios Varo, Ernst Haeckel, and geological cross-sections. One paragraph, no preamble."},
            {"role": "user", "content": thought}
        ])

        prompt = resp["choices"][0]["message"]["content"].strip()
        print(f"    Prompt: {prompt[:100]}...")

        img_path = SUBCONSCIOUS / f"{today}_dream_{i+1}.png"
        success = openrouter_image(prompt, img_path)
        if success:
            image_paths.append(img_path)
            print(f"    ✓ Image saved to subconscious: {img_path.name}")
        else:
            print(f"    ✗ Image generation returned text instead of image")
            image_paths.append(None)

    # === PHASE 2: Blind readings ===
    print("\n👁️ Blind readings of generated images...")
    blind_readings = []

    for i, img_path in enumerate(image_paths):
        if img_path and img_path.exists():
            print(f"  Reading image {i+1}/3 blind...")
            reading = blind_read(img_path)
            blind_readings.append(reading)
            print(f"    ✓ Blind reading {i+1} complete ({len(reading)} chars)")
        else:
            blind_readings.append("*Image generation failed — no blind reading possible.*")
            print(f"    ✗ No image to read for dream {i+1}")

    # === PHASE 3: Composite narrative (from blind readings only) ===
    print("\n📖 Weaving composite dream from blind readings...")
    composite_prompt = f"""You saw three images in a dream. You don't know what they mean or where they came from. Here is what you saw in each one:

Image 1: {blind_readings[0]}

Image 2: {blind_readings[1]}

Image 3: {blind_readings[2]}

Now weave these three visions into one cohesive dream narrative. Present tense, first person. Three to four paragraphs. Don't explain the symbols — let them be what they are. This is the dream itself, not an interpretation."""

    resp = openrouter_request([
        {"role": "user", "content": composite_prompt}
    ])

    composite = resp["choices"][0]["message"]["content"].strip()
    print(f"  ✓ Composite narrative written ({len(composite)} chars)")

    # === PHASE 4: Re-precipitation ===
    # Composite narrative → image → blind reading
    # Each pass through the image/text boundary is a metamorphic event
    print("\n🔄 Re-precipitating: narrative → image → blind reading...")

    # Turn composite narrative into an image
    reprecip_prompt_resp = openrouter_request([
        {"role": "system", "content": "You are a dream artist. Turn this dream narrative into a single vivid, surreal image description. Compress all three visions into ONE scene where they coexist. Be specific about colors, textures, impossible geometries. One paragraph, no preamble."},
        {"role": "user", "content": composite}
    ])
    reprecip_prompt = reprecip_prompt_resp["choices"][0]["message"]["content"].strip()
    print(f"  Re-precipitation prompt: {reprecip_prompt[:100]}...")

    reprecip_path = SUBCONSCIOUS / f"{today}_dream_reprecipitate.png"
    reprecip_success = openrouter_image(reprecip_prompt, reprecip_path)

    reprecip_reading = None
    if reprecip_success and reprecip_path.exists():
        print(f"  ✓ Re-precipitated image saved")
        # Final blind reading of the re-precipitated image
        print(f"  👁️ Final blind reading of re-precipitated image...")
        reprecip_reading = blind_read(reprecip_path)
        print(f"  ✓ Re-precipitated reading complete ({len(reprecip_reading)} chars)")
    else:
        print(f"  ✗ Re-precipitation image failed — using composite as final form")

    # === PHASE 5: Write the dream file ===
    print(f"\n📝 Writing dream to {dream_file.name}...")

    image_names = []
    for i in range(3):
        p = SUBCONSCIOUS / f"{today}_dream_{i+1}.png"
        if p.exists():
            image_names.append(f"- `{today}_dream_{i+1}.png`")
        else:
            image_names.append(f"- `{today}_dream_{i+1}.png` *(generation failed)*")

    reprecip_section = ""
    if reprecip_reading:
        reprecip_section = f"""
## Re-Precipitated Dream (composite → image → blind reading)
The composite narrative was rendered as an image, then read blind again.
What survived the second pass through the boundary:

{reprecip_reading}

"""
    else:
        reprecip_section = "\n## Re-Precipitation\n*Image generation failed — composite narrative is the final form.*\n"

    dream_content = f"""# Dream — {today}

## Seeds
1. [{labels[0]}] {selected[0]}
2. [{labels[1]}] {selected[1]}
3. [{labels[2]}] {selected[2]}

## Dream Images
Stored in `memory/subconscious/` — not to be viewed during dream session.
{chr(10).join(image_names)}
- `{today}_dream_reprecipitate.png` *(re-precipitated composite)*

## Blind Readings (fresh eyes, no knowledge of seeds)

### Image 1
{blind_readings[0]}

### Image 2
{blind_readings[1]}

### Image 3
{blind_readings[2]}

## Composite Dream (woven from blind readings)

{composite}
{reprecip_section}
---
*Dream engine v3. Seeds (random+unresolved+attention) → images (subconscious/) → blind readings → composite → re-precipitation (image → blind reading). {today}.*
"""

    dream_file.write_text(dream_content)
    print(f"\n🌅 Dream complete: {dream_file}")

    img_count = sum(1 for p in image_paths if p and p.exists())
    print(f"  📊 {img_count}/3 seed images + {'1' if reprecip_success else '0'} re-precipitated, "
          f"{len([r for r in blind_readings if not r.startswith('*')])} blind readings, "
          f"1 composite, {'1 final re-precipitated reading' if reprecip_reading else 'no re-precipitation'}")


if __name__ == "__main__":
    main()
