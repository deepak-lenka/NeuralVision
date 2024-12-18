# Image Generator

A simple Python application that generates images using the Replicate API and Stable Diffusion model.

## Setup

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file by copying `.env.example`:
```bash
cp .env.example .env
```

4. Get your Replicate API token from https://replicate.com and add it to the `.env` file:
```
REPLICATE_API_TOKEN=your_replicate_token_here
```

## Usage

1. Run the application:
```bash
python main.py
```

2. Enter your prompt when asked. Be descriptive about what kind of image you want to generate.

3. Choose how many images you want to generate (1-4).

4. The generated images will be saved in the current directory as PNG files.

5. Type 'quit' when you want to exit the program.

## Features

- Generate multiple images from a single prompt
- Uses Stable Diffusion model via Replicate API
- Simple command-line interface
- Automatic image saving
- Error handling and user feedback
