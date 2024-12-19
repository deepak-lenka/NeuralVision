# NeuralVision

A modern AI-powered image generation application that transforms textual descriptions into stunning visual artwork using state-of-the-art AI models.

## Features

- 🎨 Generate unique images from text descriptions
- 🖼️ Create multiple images in parallel
- 💫 Modern, futuristic user interface
- 🔄 Real-time image generation
- 💡 Creative prompt suggestions

## Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Python, Flask
- **AI Model**: Replicate API (Flux model)
- **Additional Libraries**: Flask-CORS, python-dotenv

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/deepak-lenka/NeuralVision.git
   cd NeuralVision
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your Replicate API key:
   ```
   REPLICATE_API_TOKEN=your_api_key_here
   ```

5. Run the application:
   ```bash
   python app.py
   ```

6. Open your browser and navigate to `http://localhost:5013`

## Environment Variables

- `REPLICATE_API_TOKEN`: Your Replicate API key (required)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
