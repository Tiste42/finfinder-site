from flask import Flask, render_template, request, jsonify, redirect, url_for
import google.generativeai as genai
import os
from dotenv import load_dotenv
import logging
import datetime # Ensure this is imported

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO)

# --- Flask App Initialization ---
app = Flask(__name__)

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
    return {'now': datetime.datetime.utcnow()} # Use datetime.datetime here

# --- Route Definitions ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fundamentals')
def fundamentals():
    return render_template('fundamentals.html')

@app.route('/setups')
def setups():
    return render_template('setups.html')

@app.route('/longboards')
def longboards():
    return render_template('longboards.html')

@app.route('/fin-systems')
def fin_systems():
    return render_template('fin_systems.html')

@app.route('/recommender')
def recommender_page():
    return render_template('recommender.html')

@app.route('/ask', methods=['POST'])
def ask():
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
        
        prompt = f"You are a surfboard fin expert. Answer the following question about surfboard fins clearly and concisely. If the question is not about surfboard fins, politely state that you can only answer questions about surfboard fins. Question: {question}"
        
        response = model.generate_content(prompt)
        
        answer = response.text if hasattr(response, 'text') else "Sorry, I could not generate a valid response."
        logging.info(f"AI Answer: {answer}")

        return jsonify({'answer': answer})

    except Exception as e:
        logging.error(f"Error in /ask endpoint: {e}", exc_info=True)
        return jsonify({'error': f'An internal error occurred: {str(e)}'}), 500

# --- Main Execution ---
if __name__ == '__main__':
    app.run(debug=True)