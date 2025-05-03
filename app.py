from flask import Flask, render_template

# Create a Flask application instance
app = Flask(__name__)

# Define a route for the homepage ('/')
@app.route('/')
def index():
    # Render the index.html template
    return render_template('index.html')

# Run the app if this script is executed directly
if __name__ == '__main__':
    # debug=True allows auto-reloading and provides error messages in the browser
    app.run(debug=True)
    