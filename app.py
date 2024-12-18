import os
from flask import Flask, request, jsonify, render_template, send_file, send_from_directory
from flask_cors import CORS
import replicate
import requests
from io import BytesIO
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if API token is set
api_token = os.getenv('REPLICATE_API_TOKEN')
if not api_token:
    raise ValueError("REPLICATE_API_TOKEN is not set in .env file")

app = Flask(__name__)
CORS(app)

# Create a temporary directory for images if it doesn't exist
TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp_images")
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/temp_images/<path:filename>')
def serve_image(filename):
    return send_from_directory(TEMP_DIR, filename)

@app.route('/generate', methods=['POST'])
def generate_image():
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        num_images = int(data.get('num_images', 1))

        print(f"Received request - Prompt: {prompt}, Num Images: {num_images}")

        # Validate API token again
        if not os.getenv('REPLICATE_API_TOKEN'):
            raise ValueError("REPLICATE_API_TOKEN is not set")

        # Run the model
        print("Calling Replicate API...")
        try:
            print("Model parameters:", {
                "prompt": prompt,
                "negative_prompt": "",
                "style": "base",
                "image_count": num_images,
                "width": 1024,
                "height": 683,
                "steps": 50,
                "guidance_scale": 7.5,
                "image_prompt_strength": 0.1,
                "safety_tolerance": 2,
                "seed": None
            })
            
            output = replicate.run(
                "black-forest-labs/flux-1.1-pro-ultra",
                input={
                    "prompt": prompt,
                    "negative_prompt": "",
                    "num_outputs": num_images,
                    "width": 1024,
                    "height": 683,
                    "num_inference_steps": 50,
                    "guidance_scale": 7.5,
                    "scheduler": "K_EULER",
                    "seed": None
                }
            )
            print(f"Replicate API response: {output}")
        except Exception as api_error:
            print(f"Replicate API error: {str(api_error)}")
            raise Exception(f"Replicate API error: {str(api_error)}")

        # Download and save images
        image_paths = []
        for img_url in output:
            print(f"Downloading image from: {img_url}")
            try:
                # Download the image
                response = requests.get(img_url)
                response.raise_for_status()  # Raise an error for bad status codes
                
                if response.status_code == 200:
                    # Generate a unique filename
                    filename = f"{uuid.uuid4()}.png"
                    filepath = os.path.join(TEMP_DIR, filename)
                    
                    print(f"Saving image to: {filepath}")
                    # Save the image
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    
                    image_paths.append(filename)
            except requests.exceptions.RequestException as req_error:
                print(f"Error downloading image: {str(req_error)}")
                continue

        if not image_paths:
            raise Exception("Failed to generate or save any images")

        print(f"Successfully processed {len(image_paths)} images")
        return jsonify({
            'images': image_paths
        })

    except Exception as e:
        import traceback
        error_msg = f"Error: {str(e)}\nTraceback: {traceback.format_exc()}"
        print(error_msg)
        return jsonify({
            'error': str(e)
        }), 500

@app.route('/download/<filename>')
def download_image(filename):
    try:
        return send_file(
            os.path.join(TEMP_DIR, filename),
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5011)
