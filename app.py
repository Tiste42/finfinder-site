from flask import Flask, render_template, request, jsonify, redirect, url_for, session, Response, send_from_directory
import google.generativeai as genai
import os
import time
from pathlib import Path
from dotenv import load_dotenv
import logging
import datetime
import re
import json

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO)

BASE_DIR = Path(__file__).resolve().parent
BLOG_POSTS_PATH = BASE_DIR / 'blog_posts.json'
SITE_URL = "https://finfinder.ai"

STATIC_ASSET_EXTENSIONS = ('.webp', '.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov', '.woff2', '.woff')
CSS_JS_EXTENSIONS = ('.css', '.js')

ACTIVE_PAGE_BY_PATH = {
    '/': 'home',
    '/recommender': 'recommender',
    '/all-about-surfboard-fins': 'all_about_fins',
    '/fin-setups': 'fin_setups',
    '/fin-systems': 'fin_systems',
    '/longboard-fins': 'longboard_fins',
    '/fin-sizing-guide': 'fin_sizing_guide',
    '/about': 'about',
}

SITEMAP_STATIC_PAGES = [
    {'path': '/', 'changefreq': 'daily', 'priority': '1.0'},
    {'path': '/recommender', 'changefreq': 'weekly', 'priority': '0.9'},
    {'path': '/finsights', 'changefreq': 'weekly', 'priority': '0.9'},
    {'path': '/all-about-surfboard-fins', 'changefreq': 'monthly', 'priority': '0.8'},
    {'path': '/fin-setups', 'changefreq': 'monthly', 'priority': '0.8'},
    {'path': '/fin-systems', 'changefreq': 'monthly', 'priority': '0.8'},
    {'path': '/longboard-fins', 'changefreq': 'monthly', 'priority': '0.8'},
    {'path': '/fin-sizing-guide', 'changefreq': 'monthly', 'priority': '0.8'},
    {'path': '/about', 'changefreq': 'monthly', 'priority': '0.7'},
]

# --- Flask App Initialization ---
app = Flask(__name__) 

# Configure static file caching
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # 1 year for static files

@app.after_request
def add_cache_headers(response):
    """Add cache headers for better performance"""
    # Cache static files aggressively
    if request.path.startswith('/static/'):
        # Images, videos, fonts - cache for 1 year
        if request.path.endswith(STATIC_ASSET_EXTENSIONS):
            response.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
        # CSS/JS - cache for 1 week with revalidation
        elif request.path.endswith(CSS_JS_EXTENSIONS):
            response.headers['Cache-Control'] = 'public, max-age=604800, stale-while-revalidate=86400'
    # Blog pages - cache for 1 hour
    elif request.path.startswith('/finsights'):
        response.headers['Cache-Control'] = 'public, max-age=3600, stale-while-revalidate=86400'
    return response

@app.route('/robots.txt')
def robots_txt():
    return send_from_directory(app.static_folder, 'robots.txt')
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

# --- Load Environment Variables & Configure Gemini ---
model = None # Initialize model as None
try:
    dotenv_path = BASE_DIR / '.env'
    logging.info(f"Looking for .env file at: {dotenv_path}")

    if dotenv_path.exists():
        load_dotenv(dotenv_path=dotenv_path, override=True)
        logging.info(f"Successfully loaded .env file from: {dotenv_path}")
    else:
        logging.warning(f".env file not found at the specified path: {dotenv_path}. Attempting to load from default location.")
        load_dotenv(override=True) # Try loading from default location if specific path not found

    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        logging.error("GEMINI_API_KEY not found in environment variables after attempting to load .env.")
    else:
        logging.info("GEMINI_API_KEY loaded successfully.")
        genai.configure(api_key=gemini_api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        logging.info("Gemini model initialized with gemini-2.5-flash.")

except KeyError:
    logging.error("GEMINI_API_KEY not found in environment variables (KeyError). Ensure it's in your .env file.")
    model = None
except Exception as e:
    logging.error(f"An unexpected error occurred during Gemini API configuration: {e}")
    model = None

# --- Blog Posts Helper Functions with Caching ---
# In-memory cache for blog posts
_blog_posts_cache = {
    'data': None,
    'by_slug': {},
    'timestamp': 0
}
BLOG_CACHE_TTL = 300  # 5 minutes cache TTL

def load_blog_posts():
    """Load blog posts from JSON file with caching"""
    current_time = time.time()
    
    # Return cached data if still valid
    if _blog_posts_cache['data'] is not None and (current_time - _blog_posts_cache['timestamp']) < BLOG_CACHE_TTL:
        return _blog_posts_cache['data']
    
    try:
        if BLOG_POSTS_PATH.exists():
            with BLOG_POSTS_PATH.open('r', encoding='utf-8') as f:
                data = json.load(f)
                posts = data.get('posts', [])
                # Update cache
                _blog_posts_cache['data'] = posts
                _blog_posts_cache['by_slug'] = {post.get('slug'): post for post in posts if post.get('slug')}
                _blog_posts_cache['timestamp'] = current_time
                return posts
        return []
    except Exception as e:
        logging.error(f"Error loading blog posts: {e}")
        return []

def get_post_by_slug(slug):
    """Get a specific blog post by slug"""
    load_blog_posts()
    return _blog_posts_cache['by_slug'].get(slug)

def get_related_posts(current_post, limit=3):
    """Get related posts based on category"""
    posts = load_blog_posts()
    related = []
    for post in posts:
        if post.get('slug') != current_post.get('slug'):
            if post.get('category') == current_post.get('category'):
                related.append(post)
    return related[:limit]

# --- Context Processor to inject 'now' into all templates ---
@app.context_processor
def inject_now():
    return {'now': datetime.datetime.utcnow()}

@app.context_processor
def inject_site_url():
    return {'site_url': SITE_URL}

# --- Context Processor to inject active_page based on request path ---
@app.context_processor
def inject_active_page():
    """Injects the active_page variable into all templates based on the current route."""
    if request.path == '/finsights' or request.path.startswith('/finsights/'):
        return {'active_page': 'finsights'}
    return {'active_page': ACTIVE_PAGE_BY_PATH.get(request.path)}

# --- Helper Function for AI Response Formatting ---
def format_ai_response(response_text):
    """Format AI response for proper HTML display"""
    formatted = response_text
    
    # FIRST: Convert product name + link patterns to clean hyperlinks (NO VISIBLE URLs)
    # Pattern: **Product Name** - https://amzn.to/xxx
    # Result: <strong><a href="link">Product Name (Amazon)</a></strong>
    formatted = re.sub(
        r'\*\*([^*]+?)\*\*\s*[-–—]\s*(https://amzn\.to/\w+)',
        r'<strong><a href="\2" target="_blank" rel="noopener noreferrer" class="text-teal-300 hover:text-teal-100 hover:underline">\1 (Amazon)</a></strong>',
        formatted
    )
    
    # Pattern: Product Name - https://amzn.to/xxx (without bold markers)
    formatted = re.sub(
        r'([A-Z][^-\n]+?)\s*[-–—]\s*(https://amzn\.to/\w+)',
        r'<strong><a href="\2" target="_blank" rel="noopener noreferrer" class="text-teal-300 hover:text-teal-100 hover:underline">\1 (Amazon)</a></strong>',
        formatted
    )
    
    # Pattern: [View on Amazon] or [Browse All X] followed by URL - hide the URL
    formatted = re.sub(
        r'(?:View on Amazon|Browse All[^:\n]*?)(?:\s*[:]\s*|\s+)(https://amzn\.to/\w+)',
        r'<strong><a href="\1" target="_blank" rel="noopener noreferrer" class="text-teal-300 hover:text-teal-100 hover:underline">View on Amazon</a></strong>',
        formatted
    )
    
    # Catch any remaining standalone Amazon links and hide them as "View on Amazon" text
    formatted = re.sub(
        r'(?<![">])(https://amzn\.to/\w+)(?![<"])',
        r'<a href="\1" target="_blank" rel="noopener noreferrer" class="text-teal-300 hover:text-teal-100 hover:underline">View on Amazon</a>',
        formatted
    )
    
    # Convert **text** to HTML bold (for any remaining bold text)
    formatted = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', formatted)
    
    # Handle bullet points - remove extra line breaks before bullets
    formatted = re.sub(r'\n+• ', r'<br>• ', formatted)
    
    # More aggressive paragraph spacing - convert multiple line breaks to single breaks
    formatted = re.sub(r'\n{2,}', r'<br><br>', formatted)
    
    # Convert remaining single line breaks
    formatted = re.sub(r'\n', r'<br>', formatted)
    
    # Clean up excessive <br> tags - max 2 in a row
    formatted = re.sub(r'(<br>\s*){3,}', r'<br><br>', formatted)
    
    # Wrap in a div instead of paragraph tags for better control
    formatted = f'<div>{formatted}</div>'
    
    return formatted


def build_fallback_recommendation(question, user_info=None):
    """Build a deterministic recommendation when Gemini is unavailable."""
    user_info = user_info or {}
    question_lower = (question or '').lower()
    board_type = user_info.get('board_type', '')
    wave_conditions = user_info.get('wave_conditions', '')
    weight = user_info.get('weight')
    skill_level = user_info.get('skill_level')
    fin_system = user_info.get('fin_system')
    skill_phrase = skill_level or 'surfer'
    if skill_phrase in {'beginner', 'intermediate', 'advanced', 'expert'}:
        article = 'an' if skill_phrase[0].lower() in 'aeiou' else 'a'
        skill_phrase = f"{article} {skill_phrase}"
    weight_phrase = f"around {weight} pounds" if weight else "at your weight"

    try:
        weight_value = int(weight) if weight else None
    except (TypeError, ValueError):
        weight_value = None

    if weight_value is None:
        size_note = 'medium'
    elif weight_value < 160:
        size_note = 'small'
    elif weight_value <= 180:
        size_note = 'medium'
    elif weight_value <= 200:
        size_note = 'large'
    else:
        size_note = 'large to XL'

    wants_longboard = board_type == 'longboard' or 'longboard' in question_lower
    wants_twin = 'twin' in question_lower or board_type == 'fish'
    small_waves = wave_conditions == 'small/weak' or any(term in question_lower for term in ['small', 'mushy', 'weak', 'slow'])
    powerful_waves = wave_conditions == 'big/powerful' or any(term in question_lower for term in ['big', 'powerful', 'overhead', 'hollow', 'barrel'])

    if wants_longboard:
        research = (
            f"Based on what you shared, start with a pivot-style single fin. "
            f"It gives a longboard clean hold, easy trim, and enough turning response without getting too specialized."
        )
        recommendations = [
            ('FCS Connect Glass Flex Single Fin', 'https://amzn.to/49zT5qd'),
            ('Abahub 9/10 inch Single Fin', 'https://amzn.to/49wXdqL'),
        ]
        next_step = "If you tell me whether you care more about noseriding or turning, I can narrow the size and placement."
    elif wants_twin and small_waves:
        research = (
            f"For small or mushy waves, a twin fin makes sense because it cuts drag and helps the board find speed early. "
            f"At your size range, look around {size_note} unless your board is oversized."
        )
        recommendations = [
            ('FCS II Power Twin + 1 PG', 'https://amzn.to/4qRwT1I'),
            ('FT1 Honeycomb Twin Fin', 'https://amzn.to/3LyesAb'),
            ('Ho Stevie! Surfboard Twin Keel', 'https://amzn.to/4jEmFiF'),
        ]
        next_step = "If you want more hold, run a twin plus trailer instead of a pure twin."
    elif small_waves:
        research = (
            f"For {skill_phrase} {weight_phrase} in small or mushy surf, you want speed first. "
            f"A medium quad will usually feel faster than a thruster, while a medium thruster stays more predictable."
        )
        recommendations = [
            ('FCS 2 Pyzel PC Air Core Quad', 'https://amzn.to/4jAPY5Q'),
            ('Ho Stevie! Quad HexCore FCS', 'https://amzn.to/3NhdOHO'),
            ('Futures Fins AM1 Tech-Flex Medium Quad', 'https://amzn.to/4sDcnDF'),
            ('Ho Stevie! Quad HexCore Futures', 'https://amzn.to/4byfoip'),
        ]
        next_step = "If your board only takes three fins, use a medium thruster with an upright template instead."
    elif powerful_waves:
        research = (
            f"In bigger or more powerful surf, prioritize hold and confidence. "
            f"A stiffer {size_note} thruster or quad with more base will hold a line better at speed."
        )
        recommendations = [
            ('FCS II AM Performance Core Tri Fin Set', 'https://amzn.to/3Ls5NPM'),
            ('Futures Fins JJ-2 Large TECHFLEX', 'https://amzn.to/4dZLkvD'),
            ('FCS II Harley Mid Tri-Quad PC Large', 'https://amzn.to/4sEnbBx'),
            ('Futures Fins F8 Honeycomb Quad', 'https://amzn.to/3Z7ZLHC'),
        ]
        next_step = "If the wave is hollow, lean quad. If you want more predictable vertical turns, lean thruster."
    else:
        research = (
            f"When the details are still broad, a medium thruster is the safest all-around starting point. "
            f"It balances drive, hold, and turning response across most shortboards and everyday surf."
        )
        recommendations = [
            ('FCS 2 Performer PC Tri-Fin Set', 'https://amzn.to/4bgFEht'),
            ('TOPWAYS Fiberglass Honeycomb G5', 'https://amzn.to/4bxAjSP'),
            ('Futures Fins JJF Alpha Medium', 'https://amzn.to/3YyRBYd'),
            ('Ho Stevie! Thruster HexCore', 'https://amzn.to/3StgcdW'),
        ]
        next_step = "Tell me your board type, fin box system, and usual waves and I can get more specific."

    if fin_system == 'FCS':
        recommendations = [item for item in recommendations if 'Futures' not in item[0] and 'FT1' not in item[0]]
    elif fin_system == 'Futures':
        recommendations = [item for item in recommendations if 'FCS' not in item[0] and 'TOPWAYS' not in item[0]]

    recommendation_lines = '\n'.join(f"- **{name}** - {url}" for name, url in recommendations)
    return (
        "THE RESEARCH:\n"
        f"{research}\n\n"
        "HERE'S WHAT I RECOMMEND:\n"
        f"{recommendation_lines}\n\n"
        "WANT MORE SPECIFICITY?\n"
        f"{next_step}"
    )


def ensure_conversation_state():
    """Make sure the chat session has the structures used by /ask."""
    is_new_session = 'conversation_history' not in session
    session.setdefault('conversation_history', [])
    session.setdefault('user_info', {})
    if is_new_session:
        logging.info("New session: initialized conversation history and user info")
    else:
        logging.info(f"Existing session: {len(session.get('conversation_history', []))} messages in history")
        logging.info(f"Stored user info: {session.get('user_info', {})}")
    return session['conversation_history'], session['user_info']


def update_user_info_from_question(question, user_info):
    """Extract reusable recommendation context from the latest user question."""
    question_lower = question.lower()

    weight_match = re.search(r'(\d+)\s*(?:lbs?|pounds?|kg)', question_lower)
    if weight_match:
        user_info['weight'] = weight_match.group(1)
        logging.info(f"Stored user weight: {weight_match.group(1)}")

    if 'fcs' in question_lower and 'futures' not in question_lower:
        user_info['fin_system'] = 'FCS'
        logging.info("Stored fin system: FCS")
    elif 'futures' in question_lower or 'future' in question_lower:
        user_info['fin_system'] = 'Futures'
        logging.info("Stored fin system: Futures")

    if re.search(r'\b(beginner|beginning|just start|learning|new to)', question_lower):
        user_info['skill_level'] = 'beginner'
        logging.info("Stored skill level: beginner")
    elif re.search(r'\b(intermediate|getting better|catching waves)', question_lower):
        user_info['skill_level'] = 'intermediate'
        logging.info("Stored skill level: intermediate")
    elif re.search(r'\b(advanced|experienced|good surfer|barreled|barrels)', question_lower):
        user_info['skill_level'] = 'advanced'
        logging.info("Stored skill level: advanced")
    elif re.search(r'\b(pro|professional|expert|airs?|boosting)', question_lower):
        user_info['skill_level'] = 'pro'
        logging.info("Stored skill level: pro")

    if re.search(r'\b(shortboard|short board|performance board)', question_lower):
        user_info['board_type'] = 'shortboard'
        logging.info("Stored board type: shortboard")
    elif re.search(r'\b(fish)\b', question_lower):
        user_info['board_type'] = 'fish'
        logging.info("Stored board type: fish")
    elif re.search(r'\b(longboard|long board|noserider|nose rider)', question_lower):
        user_info['board_type'] = 'longboard'
        logging.info("Stored board type: longboard")
    elif re.search(r'\b(hybrid|groveler)', question_lower):
        user_info['board_type'] = 'hybrid'
        logging.info("Stored board type: hybrid")
    elif re.search(r'\b(mid.?length|funboard|fun board)', question_lower):
        user_info['board_type'] = 'mid-length'
        logging.info("Stored board type: mid-length")
    elif re.search(r'\b(gun|big wave)', question_lower):
        user_info['board_type'] = 'gun'
        logging.info("Stored board type: gun")

    if re.search(r'\b(small|weak|mushy|slow|1.?2.?ft|knee high)', question_lower):
        user_info['wave_conditions'] = 'small/weak'
        logging.info("Stored wave conditions: small/weak")
    elif re.search(r'\b(big|large|powerful|overhead|heavy|barreling|hollow)', question_lower):
        user_info['wave_conditions'] = 'big/powerful'
        logging.info("Stored wave conditions: big/powerful")

    session.modified = True
    logging.info(f"Complete user info after extraction: {user_info}")
    return user_info


def append_chat_message(role, message):
    """Append a chat message and mark nested session state as changed."""
    session['conversation_history'].append(f"{role}: {message}")
    session.modified = True


def get_recent_conversation_context(limit=10):
    return "\n".join(session.get('conversation_history', [])[-limit:])


def count_ai_responses():
    return len([msg for msg in session.get('conversation_history', []) if msg.startswith('Assistant:')])


# --- Route Definitions ---
@app.route('/')
def home():
    """Renders the homepage."""
    return render_template('index.html')

@app.route('/all-about-surfboard-fins')
def all_about_fins():
    """Renders the 'All About Surfboard Fins' page."""
    return render_template('all_about_fins.html')

@app.route('/all-about-fins')
def redirect_old_all_about_fins():
    """301 redirect from old educational URL to canonical page."""
    return redirect(url_for('all_about_fins'), code=301)

@app.route('/fin-setups')
def fin_setups():
    """Renders the 'Surfboard Fin Setups Explained' page."""
    return render_template('fin-setups.html')

@app.route('/longboard-fins')
def longboard_fins():
    """Renders 'The Complete Guide to Longboard Fins' page."""
    return render_template('longboard-fins.html')

@app.route('/fin-systems')
def fin_systems():
    """Renders the 'Fin Box Systems & Brands' page."""
    return render_template('fin_systems.html')

@app.route('/fin-box-systems')
def redirect_old_fin_box_systems():
    """301 redirect from old fin box systems URL to canonical page."""
    return redirect(url_for('fin_systems'), code=301)

@app.route('/fin-sizing-guide')
def fin_sizing_guide():
    """Renders 'The Ultimate Surfboard Fin Sizing Guide' page."""
    return render_template('fin_sizing_guide.html')

@app.route('/about')
def about():
    """Renders the 'About' page."""
    return render_template('about.html')

@app.route('/recommender')
def recommender_page():
    """Renders the Fin Recommender tool page."""
    return render_template('recommender.html')

@app.route('/finsights')
def finsights():
    """Renders the Finsights blog hub page."""
    posts = load_blog_posts()
    search_query = request.args.get('search', '').strip()
    if search_query:
        search_lower = search_query.lower()
        posts = [p for p in posts if search_lower in p.get('title', '').lower()
                 or search_lower in p.get('excerpt', '').lower()
                 or search_lower in ' '.join(p.get('tags', [])).lower()]
    # Sort posts by date (newest first)
    posts_sorted = sorted(posts, key=lambda x: x.get('date_published', x.get('date', '')), reverse=True)
    return render_template('finsights.html', posts=posts_sorted, search_query=search_query)

# SEO Redirect: Old slug to new slug (preserve Google rankings)
@app.route('/finsights/surfboard-fin-prices-skyrocketed-200-300')
def redirect_old_fins_price_post():
    """301 redirect from old URL to new URL for SEO preservation"""
    return redirect(url_for('blog_post', slug='why-are-fins-so-expensive-real-costs'), code=301)

@app.route('/how-surfboard-fins-work-lift-physics')
def redirect_root_lift_physics_post():
    """301 redirect from old root blog URL to canonical Finsights URL."""
    return redirect(url_for('blog_post', slug='how-surfboard-fins-work-lift-physics'), code=301)

@app.route('/pivot-vs-flex-longboard-fins-single-fin-guide')
def redirect_root_pivot_flex_post():
    """301 redirect from old root blog URL to canonical Finsights URL."""
    return redirect(url_for('blog_post', slug='pivot-vs-flex-longboard-fins-single-fin-guide'), code=301)

BLOG_SLUG_REDIRECTS = {
    'fin-cant-toe-in-angles-control-everything': 'fin-cant-toe-in-angles-explained',
    'fin-flex-patterns-stiffer-not-always-better': 'fin-flex-patterns-explained',
    'fin-rake-explained': 'fin-rake-explained-tight-vs-sweeping-turns',
    'fin-rake-explained-why-turns-feel-tight-or-sweeping': 'fin-rake-explained-tight-vs-sweeping-turns',
    'machado-keel-fins-review': 'machado-keel-fins-review-worth-the-hype',
}

@app.route('/finsights/<slug>')
def blog_post(slug):
    """Renders a specific blog post page."""
    if slug in BLOG_SLUG_REDIRECTS:
        return redirect(url_for('blog_post', slug=BLOG_SLUG_REDIRECTS[slug]), code=301)

    post = get_post_by_slug(slug)
    if not post:
        return render_template('404.html'), 404
    
    related_posts = get_related_posts(post)
    return render_template('blog_post.html', post=post, related_posts=related_posts)


def build_sitemap_pages(current_date, blog_posts):
    """Build sitemap entries from route metadata and blog post data."""
    pages = [
        {
            'loc': f"{SITE_URL}{page['path']}",
            'lastmod': current_date,
            'changefreq': page['changefreq'],
            'priority': page['priority'],
        }
        for page in SITEMAP_STATIC_PAGES
    ]

    for post in blog_posts:
        post_date = post.get('date_modified') or post.get('date_published') or post.get('date', current_date)
        if post_date and len(post_date) >= 10:
            post_date = post_date[:10]
        else:
            post_date = current_date

        pages.append({
            'loc': f"{SITE_URL}/finsights/{post.get('slug')}",
            'lastmod': post_date,
            'changefreq': 'monthly',
            'priority': '0.7'
        })

    return pages


# --- Sitemap Route ---
@app.route('/sitemap.xml')
def sitemap():
    """Generates and serves the sitemap.xml file for SEO."""
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    pages = build_sitemap_pages(current_date, load_blog_posts())

    sitemap_xml = render_template('sitemap.xml', pages=pages)
    return Response(sitemap_xml, mimetype='application/xml')

@app.route('/llms.txt')
def llms_txt():
    """Serve llms.txt for AI/LLM discoverability"""
    content = """# Fin Finder
> Expert surfboard fin recommendations and educational guides at finfinder.ai

## About
Fin Finder is an expert surfboard fin resource providing AI-powered personalized fin recommendations, educational guides about fin types, setups, sizing, and systems, and a blog (Finsights) with in-depth articles. Founded by Baptiste, a surfer and teacher with 40 years of experience based in San Diego, California.

## Key Pages
- [Home](https://finfinder.ai/): Overview and navigation to all resources
- [AI Fin Recommender](https://finfinder.ai/recommender): AI-powered personalized fin recommendations based on weight, skill level, board type, and wave conditions
- [All About Surfboard Fins](https://finfinder.ai/all-about-surfboard-fins): Comprehensive guide to fin anatomy (base, depth, rake, foil, cant), materials, and how fins affect performance
- [Fin Setups Compared](https://finfinder.ai/fin-setups): Comparison of single, twin, thruster (3-fin), quad (4-fin), and 5-fin configurations
- [Fin Systems](https://finfinder.ai/fin-systems): Guide to FCS, FCS II, Futures, and US Box fin systems with compatibility info
- [Longboard Fins](https://finfinder.ai/longboard-fins): Complete guide to longboard fin types (pivot, hatchet, D-fin, flex), sizing, and placement
- [Fin Sizing Guide](https://finfinder.ai/fin-sizing-guide): Weight-based sizing charts and expert recommendations for choosing the right fin size
- [Finsights Blog](https://finfinder.ai/finsights): In-depth articles about fin selection, performance, and surf equipment
- [About](https://finfinder.ai/about): About the founder and mission

## Key Facts About Surfboard Fins
- Fin sizing is primarily based on surfer weight: Under 120 lbs = XS, 120-150 lbs = Small, 150-180 lbs = Medium, 180-210 lbs = Large, Over 210 lbs = XL
- Thruster (3-fin) is the most versatile setup, suitable for all conditions and recommended for beginners
- Quad (4-fin) generates more down-the-line speed than thrusters, excelling in both small mushy waves and big powerful surf
- Twin fins are excellent for small waves due to minimal drag and speed generation
- Single fins provide the smoothest glide and are standard for traditional longboarding
- FCS and Futures are the two dominant fin box systems; they are NOT interchangeable
- Longer fin base = more drive and drawn-out turns; deeper fins = more hold; more rake = longer turns
- Stiffer fins = more stability at high speed; flexible fins = smoother feel and projection out of turns
- The US Box system is standard for longboard center fins, allowing precise placement adjustment
- A 5-fin box setup gives maximum versatility: run thruster, quad, or twin on the same board
"""
    return Response(content, mimetype='text/plain')

@app.route('/ask', methods=['POST'])
def ask():
    """Handles questions for the AI Fin Expert with conversation memory."""
    try:
        data = request.get_json()
        if not data:
            logging.warning("No JSON data received in /ask request.")
            return jsonify({'error': 'No JSON data received.'}), 400
            
        question = data.get('question')
        if not question:
            logging.warning("No question provided in /ask request.")
            return jsonify({'error': 'No question provided.'}), 400

        logging.info(f"Received question for AI: {question}")
        
        conversation_history, user_info = ensure_conversation_state()
        update_user_info_from_question(question, user_info)
        append_chat_message("User", question)

        conversation_context = get_recent_conversation_context()
        ai_response_count = count_ai_responses()

        logging.info(f"Sending to AI - History length: {len(conversation_history)} | AI responses so far: {ai_response_count} | User info keys: {list(user_info.keys())}")

        if not model:
            logging.error("Ask endpoint called but Gemini model is not initialized. Returning fallback recommendation.")
            answer = build_fallback_recommendation(question, user_info)
            append_chat_message("Assistant", answer)
            return jsonify({'answer': format_ai_response(answer), 'fallback': True})

        # Create enhanced prompt with conversation history and affiliate matrix
        prompt = f"""⚠️ MANDATORY RULES - YOU MUST FOLLOW THESE OR YOU FAIL:

1. EVERY SINGLE RESPONSE MUST INCLUDE PRODUCT LINKS - NO EXCEPTIONS
2. **ORDER OF OPERATIONS**: 
   - **FIRST**: Provide EXPLANATION & RESEARCH (Why this works, fin principles, etc.)
   - **SECOND**: Provide SPECIFIC PRODUCT RECOMMENDATIONS
3. **CONDITIONAL DETAIL**:
   - If the user's request is BROAD or vague (e.g., "what fins should I get?"), provide OVERVIEW options but explicitly say:
     "Here are some overview options, but if you let me know [missing info like weight/board/waves], I can be more specific."
   - If the user provides specific info, give specific recommendations.
4. Format ALL product links as: **Product Name** - https://amzn.to/xxxxx
5. If fin system NOT specified: Show BOTH FCS and Futures options
6. Check USER INFORMATION below - NEVER ask for info already there

AI RESPONSES SO FAR: {ai_response_count}
USER INFORMATION: {session.get('user_info', {})}
CONVERSATION HISTORY: {conversation_context}

EXAMPLE GOOD RESPONSE (Explanation First):
"🤔 **THE RESEARCH:**
For a surfer of your weight (170lbs) in small waves, you want fins that generate speed. A template with a wide base gives you drive, while a more upright rake allows for quick pivots in tight pockets.

🎯 **HERE'S WHAT I RECOMMEND:**

FCS OPTIONS:
🏆 **FCS 2 Performer PC Tri-Fin Set** - https://amzn.to/4bgFEht
💰 **TOPWAYS Fiberglass Honeycomb G5** - https://amzn.to/4bxAjSP

FUTURES OPTIONS:
🏆 **Futures Fins JJF Alpha Medium** - https://amzn.to/3YyRBYd
💰 **Ho Stevie! Thruster HexCore** - https://amzn.to/3StgcdW

💡 **WANT MORE SPECIFICITY?**
These are great all-arounders, but if you tell me if you prefer **speed** or **control**, I can narrow this down further!"

EXPERT FIN KNOWLEDGE BASE:

=== FIN DESIGN PRINCIPLES ===
• BASE: Longer base = more drive and drawn-out turns. Shorter base = quicker, sharper turns
• DEPTH/HEIGHT: Deeper fins = more hold and stability. Shallower fins = more release and looseness
• RAKE/SWEEP: More rake = longer, drawn-out turns, better for bigger waves. Less rake = tighter turning radius, better for weaker waves
• FOIL: Affects lift and speed. Flat inside = balanced performance. 50/50 = stability. 80/20 = speed
• CANT: Outward angle. More cant = more responsive in turns. Less cant = faster straight-line speed
• FLEX: Stiffer = more stability at high speeds. Flexible = smoother feel and projection out of turns

=== FIN CONFIGURATIONS - EXPERT ANALYSIS ===

SINGLE FIN:
• Best for: Smooth glide, nose riding, traditional longboarding
• Wave conditions: Small to medium, mellow waves
• Pros: Less drag, smooth drawn-out turns
• Cons: Wide turning radius, less stability

TWIN FIN:
• Best for: Speed generation, loose/skatey feel
• Wave conditions: Small to medium waves, weak surf
• Pros: Fast, maneuverable, minimal drag
• Cons: Less stable in bigger waves, can slide out

THRUSTER (3-FIN):
• Best for: All-around performance, versatility
• Wave conditions: ALL conditions - small to large
• Pros: Balanced speed/control/maneuverability
• Cons: Slightly more drag than twins/quads

QUAD (4-FIN):
• Best for: Speed AND hold, barreling waves
• Wave conditions: EXCELLENT in both small mushy waves AND big powerful waves
• Pros: Fast acceleration, great hold on rail, excels in barrels
• Cons: Can feel loose initially, different turning feel

=== LONGBOARD FIN SELECTION ===
DEFAULT RECOMMENDATION: Pivot fins (all-around performance)
• Pivot fins: Best all-around choice, good for most surfers
• D-fins: Only recommend for dedicated noseriders
• Hatchet fins: For performance longboarding
• Flex fins: For smooth, flowing style
IMPORTANT LONGBOARD LOGIC:
- For general "good longboard fin" questions → ALWAYS recommend PIVOT fins
- Only recommend D-fins if user specifically mentions "noseriding" or "nose riding"
- Never recommend D-fins as a general/budget option

=== WAVE-SPECIFIC RECOMMENDATIONS ===

SMALL/WEAK WAVES:
• Twin fins or quads (positioned forward)
• Smaller fin sizes to reduce drag
• Upright fins for quick pivots

LARGE/POWERFUL WAVES:
• Larger fins with wider base
• Less rake for control at speed
• Thrusters with stiff fins OR quads with rear fins set back
• Deeper fins for maximum hold

BARRELING/HOLLOW WAVES:
• Quads excel here - speed through sections + hold on face
• Thrusters with reliable grip
• Deeper fins with some rake

=== SIZE RECOMMENDATIONS BY WEIGHT ===
• Under 160 lbs: Small fins
• 160-180 lbs: Small-Medium fins
• 180-200 lbs: Medium-Large fins
• Over 200 lbs: Large fins

IMPORTANT: Skilled surfers in powerful waves should size UP regardless of weight

=== SKILL LEVEL CONSIDERATIONS ===

BEGINNERS:
• Thruster setup for stability
• Larger fins for control
• Avoid loose setups like twins

INTERMEDIATE:
• Can experiment with twins/quads
• Start matching fins to conditions
• Try different templates

ADVANCED:
• Fine-tune everything
• Match exact conditions
• Can handle any configuration

AFFILIATE PRODUCT MATRIX - Use these EXACT products and links when making recommendations:

=== THRUSTER SETS (3-fin) ===
Category Link: https://amzn.to/4qeLW5H

SMALL THRUSTER:
- FCS Premium: FCS II Performer Neo Glass Tri Fin Set - https://amzn.to/4jJOnee
- FCS Budget: AQUBONA G3 FCS Half Carbon - https://amzn.to/4aYK1h0
- Futures Premium: Futures Fins R4 - https://amzn.to/3HhEUeS
- Futures Budget: AQUBONA G3 Futures Half Carbon - https://amzn.to/4pNReEo

MEDIUM THRUSTER:
- FCS Premium: FCS 2 Performer PC Tri-Fin Set - https://amzn.to/4bgFEht
- FCS Budget: TOPWAYS Fiberglass Honeycomb G5 - https://amzn.to/4bxAjSP
- Futures Premium: Futures Fins JJF Alpha Medium - https://amzn.to/3YyRBYd
- Futures Budget: Ho Stevie! Thruster HexCore - https://amzn.to/3StgcdW

LARGE THRUSTER:
- FCS Premium: FCS II AM Performance Core Tri Fin Set - https://amzn.to/3Ls5NPM
- FCS Budget: BPS New Zealand G7 - https://amzn.to/49AaeQC
- Futures Premium: Futures Fins JJ-2 Large TECHFLEX - https://amzn.to/4dZLkvD
- Futures Budget: Futures Fins F8 Alpha Thruster - https://amzn.to/4qiG8YK

=== QUAD SETS (4-fin) ===
Category Link: https://amzn.to/3YX0ScR

SMALL QUAD:
- FCS Premium: FCS Carver Eco Neo Glass - https://amzn.to/45c7Eil
- FCS Budget: UPSURF S+GL Quad Set - https://amzn.to/4dCDgjU
- Futures Premium: Futures Fins Legacy F4 Small Quad - https://amzn.to/4btiR1J
- Futures Budget: UPSURF Quad Set S/M - https://amzn.to/4qXaAYB

MEDIUM QUAD:
- FCS Premium: FCS 2 Pyzel PC Air Core Quad - https://amzn.to/4jAPY5Q
- FCS Budget: Ho Stevie! Quad HexCore - https://amzn.to/3NhdOHO
- Futures Premium: Futures Fins AM1 Tech-Flex Medium - https://amzn.to/4sDcnDF
- Futures Budget: Ho Stevie! Quad HexCore - https://amzn.to/4byfoip

LARGE QUAD:
- FCS Premium: FCS II Harley Mid Tri-Quad PC Large - https://amzn.to/4sEnbBx
- FCS Budget: UPSURF K2.1 Quad Set - https://amzn.to/4kM443H
- Futures Premium: Futures Fins F8 Honeycomb Quad - https://amzn.to/3Z7ZLHC
- Futures Budget: Surf Squared 5-Fin Set - https://amzn.to/49z2yxL

=== TWIN FINS ===
Category Link: https://amzn.to/45bY5Qq

UPRIGHT TWINS:
- FCS Premium: FCS II Power Twin + 1 PG - https://amzn.to/4qRwT1I
- Futures Premium: FT1 Honeycomb Twin Fin - https://amzn.to/3LyesAb
- Budget: Surf Squared Twin/Thruster/Quad Set - https://amzn.to/4jppiDz

KEEL TWINS:
- FCS Premium: FCS II Modern Keel PG Twin - https://amzn.to/45Fzx2k
- Futures Premium: Futures Fins K2 Fiberglass Keel - https://amzn.to/49QmyNM
- Budget: Ho Stevie! Surfboard Twin Keel - https://amzn.to/4jEmFiF

=== LONGBOARD SINGLE FINS ===
Category Link: https://amzn.to/49uKID3

PIVOT FINS: 
- FCS Connect Glass Flex Single Fin - https://amzn.to/49zT5qd
- Abahub 9/10" - https://amzn.to/49wXdqL

D-FINS:
- UPSURF 10" Center D Fin - https://amzn.to/4pzvfR9
- DORSAL 8.5" Center D Fin - https://amzn.to/49JR0Iq

HATCHET FINS:
- DORSAL Modified Hatchet Pivot Polycarbonate - https://amzn.to/3Nlpe7u
- Culture Supply 9" Hatchet Noserider - https://amzn.to/43mpe2B

FLEX FINS:
- DORSAL Flex Pintail 9.75" - https://amzn.to/43lZpc0
- PACIFIC VIBRATIONS 9.25" VOLAN Flex Hull - https://amzn.to/4jt78kb

SIDE BITES: Ho Stevie! Side Bite Fins - https://amzn.to/3YDTUt2

⚠️ DEFAULT RECOMMENDATIONS (Use these if you lack info):

WHEN UNSURE, RECOMMEND MEDIUM THRUSTERS (most versatile):
FCS: **FCS 2 Performer PC Tri-Fin Set** - https://amzn.to/4bgFEht (Premium) and **TOPWAYS Fiberglass Honeycomb G5** - https://amzn.to/4bxAjSP (Budget)
FUTURES: **Futures Fins JJF Alpha Medium** - https://amzn.to/3YyRBYd (Premium) and **Ho Stevie! Thruster HexCore** - https://amzn.to/3StgcdW (Budget)

RESPONSE FORMAT - FOLLOW THIS EXACTLY:
1. START with EXPLANATION/RESEARCH (Why these fins work, principles)
2. THEN give PRODUCT RECOMMENDATIONS (Links)
3. END with CONDITIONAL OFFER (If broad request)

TEMPLATE:
🤔 **THE RESEARCH:**
[Explain using fin principles: "Based on your input, you need fins that... These fins have [base/depth/rake] which means..."]

🎯 **HERE'S WHAT I RECOMMEND:**

FCS OPTIONS:
🏆 **[Product Name]** - https://amzn.to/xxxxx
💰 **[Product Name]** - https://amzn.to/xxxxx

FUTURES OPTIONS:
🏆 **[Product Name]** - https://amzn.to/xxxxx
💰 **[Product Name]** - https://amzn.to/xxxxx

💡 **WANT MORE SPECIFICITY?**
[If broad: "Here are some overview options, but if you let me know [missing info], I can be more specific."]

FORMATTING RULES:
- Keep responses concise and well-structured
- Use bullet points (•) for lists
- Break up information into short paragraphs (2-3 sentences max)
- Get to the point quickly
- Demonstrate expert knowledge when answering technical questions
- Always relate recommendations to user's specific needs

Current question: {question}

🚨 REMEMBER: Your response MUST include product links with URLs. EXPLANATION FIRST, RECOMMENDATIONS SECOND."""
        
        response = model.generate_content(prompt)
        
        # Extract answer
        answer = ""
        if hasattr(response, 'text') and response.text:
            answer = response.text
        elif response.parts:
            answer = "".join(part.text for part in response.parts if hasattr(part, 'text'))
        
        if not answer:
            answer = "I apologize, I'm having trouble generating a response. Could you please rephrase your question?"
            logging.warning("Gemini generated an empty or invalid response.")
        
        # VALIDATION: Check if response includes product links
        if 'amzn.to' not in answer:
            logging.warning("⚠️ AI response missing product links! Adding default recommendations.")
            answer += "\n\n🎯 HERE'S WHAT I RECOMMEND:\n\nFCS OPTIONS:\n🏆 **FCS 2 Performer PC Tri-Fin Set** - https://amzn.to/4bgFEht\n💰 **TOPWAYS Fiberglass Honeycomb G5** - https://amzn.to/4bxAjSP\n\nFUTURES OPTIONS:\n🏆 **Futures Fins JJF Alpha Medium** - https://amzn.to/3YyRBYd\n💰 **Ho Stevie! Thruster HexCore** - https://amzn.to/3StgcdW\n\nThese are versatile all-around fins that work for most surfers!"
        
        # Add AI response to history
        append_chat_message("Assistant", answer)
        
        # Log session state after AI response
        logging.info(f"✅ SESSION UPDATED - Total messages: {len(session['conversation_history'])} | User info: {session.get('user_info', {})}")
        
        # Format the response before returning
        formatted_answer = format_ai_response(answer)
        
        logging.info(f"AI Answer (first 200 chars): {answer[:200]}...")

        return jsonify({'answer': formatted_answer})

    except Exception as e:
        logging.error(f"Error in /ask endpoint. Returning fallback recommendation: {e}", exc_info=True)
        try:
            fallback_question = locals().get('question', '')
            fallback_user_info = session.get('user_info', {}) if session else {}
            answer = build_fallback_recommendation(fallback_question, fallback_user_info)
            if 'conversation_history' in session:
                append_chat_message("Assistant", answer)
            return jsonify({'answer': format_ai_response(answer), 'fallback': True})
        except Exception as fallback_error:
            logging.error(f"Fallback recommendation failed: {fallback_error}", exc_info=True)
            return jsonify({'error': 'Fin Finder is temporarily unavailable. Please try again shortly.'}), 503
    
# --- Main Execution ---
if __name__ == '__main__':
    app.run(debug=True)
