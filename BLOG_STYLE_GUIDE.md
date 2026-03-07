# FinFinder Blog Style Guide

## Voice Baseline
Irreverent, honest, sharp. Stab Magazine editorial energy. See `voice-profile.md` for full tone rules.
- Always use contractions. Fragments welcome. No paragraphs over 4 sentences.
- Never use banned words (delve, landscape, leverage, unleash, comprehensive, robust, etc.).
- Never use em dashes.
- Author: "FinFinder Team" on all posts.

## Heading Structure
- **H1:** Post title only. One per post. Set via `title` field in blog_posts.json (rendered by template).
- **H2:** Major sections. Use keyword-rich, conversational phrasing. No generic labels like "Introduction."
- **H3:** Subsections under H2s. Use for breakdowns, comparisons, or lists that need a label.
- **No H4+.** If you need that depth, restructure.
- Vary section headers between posts. Never reuse the same structural formula.

## Post Length
- **Fin-specific posts** (guides, reviews, comparisons): 1,200-1,800 words. Enough depth to be the best answer on the topic.
- **Surf news posts** (WSL, culture, industry): 600-1,000 words. Get in, make the point, get out.

## Post Structure
### Fin-Specific Posts
1. Scenario opening (put the reader in the water or at the shop)
2. Core insight/argument
3. Technical details with sensory descriptions
4. Honest verdict (take a stance)
5. Key Takeaways (bulleted, scannable)
6. Natural CTA to /recommender (woven in, not bolted on)

### Surf News Posts
1. News hook (what happened)
2. Editorial angle (why it matters)
3. Cultural context
4. Fin angle (only if it fits naturally, skip if it doesn't)
5. Key Takeaways

## Key Takeaways Section
- Place near the end, before any closing CTA.
- Use an H2: "Key Takeaways"
- 3-5 bullet points. Each bullet is one clear, opinionated sentence.
- No filler bullets. Every point should be something the reader can act on.

## Image Placement
- **Hero image:** One per post. WebP only. Stored flat in `/static/`. Dimensions: 1200x448.
- **In-post images:** Optional. Place after the H2 they support, not before. WebP only.
- **Blog cards:** 400x192, lazy loaded. Set via `featured_image` in JSON.
- **Alt text:** Descriptive and specific. Not "surfboard fins" but "FCS II Performer fins mounted on a 5'10 shortboard."

## AI-Generated Image Rules
- AI models **cannot accurately render fin geometry.** Never prompt for close-up fin detail, fin curves, or fin shapes.
- Use only the 5 safe scene types: FINS_ON_SAND, FINS_ON_WOOD, SILHOUETTE, WAVE_FRAME, ACTION_SHOT (see `blog.md` for full descriptions).
- Keep fins small in frame, silhouetted, or overhead flat lay only.
- Style: editorial surf photography, photorealistic, warm natural tones.
- No text, logos, or readable faces in any generated image.
- Check `last_image_type` on the last 2 posts to avoid repeating the same scene type.

## Metadata (blog_posts.json)
Every post requires all fields. See CLAUDE.md for the full list. Key rules:
- `date`: "Mon DD, YYYY" format (e.g., "Mar 03, 2026")
- `date_published` / `date_modified`: ISO 8601 (e.g., "2026-03-03")
- `category`: One of: guides, tips, reviews, news
- `content`: Full HTML, not markdown
- `faqs`: Array of {question, answer}. All new posts should include 3-5 FAQs.
- `read_time`: Integer. Estimate ~250 words per minute.
- `tags`: 4-8 relevant tags per post.

## Internal Linking
- Every post links to at least 2 other FinFinder pages (other posts, /recommender, educational pages).
- Link with descriptive anchor text, not "click here."
- Prioritize linking to cornerstone pages: /recommender, /all-about-fins, /fin-setups, /fin-sizing-guide.
- New posts should link to related older posts. Update older posts to link back when relevant.

## CTA Rules
- No dedicated CTA sections. Weave naturally into the closing.
- Vary phrasing every post. Never repeat a CTA across posts.
- Frame editorially: "We built a tool for this" not "Try our amazing tool."
- Skip the CTA entirely if it doesn't fit (especially news posts).
