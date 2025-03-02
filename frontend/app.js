/**
 * Appends a formatted chat message to the chat display.
 *
 * Creates a new message element styled based on the sender. If the sender is "You", the message
 * is displayed with user styling; otherwise, it uses bot styling. The sender's name is emphasized,
 * and the complete message is added to the chat box, which is then auto-scrolled to reveal the new entry.
 *
 * @param {string} text - The content of the message to display.
 * @param {string} sender - The name of the message sender, used to determine styling.
 */
function addMessage(text, sender) {
    let chatBox = document.getElementById("chat-box");
    let messageElement = document.createElement("div");

    messageElement.classList.add("message", sender === "You" ? "user-message" : "bot-message");
    messageElement.innerHTML = `<strong>${sender}:</strong> ${text}`;

    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll
}

// Auto-expand textarea when typing
document.getElementById("user-input").addEventListener("input", function () {
    this.style.height = "40px"; // Reset height
    this.style.height = Math.min(this.scrollHeight, 120) + "px"; // Expand but limit max height
});

/**
 * Sends a chat message to the backend and updates the chat interface with both the user's input and the bot's response.
 *
 * This asynchronous function retrieves trimmed text from the "user-input" textarea. If the input is non-empty,
 * it displays the user's message, resets the textarea's content and height, and sends a POST request to the backend
 * endpoint with the message encapsulated in a JSON object. Upon receiving a successful JSON response, it displays the
 * bot's answer. In case of a fetch or parsing error, an error message is displayed instead.
 */
async function sendMessage() {
    let userInput = document.getElementById("user-input");
    let text = userInput.value.trim();
    
    if (!text) return;
    
    addMessage(text, "You"); // Display user message
    userInput.value = "";
    userInput.style.height = "40px"; // Reset textarea height after sending

    try {
        let response = await fetch("http://127.0.0.1:8000/chat/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question: text })
        });

        let data = await response.json();
        addMessage(data.answer, "Bot"); // Display bot response
    } catch (error) {
        addMessage("Error: Unable to fetch response", "Bot");
    }
}
