import json, io

path = "blog_posts.json"
with io.open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

content = """<p>Paddle out on a truly finless board sometime. A flat plank with nothing under the tail. You'll catch the wave fine and drop in fine, and then the second you lean into a turn the back of the board lets go and slides out from under you like a banana peel on a tile floor. The old Waikiki crew had a name for that feeling. They called it "sliding ass."</p>

<p>For most of surfing's history, that was just surfing. Riders angled across a wave by dragging a back foot, throwing their whole body into it, and hoping. Then in 1935 a stubborn Wisconsin transplant named Tom Blake bolted a chunk of scrap metal to his board and quietly ended the sliding-ass era for good.</p>

<p>So who invented the surfboard fin? Tom Blake. One guy, one scavenged speedboat keel, one afternoon at Waikiki. Here's how it actually happened, and why it took the rest of surfing a full decade to admit he was right.</p>

<h2>Who invented the surfboard fin?</h2>

<p>Tom Blake invented the surfboard fin in 1935 at Waikiki, Hawaii. He pulled a metal keel off an abandoned speedboat in Honolulu Harbor, roughly 12 inches long and 4 inches deep, and fixed it to the tail of a 14-foot hollow board he had built himself.</p>

<p>That is the whole origin story in one sentence. A junked boat part, a hand-shaped board, and a hunch. The keel was so sharp that Blake nailed a wooden sheath along the leading edge so it wouldn't open up anyone's shin. Crude doesn't begin to cover it.</p>

<p>It worked on the first wave. "Never before had I experienced such control and stability," Blake said later. "It steered easy because the tail held steady when you put the pressure on the front." He paddled in knowing he'd changed the thing permanently.</p>

<h2>What problem was the fin actually solving?</h2>

<p>Before the fin, a surfboard was basically a planing surface with no anchor. It would skip across the water happily as long as you went more or less straight. Ask it to hold a line at an angle and the tail would skate sideways, breaking free of the wave face entirely.</p>

<p>That is the sliding-ass problem, and it capped how hard anyone could turn. You could not commit to a rail because the board would not let you. Every meaningful direction change was a negotiation you usually lost.</p>

<p>The fin changed the physics. Drop a vertical surface into the water behind the rider and you give the board something to pivot against. Set your weight forward and the tail digs in instead of washing out. That bite is the same sensation you feel today when you bury a rail in a clean bottom turn and the board grips with a quiet, confident hold rather than chattering loose. Blake found that feeling first, with a piece of someone's wrecked speedboat.</p>

<p>If you want the modern version of why this works, we break the hydrodynamics down in <a href="/finsights/how-surfboard-fins-work-lift-physics">how surfboard fins actually work</a>. Blake had none of that language. He just knew his board suddenly did what he told it to.</p>

<h2>Who was Tom Blake?</h2>

<p>Blake wasn't a born waterman. He was a kid from Wisconsin, nowhere near an ocean, who reportedly got hooked after a chance meeting with Duke Kahanamoku in a Detroit movie theater lobby in 1920. He moved west, taught himself to swim and surf, and turned into one of the most relentless tinkerers the sport has ever produced.</p>

<p>His bigger early invention came in 1931: the hollow board. By drilling out a solid redwood plank and sealing it, he cut board weight roughly in half and made the sport accessible to people who couldn't haul a 100-pound log to the beach. That board fueled the first real surfing boom.</p>

<p>The fin came four years later and turned out to be the one that stuck. Blake's hollow boards were eventually replaced by foam and fiberglass. The fin never left. He's in the National Inventors Hall of Fame, which is a sentence almost no other surfer gets to claim.</p>

<h2>Why surfers ignored the fin for ten years</h2>

<p>Here's the part that always surprises people. The best idea in surfboard design sat there, proven, for the better part of a decade while almost nobody copied it.</p>

<p>The fin didn't catch on in Hawaii for about five years, and didn't become standard until around 1940. Plenty of Hawaiian surfing stars were still riding finless boards into the late 1940s, more than ten years after Blake's afternoon at Waikiki. Surfers are traditionalists, and the old guard had spent their whole lives mastering the foot-drag method. They weren't eager to be told a scrap of metal did it better.</p>

<p>It took a new generation, and a few obsessive shapers, to push the fin from novelty to non-negotiable.</p>

<h2>From one junkyard keel to four-fin quads</h2>

<p>Once the fin stuck, the whole sport sped up. Everything in your fin box today is a descendant of that 1935 keel.</p>

<h3>Bob Simmons and the modern keel</h3>

<p>In the 1940s, hydrodynamics-obsessed shaper Bob Simmons reworked Blake's clunky keel into something more raked and refined, a shape still echoed in fish keels today. Simmons is also widely credited with building the first twin-fin surfboard, which is wild for a guy working out of a garage with a math background and a chip on his shoulder.</p>

<h3>George Greenough and flex</h3>

<p>In the 1960s, Californian eccentric George Greenough ditched the big stiff keel for a narrow, raked fin modeled on a dolphin's dorsal, with flex built into the tip. That flex let the tail load up and release through a turn, and it helped kick off the shortboard revolution. We dig into his template in our piece on the <a href="/finsights/greenough-4a-fin-template-shortboard-revolution">Greenough 4A</a>.</p>

<h3>Mark Richards and the twin</h3>

<p>Single fins and keel twins ran the show into the 1970s, until Australian Mark Richards modernized the twin-fin and won four straight world titles on it between 1979 and 1982. The retro twins clogging your local lineup right now owe him directly. More on that in <a href="/finsights/mark-richards-twin-fin-four-world-titles">MR and the twin-fin</a>.</p>

<h3>Simon Anderson and the thruster</h3>

<p>Then in 1981, frustrated Sydney surfer Simon Anderson added a third fin and changed everything again. He won Bells, the Coke Surfabout, and the Pipeline Masters that year on his three-fin "Thruster," and the design still sits under the majority of boards sold today. The full story is in our <a href="/finsights/simon-anderson-thruster-history-invention">Simon Anderson thruster</a> breakdown.</p>

<p>Every one of those leaps started with the same realization Blake had on a single wave. Put a surface under the tail and the board will finally listen. If you want the wider map of how single fins, twins, quads, and thrusters compare, the <a href="/all-about-fins">all about fins</a> guide lays it out, and the <a href="/fin-setups">fin setups</a> page covers which configuration fits which surfer.</p>

<h2>Key Takeaways</h2>

<ul>
<li>Tom Blake invented the surfboard fin in 1935 at Waikiki using a 12-inch metal keel salvaged from a wrecked speedboat.</li>
<li>The fin solved "sliding ass," the tail-slide that made hard turning nearly impossible on finless boards.</li>
<li>Surfers were slow to adopt it. The fin didn't become standard until around 1940, and some riders stayed finless into the late 1940s.</li>
<li>Bob Simmons, George Greenough, Mark Richards, and Simon Anderson each built on Blake's idea to give us keels, flex fins, twins, and the thruster.</li>
<li>Every fin in your quiver, from a single to a five-fin box, traces back to one scavenged boat keel.</li>
</ul>

<p>Blake had exactly one fin option: whatever he could pry off a junked hull. You have hundreds, which is its own kind of problem. If you'd rather not test every template the way he did, tell our <a href="/recommender">fin recommender</a> what you ride and let it point you to the setup that fits your board and your waves. Ninety years of evolution, sorted in about a minute.</p>"""

post = {
    "slug": "who-invented-the-surfboard-fin-tom-blake",
    "title": "Who Invented the Surfboard Fin? Tom Blake and the 1935 Junkyard Keel",
    "excerpt": "Who invented the surfboard fin? Tom Blake, in 1935, with a keel he ripped off a junked speedboat at Waikiki. The story of the part that fixed surfing.",
    "content": content,
    "category": "guides",
    "author": "FinFinder Team",
    "date": "Jun 16, 2026",
    "date_published": "2026-06-16",
    "date_modified": "2026-06-16",
    "read_time": 6,
    "featured_image": "",
    "featured_image_alt": "A single vintage surfboard keel fin resting on weathered wood, evoking Tom Blake's 1935 speedboat-keel invention",
    "meta_description": "Who invented the surfboard fin? Tom Blake, in 1935, with a keel ripped off a junked speedboat at Waikiki. The story of the part that fixed surfing.",
    "tags": ["surf history", "surfboard fins", "tom blake", "fin design", "single fin", "surfing origins"],
    "primary_keyword": "who invented the surfboard fin",
    "secondary_keywords": ["tom blake surfboard fin", "history of the surfboard fin", "first surfboard fin", "when was the surfboard fin invented", "skeg invention"],
    "faqs": [
        {"question": "Who invented the surfboard fin?", "answer": "Tom Blake invented the surfboard fin in 1935 at Waikiki, Hawaii. He attached a metal keel salvaged from an abandoned speedboat to the tail of a hollow surfboard he had built himself."},
        {"question": "What year was the surfboard fin invented?", "answer": "1935. Tom Blake fixed his scavenged speedboat keel to a board that year, though the fin did not become standard equipment until around 1940."},
        {"question": "What was the first surfboard fin made of?", "answer": "Metal. The first fin was a roughly 12-inch-long, 4-inch-deep keel pulled off a wrecked speedboat. It was so sharp that Blake added a wooden sheath along the edge for safety."},
        {"question": "Did surfers use fins before Tom Blake?", "answer": "No. Before 1935, surfboards had no fin. Riders held a line by dragging a foot and shifting their weight, which caused the tail to slide out, a problem the Waikiki crew called \"sliding ass.\""},
        {"question": "How did the fin lead to the thruster?", "answer": "Blake's single keel inspired decades of refinement. Bob Simmons modernized the keel and built the first twin, George Greenough added flex, Mark Richards proved the twin, and Simon Anderson added a third fin in 1981 to create the thruster."}
    ],
    "last_image_type": "PENDING_FINS_ON_WOOD"
}

data["posts"].append(post)

with io.open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# validate
with io.open(path, "r", encoding="utf-8") as f:
    d2 = json.load(f)
print("OK posts:", len(d2["posts"]))
print("slug:", d2["posts"][-1]["slug"])

import re
text = re.sub("<[^>]+>", " ", content)
words = len(text.split())
print("word count:", words)

banned = ["delve","landscape","leverage","unleash","elevate","harness","comprehensive","robust","streamline","cutting-edge","revolutionize","game-changer","dive in","navigate"]
low = content.lower()
hits = [b for b in banned if b in low]
print("banned hits:", hits)
print("em dash present:", "—" in content)
print("meta len:", len(post["meta_description"]))
