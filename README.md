# NeuralVision 🎨

<div align="center" style="background-color: #0a0a0a; padding: 20px;">
  <div style="display: inline-flex; align-items: center; gap: 12px;">
    <img src="assets/logo.svg" alt="NeuralVision Logo" width="180" height="180">
    <h1 style="font-family: 'Segoe UI', system-ui, sans-serif; font-size: 42px; font-weight: 600; margin: 0; color: white; letter-spacing: -0.5px;">Neural<span style="background: linear-gradient(90deg, #6c63ff 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Vision</span></h1>
  </div>
</div>

A cutting-edge AI-powered image generation platform that transforms your imagination into stunning visual artwork using state-of-the-art AI models.

## ✨ Features

- 🎨 Transform text descriptions into high-quality images
- 🖼️ Browse and download your generated images
- 💫 Modern, intuitive interface
- 💡 Creative prompt suggestions

## 🚀 Setup Guide

1. **Clone the Repository**
   ```bash
   git clone https://github.com/deepak-lenka/NeuralVision.git
   cd NeuralVision
   ```

2. **Set Up Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install flask python-dotenv requests openai
   ```

4. **Configure Environment**
   Create a `.env` file:
   ```env
   REPLICATE_API_TOKEN=your_api_key_here
   PORT=5013  # Optional, defaults to 5013
   ```

5. **Run the Application**
   ```bash
   python app.py
   ```

6. **Access the Application**
   Open `http://localhost:5013` in your browser

---
Created with ❤️ by Deepak Lenka
