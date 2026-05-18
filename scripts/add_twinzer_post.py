import json, io

POST = {
    "slug": "twinzer-fin-setup-canards-explained",
    "title": "The Twinzer Fin Setup: Two Mains, Two Canards, and the Cult That Won a World Title",
    "excerpt": "It won a world title in 1989, then got forgotten for 25 years. The twinzer is a twin fin with two tiny helpers up front, and it might be the most underrated setup in surfing.",
    "content": "",  # filled below
    "category": "guides",
    "author": "FinFinder Team",
    "date": "May 18, 2026",
    "date_published": "2026-05-18",
    "date_modified": "2026-05-18",
    "read_time": 6,
    "featured_image": "",
    "featured_image_alt": "A twinzer fin setup laid out on a weathered wood deck, two larger twin fins beside two small canard fins in warm natural light.",
    "meta_description": "The twinzer fin setup won a 1989 world title, then vanished for 25 years. Two mains, two tiny canards, and more drive than a twin should have.",
    "tags": ["twinzer", "twin fins", "fin setups", "canard fins", "retro surfboards", "Wil Jobson", "surfboard design"],
    "primary_keyword": "twinzer fin setup",
    "secondary_keywords": ["twinzer fins", "what is a twinzer", "twinzer vs twin fin", "canard fins", "twinzer surfboard"],
    "faqs": [
        {
            "question": "What is a twinzer fin setup?",
            "answer": "A twinzer is a twin fin with two small extra fins, called canards, mounted just forward and toward the rail of each main fin. Four fins total, but it is not a quad. The canard cleans up the water flow ahead of the main fin so the main fin can be smaller and still drive."
        },
        {
            "question": "Is a twinzer better than a twin fin?",
            "answer": "For surfers who love twins but want more hold in steeper waves, yes. The twinzer keeps most of a twin's free speed and glide while killing the squirrelly, slide-out feeling twins get when the wave stands up. If you never push your twin hard, a plain twin is simpler and fine."
        },
        {
            "question": "What size canard fins do I need for a twinzer?",
            "answer": "Canards are small flow directors, not side fins. A typical twinzer canard runs roughly a 2.77 inch base, around 3.16 inch height, and about 7 square inches of area with a flat foil. Match the canard to the main fin and run more cant in the canard than the rear fin."
        },
        {
            "question": "Can you turn any twin fin board into a twinzer?",
            "answer": "No. The board has to be built with the canard boxes in the correct forward, toward-the-rail position. Adding canards to a board that was never shaped for the twinzer usually just adds drag instead of drive."
        },
        {
            "question": "Twinzer vs quad, what is the difference?",
            "answer": "A quad has four full-size fins in two clusters and surfs with drive but can feel tracky and stiff in tight turns. A twinzer has two main fins plus two tiny canards, so it surfs looser and freer like a twin while still holding a line. Different geometry, different feel."
        }
    ],
    "last_image_type": "FINS_ON_WOOD"
}

CONTENT = """
<p>You're standing in the used rack at a San Diego shop and you pull out a board that looks wrong. Four boxes, but it's not a quad. The back two fins are normal size. The front two are tiny, set way up toward the rail, like someone glued training fins onto a twinnie.</p>

<p>You ask the guy behind the counter what it is. He grins and says one word: twinzer.</p>

<p>Most surfers have never ridden one. Plenty have never seen one. That's a shame, because the twinzer fin setup is one of the few designs that won a world title and then got shoved in a closet for 25 years.</p>

<h2>What a twinzer fin setup is</h2>

<p>A twinzer is a twin fin with two small helper fins, called canards, set just forward and out toward the rail of each main fin. Four fins total. It is not a quad. The geometry and the job each fin does are completely different, which is its own rabbit hole if you want the full <a href="/fin-setups">fin setups</a> breakdown.</p>

<p>Here's the trick. The little canard sits in front of the main fin and punches a hole in the water before the big fin ever gets there. The high pressure side of the canard shoves clean, organized flow onto the low pressure side of the main fin. The main fin suddenly does more work for less drag.</p>

<p>So you shrink the main fin. You stand it up more upright and pivoty. You get twin fin speed and twin fin freedom, but the skatey, terminal looseness that makes twins scary in steep sections mostly disappears.</p>

<h2>The setup that won a title, then vanished</h2>

<p>Wil Jobson dreamed this up shaping in Southern California in the late 80s. In 1988 Martin Potter got on one. In 1989 Pottz won six events out of 25 and the world title with a twinzer in his quiver.</p>

<p>That's not a fluke. That's a design proving itself at the top of the sport during the same wild Christian Fletcher era when getting airborne was still considered cheating.</p>

<p>Jobson drove to San Diego and showed it to Rusty Preisendorfer. Rusty was, by his own account, blown away by how different it felt from a normal twin. He built quite a few and paid Jobson a royalty, which basically never happens in surfboard design.</p>

<p>Then the late 90s hit. The fish came roaring back, quads got popular, and the twinzer quietly got forgotten. For two decades it survived almost entirely because a handful of San Diego shapers refused to let it die.</p>

<h2>What it feels like under your feet</h2>

<p>A good twinzer is a strange, addictive sensation the first time. You take off, do one pump, and the board is just gone. That's the twin part, the free speed, the sense that the thing wants to run before you've asked it to.</p>

<p>Then you set a hard bottom turn into a steep section, the exact place a regular twin starts to chatter and slide and make you nervous. It doesn't. The canards bite, the main fins hold, and the board drives off the bottom like it has a center fin it doesn't have. You come off the top and it releases clean, no stickiness, no thruster drag yanking you back.</p>

<p>Loose but locked. That's the whole pitch. It surfs looser than a quad and holds better than a twin, at the same time, which sounds like marketing copy until you ride one.</p>

<h2>Twinzer versus twin versus quad</h2>

<p>People lump all the multi-fin retro setups together. They shouldn't. Each one trades away something different.</p>

<h3>Twin</h3>
<p>Maximum speed and glide, especially in weak surf. The tradeoff is hold. Push a twin hard off the bottom in an overhead wave and the tail can let go without warning. Fun until it isn't.</p>
<p>The <a href="/finsights/twin-fins-back-retro-setup">twin fin</a> is the foundation the twinzer is built on top of.</p>

<h3>Quad</h3>
<p>Speed plus drive down the line, because the rear fins sit close to the stringer and give you something to push against. The tradeoff is that quads can feel tracky and stiff through tight turns, like the board wants to go straight when you want to pivot. There's a full <a href="/finsights/quad-vs-thruster-when-speed-matters">quad versus thruster</a> argument worth reading if that's your debate.</p>

<h3>Twinzer</h3>
<p>It splits the difference in a way the other two can't. You keep most of the twin's free speed because the main fins are small. You keep most of the quad's hold because the canard organizes the flow and lets the main fin grip.</p>
<p>What you give up is simplicity. More variables, and a badly tuned twinzer is worse than a good twin.</p>

<h2>Canard size, placement, and cant</h2>

<p>The canards are small. For reference, a Stu Kenson twinzer canard runs about a 2.77 inch base, 3.16 inch height, and roughly 7 square inches of area with a flat foil. The Mandala Acme canard is in the same range with a 2 and 7/8 inch base.</p>
<p>These aren't side fins. They're flow directors.</p>

<p>Placement is everything, and this is where the twinzer humbles people. The canards sit further forward and closer to the rail than a normal front fin. Jobson's original spacing off the rail and between the fins reportedly worked out to golden ratio proportions, which is either profound or a great story, depending on how many you've had at the Boardroom Show.</p>

<p>Cant matters too. Canards usually run more cant than the rear fins. <a href="/finsights/fin-cant-toe-in-angles-explained">Cant and toe-in</a> are the angles most surfers ignore, and on a twinzer they decide whether the thing sings or fights you. True Ames sells canards in 0, 4, and 9 degree options, with a simple rule: if your canard boxes are 0 degree, run the 9 degree fin; if the boxes are already 9 degree, run the 0 degree fin.</p>

<p>One hard truth. You cannot turn any twin into a twinzer by buying canards. The board has to be built with the canard boxes in the right spot. Glue-on placement on a board that was never designed for it usually just buys you drag and disappointment.</p>

<h2>Should you ride one?</h2>

<p>Straight answer. If you already love twin fins and your only complaint is that they get squirrelly when the wave stands up, the twinzer is the fix you've been after. It keeps the glide and removes most of the fear.</p>

<p>If you're a committed thruster surfer who likes the predictable, slightly stiff feel of three fins, this isn't your board. You'll find it loose and weird and you'll be back on three fins within two waves. That's fine. Different tools for different surfers.</p>

<p>And if you're newer and still figuring out what a fin even does, learn the twin first. The twinzer is a refinement of a twin, not a beginner setup. It rewards surfers who already understand what their <a href="/finsights/trailer-fins-explained">extra little fins</a> are supposed to be doing back there.</p>

<p>The good news is you can finally buy one without commissioning a custom from a guy in a Leucadia garage. Stu Kenson, the twinzer's most stubborn believer, has done it with Firewire. Manuel Caro keeps building them at Mandala. Album's Twinzman put the design in front of a new audience, with shaper Matt Parker pointing out that the canards clear turbulence so the big fin can drive on rail clean.</p>

<p>The 2024 Boardroom Show in Del Mar made Jobson's design the theme of its Best in Show event. Stab even ran a piece asking whether you can hard launch a twinzer in 2025. The answer, for the record, is yes.</p>

<h2>Key Takeaways</h2>
<ul>
<li>A twinzer is a twin fin plus two small canards set forward and toward the rail. It's not a quad and doesn't surf like one.</li>
<li>The canard feeds clean water to the main fin, so you can shrink the main fin for twin speed without twin-fin slip.</li>
<li>Wil Jobson invented it, Martin Potter won the 1989 world title with one, and then it got forgotten for two decades.</li>
<li>Placement and cant make or break it. You can't convert a regular twin by gluing on canards.</li>
<li>It's the right call for twin-fin lovers who want more hold, and the wrong call for happy thruster surfers.</li>
</ul>

<p>If you're not sure whether your board can even take a twinzer, or whether you'd be happier on a clean twin or a quad, that's a 60 second question, not a 60 day experiment. Tell our <a href="/recommender">fin recommender</a> what you ride and how you surf, and it'll point you at the setup that fits before you spend money finding out the hard way.</p>
""".strip()

POST["content"] = CONTENT

with io.open("blog_posts.json", "r", encoding="utf-8") as f:
    data = json.load(f)

slugs = {p["slug"] for p in data["posts"]}
if POST["slug"] in slugs:
    raise SystemExit("Duplicate slug, aborting: " + POST["slug"])

data["posts"].append(POST)

with io.open("blog_posts.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

# Validate round-trip
with io.open("blog_posts.json", "r", encoding="utf-8") as f:
    reloaded = json.load(f)

assert reloaded["posts"][-1]["slug"] == POST["slug"]
wc = len(__import__("re").sub("<[^>]+>", " ", CONTENT).split())
print("OK. posts now:", len(reloaded["posts"]))
print("word count (approx):", wc)
print("meta_description len:", len(POST["meta_description"]))
print("em dash present:", "—" in CONTENT)
print("h1 present:", "<h1" in CONTENT.lower())
