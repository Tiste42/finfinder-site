"""Add the 'Cracked Fin Box' blog post to blog_posts.json."""
import json
from pathlib import Path

POSTS_FILE = Path(__file__).parent.parent / "blog_posts.json"

SLUG = "cracked-fin-box-repair-save-your-board"

CONTENT = """<p>You finish a session at Black's, hop out, and notice it as you wash the board: one of your back fins has a faint wobble. Not the kind you can ignore. The kind that says something cracked.</p>

<p>The fin's fine. The box isn't.</p>

<p>Cracked fin boxes are the quietly catastrophic damage a board can suffer. Worse than a snapped nose. Worse than a heel dent.</p>

<p>A cracked box doesn't shout. It just slowly turns your favorite shortboard into a wall hanger. The good news: most are repairable. The bad news: most surfers do the repair wrong and finish what the crack started.</p>

<p>This is the breakdown. What cracked, why, and whether you can still save the board.</p>

<h2>Why Fin Boxes Crack in the First Place</h2>

<p>Fin boxes are plastic, glassed into a foam blank under fiberglass cloth and resin. They're strong in compression. They're not great in torsion.</p>

<p>Three things crack them:</p>

<ol>
  <li><strong>Hard hits from underneath.</strong> Rocky shore launch, dragging the board fin-down across gravel, a rogue cobble in the inside section at Trestles. The base of the box takes a shock the fin's supposed to take, and the plastic shears.</li>
  <li><strong>Lateral forces from the fin itself.</strong> Big surfer, big wave, fin loaded up hard mid-bottom-turn. The fin pries against the box wall like a crowbar. If the resin around the box has any voids, the box starts moving inside the foam.</li>
  <li><strong>Compression from over-tightening.</strong> This one's painful because it's self-inflicted. Cranking your FCS II screws past finger-tight cracks the box where the grub screw meets the plastic. We've seen it on $1,200 customs. Doesn't care about price.</li>
</ol>

<p>Old boards crack from fatigue. New boards crack from impact. The pattern matters because it tells you how deep the damage goes.</p>

<h2>The Three Crack Types You'll See</h2>

<h3>Surface star crack</h3>

<p>The glass around the box shows a starburst of hairline cracks. The box itself feels fine. The fin doesn't wobble.</p>

<p>Surface only. Seal it the same day with a drop of UV resin or even a smear of clear nail polish to stop water getting in. Water in a foam blank is the slowest, ugliest death a board can suffer. Don't put it off.</p>

<h3>Wobble-in-box</h3>

<p>You can feel the fin moving when you torque it side to side with your hand. The box has separated from the surrounding glass, or the bond between box and foam has failed. From the deck side, you might see a faint dimple or crack.</p>

<p>This is repairable but it needs glasswork. Either drill out the damaged area, clean the void with acetone, and inject thickened epoxy with Q-Cell, or pull the whole box and re-set it. The first is a 90-minute job for a competent home repairer. The second is a ding shop appointment.</p>

<h3>Side blow-out</h3>

<p>The plastic side wall of the box is split or pushed outward. Sometimes you can see daylight through the crack. Fin sits crooked even when you don't push on it.</p>

<p>This one's the death sentence for the box, not necessarily the board. You're cutting it out and replacing it. That's $100 to $180 at a decent ding shop in Encinitas or Costa Mesa. DIY only if you've done it before and own a router.</p>

<h2>FCS vs Futures: They Don't Crack the Same</h2>

<p>Worth noting because the repair path changes.</p>

<p>FCS II boxes have plastic side walls and a hollow channel. When they fail, they tend to fail at the channel walls or at the screw point. The plastic is replaceable as a unit because the box is shallow.</p>

<p>Futures boxes are deeper, single-piece, and bonded to the foam more aggressively. They fail at the base or the fin slot. Deeper repair means more glass work and more chance of the fix adding stiffness in a spot the shaper didn't intend.</p>

<p>If you're swapping systems entirely while you're in there, <a href="/finsights/switching-fcs-to-futures-what-to-know">here's the honest answer on Futures-to-FCS</a>. Spoiler: it's not as bad as it sounds.</p>

<h2>The DIY Repair, When the Damage Is Minor</h2>

<p>You'll need:</p>

<ul>
  <li>Epoxy resin (not polyester unless your board is PU/PE)</li>
  <li>Q-Cell or microballoons to thicken it</li>
  <li>A syringe with a blunt needle</li>
  <li>Sandpaper (80, 220, 400 grit)</li>
  <li>Clear UV resin for the finish coat</li>
  <li>Masking tape</li>
</ul>

<p>Process:</p>

<p>Dry the board for at least 48 hours. Foam holds water. Repairing a wet box is paving over a sinkhole.</p>

<p>Tape around the damaged area. Sand off the topcoat in the immediate zone, exposing clean glass.</p>

<p>Mix your epoxy with enough Q-Cell to make a peanut butter consistency. Inject into the void with the syringe. Press the box down flush.</p>

<p>Let it cure for the time the resin spec says, then sand flat and finish with UV resin. Done.</p>

<p>The whole thing takes a Sunday afternoon and runs about $40 in materials if you already own a sander.</p>

<h2>When to Pay Someone Else</h2>

<p>Take it to a shop if:</p>

<ul>
  <li>You can see foam, not glass</li>
  <li>The box is moving more than 1mm in any direction</li>
  <li>The crack is on the deck side (means the load path is compromised)</li>
  <li>You don't own a sander</li>
  <li>The board is worth more than $600 new</li>
</ul>

<p>Good ding repair shops in San Diego, Orange County, and Ventura charge $90 to $150 for a fin box repair done right. That's cheap insurance compared to a $900 replacement board.</p>

<h2>What a Bad Repair Feels Like</h2>

<p>Bad repairs telegraph through the rail line. You'll feel the fin loading up and then a sudden, sketchy give halfway through a hard cutback.</p>

<p>The board hesitates. Like driving a car with a slightly out-of-balance wheel. Nothing catastrophic until it suddenly is.</p>

<p>Done right, you should never feel where the repair was. The fin should torque from the deck-flex side, not the box. If you can feel the box moving under load, the repair failed and you need to redo it before the next session.</p>

<h2>Can You Just Switch Boxes While You're At It?</h2>

<p>Sometimes. If you've always wanted to convert a glassed-on single fin to a removable, or move a FCS board to Futures, a fin box repair is the cheapest moment to do it. You're already cutting glass.</p>

<p>That said, a shop will charge for the system swap on top of the repair, and the conversion adds time. If the rest of the board is tired, you might be polishing a turd. Read our breakdown of <a href="/finsights/fin-box-systems-beyond-fcs-futures-probox-lokbox-bahne">the smaller fin box systems still holding on</a> before committing to anything past FCS or Futures.</p>

<h2>Key Takeaways</h2>

<ul>
  <li>A cracked fin box rarely kills a board. A bad repair often does.</li>
  <li>Dry your board for 48 hours before any work. Wet foam ruins the bond every single time.</li>
  <li>FCS II boxes fail at the plastic walls. Futures fail at the base or slot. Repair the type, not the symptom.</li>
  <li>Star cracks can wait one day. Wobble-in-box can't. Side blow-outs go to a pro.</li>
  <li>Quality ding shop work runs $90 to $150. Worth it on any board over $600 new.</li>
</ul>

<p>If you're not sure your current fin setup is even worth saving the box for, our <a href="/recommender">fin recommender</a> takes about a minute to tell you whether you've been riding the wrong template on this board all along. Sometimes the box wasn't the actual problem.</p>"""


POST = {
    "slug": SLUG,
    "title": "Cracked Fin Box: How to Tell If Your Board's Done or Just Wounded",
    "excerpt": "A cracked fin box doesn't always kill a board. Most surfers do the repair wrong and finish what the crack started. Here's how to tell.",
    "content": CONTENT,
    "category": "guides",
    "author": "FinFinder Team",
    "date": "Jun 04, 2026",
    "date_published": "2026-06-04",
    "date_modified": "2026-06-04",
    "read_time": 6,
    "featured_image": "",
    "featured_image_alt": "Surfboard fin box and repair tools laid out on a weathered wood workbench",
    "meta_description": "A cracked fin box doesn't always kill a board. Here's how to spot surface damage from the real thing, and when DIY beats paying a shop.",
    "tags": [
        "fin box repair",
        "ding repair",
        "FCS",
        "Futures",
        "surfboard maintenance",
        "DIY surfboard",
        "fin systems"
    ],
    "primary_keyword": "cracked fin box repair",
    "secondary_keywords": [
        "fin box damage",
        "surfboard fin box repair",
        "FCS box crack",
        "Futures box repair",
        "fin box DIY"
    ],
    "faqs": [
        {
            "question": "Can you surf with a cracked fin box?",
            "answer": "Only if it's a surface star crack and you've sealed it with UV resin or nail polish to keep water out. Any wobble in the box itself means the load path is compromised. Surfing on a wobbly box risks ripping the entire box out mid-session, which turns a $90 repair into a $300 one."
        },
        {
            "question": "How much does a fin box repair cost?",
            "answer": "A standard fin box repair runs $90 to $150 at a quality ding shop in California. A full box replacement runs $100 to $180. DIY costs about $40 in epoxy, Q-Cell, and sandpaper if you already own a sander."
        },
        {
            "question": "Can you repair a cracked fin box yourself?",
            "answer": "Yes, if the damage is a star crack or a minor wobble. Dry the board for 48 hours, sand the area down, inject thickened epoxy into the void with a syringe, then finish with UV resin. Side blow-outs and visible foam exposure should go to a pro because they need router work."
        },
        {
            "question": "What causes a fin box to crack?",
            "answer": "Three main causes: hard impacts from rocks or gravel hitting the box base, lateral force from heavy surfers loading fins hard in big surf, and over-tightening the grub screws past finger-tight on FCS II systems. Fatigue cracks happen on older boards. New boards almost always crack from impact."
        },
        {
            "question": "How long does a fin box repair take to cure?",
            "answer": "Epoxy needs 24 hours to cure fully before the board sees water. UV resin finish coats cure in minutes under direct sunlight. Total downtime from crack to surfable is usually 3 to 5 days, including the 48-hour drying window before any resin work."
        }
    ],
    "last_image_type": "FINS_ON_WOOD"
}


def main():
    data = json.loads(POSTS_FILE.read_text(encoding="utf-8"))
    existing = {p["slug"] for p in data["posts"]}
    if SLUG in existing:
        print(f"Post {SLUG} already exists. Aborting.")
        return
    data["posts"].append(POST)
    POSTS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    # Validate
    json.loads(POSTS_FILE.read_text(encoding="utf-8"))
    # Word count
    import re
    text = re.sub(r"<[^>]+>", " ", CONTENT)
    words = len(text.split())
    print(f"Added post: {SLUG}")
    print(f"Word count: {words}")
    print(f"Total posts: {len(data['posts'])}")


if __name__ == "__main__":
    main()
