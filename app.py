import os
from flask import Flask, request, jsonify, render_template, send_file, send_from_directory
from flask_cors import CORS
import replicate
import requests
from io import BytesIO
import uuid
from dotenv import load_dotenv
import json
import time
import asyncio
import concurrent.futures

load_dotenv()

# Check if API token is set
if not os.getenv('REPLICATE_API_TOKEN'):
    raise ValueError("REPLICATE_API_TOKEN is not set in .env file")

app = Flask(__name__)
CORS(app)

# Create a temporary directory for images if it doesn't exist
TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp_images")
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

def generate_single_image(prompt, index):
    """Generate a single image using the model with a unique seed"""
    try:
        print(f"Starting image generation {index + 1} with prompt: {prompt}")
        # Generate a different seed for each image based on the index
        seed = 42 + index * 1000  # This ensures each image gets a different seed
        
        model_input = {
            "prompt": prompt,
            "width": 1024,
            "height": 683,
            "guidance_scale": 7.5,
            "negative_prompt": "",
            "seed": seed  # Use the unique seed
        }

        print(f"Creating prediction with model input: {model_input}")
        prediction = replicate.predictions.create(
            model="black-forest-labs/flux-1.1-pro-ultra",
            input=model_input
        )

        print(f"Waiting for prediction {index + 1} to complete...")
        while prediction.status not in ["succeeded", "failed", "canceled"]:
            time.sleep(1)
            prediction.reload()
            print(f"Prediction {index + 1} status: {prediction.status}")

        if prediction.status == "succeeded":
            print(f"Prediction {index + 1} succeeded. Output: {prediction.output}")
            return prediction.output
        else:
            raise Exception(f"Prediction failed with status: {prediction.status}")

    except Exception as e:
        print(f"Error generating single image: {str(e)}")
        raise e

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_image():
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        num_images = int(data.get('num_images', 1))

        print(f"Starting image generation request - Prompt: {prompt}, Num Images: {num_images}")

        # Generate multiple images in parallel
        image_outputs = []
        print("Starting parallel image generation...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_images) as executor:
            # Create a list of futures for parallel execution
            futures = [executor.submit(generate_single_image, prompt, i) for i in range(num_images)]
            
            # Wait for all futures to complete
            for future in concurrent.futures.as_completed(futures):
                try:
                    output = future.result()
                    print(f"Received output from future: {output}")
                    if output:
                        if isinstance(output, str):
                            image_outputs.append(output)
                        elif isinstance(output, list):
                            image_outputs.extend(output)
                        elif isinstance(output, dict):
                            if 'images' in output:
                                image_outputs.extend(output['images'])
                            else:
                                image_outputs.append(output.get('image', ''))
                except Exception as e:
                    print(f"Error in future: {str(e)}")
                    continue

        print(f"Generated {len(image_outputs)} images. Image URLs: {image_outputs}")

        # Download and save images
        image_paths = []
        for img_url in image_outputs:
            if not img_url:  # Skip empty URLs
                continue
                
            print(f"Downloading image from: {img_url}")
            try:
                # Download the image
                response = requests.get(img_url)
                response.raise_for_status()
                
                # Generate a unique filename
                filename = f"{uuid.uuid4()}.png"
                filepath = os.path.join(TEMP_DIR, filename)
                
                print(f"Saving image to: {filepath}")
                # Save the image
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                image_paths.append(filename)
                print(f"Successfully saved image as: {filename}")
            except requests.exceptions.RequestException as req_error:
                print(f"Error downloading image: {str(req_error)}")
                continue

        if not image_paths:
            raise Exception("Failed to generate or save any images")

        print(f"Successfully processed {len(image_paths)} images. Returning filenames: {image_paths}")
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

@app.route('/get-showcase-images')
def get_showcase_images():
    try:
        # Get list of all images in temp_images directory
        image_files = [f for f in os.listdir(TEMP_DIR) if f.endswith('.png')]
        # Sort by creation time, newest first
        image_files.sort(key=lambda x: os.path.getctime(os.path.join(TEMP_DIR, x)), reverse=True)
        return jsonify({'images': image_files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/temp_images/<path:filename>')
def serve_image(filename):
    return send_from_directory(TEMP_DIR, filename)

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
    app.run(debug=True, port=5013)
