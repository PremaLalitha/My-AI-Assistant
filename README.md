# AI Assistant (Mistral AI)

A clean, minimalist AI chatbot built with Flask and Mistral AI.


## ✨ Features

- Real-time AI responses using Mistral AI
- Automatic model fallbacks to handle API rate limits
- Simple, dark mode toggle responsive UI
- Secure API key handling

## 🛠️ Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set API Key**:
   Create a `.env` file and add:
   ```env
   MISTRAL_API_KEY=your_api_key_here
   ```

3. **Run App**:
   ```bash
   python app.py
   ```

## 🚀 Deployment

- **Hosting**: Recommended on [Render.com](https://render.com).
- **Setup**: Link your GitHub repository and set `MISTRAL_API_KEY` in the Environment Variables tab on Render.
