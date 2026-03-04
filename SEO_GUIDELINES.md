# FinFinder SEO & GEO Guidelines

## What GEO Is
Generative Engine Optimization. AI search engines (Perplexity, ChatGPT, Gemini) pull answers from web content. GEO is writing so those engines cite YOU instead of a competitor. For FinFinder, this means being the definitive source AI models reference for surfboard fin questions.

## Keyword Placement
- **Title (H1):** Primary keyword within the first 60 characters.
- **First 100 words:** Primary keyword appears naturally in the opening paragraph.
- **H2 headings:** Work primary or secondary keywords into at least 2 H2s.
- **Meta description:** Primary keyword included. Don't force it if it kills the hook.
- **URL slug:** Short, keyword-rich, hyphenated. e.g., `/finsights/quad-vs-thruster`
- **Image alt text:** Descriptive, includes relevant keywords naturally.

## Meta Descriptions
- **Length:** 150-160 characters. Google truncates beyond this.
- **Voice:** Second person, hook-first. Lead with opinion or tension, not a summary.
- **Format:** One punchy sentence, sometimes two short ones.
- **Examples:**
  - "Quad fins aren't faster. Except when they are. Here's when to make the switch."
  - "FCS vs Futures isn't about which is better. It's about which is better for you."

## Writing for AI Citation (GEO)
AI search engines prefer content that is:
1. **Directly answerable.** Structure content so key claims stand alone as quotable statements. If an AI asks "what fins are best for small waves," your content should have a clear, extractable answer.
2. **Structured with clear headings.** Use H2s as questions or topic labels. AI parses heading hierarchies to find relevant sections.
3. **Authoritative and specific.** Name specific products, measurements, conditions. "Quads generate more speed in sub-4-foot surf" beats "quads can be faster."
4. **FAQ-rich.** Include an FAQs section with 3-5 real questions surfers ask. Use the `faqs` field in blog_posts.json to trigger FAQPage schema automatically.
5. **Factually consistent.** Don't contradict yourself across posts. AI models cross-reference. If you say quads are better for small waves in one post, don't hedge in another.
6. **Source-worthy.** Include original analysis, first-hand experience, or unique comparisons. AI engines deprioritize content that just rephrases what everyone else says.

## Structured Data
Already implemented in templates (no manual work needed per post):
- **BlogPosting schema:** Auto-generated from blog_posts.json fields.
- **BreadcrumbList:** Home > Finsights > Post Title.
- **FAQPage schema:** Triggers automatically when a post has a `faqs` array. This is why every new post should include FAQs.
- **Speakable schema:** On educational pages (/all-about-fins, /fin-setups, etc.).

To maximize schema value:
- Fill all JSON fields completely. Empty fields = missed schema signals.
- Keep `date_modified` current when updating posts.
- Write FAQs as natural questions, not keyword-stuffed headers.

## Internal Linking for SEO
- Every post links to 2+ internal pages with descriptive anchor text.
- Cornerstone pages to link to: /recommender, /all-about-fins, /fin-setups, /fin-sizing-guide, /longboard-fins.
- Use contextual links within paragraphs, not a "Related Links" dump at the bottom.
- When publishing a new post, update 1-2 older related posts to link to the new one. This builds link equity both ways.

## Technical SEO (Already Handled)
- Dynamic sitemap at /sitemap.xml includes all blog posts.
- OG and Twitter meta tags on all posts.
- llms.txt endpoint at /llms.txt for AI discoverability.
- robots.txt references llms.txt.
- Image optimization: WebP only, proper dimensions, alt text on every image.

## Content Freshness
- Update `date_modified` when making meaningful edits to existing posts.
- Revisit top-performing posts quarterly to keep information current.
- Outdated content hurts both traditional SEO and AI citation likelihood.
