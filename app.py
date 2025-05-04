from flask import Flask, render_template, request

app = Flask(__name__)

# Route for the main page (displaying the form)
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the form submission
@app.route('/ask', methods=['POST'])
def ask():
    # Get the question from the submitted form data
    user_question = request.form['user_question']

    # For now, just print it to the terminal
    print(f"Received question: {user_question}")

    # You could eventually process the question and return a response page
    # For now, let's just redirect back to the main page or show a simple confirmation
    # return render_template('response.html', question=user_question, answer="Thinking...")
    return f"Okay, I received your question: '{user_question}'. We'll process this later."

if __name__ == '__main__':
    app.run(debug=True)
    