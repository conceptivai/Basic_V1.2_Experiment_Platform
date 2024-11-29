document.getElementById('send-button').addEventListener('click', sendMessage);
document.getElementById('message-input').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

async function sendMessage() {
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value.trim();

    if (!message) return;

    // Display the user's message
    displayMessage('user', message);

    // Clear the input field
    messageInput.value = '';

    // Show typing indicator
    const typingIndicator = document.createElement('div');
    typingIndicator.classList.add('gpt', 'typing');
    typingIndicator.textContent = 'Typing...';
    displayMessageElement(typingIndicator);

    try {
        // Send the message to the Flask server
        const response = await fetch('http://127.0.0.1:5000/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message }),
        });

        const data = await response.json();

        // Remove typing indicator
        removeTypingIndicator();

        if (data.reply) {

            displayTypingEffect('gpt', data.reply);
            


            // Display GPT's reply with typing effect
            // displayTypingEffect('gpt', data.reply);
        } else {
            // Handle errors if no reply
            displayMessage('gpt', 'Sorry, something went wrong.');
        }
    } catch (error) {
        console.error('Error:', error);
        removeTypingIndicator();
        displayMessage('gpt', 'An error occurred while processing your request.');
    }
}


function displayMessage(sender, text) {
    const chatBox = document.getElementById('chat-box');

    const messageDiv = document.createElement('div');
    messageDiv.classList.add(sender);
    messageDiv.textContent = text;

    displayMessageElement(messageDiv);
}

function displayMessageElement(element) {
    const chatBox = document.getElementById('chat-box');

    chatBox.appendChild(element);

    // Scroll to the bottom of the chat
    chatBox.scrollTop = chatBox.scrollHeight;
}

function removeTypingIndicator() {
    const typingIndicator = document.querySelector('.typing');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

function displayTypingEffect(sender, text) {
    const chatBox = document.getElementById('chat-box');

    const messageDiv = document.createElement('div');
    messageDiv.classList.add(sender);
    messageDiv.textContent = '';

    displayMessageElement(messageDiv);

    let index = 0;

    function type() {
        if (index < text.length) {
            messageDiv.textContent += text.charAt(index);
            index++;
            setTimeout(type, 50); // Typing speed
        }
    }

    type();
}
