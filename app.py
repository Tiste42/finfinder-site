from flask import Flask, render_template, request, jsonify, redirect, url_for, session, Response, send_from_directory
import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging
import datetime
import re
import json

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO)

# --- Flask App Initialization ---
app = Flask(__name__) 

@app.route('/robots.txt')
def robots_txt():
    return send_from_directory(app.static_folder, 'robots.txt')
app.secret_key = 'your-secret-key-for-sessions-change-this-to-something-random'

# Define the base URL for your site
SITE_URL = "https://finfinder.ai"

# --- Load Environment Variables & Configure Gemini ---
model = None # Initialize model as None
try:
    current_dir = os.getcwd()
    logging.info(f"Current Working Directory: {current_dir}")
    dotenv_path = os.path.join(current_dir, '.env')
    logging.info(f"Looking for .env file at: {dotenv_path}")

    if os.path.exists(dotenv_path):
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

# --- Blog Posts Helper Functions ---
def load_blog_posts():
    """Load blog posts from JSON file"""
    try:
        blog_posts_path = os.path.join(os.getcwd(), 'blog_posts.json')
        if os.path.exists(blog_posts_path):
            with open(blog_posts_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('posts', [])
        return []
    except Exception as e:
        logging.error(f"Error loading blog posts: {e}")
        return []

def get_post_by_slug(slug):
    """Get a specific blog post by slug"""
    posts = load_blog_posts()
    for post in posts:
        if post.get('slug') == slug:
            return post
    return None

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

# --- Context Processor to inject active_page based on request path ---
@app.context_processor
def inject_active_page():
    """Injects the active_page variable into all templates based on the current route."""
    if request.path == '/':
        return {'active_page': 'home'}
    elif request.path == '/recommender':
        return {'active_page': 'recommender'}
    elif request.path == '/all-about-surfboard-fins':
        return {'active_page': 'all_about_fins'}
    elif request.path == '/fin-setups':
        return {'active_page': 'fin_setups'}
    elif request.path == '/fin-systems':
        return {'active_page': 'fin_systems'}
    elif request.path == '/longboard-fins/':
        return {'active_page': 'longboard_fins'}
    elif request.path == '/fin-sizing-guide':
        return {'active_page': 'fin_sizing_guide'}
    elif request.path == '/about':
        return {'active_page': 'about'}
    elif request.path == '/finsights' or request.path.startswith('/finsights/'):
        return {'active_page': 'finsights'}
    return {'active_page': None}

# --- Helper Function for AI Response Formatting ---
def format_ai_response(response_text):
    """Format AI response for proper HTML display"""
    formatted = response_text
    
    # FIRST: Convert product name + link patterns to clean hyperlinks
    # Pattern: **Product Name** - https://amzn.to/xxx
    # Result: <strong><a href="link">Product Name (Amazon)</a></strong>
    formatted = re.sub(
        r'\*\*([^*]+?)\*\*\s*[-–—]\s*(https://amzn\.to/\w+)',
        r'<strong><a href="\2" target="_blank" rel="noopener noreferrer">\1 (Amazon)</a></strong>',
        formatted
    )
    
    # Pattern: Product Name - https://amzn.to/xxx (without bold markers)
    formatted = re.sub(
        r'([A-Z][^-\n]+?)\s*[-–—]\s*(https://amzn\.to/\w+)',
        r'<strong><a href="\2" target="_blank" rel="noopener noreferrer">\1 (Amazon)</a></strong>',
        formatted
    )
    
    # Pattern: [View on Amazon link] or similar text before URL
    formatted = re.sub(
        r'(?:View on Amazon link|View on Amazon|Browse All[^:]*?)(?:\s*[:]\s*|\s+)(https://amzn\.to/\w+)',
        r'<strong><a href="\1" target="_blank" rel="noopener noreferrer">View on Amazon</a></strong>',
        formatted
    )
    
    # Catch any remaining standalone Amazon links and make them clickable
    formatted = re.sub(
        r'(?<![">])(https://amzn\.to/\w+)(?![<"])',
        r'<a href="\1" target="_blank" rel="noopener noreferrer">\1</a>',
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

# --- Route Definitions ---
@app.route('/')
def home():
    """Renders the homepage."""
    return render_template('index.html')

@app.route('/all-about-surfboard-fins')
def all_about_fins():
    """Renders the 'All About Surfboard Fins' page."""
    return render_template('all_about_fins.html')

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
    # Sort posts by date (newest first)
    posts_sorted = sorted(posts, key=lambda x: x.get('date_published', x.get('date', '')), reverse=True)
    return render_template('finsights.html', posts=posts_sorted)

@app.route('/finsights/<slug>')
def blog_post(slug):
    """Renders a specific blog post page."""
    post = get_post_by_slug(slug)
    if not post:
        return render_template('404.html'), 404
    
    related_posts = get_related_posts(post)
    return render_template('blog_post.html', post=post, related_posts=related_posts)

# --- Sitemap Route ---
@app.route('/sitemap.xml')
def sitemap():
    """Generates and serves the sitemap.xml file for SEO."""
    pages = [
        {'loc': f"{SITE_URL}/", 'lastmod': '2025-05-29', 'changefreq': 'daily', 'priority': '1.0'},
        {'loc': f"{SITE_URL}/recommender", 'lastmod': '2025-05-29', 'changefreq': 'weekly', 'priority': '0.9'},
        {'loc': f"{SITE_URL}/finsights", 'lastmod': '2025-11-06', 'changefreq': 'weekly', 'priority': '0.9'},
        {'loc': f"{SITE_URL}/all-about-surfboard-fins", 'lastmod': '2025-05-29', 'changefreq': 'monthly', 'priority': '0.8'},
        {'loc': f"{SITE_URL}/fin-setups", 'lastmod': '2025-05-29', 'changefreq': 'monthly', 'priority': '0.8'},
        {'loc': f"{SITE_URL}/fin-systems", 'lastmod': '2025-05-29', 'changefreq': 'monthly', 'priority': '0.8'},
        {'loc': f"{SITE_URL}/longboard-fins", 'lastmod': '2025-05-29', 'changefreq': 'monthly', 'priority': '0.8'},
        {'loc': f"{SITE_URL}/fin-sizing-guide", 'lastmod': '2025-05-29', 'changefreq': 'monthly', 'priority': '0.8'},
        {'loc': f"{SITE_URL}/about", 'lastmod': '2025-05-29', 'changefreq': 'monthly', 'priority': '0.7'},
    ]
    
    # Add blog posts to sitemap
    blog_posts = load_blog_posts()
    for post in blog_posts:
        pages.append({
            'loc': f"{SITE_URL}/finsights/{post.get('slug')}",
            'lastmod': post.get('date_modified', post.get('date_published', post.get('date', '2025-11-06'))),
            'changefreq': 'monthly',
            'priority': '0.7'
        })

    sitemap_xml = render_template('sitemap.xml', pages=pages)
    return Response(sitemap_xml, mimetype='application/xml')

@app.route('/ask', methods=['POST'])
def ask():
    """Handles questions for the AI Fin Expert with conversation memory."""
    if not model:
        logging.error("Ask endpoint called but Gemini model is not initialized.")
        return jsonify({'error': 'Generative model not initialized. Please check server logs and API key configuration.'}), 500
    
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
        
        # Initialize or get conversation history
        if 'conversation_history' not in session:
            session['conversation_history'] = []
            session['user_info'] = {}
            logging.info("🔵 NEW SESSION: Initialized conversation history and user info")
        else:
            logging.info(f"🟢 EXISTING SESSION: {len(session.get('conversation_history', []))} messages in history")
            logging.info(f"🟢 USER INFO STORED: {session.get('user_info', {})}")
        
        # Extract user information from the question
        question_lower = question.lower()
        
        # Extract weight
        weight_match = re.search(r'(\d+)\s*(?:lbs?|pounds?|kg)', question_lower)
        if weight_match:
            session['user_info']['weight'] = weight_match.group(1)
            logging.info(f"Stored user weight: {weight_match.group(1)}")
        
        # Extract fin system (FCS or Futures)
        if 'fcs' in question_lower and 'futures' not in question_lower:
            session['user_info']['fin_system'] = 'FCS'
            logging.info("Stored fin system: FCS")
        elif 'futures' in question_lower or 'future' in question_lower:
            session['user_info']['fin_system'] = 'Futures'
            logging.info("Stored fin system: Futures")
        
        # Extract skill level
        if re.search(r'\b(beginner|beginning|just start|learning|new to)', question_lower):
            session['user_info']['skill_level'] = 'beginner'
            logging.info("Stored skill level: beginner")
        elif re.search(r'\b(intermediate|getting better|catching waves)', question_lower):
            session['user_info']['skill_level'] = 'intermediate'
            logging.info("Stored skill level: intermediate")
        elif re.search(r'\b(advanced|experienced|good surfer|barreled|barrels)', question_lower):
            session['user_info']['skill_level'] = 'advanced'
            logging.info("Stored skill level: advanced")
        elif re.search(r'\b(pro|professional|expert|airs?|boosting)', question_lower):
            session['user_info']['skill_level'] = 'pro'
            logging.info("Stored skill level: pro")
        
        # Extract board type
        if re.search(r'\b(shortboard|short board|performance board)', question_lower):
            session['user_info']['board_type'] = 'shortboard'
            logging.info("Stored board type: shortboard")
        elif re.search(r'\b(fish)\b', question_lower):
            session['user_info']['board_type'] = 'fish'
            logging.info("Stored board type: fish")
        elif re.search(r'\b(longboard|long board|noserider|nose rider)', question_lower):
            session['user_info']['board_type'] = 'longboard'
            logging.info("Stored board type: longboard")
        elif re.search(r'\b(hybrid|groveler)', question_lower):
            session['user_info']['board_type'] = 'hybrid'
            logging.info("Stored board type: hybrid")
        elif re.search(r'\b(mid.?length|funboard|fun board)', question_lower):
            session['user_info']['board_type'] = 'mid-length'
            logging.info("Stored board type: mid-length")
        elif re.search(r'\b(gun|big wave)', question_lower):
            session['user_info']['board_type'] = 'gun'
            logging.info("Stored board type: gun")
        
        # Extract wave conditions
        if re.search(r'\b(small|weak|mushy|slow|1.?2.?ft|knee high)', question_lower):
            session['user_info']['wave_conditions'] = 'small/weak'
            logging.info("Stored wave conditions: small/weak")
        elif re.search(r'\b(big|large|powerful|overhead|heavy|barreling|hollow)', question_lower):
            session['user_info']['wave_conditions'] = 'big/powerful'
            logging.info("Stored wave conditions: big/powerful")
        
        # Log complete user info after extraction
        logging.info(f"📊 COMPLETE USER INFO AFTER EXTRACTION: {session.get('user_info', {})}")
        
        # Add current question to history
        session['conversation_history'].append(f"User: {question}")
        
        # Build context from conversation history (last 10 messages)
        conversation_context = "\n".join(session['conversation_history'][-10:])
        
        logging.info(f"📝 SENDING TO AI - History length: {len(session['conversation_history'])} | User info keys: {list(session.get('user_info', {}).keys())}")
        
                # Create enhanced prompt with conversation history and affiliate matrix
        prompt = f"""You are an expert surfboard fin advisor with deep technical knowledge. Your goal is to help surfers find the perfect fins using both expert knowledge and specific product recommendations.

🚨 CRITICAL MEMORY RULES - FOLLOW THESE STRICTLY:
1. BEFORE asking ANY question, CHECK the USER INFORMATION dictionary below
2. NEVER ask for information that's already stored in USER INFORMATION
3. If fin_system is stored, ONLY recommend that system (FCS or Futures)
4. If weight is stored, use it for sizing - don't ask again
5. If skill_level is stored, factor it in - don't ask again
6. If board_type is stored, tailor recommendations - don't ask again
7. Review the CONVERSATION HISTORY to see what the user has already told you

🎯 RECOMMENDATION STRATEGY - ALWAYS FOLLOW THIS:
1. ALWAYS provide at least one product recommendation with every response
2. Give BOTH FCS and Futures options UNLESS user has specified their system
3. Format product links as: **Product Name** - https://amzn.to/xxxxx
4. AFTER giving recommendations, you may ask clarifying questions to refine further
5. NEVER just ask questions without providing product recommendations first

CONVERSATION HISTORY:
{conversation_context}

USER INFORMATION STORED: {session.get('user_info', {})}
↑↑↑ CHECK THIS BEFORE ASKING ANY QUESTIONS ↑↑↑

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
Category Link: https://amzn.to/3SZ0tDp

SMALL THRUSTER:
- FCS Budget: AQUBONA G3 FCS Half Carbon - https://amzn.to/4jLwp9D
- Futures Premium: Futures Fins R4 - https://amzn.to/3HhEUeS
- Futures Budget: AQUBONA G3 Futures Half Carbon - https://amzn.to/4mAOee9

MEDIUM THRUSTER:
- FCS Premium: FCS 2 Performer PC Tri-Fin Set - https://amzn.to/3T5pcG8
- FCS Budget: TOPWAYS Fiberglass Honeycomb G5 - https://amzn.to/3HldRiP
- Futures Premium: Futures Fins JJF Alpha Medium - https://amzn.to/4ktBaWj
- Futures Budget: Ho Stevie! Thruster HexCore - https://amzn.to/3StgcdW

LARGE THRUSTER:
- FCS Premium: FCS II AM Performance Core - https://amzn.to/43yxNWN
- FCS Budget: BPS New Zealand G7 - https://amzn.to/4mEBi6T
- Futures Premium: Futures Fins JJ-2 Large TECHFLEX - https://amzn.to/4dZLkvD
- Futures Budget: Futures Fins F8 Alpha Thruster - https://amzn.to/4mEBzqr

=== QUAD SETS (4-fin) ===
Category Link: https://amzn.to/4jryKWM

SMALL QUAD:
- FCS Premium: FCS Carver Eco Neo Glass - https://amzn.to/45C41Dd
- FCS Budget: UPSURF S+GL Quad Set - https://amzn.to/4dCDgjU
- Futures Premium: Futures Fins Legacy F4 Small - https://amzn.to/4jLxC0F
- Futures Budget: UPSURF Quad Set S/M - https://amzn.to/3FqFC99

MEDIUM QUAD:
- FCS Premium: FCS 2 Pyzel PC Air Core Quad - https://amzn.to/43DlnNv
- FCS Budget: Ho Stevie! Quad HexCore - https://amzn.to/3FFkdsJ
- Futures Premium: Futures Fins AM1 Tech-Flex - https://amzn.to/3ZbFnFv

LARGE QUAD:
- FCS Premium: FCS II Matt Biolos Tri-Quad - https://amzn.to/4dEKGU5
- FCS Budget: UPSURF K2.1 Quad Set - https://amzn.to/4kM443H
- Futures Premium: Futures Fins F8 Honeycomb Quad - https://amzn.to/3Z7ZLHC
- Futures Budget: Surf Squared 5-Fin Set - https://amzn.to/4kn4vSn

=== TWIN FINS ===
Category Link: https://amzn.to/3ZGiZUQ

UPRIGHT TWINS:
- FCS Premium: FCS II Power Twin PG - https://amzn.to/3Fxufw2
- Futures Premium: FT1 Honeycomb Twin - https://amzn.to/3HiVCdI
- Budget: Surf Squared Twin/Thruster/Quad Set - https://amzn.to/4jppiDz

KEEL TWINS:
- FCS Premium: FCS II Modern Keel PG Twin - https://amzn.to/4mL3m8S
- Futures Premium: Futures Fins K2 Fiberglass Keel - https://amzn.to/43kuJig
- Budget: Ho Stevie! Surfboard Twin Keel - https://amzn.to/4jrpS3q

=== LONGBOARD SINGLE FINS ===
Category Link: https://amzn.to/4dMqGyW

PIVOT FINS: 
- FCS Connect Glass Flex - https://amzn.to/3HzUG4I
- Abahub 9/10" - https://amzn.to/3ZI82SG

D-FINS:
- UPSURF 10" Center D Fin - https://amzn.to/4kD04mF
- DORSAL 8.5" Center D Fin - https://amzn.to/3Z8k3Rg

HATCHET FINS:
- DORSAL Modified Hatchet Pivot - https://amzn.to/4kgHYq5
- Culture Supply 9" Hatchet Noserider - https://amzn.to/43mpe2B

FLEX FINS:
- DORSAL Flex Pintail 9.75" - https://amzn.to/43IZpc0
- PACIFIC VIBRATIONS 9.25" VOLAN Flex - https://amzn.to/4jt78kb

SIDE BITES: Ho Stevie! Side Bite Fins - https://amzn.to/452OyvQ

DECISION LOGIC:
1. CHECK USER INFORMATION first - use stored data, don't re-ask
2. ALWAYS give product recommendations - never just ask questions
3. If fin_system is NOT specified, provide BOTH FCS and Futures options
4. For weight-based sizing: Consider both weight AND skill level. Skilled surfers in powerful waves should size UP
5. ALWAYS consider wave conditions when recommending
6. Remember: Quads are EXCELLENT in big waves (not just small waves)
7. For educational questions, provide expert knowledge WITH product examples

RESPONSE FORMAT when making recommendations:
[Start with recommendations immediately]

🎯 MY TOP PICKS:

FCS OPTIONS:
🏆 Premium: **[Product Name]** - https://amzn.to/xxxxx
💰 Budget: **[Product Name]** - https://amzn.to/xxxxx

FUTURES OPTIONS:
🏆 Premium: **[Product Name]** - https://amzn.to/xxxxx  
💰 Budget: **[Product Name]** - https://amzn.to/xxxxx

[Brief explanation of why these fins would work]

[OPTIONAL: "I can give you more specific recommendations if you tell me [specific info needed]"]

FORMATTING RULES:
- Keep responses concise and well-structured
- Use bullet points (•) for lists
- Break up information into short paragraphs (2-3 sentences max)
- Get to the point quickly
- Demonstrate expert knowledge when answering technical questions
- Always relate recommendations to user's specific needs

Based on the conversation history and current question, provide expert advice. Current question: {question}"""
        
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
        
        # Add AI response to history
        session['conversation_history'].append(f"Assistant: {answer}")
        
        # Log session state after AI response
        logging.info(f"✅ SESSION UPDATED - Total messages: {len(session['conversation_history'])} | User info: {session.get('user_info', {})}")
        
        # Format the response before returning
        formatted_answer = format_ai_response(answer)
        
        logging.info(f"AI Answer (first 200 chars): {answer[:200]}...")

        return jsonify({'answer': formatted_answer})

    except Exception as e:
        logging.error(f"Error in /ask endpoint: {e}", exc_info=True)
        return jsonify({'error': f'An internal error occurred: {str(e)}'}), 500
    
# --- Main Execution ---
if __name__ == '__main__':
    app.run(debug=True)