# -*- coding: utf-8 -*-
import json, io

PATH = "blog_posts.json"

content = """
<p>You're standing in the surf shop holding two FCS Performer fins that look identical. Same template, same size, same little letter printed on the side. One's forty bucks, the other's a hundred and twenty. The only thing separating them is two letters on the box, PG and PC, and the kid behind the counter just shrugged when you asked.</p>

<p>Those letters aren't decoration. They're construction. FCS sells the exact same fin shape in something like eight different materials, and the material decides how the fin flexes, how much it weighs, how long it survives, and how much of your money vanishes. Pick wrong and you either overpay for stiffness you can't use yet, or you buy a noodle that folds the second you start surfing hard.</p>

<p>So let's decode the alphabet soup. By the end you'll know which code on the box matches the surfer you actually are.</p>

<h2>The Letters Are Materials, Not Models</h2>

<p>Here's the part that trips everyone up. The fin's name, Performer or Reactor or Carver, is the template, the outline and rake and area that decide how the fin turns. The letters tacked on after it, PC, PG, Neo Glass, are the construction. Same shape, different recipe.</p>

<p>If template versus construction is fuzzy for you, our breakdown of <a href="/finsights/fin-templates-decoded-am-h4-performer-reactor">why the AM, H4, and Performer all feel different</a> sorts the shapes out. This post is about everything that happens after you've picked the shape.</p>

<p>Construction matters because flex is half of how a fin feels. A stiff fin drives and holds, a soft one bends and forgives. The same Performer template can do either, depending on what it's built from. We dug into the <a href="/finsights/carbon-vs-fiberglass-vs-plastic-fins">carbon versus fiberglass versus plastic question</a> already, but FCS layers its own naming system on top, and that's where people get lost.</p>

<h2>The Budget Tier: Glass Flex and Soft Flex</h2>

<h3>Glass Flex (GF)</h3>

<p>This is the construction that comes free in a lot of starter packs, and it's the one most surfers outgrow without realizing the fin was holding them back. Glass Flex is injection molded to mimic fiberglass, with nice tip flex and barely any base flex. FCS aims it at novice surfers, and for that it's honestly fine.</p>

<p>The problem shows up the day you start pushing. You set your rail hard on a head-high wall and the fin keeps bending after you wanted it to grip. The turn arrives late and soft, a half-beat behind your feet. It feels like steering a car with loose tie rods, great until you ask it for something real.</p>

<h3>Soft Flex</h3>

<p>Pure flexible urethane, built for softboards and total beginners. It exists so a fin to the shin at Tourmaline doesn't put you in urgent care. Nobody progressing past whitewater is shopping in this tier, and that's the point of it. Safe over fast.</p>

<h2>The Sweet Spot: Neo Glass and Performance Glass</h2>

<h3>Neo Glass</h3>

<p>If you read one paragraph here, read this one. Neo Glass is the best value FCS makes, full stop. It's precision molded from long-strand fiberglass and a marine-grade polymer, so you get genuinely high fiberglass content and an active flex pattern for around half the price of the premium stuff.</p>

<p>FCS markets it at novice and intermediate surfers, which undersells it. Plenty of solid surfers ride Neo Glass and never feel cheated. The flex is lively, the foils are dialed, and the fin holds together. If you're not sure where you land on the skill ladder, this is the safe money.</p>

<h3>Performance Glass (PG)</h3>

<p>PG is the old-school answer. Machine cut from layers of solid fiberglass, stiff through the base, with a subtle responsive tip. It's the construction that flexes exactly like the glass-on fins your dad's longboard had, which is why pros trust it when the wave is throwing real force at the fin.</p>

<p>Set a bottom turn on PG and the base doesn't budge. The fin grips and the board rotates around it like the rail is locked in. That stiffness is the whole appeal, and also the catch. If you're not surfing hard enough to load the fin, PG feels like a plank that rewards power and punishes hesitation.</p>

<h2>The Performance Tier: Performance Core and Its Carbon Cousins</h2>

<h3>Performance Core (PC)</h3>

<p>This is the most popular FCS construction for a reason. PC fins are built with a resin transfer molding process that drops weight while keeping a flex pattern that runs progressively from the base out to the tip. The base holds, the tip gives, and the handoff between them is smooth.</p>

<p>The feel is forgiving in the best way. You can be slightly late on a turn and the fin covers for you, flexing and then snapping back to push you down the line. Mick Fanning rode PC his entire career and won three world titles being smooth, not stiff. That tells you who it's for, most surfers on most days.</p>

<h3>Performance Core Carbon (PCC)</h3>

<p>Take PC, run carbon frames through it, swap the base inserts for Innegra, and you get PCC. FCS rebuilt this line with what they call a Linear Flex pattern, putting stiffness and give exactly where the engineering wants them. The result is a fin with immediate response and a sharper recoil.</p>

<p>You feel it off the top. You finish a turn, the fin loads, and it spits you out of the snap with a little spring you didn't ask for and definitely keep. It's a fin for advanced surfers who finish turns hard and want the board to react now, not a beat later. Overkill for most weekend surfers, glorious for the ones who earn it.</p>

<h3>AirCore and Neo Carbon</h3>

<p>AirCore is the weight trick. FCS presses a polyurethane foam core that mimics the fin's foil, which cuts the fiberglass needed and lets them tune the flex however they want. The fin gets lighter without going dead. Gabriel Medina, a surfer who lives in the air, rides PC AirCore for exactly that reason, less swing weight and faster reaction.</p>

<p>Neo Carbon is the small-wave weapon. Molded from long-strand carbon and high-grade European resin, it's feather light with a firm, spring-loaded flex. In gutless surf it does this whipping thing, loading on one turn and flinging you into the next with speed you didn't generate yourself. On a mushy summer day at Doheny it feels borderline like cheating.</p>

<h2>So Which One Should You Buy</h2>

<p>Real talk. Most surfers reading this should be on Neo Glass or Performance Core, and the choice between them is money versus weight. Neo Glass if you want the most performance per dollar. PC if you'll pay extra for a lighter, livelier fin that forgives a late turn.</p>

<p>Buy PG or PCC only if you genuinely surf hard, finish turns with power, and load the fin enough to feel the stiffness work for you. If you can't honestly say that yet, the premium construction is wasted, and a softer fin will teach you more. Skip Glass Flex the moment you've left whitewater behind.</p>

<p>Construction is only half the equation, though. The wrong template in the perfect material still surfs wrong, and fin area has to match your weight and your board before any of this matters. That's the math our <a href="/recommender">fin recommender</a> runs in about a minute, and it'll tell you the shape and size before you ever stress about which letters to chase. Pair it with the <a href="/all-about-fins">all about fins guide</a> if you want the full picture.</p>

<h2>Key Takeaways</h2>

<ul>
<li>The letters after a fin's name (PC, PG, Neo Glass) are construction, not template. Same shape, different flex, weight, and price.</li>
<li>Neo Glass is the best value FCS makes. High fiberglass content and lively flex for roughly half the premium price.</li>
<li>Performance Core (PC) is the smart default for most surfers. Light, forgiving, and smooth, the construction Mick Fanning won titles on.</li>
<li>Performance Glass (PG) and PC Carbon (PCC) only pay off if you surf hard enough to load a stiff fin. Otherwise they feel like planks.</li>
<li>Neo Carbon and AirCore are about weight. Featherlight constructions that snap you between turns in weak surf, which is why air surfers like Gabriel Medina ride them.</li>
</ul>
"""

post = {
    "slug": "fcs-fin-materials-pc-pg-neo-glass-explained",
    "title": "FCS Fin Materials Explained: Why PC, PG, and Neo Glass Feel Nothing Alike",
    "excerpt": "Same fin shape, eight different prices. Those letters on the FCS box are construction, not marketing. Here's what PC, PG, Neo Glass, and Air Core actually change.",
    "content": content.strip(),
    "category": "guides",
    "author": "FinFinder Team",
    "date": "Jun 07, 2026",
    "date_published": "2026-06-07",
    "date_modified": "2026-06-07",
    "read_time": 7,
    "featured_image": "",
    "featured_image_alt": "FCS surfboard fins in different constructions laid out on weathered wood, showing fiberglass and carbon material finishes",
    "meta_description": "Same FCS fin shape, eight different prices. The letters on the box are construction, not marketing. Here's what PC, PG, and Neo Glass really change.",
    "tags": ["FCS fins", "fin materials", "fin construction", "Performance Core", "Neo Glass", "carbon fins", "fiberglass fins", "fin flex"],
    "primary_keyword": "FCS fin materials",
    "secondary_keywords": ["FCS fin construction", "Performance Core vs Performance Glass", "Neo Glass fins", "PC vs PG fins", "FCS fin types explained"],
    "faqs": [
        {
            "question": "What does PC and PG mean on FCS fins?",
            "answer": "PC stands for Performance Core and PG stands for Performance Glass. Both are constructions, not fin shapes. PG is machine-cut solid fiberglass with a stiff base, favored by surfers who push hard. PC is resin transfer molded, lighter and more forgiving, with a progressive flex from base to tip that suits most surfers."
        },
        {
            "question": "Which FCS fin construction is best for intermediate surfers?",
            "answer": "Neo Glass or Performance Core (PC). Neo Glass gives high fiberglass content and lively flex for about half the price of premium constructions, making it the best value. PC costs more but is lighter and forgives a late turn, which helps surfers who are still dialing in their timing."
        },
        {
            "question": "Are carbon FCS fins like PC Carbon or Neo Carbon worth it?",
            "answer": "Only if you surf hard enough to load them. PC Carbon (PCC) adds carbon frames for immediate response and sharp recoil off the top, built for advanced surfers who finish turns with power. Neo Carbon is super light with a spring-loaded flex that whips you between turns in weak surf. For most weekend surfers, both are more fin than the surfing demands."
        },
        {
            "question": "Is Glass Flex good for beginners?",
            "answer": "It's fine while you're learning, but you'll outgrow it fast. Glass Flex is injection molded with lots of tip flex and little base flex, so it feels forgiving in whitewater. The moment you start setting your rail on real waves, the fin keeps bending when you want it to grip, and turns arrive late."
        },
        {
            "question": "Does FCS fin material change how the fin feels more than the shape?",
            "answer": "They matter together, but you should pick the shape first. The template decides rake, area, and how the fin turns. The construction decides flex, weight, and price. The same Performer template feels stiff and drivey in Performance Glass and lighter and livelier in Performance Core, so material is how you fine-tune a shape you've already chosen."
        }
    ],
    "last_image_type": "FINS_ON_WOOD"
}

d = json.load(io.open(PATH, encoding="utf-8"))
slugs = {p["slug"] for p in d["posts"]}
assert post["slug"] not in slugs, "duplicate slug"
d["posts"].append(post)
with io.open(PATH, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

# validate round-trip
d2 = json.load(io.open(PATH, encoding="utf-8"))
import re
words = len(re.sub(r"<[^>]+>", " ", post["content"]).split())
print("OK posts:", len(d2["posts"]))
print("word_count:", words)
print("meta_len:", len(post["meta_description"]))
print("title_len:", len(post["title"]))
