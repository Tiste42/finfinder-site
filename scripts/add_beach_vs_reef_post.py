import json
import os
import re
import sys
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = ROOT / "blog_posts.json"
STATIC_DIR = ROOT / "static"
MCP_PATH = ROOT / ".claude" / "mcp.json"

SLUG = "beach-break-vs-reef-break-fins-setup-choice"

CONTENT = """<p>You wake at 5 a.m. for dawn patrol at Hossegor. The wind's offshore, the sandbars look weirdly perfect after last week's storm, and you've got the same thruster set bolted in your board that you ran a month ago at a hollow reef in Indo. Three waves in, you're getting smoked.</p>

<p>Not the surfer's fault. Not the board's. Wrong fins for the wave.</p>

<p>Most surfers ride one fin template in everything. Same set at the punchy beach break, the predictable reef, the long-walled point. The board feels off and they blame their conditioning, their timing, the wax. The fins are doing exactly what they were designed to do. They were just designed for a different wave.</p>

<h2>Why the Wave Shape Decides Your Fin</h2>

<p>A beach break is chaos with a schedule. Sandbars shift week to week, waves wedge off close-outs, sections jack up without warning, and you're constantly redirecting mid-line. You aren't drawing long arcs out there. You're squaring off pockets and trying to make sections that close out three feet ahead.</p>

<p>A reef break is the opposite. Pipeline, Cloudbreak, Teahupoo, Uluwatu. The wave breaks in roughly the same spot every set, the takeoff is committed, and once you're in the barrel the board has to hold its line. There's no "let me see what this section does." The wave already told you what it's going to do.</p>

<p>Your fins decide whether the board pivots quick or tracks long. That's the whole conversation. Everything else is detail.</p>

<h2>The Beach Break Fin: Upright, Pivoty, Releasey</h2>

<p>Pull up to a 3-foot beach break with stiff, heavily raked fins and the board feels stuck in second gear. Every turn needs a half-second of planning. The lip's already crashed by the time your rail's set.</p>

<p>Beach break fins want to be upright. Less rake, taller height, more pivot. Templates like the FCS II Performer, the Futures John John Florence Medium, or the FCS II Reactor live in this lane. They give you a tighter turning radius and they release off the top with way less effort.</p>

<p>The feel: you square off a bottom turn, the fins grip just long enough to set the rail, then they let go on command when you hit the lip. That snappy release is everything in shifty beach break surf. You're not flowing through long sweeping arcs. You're stabbing, pivoting, recovering, repeating.</p>

<p>Ocean Beach in San Francisco, La Graviere in France, the Wedge in Newport, Puerto Escondido on the smaller days. Same fin logic everywhere. Quick on, quick off, no commitment.</p>

<h2>The Reef Break Fin: Raked, Drivey, Locked In</h2>

<p>Now flip it. You're paddling out at a heavy reef and the wave's going to test your hold from the moment you stand up. You need fins that bite when the wave goes vertical and refuse to skip out when you're high-lining through a section.</p>

<p>Reef break fins lean raked and slightly stiffer. Templates like the Futures Alpha, the FCS II AM (Al Merrick), or the Futures Pyzel John John want to drive long. More rake means a longer turning arc but more hold through critical sections. Stiffness means less chatter when you're locked in at speed on a 6-foot face.</p>

<p>The feel: you draw a long bottom turn, the fins lock in like a confident handshake, and the board just goes. You're not fighting to keep the rail buried. The fins are doing that work for you.</p>

<p>That's why pros at Pipeline overwhelmingly run quads with a neutral rake. Quads kill the center-fin drag and the rear pair adds hold deep in the barrel. John John's set at Pipe is a thruster with a heavier-rake template for the same reason. He wants the board to drive through whatever the wave throws without fighting back. <a href="/finsights/pipeline-fin-setups-what-pros-ride">We broke down what the Pipe lineup actually rides</a> in more depth if you want the specific templates.</p>

<h2>The Point Break Wildcard</h2>

<p>Points are their own animal. Long walls, predictable shape, often slower than a punchy beach break but more sustained than a one-section reef. Snapper Rocks, Rincon, Malibu, J-Bay.</p>

<p>You want rake and drive here. Templates like the Futures Mayhem or a deeper-rake Reactor variant let you connect long sections without pumping yourself into oxygen debt. A pivoty beach-break fin feels weak on a J-Bay wall. The board pumps but it doesn't go. You're working twice as hard for half the speed.</p>

<h2>Why Quads Tilt the Math</h2>

<p>Going quad changes the whole equation. Take out the center fin and the board becomes a different animal. Quads suit reef break and heavy wave riding way better than they suit shifty beach breaks, because the four fins give you grip on critical faces without the drag of a center fin slowing your line.</p>

<p>The pros at Tahiti and Pipe run quads for a reason. The Mick Fanning Quad in a slightly bigger size, the Kelly Slater K2.1, the Futures JJF Quad. Deep-hold setups for waves that demand them.</p>

<p>At a beach break, the same quad can feel skatey and unhooked. You want the bite of a thruster's center fin when you're squaring off short sections at the Wedge or Salina Cruz. <a href="/finsights/quad-vs-thruster-when-speed-matters">We've broken down when quads make sense and when they don't</a> if you want to go deeper on the setup tradeoff.</p>

<h2>The Most Common Mistake</h2>

<p>Ask a surfer what fins they're running and most will tell you the template they bought three years ago because the shop guy recommended it. That setup is now bolted in every board, ridden in every wave, and blamed when the session goes sideways.</p>

<p>The fix isn't expensive. It's awareness. If the wave is sectiony and quick, you want upright. If the wave is hollow and powerful, you want raked. If the wave is long and walled, you want drive. <a href="/finsights/fin-rake-explained-tight-vs-sweeping-turns">Rake controls turning arc more than almost any other variable</a>, and once you feel the difference you don't go back.</p>

<p>Three templates and a few fin keys covers more conditions than most surfers ever encounter in a season.</p>

<h2>The Honest Verdict</h2>

<p>If you only surf one type of break, match your fin set to that wave. Don't run reef break fins at a punchy beachie and don't bring upright beach break fins to a heavy reef. The board can do both. The fins can't.</p>

<p>If you bounce around, and most of us do, keep a two-set quiver. One upright, releasey template for shifty conditions. One raked, drivey template (or a quad set) for the heavier days. <a href="/finsights/fin-quiver-budget-two-set-arsenal">A two-set arsenal under $200 isn't hard to build</a>, and it covers more waves than people think.</p>

<p>The lazy move is running the same fins year-round and blaming everything else when the board feels wrong. Don't be that surfer.</p>

<h2>Key Takeaways</h2>
<ul>
<li>Beach break fins want to be upright with less rake. Pivot, quick release, tighter turning radius.</li>
<li>Reef break fins want rake and stiffness. Hold, drive, less chatter at speed.</li>
<li>Point breaks reward raked drivers that let you connect long sections without pumping yourself out.</li>
<li>Quads shine at hollow reefs like Pipe and Teahupoo, and feel skatey at punchy beach breaks.</li>
<li>A two-set fin quiver covers 90% of conditions. One pivoty, one drivey. Done.</li>
</ul>

<p>Not sure which template fits the wave you're surfing tomorrow? Tell our <a href="/recommender">fin recommender</a> what you ride and where, and it'll spit out the set that actually matches the conditions. Faster than scrolling Reddit threads about fin templates at midnight.</p>"""

POST = {
    "slug": SLUG,
    "title": "Beach Break Fins vs Reef Break Fins: One Quiver Won't Cover Both",
    "excerpt": "Beach break fins want to pivot. Reef break fins want to hold. Run the wrong set in the wrong wave and you'll feel every mistake. Here's how to match fin to break.",
    "content": CONTENT,
    "category": "guides",
    "tags": [
        "beach break fins",
        "reef break fins",
        "fin templates",
        "fin setup",
        "surf conditions",
        "fin selection",
        "upright fins",
        "raked fins"
    ],
    "author": "FinFinder Team",
    "date": "May 30, 2026",
    "date_published": "2026-05-30",
    "date_modified": "2026-05-30",
    "read_time": 6,
    "featured_image": "",
    "featured_image_alt": "Clean turquoise reef break wave peeling along a shallow coral reef under warm light",
    "meta_description": "Beach break fins want to pivot. Reef break fins want to hold. Run the wrong set in the wrong wave and you'll feel every mistake. Here's the fix.",
    "primary_keyword": "beach break vs reef break fins",
    "secondary_keywords": [
        "fin templates for beach break",
        "best fins for reef break",
        "upright vs raked fins",
        "fin choice by wave type",
        "two-set fin quiver"
    ],
    "faqs": [
        {
            "question": "What fins work best for a beach break?",
            "answer": "Upright templates with less rake. Fins like the FCS II Performer, FCS II Reactor, or Futures John John Florence Medium give you a tighter turning radius and quick release off the lip, which is what shifty beach break sections demand."
        },
        {
            "question": "Are quad fins better for reef breaks?",
            "answer": "Often, yes. Quads remove the center-fin drag and add hold from the rear pair, which is why pros at Pipeline and Teahupoo run quad setups. They lock in deep in the barrel and let the board drive long without the brake of a thruster center fin."
        },
        {
            "question": "Can the same fin set work for every type of wave?",
            "answer": "One set will work, but it won't be optimal anywhere. Beach breaks reward upright pivot fins. Reefs reward raked drivey fins or quads. Points reward raked templates with drive. Running one set everywhere means you're giving up performance in at least one type of wave."
        },
        {
            "question": "What is fin rake and why does it matter?",
            "answer": "Rake is how far back the fin's tip sweeps from the base. Upright fins (less rake) pivot quickly in a tight arc and release easily. Raked fins (swept back further) hold longer through a turn and drive through sections. Less rake suits beach breaks. More rake suits points and reefs."
        },
        {
            "question": "Do I need different fins for different surf trips?",
            "answer": "If the trip changes the wave type, yes. A two-set quiver with one upright template and one raked or quad template covers almost every condition a recreational surfer will see in a season. Same board, different fins, very different rides."
        }
    ],
    "last_image_type": "WAVE_FRAME"
}


def append_post():
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    # Guard: avoid duplicate
    if any(p["slug"] == SLUG for p in data["posts"]):
        print(f"Post {SLUG} already exists, skipping append.")
        return
    data["posts"].append(POST)
    JSON_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Appended {SLUG}")


def try_generate_image():
    """Try to generate the hero image via Gemini. Returns True on success."""
    try:
        from google import genai
        from google.genai import types
        from PIL import Image
    except ImportError:
        print("google-genai or Pillow not installed.")
        return False

    mcp = json.loads(MCP_PATH.read_text(encoding="utf-8"))
    api_key = None
    try:
        api_key = mcp["mcpServers"]["nano-banana-pro"]["env"]["GEMINI_API_KEY"]
    except Exception:
        for srv in mcp.get("mcpServers", {}).values():
            env = srv.get("env", {})
            if "GEMINI_API_KEY" in env:
                api_key = env["GEMINI_API_KEY"]
                break
    if not api_key:
        print("No GEMINI_API_KEY found.")
        return False

    prompt = (
        "Editorial surf photography of a clean, glassy reef break wave peeling "
        "along a shallow coral reef in turquoise tropical water, warm golden "
        "afternoon light, soft offshore spray feathering the lip, distant blue "
        "horizon, no people, no surfers, no boards visible, photorealistic, "
        "wide landscape framing, cinematic depth, warm natural tones. "
        "No text, no logos, no readable letters, no faces."
    )

    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-3.1-flash-image-preview",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio="16:9",
                    image_size="2K",
                ),
            ),
        )
    except Exception as e:
        print(f"Gemini call failed: {e}")
        return False

    image_bytes = None
    for part in response.candidates[0].content.parts:
        if getattr(part, "inline_data", None) and part.inline_data.data:
            image_bytes = part.inline_data.data
            break

    if not image_bytes:
        print("No image data in response.")
        return False

    img = Image.open(BytesIO(image_bytes)).convert("RGB")
    scale = 1200 / img.width
    new_h = int(img.height * scale)
    img = img.resize((1200, new_h), Image.LANCZOS)
    if img.height < 448:
        scale = 448 / img.height
        img = img.resize((int(img.width * scale), 448), Image.LANCZOS)
        left = (img.width - 1200) // 2
        img = img.crop((left, 0, left + 1200, 448))
    else:
        top = (img.height - 448) // 2
        img = img.crop((0, top, 1200, top + 448))

    out = STATIC_DIR / f"{SLUG}.webp"
    img.save(out, "WEBP", quality=85)
    print(f"Saved hero {out}")
    # Update JSON entry
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    for p in data["posts"]:
        if p["slug"] == SLUG:
            p["featured_image"] = f"{SLUG}.webp"
            break
    JSON_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return True


if __name__ == "__main__":
    append_post()
    ok = try_generate_image()
    if not ok:
        print("Image generation skipped/failed. Publishing without hero image.")
