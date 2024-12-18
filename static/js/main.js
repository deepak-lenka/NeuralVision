function usePrompt(element) {
    document.getElementById('prompt').value = element.textContent;
}

async function generateImages() {
    const prompt = document.getElementById('prompt').value;
    const numImages = document.getElementById('num-images').value;
    const generateBtn = document.getElementById('generate-btn');
    const gallery = document.getElementById('image-gallery');

    if (!prompt) {
        alert('Please enter a prompt');
        return;
    }

    // Clear previous images and show loading state
    gallery.innerHTML = '';
    generateBtn.classList.add('loading');
    generateBtn.disabled = true;

    try {
        console.log('Sending request with:', { prompt, numImages });
        const response = await fetch('http://localhost:5013/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prompt: prompt,
                num_images: parseInt(numImages)
            })
        });

        const data = await response.json();
        console.log('Server response:', data);

        if (!response.ok) {
            throw new Error(data.error || 'Failed to generate images');
        }

        if (data.error) {
            throw new Error(data.error);
        }

        // Clear gallery before adding new images
        gallery.innerHTML = '';

        // Add each image to the gallery
        data.images.forEach(filename => {
            const imgContainer = document.createElement('div');
            imgContainer.className = 'image-container';

            const img = document.createElement('img');
            img.src = `/temp_images/${filename}`;
            img.alt = prompt;
            img.onerror = () => {
                console.error('Failed to load image:', filename);
                img.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><text x="50%" y="50%" text-anchor="middle" fill="red">Error loading image</text></svg>';
            };
            
            const downloadBtn = document.createElement('button');
            downloadBtn.className = 'download-btn';
            downloadBtn.textContent = 'Download';
            downloadBtn.onclick = () => {
                window.location.href = `/download/${filename}`;
            };

            imgContainer.appendChild(img);
            imgContainer.appendChild(downloadBtn);
            gallery.appendChild(imgContainer);
        });

    } catch (error) {
        console.error('Error details:', error);
        alert('Error: ' + error.message);
        gallery.innerHTML = `<div class="error-message">Error: ${error.message}</div>`;
    } finally {
        // Reset button state
        generateBtn.classList.remove('loading');
        generateBtn.disabled = false;
    }
}

// Add smooth scrolling to gallery when new images are generated
document.getElementById('generate-btn').addEventListener('click', () => {
    setTimeout(() => {
        const gallery = document.getElementById('image-gallery');
        gallery.scrollIntoView({ behavior: 'smooth' });
    }, 100);
});
