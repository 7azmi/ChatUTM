/**
 * Retrieves user input, sends it to the backend, and updates the chat display.
 *
 * The function first obtains the text from the HTML element with the ID "user-input". If the input is empty, it exits early.
 * Otherwise, it appends the user's message to the "chat-box" element, then sends a POST request to the backend endpoint
 * at "http://127.0.0.1:8000/chat/ask" with the input as a JSON payload. Upon receiving the response, it extracts the answer
 * from the JSON data and appends it to the "chat-box" as the bot's reply, and finally clears the user input field.
 */
async function sendMessage() {
    let userInput = document.getElementById("user-input").value;
    if (!userInput) return;

    let chatBox = document.getElementById("chat-box");
    chatBox.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;

    // Send request to backend
    let response = await fetch("http://127.0.0.1:8000/chat/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: userInput })
    });

    let data = await response.json();
    chatBox.innerHTML += `<p><strong>Bot:</strong> ${data.answer}</p>`;

    document.getElementById("user-input").value = "";
}
