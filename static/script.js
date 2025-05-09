// Wait for the HTML document to be fully loaded before running the script
document.addEventListener('DOMContentLoaded', () => {
    console.log("Fin Finder Javascript loaded!"); // Keep your original log

    // Get references to the HTML elements using their new IDs
    const askForm = document.getElementById('ask-form');
    const questionInput = document.getElementById('question-input');
    const responseArea = document.getElementById('response-area');

    // Check if all elements were found
    if (!askForm || !questionInput || !responseArea) {
        console.error("Error: Could not find one or more required HTML elements (form, input, or response area). Check IDs in index.html.");
        return; // Stop if elements are missing
    }

    // Add an event listener to the form for the 'submit' event
    askForm.addEventListener('submit', (event) => {
        event.preventDefault(); // IMPORTANT: Prevent the default browser form submission

        const question = questionInput.value.trim(); // Get the question text and remove extra whitespace

        if (!question) {
            responseArea.textContent = 'Please enter a question.'; // Basic validation
            return; // Stop if the question is empty
        }

        // Display a loading message
        responseArea.textContent = 'Asking the AI...'; 
        responseArea.style.color = '#666'; // Optional: style the loading message

        // Use fetch to send the data to the Flask backend
        fetch('/ask', {
            method: 'POST',
            headers: {
                // THIS IS THE CRUCIAL PART: Tell the server we're sending JSON
                'Content-Type': 'application/json', 
            },
            // Convert the JavaScript object { question: question } into a JSON string
            body: JSON.stringify({ question: question }) 
        })
        .then(response => {
            // Check if the response from the server is okay (status code 200-299)
            if (!response.ok) {
                // If not okay, try to parse the error message from the server's JSON response
                return response.json().then(err => {
                    // Throw an error that includes the server's error message
                    throw new Error(`Server error: ${response.status} ${response.statusText}. ${err.error || 'No specific error message provided.'}`);
                }).catch(() => {
                    // If parsing the JSON error fails, throw a generic error
                    throw new Error(`Server error: ${response.status} ${response.statusText}. Could not parse error response.`);
                });
            }
            // If the response is okay, parse the JSON body
            return response.json(); 
        })
        .then(data => {
            // Handle the successful response from the server
            if (data.response) {
                responseArea.textContent = data.response; // Display the AI's answer
                responseArea.style.color = '#333'; // Reset text color
            } else if (data.error) {
                // Handle cases where the server responded 200 OK but sent an error payload
                responseArea.textContent = `Error: ${data.error}`;
                responseArea.style.color = 'red'; 
            } else {
                 // Handle unexpected successful response format
                 responseArea.textContent = 'Received an unexpected response format from the server.';
                 responseArea.style.color = 'orange';
            }
        })
        .catch(error => {
            // Handle network errors or errors thrown from the .then blocks
            console.error('Fetch Error:', error);
            responseArea.textContent = `Failed to get response: ${error.message}`;
            responseArea.style.color = 'red'; 
        });
    });
});