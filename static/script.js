// Configure Marked.js
marked.setOptions({
    highlight: function (code, lang) {
        if (lang && hljs.getLanguage(lang)) {
            return hljs.highlight(code, { language: lang }).value;
        }
        return hljs.highlightAuto(code).value;
    },
    breaks: true,
    gfm: true
});

// Essential selectors
const chatBox = document.getElementById("chat-box");
const messageInput = document.getElementById("message");

// Theme management
function toggleTheme() {
    const body = document.body;
    const currentTheme = body.getAttribute('data-theme') || 'light';
    const newTheme = currentTheme === 'light' ? 'dark' : 'light';

    body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcons(newTheme);
}

function updateThemeIcons(theme) {
    const iconMain = document.getElementById('themeIcon');
    if (theme === 'dark') {
        if (iconMain) iconMain.className = 'fas fa-sun';
    } else {
        if (iconMain) iconMain.className = 'fas fa-moon';
    }
}

function loadTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.body.setAttribute('data-theme', savedTheme);
    updateThemeIcons(savedTheme);
}

// Chat logic
async function sendMessage() {
    const message = messageInput.value.trim();
    if (message === "") return;

    // Add user message
    appendMessage('user', message);
    messageInput.value = "";

    // Show typing
    const typingIndicator = document.getElementById("typing");
    typingIndicator.style.display = "flex";
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();
        typingIndicator.style.display = "none";

        if (data.reply) {
            appendMessage('bot', data.reply);
        }

    } catch (error) {
        typingIndicator.style.display = "none";
        appendMessage('bot', "⚠️ Connection error. Please try again.");
    } finally {
        chatBox.scrollTop = chatBox.scrollHeight;
    }
}

function appendMessage(role, text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `${role} message`;

    const emoji = role === 'user' ? '👤' : getBotEmoji();
    const content = role === 'bot' ? marked.parse(text) : text;

    msgDiv.innerHTML = `
        <div class="avatar-small notion-emoji-small">${emoji}</div>
        <div class="text">${role === 'user' ? escapeHTML(content) : content}</div>
    `;

    chatBox.appendChild(msgDiv);

    // Highlight code blocks if any
    if (role === 'bot') {
        msgDiv.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightElement(block);
        });
    }
}

function getBotEmoji() {
    const emojis = ['✨', '🧠', '⚡', '💡', '🤖'];
    return emojis[Math.floor(Math.random() * emojis.length)];
}

function escapeHTML(str) {
    return str.replace(/[&<>"']/g, function (m) {
        return {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        }[m];
    });
}

// Listeners
messageInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

document.getElementById("sendBtn").addEventListener("click", sendMessage);

window.onload = () => {
    loadTheme();
};
