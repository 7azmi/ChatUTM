/**
 * Retrieves user input, sends it to the backend, and updates the chat display.
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
 * Handles sending user input and getting a response from the backend.
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
