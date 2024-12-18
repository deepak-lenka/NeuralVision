import os
import replicate
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

def generate_image(prompt, num_samples=1):
    """
    Generate images using the Stable Diffusion model via Replicate API
    """
    try:
        # Run the model
        output = replicate.run(
            "black-forest-labs/flux-1.1-pro-ultra",
            input={
                "prompt": prompt,
                "num_outputs": num_samples,
                "scheduler": "K_EULER",
                "num_inference_steps": 50
            }
        )
        
        # Download and save the generated images
        for i, image_url in enumerate(output):
            response = requests.get(image_url)
            filename = f"generated_image_{i+1}.png"
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"Image saved as {filename}")
            
        return True
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

def main():
    # Check if API token is set
    if not os.getenv("REPLICATE_API_TOKEN"):
        print("Please set your REPLICATE_API_TOKEN in the .env file")
        return
    
    while True:
        prompt = input("\nEnter your image prompt (or 'quit' to exit): ")
        
        if prompt.lower() == 'quit':
            break
            
        num_samples = input("How many images do you want to generate? (1-4): ")
        try:
            num_samples = int(num_samples)
            num_samples = max(1, min(4, num_samples))  # Limit between 1 and 4
        except ValueError:
            num_samples = 1
            
        print("\nGenerating images... This may take a minute.")
        success = generate_image(prompt, num_samples)
        
        if success:
            print("\nImages generated successfully!")
        else:
            print("\nFailed to generate images. Please try again.")

if __name__ == "__main__":
    main()
