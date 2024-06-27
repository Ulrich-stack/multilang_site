// Cette fonction gère l'ouverture et la fermeture du chatbot
function toggleChatbot() {
    var chatbot = document.getElementById("chat-bubble");
    var chat = document.getElementById("chat");
    var exit = document.getElementById("exit");

    // Alterne l'affichage du chatbot et des icônes d'ouverture/fermeture
    if (chatbot.style.display === "none") {
        chatbot.style.display = "block";
        chat.style.display = "none";
        exit.style.display = "block";
    } else {
        chatbot.style.display = "none";
        chat.style.display = "block";
        exit.style.display = "none";
    }
}

// Cette fonction nettoie le texte en supprimant les symboles #
function cleanText(text) {
    return text.replace(/[#]+/g, "").trim();
}

// Cette fonction crée un élément de message selon l'expéditeur et applique les styles définis dans le fichier CSS
function createChatMessage({ sender, message }) {
    // Crée l'élément principal du message
    const messageElement = document.createElement("div");
    messageElement.classList.add("message");
    messageElement.dataset.sender = sender;

    // Crée l'élément de contenu du message
    const messageContentElement = document.createElement("div");

    // Applique des classes différentes selon l'expéditeur (chatbot ou utilisateur)
    if (sender === "chatbot") {
        messageContentElement.classList.add("chatbot-message");
    } else {
        messageContentElement.classList.add("user-message");
    }

    // Crée l'élément pour l'avatar et le nom d'utilisateur
    const avatarUsernameElement = document.createElement("div");
    avatarUsernameElement.classList.add("avatar-username");

    // Si l'expéditeur est le chatbot, ajoute une icône de robot
    if (sender === "chatbot") {
        const chatbotImage = document.createElement("span");
        chatbotImage.classList.add("material-symbols-outlined");
        chatbotImage.textContent = "smart_toy";
        avatarUsernameElement.appendChild(chatbotImage);
        messageContentElement.appendChild(avatarUsernameElement);
    }

    // Crée l'élément pour le texte du message
    const messageTextElement = document.createElement("p");
    messageTextElement.classList.add("message-text");

    // Applique des classes de style différentes selon l'expéditeur
    if (sender === 'chatbot') {
        messageTextElement.classList.add("chatbot-text");
    } else {
        messageTextElement.classList.add("user-text");
    }

    messageTextElement.textContent = message;

    // Ajoute le texte du message au contenu du message
    messageContentElement.appendChild(messageTextElement);

    // Ajoute le contenu du message à l'élément principal du message
    messageElement.appendChild(messageContentElement);

    return messageElement;
}

// Cette fonction récupère le message de l'utilisateur, fait une requête à la vue chatbot pour obtenir une réponse
function sendMessage(lang) {
    var userInput = document.getElementById("user-input");
    var chatMessages = document.getElementById("chat-box");

    // Create the user's message and add it to the chat box
    const userMessage = createChatMessage({
        sender: "user",
        message: userInput.value,
    });
    chatMessages.appendChild(userMessage);

    // Clear the input field
    userInput.value = "";

    // Show typing indicator
    const typingIndicator = document.createElement("div");
    typingIndicator.className = "message typing-indicator";
    typingIndicator.innerHTML = `
        <div class="chatbot-message">
            <div class="avatar-username">
                <span class="material-symbols-outlined">smart_toy</span>
            </div>
            <p class="message-text chatbot-text">
                <span class="dot"></span>
                <span class="dot"></span>
                <span class="dot"></span>
            </p>
        </div>
    `;
    chatMessages.appendChild(typingIndicator);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Send a POST request to the chatbot view with the user's message
    fetch(`/${lang}/main/chatbot/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": "{{ csrf_token }}",
        },
        body: JSON.stringify({ message: userMessage.innerText }),
    })
    .then((response) => response.json())
    .then((data) => {
        // Remove typing indicator
        chatMessages.removeChild(typingIndicator);

        // Create the chatbot's message and add it to the chat box
        const botMessage = createChatMessage({
            sender: "chatbot",
            message: cleanText(data.response),
        });
        chatMessages.appendChild(botMessage);

        // Scroll the chat box to the bottom to show the new message
        chatMessages.scrollTop = chatMessages.scrollHeight;
    })
    .catch((error) => {
        console.error("Error:", error);
    });
}
