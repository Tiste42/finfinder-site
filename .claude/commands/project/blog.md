Write, image, publish, and push a complete FinFinder blog post. Fully automated end-to-end.

**Topic:** $ARGUMENTS

If $ARGUMENTS is empty or says "auto", pick the next available topic from `.claude/topics.md` (first unchecked `[ ]` item).

---

## PHASE 1: TOPIC SELECTION & RESEARCH

1. **If no topic given**, read `.claude/topics.md` and pick the first `[ ]` topic. Mark it `[~]` (in progress).

2. **Research the topic** using WebSearch. Search 3-5 angles: technical, cultural, competitive, product, and conditions. Get real names, real stats, real quotes. No generic filler.

3. **Read these files:**
   - `~/.claude/skills/voiceprint/voice-profile.md` (tone, banned words, sentence architecture)
   - `BLOG_STYLE_GUIDE.md` (structure, formatting, CTA rules)
   - `SEO_GUIDELINES.md` (keywords, meta, GEO optimization)

4. **Read `blog_posts.json`** to check for duplicate topics, match JSON structure, and avoid repeating CTA phrasing.

## PHASE 2: WRITE THE POST

5. **Classify the post type:**
   - **Fin-specific** (guides, reviews, comparisons, sizing, setup): category "guides", "tips", or "reviews". Target 1,200-1,800 words.
   - **Surf news** (WSL, Olympics, industry, culture, viral clips): category "news". Target 600-1,000 words.

6. **Write the post following all rules:**
   - Voice: Stab Magazine editorial energy. Irreverent, honest, sharp.
   - Use the correct post structure (fin-specific or surf news) from the style guide.
   - Include 2+ internal links to cornerstone pages (/recommender, /all-about-fins, /fin-setups, /fin-sizing-guide, /longboard-fins).
   - Include 3-5 FAQs in the faqs array.
   - Content must be full HTML (not markdown).
   - No em dashes. No banned words. No paragraphs over 4 sentences. Use contractions.
   - At least 2 sensory descriptions for fin posts.
   - At least 1 specific cultural reference (named surfer, break, or contest).
   - CTA to /recommender woven naturally into closing (skip if it doesn't fit).

7. **Set all required JSON fields:**
   - slug, title, excerpt, content (HTML), category, author ("FinFinder Team")
   - date ("Mon DD, YYYY"), date_published (ISO), date_modified (ISO)
   - read_time (integer), featured_image, featured_image_alt
   - meta_description (150-160 chars, hook-first), tags (4-8), primary_keyword, secondary_keywords, faqs

8. **Self-check** (voice verification checklist):
   - Opens with scenario (fin) or news hook (news), never a definition
   - Zero banned words/phrases from voice-profile.md
   - No paragraphs over 4 sentences
   - Short/medium/short rhythm present
   - At least one opinionated stance someone could disagree with
   - Sensory descriptions present (fin posts)
   - Contractions used throughout
   - CTA uses unique language not repeated from other posts
   - No retired patterns (Section 11 of voice-profile.md)
   - Reads like a Stab article, not a content-marketing blog

## PHASE 3: GENERATE HERO IMAGE

9. **Generate a hero image** using Nano Banana 2 (google-genai Python library):
   - First, ensure the library is installed: `pip install google-genai` (skip if already installed)
   - Read the API key from `.claude/mcp.json` (GEMINI_API_KEY in nano-banana-pro env)
   - Use `google.genai.Client` with model `gemini-3.1-flash-image-preview`

   **IMPORTANT: AI models cannot accurately render fin geometry.** Close-up fin shapes come out warped, bent, and unrealistic. Use only these 5 safe scene types:

   | # | Scene Type | Description | Best For |
   |---|-----------|-------------|----------|
   | 1 | FINS_ON_SAND | Overhead flat lay of fins on beach sand, golden hour | Fin types, comparisons, materials |
   | 2 | FINS_ON_WOOD | Fins laid on weathered wood table/deck, natural light, overhead | Gear reviews, setup guides, technical |
   | 3 | SILHOUETTE | Surfer holding board at sunset, backlit, wide shot | Beginner guides, lifestyle posts |
   | 4 | WAVE_FRAME | Clean breaking wave, no people, turquoise water, editorial landscape | Wave types, conditions, surf spots |
   | 5 | ACTION_SHOT | Distant surfer riding a wave, shot from shore, small in frame | Performance, technique, board comparisons |

   **Selection logic:**
   1. Pick the scene type that best matches the blog topic
   2. Check the `last_image_type` field on the last 2 entries in `blog_posts.json`
   3. If your pick matches either of the last 2, choose your second-best match instead

   **Prompt rules (ALL scenes):**
   - NEVER request close-up fin geometry, fin curves, or fin detail
   - Keep fins small in frame, silhouetted, or overhead flat lay only
   - Style: editorial surf photography, photorealistic, warm natural tones
   - End every prompt with: `No text, no logos, no readable letters, no faces.`

   - Set `config=types.GenerateContentConfig(response_modalities=["TEXT", "IMAGE"])` with `aspect_ratio="16:9"` and `image_size="2K"` in the config
   - Extract the image from `response.candidates[0].content.parts`, find the part with `inline_data`, and save the raw bytes
   - **Resize using crop-to-fit (NEVER force-stretch):**
     1. Open image with Pillow, convert to RGB
     2. Calculate scale factor to fit **width** first: `scale = 1200 / img.width`
     3. Resize maintaining aspect ratio: `(1200, int(img.height * scale))` with `Image.LANCZOS`
     4. If resized height < 448, recalculate using height instead: `scale = 448 / img.height`, resize to `(int(img.width * scale), 448)`, then center-crop width
     5. Center-crop to exactly 1200x448: `top = (h - 448) // 2; img.crop((left, top, left + 1200, top + 448))`
     6. Save as WebP (quality=85) to `static/<slug>.webp`
   - This ensures no distortion regardless of source image dimensions
   - Set `featured_image` in the JSON to match the filename
   - **Add `last_image_type` field** to the post JSON (e.g., `"last_image_type": "FINS_ON_SAND"`)

## PHASE 4: QUALITY CHECKS

Run these checks BEFORE publishing. If any check fails, flag it in the final output so it can be reviewed manually.

### Step 10: AI Detection & Humanization

Use the **`detect-ai`** skill on the post content. This returns a 0-100 AI detection score.
- **Score 0-30:** Pass. Move on.
- **Score 31-50:** Borderline. Use the **`humanizer`** skill to rewrite flagged sections, then re-run `detect-ai` to confirm the score dropped below 30.
- **Score 51+:** Fail. Use the **`humanizer`** skill on the full post, then re-run `detect-ai`. If still above 30, manually rewrite the worst sections.

After humanization (if needed), also do a manual scan for:
- Banned words from `voice-profile.md` ("delve", "landscape", "leverage", "unleash", "elevate", "harness", "comprehensive", "robust", "streamline", "cutting-edge", "revolutionize", "game-changer", "dive in", "in today's fast-paced world", "it's important to note", "in conclusion", "without further ado", "unlock your potential", "we've got you covered", "here's what nobody tells you", "navigate")
- Em dashes (banned in CLAUDE.md)
- Paragraphs over 4 sentences
- Stiff non-contractions ("do not", "it is", "you will") unless used for deliberate emphasis

### Step 11: SEO Audit

Use the **`seo-audit`** skill on the raw HTML content and JSON fields. Verify:
- Meta description is under 160 characters
- Heading structure is valid (one H1, H2s for sections, H3s under H2s only)
- Primary keyword appears in the first paragraph
- At least one internal link to `/recommender` exists
- `featured_image_alt` is non-empty and descriptive
- No broken internal links

### Step 12: GEO / AI Search Optimization

Use the **`ai-seo`** skill on the post content to check AI citation readiness:
- At least 2 paragraphs contain direct-answer statements an AI search engine could extract as a citation
- Post has structured FAQ data (the `faqs` array triggers FAQPage schema automatically)
- Post includes specific product names, measurements, or stats (not vague generalities)
- Content is structured with clear H2 question/topic headers that AI can parse

## PHASE 5: PUBLISH

Everything has passed quality checks. Now write to disk and ship it.

16. **Add the post to `blog_posts.json`:**
    - Write a Python script to load the JSON, append the new post object, and save
    - Verify JSON is valid after writing

17. **Update topics queue** (if topic came from `.claude/topics.md`):
    - Change the topic from `[~]` to `[x]`

18. **Commit and push:**
    - `git add blog_posts.json static/<image>.webp`
    - Commit message: `Add blog post: <post-title>`
    - `git push origin main`

19. **Report what was done:**
    - Post title and slug
    - Word count and readability grade
    - AI detection score
    - Image filename and size
    - Commit hash
    - URL: `https://finfinder.ai/finsights/<slug>`
