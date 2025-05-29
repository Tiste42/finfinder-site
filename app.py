from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging
import datetime
import re

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO)

# --- Flask App Initialization ---
app = Flask(__name__) 
app.secret_key = 'your-secret-key-for-sessions-change-this-to-something-random'

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
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        logging.info("Gemini model initialized.")

except KeyError:
    logging.error("GEMINI_API_KEY not found in environment variables (KeyError). Ensure it's in your .env file.")
    model = None
except Exception as e:
    logging.error(f"An unexpected error occurred during Gemini API configuration: {e}")
    model = None

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
    return {'active_page': None}

# --- Helper Function for AI Response Formatting ---
def format_ai_response(response_text):
    """Format AI response for proper HTML display"""
    formatted = response_text
    
    # Convert **text** to HTML bold
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
        
        # Check if user is providing info about themselves
        weight_match = re.search(r'(\d+)\s*(?:lbs?|pounds?|kg)', question.lower())
        if weight_match:
            session['user_info']['weight'] = weight_match.group(1)
            logging.info(f"Stored user weight: {weight_match.group(1)}")
        
        # Add current question to history
        session['conversation_history'].append(f"User: {question}")
        
        # Build context from conversation history (last 10 messages)
        conversation_context = "\n".join(session['conversation_history'][-10:])
        
        # Create enhanced prompt with conversation history
        prompt = f"""You are an expert surfboard fin advisor. You have access to the following conversation history:

{conversation_context}

User Information: {session.get('user_info', {})}

Based on this context and any previous information the user has shared, answer their current question: {question}

FORMATTING RULES - VERY IMPORTANT:
IMPORTANT: When recommending fins, DO NOT mention specific brand names or models (like FCS II Carver, Accelerator, etc.). Instead recommend general categories like "medium-sized thruster fins" or "performance longboard fin".
- Keep responses concise and well-structured
- Use bullet points (•) for lists
- Break up information into short paragraphs (2-3 sentences max)
- For fin recommendations, use this format:
  • Fin Type: [General category, not brand name]
  • Size: [Size recommendation]
  • Why: [Brief reason]
  
- Avoid long walls of text
- Get to the point quickly
- Use line breaks between different topics

Content guidelines:
- Remember user's weight, board type, skill level from previous messages
- Provide specific fin characteristics but avoid brand names
- Stay focused on surfboard fins
- If someone just says a number (like "200 lbs"), understand they're giving their weight"""
        
        response = model.generate_content(prompt)
        
        # Extract answer
        answer = ""
        if hasattr(response, 'text') and response.text:
            answer = response.text
        elif response.parts:
            answer = "".join(part.text for part in response.parts if hasattr(part, 'text'))
        
        if not answer:
            answer = "Sorry, I could not generate a valid response at this time."
            logging.warning("Gemini generated an empty or invalid response.")
        
        # Add AI response to history
        session['conversation_history'].append(f"Assistant: {answer}")
        
        # Format the response before returning
        formatted_answer = format_ai_response(answer)
        
        logging.info(f"AI Answer: {answer}")

        return jsonify({'answer': formatted_answer})

    except Exception as e:
        logging.error(f"Error in /ask endpoint: {e}", exc_info=True)
        return jsonify({'error': f'An internal error occurred: {str(e)}'}), 500
    
# --- Main Execution ---
if __name__ == '__main__':
    app.run(debug=True)