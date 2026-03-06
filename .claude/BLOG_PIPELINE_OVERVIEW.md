# /project:blog auto - Complete Pipeline Reference

Full walkthrough of every phase, step, tool, skill, and file involved when running `/project:blog auto`.

---

## PHASE 1: TOPIC SELECTION & RESEARCH

### Step 1: Pick a Topic
- **What:** If `$ARGUMENTS` is "auto" or empty, read `.claude/topics.md` and pick the first unchecked `[ ]` item. Mark it `[~]` (in progress).
- **Tools:** `Read` tool, `Edit` tool
- **Files read:** `.claude/topics.md`
- **Files modified:** `.claude/topics.md` (status changes from `[ ]` to `[~]`)

### Step 2: Research the Topic
- **What:** Run 3-5 web searches covering technical, cultural, competitive, product, and conditions angles. Collect real names, stats, quotes, and product details. No generic filler.
- **Tools:** `WebSearch` (3-5 calls in parallel)
- **Files modified:** None (research is held in context)

### Step 3: Read Reference Files
- **What:** Load all voice, style, and SEO rules into context.
- **Tools:** `Read` tool (3 calls in parallel)
- **Files read:**
  - `~/.claude/skills/voiceprint/voice-profile.md` (tone, banned words, sentence architecture)
  - `BLOG_STYLE_GUIDE.md` (structure, formatting, CTA rules)
  - `SEO_GUIDELINES.md` (keywords, meta, GEO optimization)

### Step 4: Check Existing Posts
- **What:** Read `blog_posts.json` to check for duplicate topics, match the JSON structure of existing posts, and catalog existing CTA phrasing so we don't repeat it.
- **Tools:** `Read` tool, `Grep` tool
- **Files read:** `blog_posts.json`

---

## PHASE 2: WRITE THE POST

### Step 5: Classify the Post Type
- **What:** Determine category and target word count:
  - **Fin-specific** (guides, reviews, comparisons, sizing, setup): category `"guides"`, `"tips"`, or `"reviews"`. Target **1,200-1,800 words**.
  - **Surf news** (WSL, Olympics, industry, culture, viral clips): category `"news"`. Target **600-1,000 words**.
- **Tools:** None (classification decision)
- **Files modified:** None

### Step 6: Write the Post Content
- **What:** Write full HTML content following all rules:
  - Stab Magazine editorial voice (irreverent, honest, sharp)
  - Correct structure (scenario opening for fin posts, news hook for news posts)
  - 2+ internal links to cornerstone pages (`/recommender`, `/all-about-fins`, `/fin-setups`, `/fin-sizing-guide`, `/longboard-fins`)
  - 3-5 FAQs in the `faqs` array
  - No em dashes, no banned words, no paragraphs over 4 sentences
  - Contractions throughout
  - 2+ sensory descriptions (fin posts)
  - 1+ specific cultural reference (named surfer, break, or contest)
  - CTA to `/recommender` woven naturally into closing (skip if forced)
- **Tools:** None (writing in context)
- **Files modified:** None yet (post is assembled in memory)

### Step 7: Set All Required JSON Fields
- **What:** Build the complete post object with every required field:
  - `slug` - URL-friendly identifier
  - `title` - Post title (primary keyword in first 60 chars)
  - `excerpt` - Short summary for blog cards
  - `content` - Full HTML (not markdown)
  - `category` - One of: `guides`, `tips`, `reviews`, `news`
  - `author` - Always `"FinFinder Team"`
  - `date` - Format: `"Mon DD, YYYY"` (e.g., `"Mar 05, 2026"`)
  - `date_published` - ISO 8601 (e.g., `"2026-03-05"`)
  - `date_modified` - ISO 8601 (same as published for new posts)
  - `read_time` - Integer (minutes, ~250 words/minute)
  - `featured_image` - Filename in `/static/` (WebP)
  - `featured_image_alt` - Descriptive alt text with keywords
  - `meta_description` - 150-160 chars, hook-first, second person
  - `tags` - Array of 4-8 relevant tags
  - `primary_keyword` - Main SEO target
  - `secondary_keywords` - Array of supporting keywords
  - `faqs` - Array of `{question, answer}` objects (3-5 entries)
- **Tools:** None (JSON object built in memory)
- **Files modified:** None yet

### Step 8: Self-Check (Voice Verification)
- **What:** Run through the voice verification checklist before proceeding:
  - Opens with scenario (fin) or news hook (news), never a definition
  - Zero banned words/phrases from voice-profile.md
  - No paragraphs over 4 sentences
  - Short/medium/short sentence rhythm present
  - At least one opinionated stance someone could disagree with
  - Sensory descriptions present (fin posts only)
  - Contractions used throughout
  - CTA uses unique language not repeated from other posts
  - No retired patterns (Section 11 of voice-profile.md)
  - Reads like a Stab article, not a content-marketing blog
- **Tools:** None (internal review against rules)
- **Files modified:** Post content revised if any check fails

---

## PHASE 3: GENERATE HERO IMAGE

### Step 9: Generate and Process Hero Image
- **What:** Create a hero image using Nano Banana 2 (Gemini image generation), resize to blog dimensions, save as WebP.
- **Tools:** `Bash` tool (Python script)
- **API:** `google.genai.Client` with model `gemini-3.1-flash-image-preview`
- **Dependencies:** `pip install google-genai` (installed if missing), `Pillow`

**9a: Install google-genai if needed**
- Run `pip install google-genai` (skipped if already installed)

**9b: Read API key**
- Read `.claude/mcp.json`, extract `GEMINI_API_KEY` from `mcpServers.nano-banana-pro.env`
- **Files read:** `.claude/mcp.json`

**9c: Choose prompt based on post category**
- **Gear/science/how-to** (guides, tips, reviews about products, materials, sizing):
  > "Overhead flat lay product photograph of [specific fin type] on clean white sand. Translucent fiberglass with visible weave texture. Natural sunlight, soft shadows. Editorial product photography. No text, no logos."
- **Culture/pro setup** (profiles, pro gear, industry news, WSL):
  > "Silhouette of a surfer on the beach at golden hour holding a [board type] under their arm, looking out at waves. Shot from behind, no face visible. Cinematic 35mm film look. No text, no logos."
- **Action/wave-specific** (wave guides, spot content, performance comparisons):
  > "Surfer bottom-turning on a [wave type] wave, shot from water angle. Golden afternoon light. Editorial surf photography like Stab Magazine. No face detail visible. No text, no logos."

**9d: Call Gemini API**
- Config: `response_modalities=["TEXT", "IMAGE"]`, `aspect_ratio="16:9"`, `image_size="2K"`
- Extract image bytes from `response.candidates[0].content.parts` (find part with `inline_data`)
- Save raw image to temp file

**9e: Crop-to-fit resize (never stretch)**
1. Open with Pillow, convert to RGB
2. Scale to fit width first: `scale = 1200 / img.width`
3. Resize maintaining aspect ratio: `(1200, int(img.height * scale))` with `LANCZOS`
4. If resized height < 448: recalculate with `scale = 448 / img.height`, resize, then center-crop width
5. Center-crop to exactly **1200x448**
6. Save as WebP (quality=85) to `static/<slug>.webp`
7. Delete temp file

- **Files created:** `static/<slug>.webp`

---

## PHASE 4: PUBLISH

### Step 10: Add Post to blog_posts.json
- **What:** Write a Python script that loads `blog_posts.json`, appends the new post object, saves, and verifies the JSON is valid.
- **Tools:** `Write` tool (Python script), `Bash` tool (run script, delete script)
- **Files modified:** `blog_posts.json` (new post appended to `posts` array)

### Step 11: Update Topics Queue
- **What:** If the topic came from `.claude/topics.md`, change its status from `[~]` to `[x]`.
- **Tools:** `Edit` tool
- **Files modified:** `.claude/topics.md` (gitignored, won't be committed)

### Step 12: Commit and Push
- **What:** Stage files, commit with standard message format, push to remote.
- **Tools:** `Bash` tool (git commands)
- **Commands:**
  ```
  git add blog_posts.json static/<slug>.webp
  git commit -m "Add blog post: <post-title>"
  git push origin main
  ```
- **Files committed:** `blog_posts.json`, `static/<slug>.webp`
- **Note:** `.claude/topics.md` is gitignored and won't be included

### Step 13: Report Results
- **What:** Output a summary of what was published:
  - Post title and slug
  - Word count
  - Image filename and file size
  - Commit hash
  - Live URL: `https://finfinder.ai/finsights/<slug>`
- **Tools:** None (text output)

---

## PHASE 5: POST-PUBLISH QUALITY CHECK

All checks use real installed skills via the `Skill` tool. If any check fails, the issue is fixed, re-committed, and re-pushed before the topic is marked complete.

### Step 14: Word Count & Readability
- **What:** Verify word count hits target range and readability is appropriate.
- **Skills called:**
  - **`word-stats`** - Returns word count, character count, reading time. Confirm fin-specific posts are 1,200-1,800 words, news posts are 600-1,000 words.
  - **`readability`** - Returns Flesch-Kincaid, Gunning Fog, SMOG scores. Target Flesch-Kincaid grade level 6-10.
- **Input:** Post content with HTML tags stripped
- **Action if failed:** Simplify long sentences or expand thin content, then recheck

### Step 15: AI Detection & Humanization
- **What:** Detect AI-generated patterns and fix them.
- **Skills called:**
  - **`detect-ai`** - Returns 0-100 AI detection score with detailed metrics
    - Score 0-30: Pass
    - Score 31-50: Borderline, run humanizer on flagged sections
    - Score 51+: Fail, run humanizer on full post
  - **`humanizer`** - Rewrites flagged sections to remove AI writing patterns (only called if detect-ai score > 30)
- **Input:** Post content (plain text)
- **Action if failed:** Apply humanizer, re-run detect-ai to confirm score dropped below 30
- **Manual scan after humanization:**
  - Banned words from voice-profile.md (delve, landscape, leverage, unleash, elevate, harness, comprehensive, robust, streamline, cutting-edge, revolutionize, game-changer, dive in, navigate, etc.)
  - Em dashes (banned in CLAUDE.md)
  - Paragraphs over 4 sentences
  - Stiff non-contractions ("do not", "it is", "you will") unless deliberate emphasis

### Step 16: SEO Audit
- **What:** Full SEO check on the published post.
- **Skills called:**
  - **`seo-audit`** - Audits technical SEO, heading structure, meta tags, internal linking
- **Input:** Post URL (`https://finfinder.ai/finsights/<slug>`) or raw HTML content if not yet deployed
- **Checks:**
  - Meta description under 160 characters
  - Valid heading hierarchy (one H1, H2s for sections, H3s under H2s only)
  - Primary keyword in first paragraph
  - At least one internal link to `/recommender`
  - `featured_image_alt` is non-empty and descriptive
  - No broken internal links
- **Action if failed:** Fix the specific issue in blog_posts.json

### Step 17: GEO / AI Search Optimization
- **What:** Check whether the post is structured for AI search engine citation.
- **Skills called:**
  - **`ai-seo`** - Analyzes content for AI citation readiness (Perplexity, ChatGPT, Gemini)
- **Input:** Post content
- **Checks:**
  - At least 2 paragraphs with direct-answer statements AI could extract as citations
  - Structured FAQ data present (triggers FAQPage schema)
  - Specific product names, measurements, or stats (not vague generalities)
  - Clear H2 question/topic headers AI can parse
- **Action if failed:** Add quotable direct-answer sentences, specific data points

### Step 18: FAQ Validation
- **What:** Programmatically verify FAQ data integrity.
- **Tools:** `Read` tool (read blog_posts.json), `Bash` or inline validation
- **Checks:**
  - `faqs` array has at least 3 entries
  - Each FAQ has both `question` and `answer` fields, both non-empty strings
  - FAQs are real questions a surfer would search for, not keyword-stuffed headers
- **Files read:** `blog_posts.json`
- **Action if failed:** Add or fix FAQ entries

### Step 19: Fix & Re-publish (if needed)
- **What:** If any check from Steps 14-18 failed, fix the issues and push a correction.
- **Tools:** `Edit` tool (fix blog_posts.json), `Bash` tool (git commands)
- **Commands:**
  ```
  git add blog_posts.json
  git commit -m "Fix quality issues: <post-title>"
  git push origin main
  ```
- **Files modified:** `blog_posts.json`
- **Then:** Re-run any failed checks to confirm they pass

### Step 20: Mark Complete
- **What:** If all checks pass, ensure the topic is marked `[x]` in the topics queue.
- **Tools:** `Edit` tool
- **Files modified:** `.claude/topics.md` (if not already marked done in Step 11)

---

## File Summary

### Files Read (not modified)
| File | Phase | Purpose |
|------|-------|---------|
| `.claude/topics.md` | 1 | Pick next topic |
| `~/.claude/skills/voiceprint/voice-profile.md` | 1 | Voice rules, banned words |
| `BLOG_STYLE_GUIDE.md` | 1 | Structure, formatting, CTA rules |
| `SEO_GUIDELINES.md` | 1 | SEO and GEO rules |
| `blog_posts.json` | 1, 5 | Existing posts, duplicate check, FAQ validation |
| `.claude/mcp.json` | 3 | Gemini API key |

### Files Created
| File | Phase | Purpose |
|------|-------|---------|
| `static/<slug>.webp` | 3 | Hero image (1200x448, WebP quality 85) |

### Files Modified
| File | Phase | Purpose |
|------|-------|---------|
| `blog_posts.json` | 4, 5 | New post appended; fixes if quality checks fail |
| `.claude/topics.md` | 1, 5 | Status: `[ ]` -> `[~]` -> `[x]` (gitignored) |

### External APIs Called
| API | Phase | Purpose |
|-----|-------|---------|
| Web search | 1 | Topic research (3-5 queries) |
| Gemini `gemini-3.1-flash-image-preview` | 3 | Hero image generation |

### Skills Called (Phase 5)
| Skill | Step | Purpose |
|-------|------|---------|
| `word-stats` | 14 | Word count verification |
| `readability` | 14 | Flesch-Kincaid grade level check |
| `detect-ai` | 15 | AI detection score (0-100) |
| `humanizer` | 15 | Fix AI patterns if score > 30 |
| `seo-audit` | 16 | Technical SEO audit |
| `ai-seo` | 17 | GEO / AI citation readiness |

### Git Operations
| Command | Phase | When |
|---------|-------|------|
| `git add` + `git commit` + `git push` | 4 | Initial publish |
| `git add` + `git commit` + `git push` | 5 | Only if quality fixes needed |
