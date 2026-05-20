"""Add the Tow-In Fins blog post to blog_posts.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "blog_posts.json"

slug = "tow-in-fins-big-wave-strapped-board-setup"

content = """<p>Sebastian Steudtner gets towed into a six-story Nazaré bomb on a 6'6" weighted gun with foot straps and a fin setup most shapers would call wrong for any other wave on earth. Tiny bases. Stiff foils. Cant angles you'd never run on a shortboard. That's not an accident. That's the whole point of tow surfing.</p>

<p>The thing is, when you're hitting 40 mph on the face before you even let go of the rope, the rules of fin design flip on their head.</p>

<h2>Tow boards are nothing like the guns under Greg Long at Mavericks</h2>

<p>Paddle big wave boards are built for getting <em>into</em> the wave. Long planshape, long fins, every gram of lift dedicated to catching a moving mountain under arm power. Those are the 10' pintails you see Greg Long and Grant Baker swing around at Cortes Bank and Mavs.</p>

<p>Tow boards solve the opposite problem. The ski catches you the wave. Your job is staying on the board through chop, bumps, and the kind of speed your spine wasn't built for.</p>

<p>So tow boards are short. Most sit between 5'8" and 6'8". They're heavy, often with brass weights or extra glass in the deck so they punch through chop instead of skipping off it. And they have foot straps, because at 50 mph a slip is a coffin.</p>

<p>The fins follow that same heavy-and-stable logic.</p>

<h2>Speed kills drag, not just surfers</h2>

<p>At paddle-in speeds, a wide-based fin gives you drive. It pushes water, and that translates into forward motion. Useful. Necessary.</p>

<p>At tow speeds, that same wide base is a parachute. Speed comes from the wave, not from your fins. Anything generating extra drag is robbing you of control on the face.</p>

<p>That's why tow fins almost universally have:</p>

<ul>
<li><strong>Smaller bases</strong> for less drag at sustained speed</li>
<li><strong>Stiffer materials</strong> so you don't get flex chatter at 40+ mph</li>
<li><strong>More rake</strong> for smoother, longer arcs through high-G turns</li>
<li><strong>Thicker foil profiles</strong> that favor stability over snap</li>
</ul>

<p>You'll still see thruster setups, quads, and the occasional wild bonzer or twin keel experiment at giant Jaws sessions. But the templates inside those clusters look nothing like what's on your daily driver. If you want a refresher on how the different <a href="/fin-setups">fin setups</a> compare in normal surf, that page covers it.</p>

<h2>The strap factor changes everything</h2>

<p>Foot straps do something weird to fin physics. When you can't shift your feet, you can't unweight the tail the way you'd flick out of a turn on a paddle board. Every input has to go through your knees and hips.</p>

<p>That means the fins have to be more forgiving on inputs you can't take back. Riding strapped is closer to snowboarding than to surfing in a lot of ways. The board has to want to track. The fins have to hold without you asking them to.</p>

<p>Which is why most tow templates lean toward stiffer flex patterns and slightly forward cant. You want a board that locks in and stays locked. Loose isn't a feature here.</p>

<h2>What pros actually run on tow days</h2>

<p>Tow fin setups vary by athlete and wave, but a few patterns repeat.</p>

<h3>Quads for Nazaré-style speed runs</h3>
<p>Lucas "Chumbo" Chianca and a lot of the Nazaré crew lean quad. Two sets of side fins, no center fin to bog through high-speed transitions. Speed and release. Quads in this configuration are usually shorter than what you'd run on a 5'10" fish, closer to H-series templates from FCS or smaller AM-style inserts from Futures.</p>

<h3>Thrusters with a tiny center fin</h3>
<p>Kai Lenny has been spotted running thruster setups on tow boards at Jaws, but with a noticeably small center fin. The center fin is there for stability through chop, not for pivot. Think of it like training wheels for high-speed straight running. The trailing fin is also typically softer in flex than the side fins so it absorbs micro-corrections instead of fighting them.</p>

<h3>Glass-on for the absolute biggest days</h3>
<p>Some of the heaviest tow guns, the 6'10" weighted weapons for 60-foot-plus days, still run glass-on fins. Old school. Locked in. You're not swapping fins on a board you might snap in the first 30 seconds anyway, so why bother with a removable system that adds two tabs of failure point.</p>

<h2>It's not just smaller, it's calibrated different</h2>

<p>A common misread: tow fins are just shrunken versions of your normal fins. Wrong.</p>

<p>A tow-specific template like the Futures Tow Quad or FCS H-series Tow has a foil profile designed for sustained high-speed water flow. Normal fins assume bursts of acceleration and deceleration. Tow fins assume the whole ride is one long screaming bottom turn followed by a few hopeful arcs at the top of the wave.</p>

<p>Different physics, different shape, different feel.</p>

<h2>Should you care if you're never towing into Pe'ahi?</h2>

<p>Probably not. The vast majority of surfers will never need a tow setup. If you're reading this from your couch in San Diego, your daily driver fins are doing a fine job and don't need tow-specific anything.</p>

<p>But there's a sneaky takeaway here for everyone else. The tow crew has been running smaller-base, higher-rake fins for stability at speed long before that combo became popular in normal performance shortboard templates. Watch what big wave guys ride, and the trends quietly flow back down to your local lineup three years later.</p>

<p>If you've ever wondered why your H4s feel locked in but loose at the same time, this is part of the answer. The DNA is partially borrowed from a 6'4" tow board ridden into a Cortes Bank bomb a decade ago. Same with the rake-heavy templates in the <a href="/all-about-fins">all about fins</a> breakdown.</p>

<h2>Key Takeaways</h2>
<ul>
<li>Tow boards solve a different problem than paddle big wave guns: control at speed, not catching the wave.</li>
<li>Tow fins lean smaller, stiffer, and higher-rake because drag becomes the enemy when the wave is doing the work.</li>
<li>Foot straps change the input game, so most tow templates favor hold over snap and stability over release.</li>
<li>Quads dominate at Nazaré, thrusters with small centers show up at Jaws, and glass-on setups still ride the absolute heaviest days.</li>
<li>Fin trends pioneered for tow surfing eventually show up in normal performance templates years later, so what looks niche today might be on your shortboard in 2028.</li>
</ul>

<p>We built a tool that walks you through fin selection for your actual board and the actual waves you surf, not the 80-foot bomb you'll never see. The <a href="/recommender">Fin Finder</a> handles the boring math so you can skip the guesswork.</p>"""

post = {
    "slug": slug,
    "title": "Tow-In Fins: Why Big Wave Tow Boards Don't Use Normal Setups",
    "excerpt": "Strapped tow boards at Nazaré and Jaws run tiny, stiff, high-rake fins that would feel wrong on any other wave. Here's why the physics demand it.",
    "content": content,
    "category": "guides",
    "author": "FinFinder Team",
    "date": "May 20, 2026",
    "date_published": "2026-05-20",
    "date_modified": "2026-05-20",
    "read_time": 6,
    "featured_image": "",
    "featured_image_alt": "A small surfer dropping into a giant wave at Nazare with the foamball chasing behind",
    "meta_description": "Why big wave tow boards run tiny, stiff fins with more rake than your shortboard. The physics of strapped surfing at Nazare, Jaws, and Cortes Bank.",
    "tags": ["tow surfing", "big wave fins", "nazare", "jaws", "fin templates", "fin setup", "advanced fins"],
    "primary_keyword": "tow-in fins",
    "secondary_keywords": ["tow surfing fins", "tow board fin setup", "big wave tow fins", "strapped surfboard fins"],
    "last_image_type": "ACTION_SHOT",
    "faqs": [
        {
            "question": "What's the difference between tow-in fins and regular big wave fins?",
            "answer": "Paddle big wave fins are tall and wide-based for lift and drive when you're trying to catch a moving mountain under arm power. Tow fins are shorter, stiffer, and have more rake because the ski gives you the wave, so drag becomes the enemy. The whole design goal flips from generating speed to controlling speed."
        },
        {
            "question": "Can I use regular thruster fins on a tow board?",
            "answer": "You can, but you shouldn't. Standard performance thrusters have wider bases that create drag at sustained tow speeds, and the foil profile assumes bursts of acceleration that don't exist when a ski is doing the towing. Brands like Futures and FCS sell tow-specific templates because the physics genuinely differ."
        },
        {
            "question": "Why are tow boards so short if the waves are so big?",
            "answer": "Because you're not paddling. Length helps you catch waves under arm power, and tow boards skip that entire step. Shorter boards are more maneuverable on the face, easier to control at speed, and they pair better with the foot strap setup. Most tow boards sit between 5'8\" and 6'8\" even on 60-foot days."
        },
        {
            "question": "Do tow surfers run thrusters or quads?",
            "answer": "Both, depending on the wave. The Nazare crew including Lucas Chianca tend toward quads because the ride is mostly a long high-speed line and the quad releases easier. At Jaws, Kai Lenny and others have been seen running thrusters with a tiny center fin for chop stability. There's no universal answer."
        },
        {
            "question": "Are glass-on fins still used in tow surfing?",
            "answer": "Yes, especially on the heaviest weighted tow guns for 60-foot-plus days. Glass-on fins lock in completely and add fewer failure points than a removable system, which matters when one bad wipeout can snap the board in half. Most pros keep at least one glass-on tow weapon for the days that really matter."
        }
    ]
}

with open(DATA, "r", encoding="utf-8") as f:
    data = json.load(f)

if any(p["slug"] == slug for p in data["posts"]):
    print(f"Post {slug} already exists, aborting.")
    raise SystemExit(1)

data["posts"].append(post)

with open(DATA, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Added post: {slug}")
print(f"Total posts: {len(data['posts'])}")

# Basic word count and banned word scan
import re
text = re.sub(r"<[^>]+>", " ", content)
words = text.split()
print(f"Word count: {len(words)}")

banned = ["delve", "landscape", "leverage", "unleash", "elevate", "harness",
          "comprehensive", "robust", "streamline", "cutting-edge", "revolutionize",
          "game-changer", "dive in", "in today's fast-paced", "it's important to note",
          "in conclusion", "without further ado", "unlock your potential",
          "we've got you covered", "here's what nobody tells you", "the real problem",
          "stop guessing", "navigate"]
low = text.lower()
hits = [b for b in banned if b in low]
print(f"Banned word hits: {hits if hits else 'none'}")

if "—" in content or "—" in content:
    print("WARNING: em dash found")
else:
    print("Em dash check: clean")
