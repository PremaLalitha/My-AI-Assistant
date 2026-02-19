# Notion-Style AI Assistant (Mistral AI)

A professional, feature-rich AI chatbot built with Flask and Mistral AI, featuring a clean Notion-inspired UI, markdown rendering, and session-based conversation history.

![Preview](https://via.placeholder.com/800x400?text=AI+Assistant+Preview) <!-- Replace with real screenshot if possible -->

## ✨ Features
- **🧠 Mistral AI Powered**: Intelligent responses using `mistral-small-latest`.
- **📝 Markdown Support**: Full rendering of bold text, lists, and code blocks.
- **💻 Syntax Highlighting**: Professional code formatting for multiple languages.
- **🕒 Conversation History**: remembers context within each session.
- **🎨 Notion UI**: Minimalist, high-end design with light/dark mode.
- **📱 Responsive**: works perfectly on desktop and mobile.
- **🚀 Deployment Ready**: Includes Docker and Procfile for instant hosting.

## 🛠️ Setup Instructions

### 1. Prerequisites
- Python 3.8+
- Mistral AI API Key

### 2. Installation
```bash
# Clone the repository (or copy files)
cd ChatBot

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory:
```env
MISTRAL_API_KEY=your_api_key_here
FLASK_SECRET_KEY=your_random_secret_here
```

### 4. Run the App
```bash
python app.py
```
Visit `http://localhost:5000` in your browser.

## 🐳 Running with Docker
```bash
docker-compose up --build
```

## 🚀 Deployment (Render/Railway/Heroku)
1. Push your code to GitHub (Note: ensure `.env` is ignored!).
2. Connect your repository to the deployment platform.
3. Set your **Environment Variables** (`MISTRAL_API_KEY`, etc.) in the platform's dashboard.
4. The platform will use the `Procfile` or `Dockerfile` automatically.

## 📄 License
MIT
