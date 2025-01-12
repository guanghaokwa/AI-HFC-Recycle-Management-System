function navigateTo(value) {
    if (value) {
        window.location.href = value;
    }
}

function sendMessage() {
    const input = document.getElementById('chat-input');
    const chatDisplay = document.getElementById('chat-display');

    if (input.value.trim()) {
        const userMessage = document.createElement('div');
        userMessage.className = 'message user-message';
        userMessage.textContent = input.value;
        chatDisplay.appendChild(userMessage);

        const botMessage = document.createElement('div');
        botMessage.className = 'message bot-message';
        botMessage.textContent = "I'm sorry, I didn't understand that.";
        chatDisplay.appendChild(botMessage);

        input.value = '';
        chatDisplay.scrollTop = chatDisplay.scrollHeight;
    }
}
