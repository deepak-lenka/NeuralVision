function usePrompt(element) {
    document.getElementById('prompt').value = element.textContent;
}

function updateProgress(percentage) {
    const circle = document.querySelector('.progress-ring-circle');
    const percentageText = document.querySelector('.percentage');
    const circumference = 2 * Math.PI * 54; // r=54 from the SVG

    // Update circle progress
    const offset = circumference - (percentage / 100 * circumference);
    circle.style.strokeDashoffset = offset;

    // Update percentage text
    percentageText.textContent = `${Math.round(percentage)}%`;
}

async function generateImages() {
    const prompt = document.getElementById('prompt').value;
    const numImages = document.getElementById('num-images').value;
    const generateBtn = document.getElementById('generate-btn');
    const status = document.getElementById('generation-status');
    const gallery = document.getElementById('image-gallery');

    if (!prompt) return;

    // Show loading state
    generateBtn.classList.add('loading');
    status.classList.add('active');
    gallery.innerHTML = '';

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt, num_images: parseInt(numImages) })
        });

        const data = await response.json();

        if (data.images) {
            setTimeout(() => {
                status.classList.remove('active');
                data.images.forEach(imagePath => {
                    const imgContainer = document.createElement('div');
                    imgContainer.className = 'image-container';
                    
                    const img = document.createElement('img');
                    img.src = imagePath;
                    img.alt = prompt;
                    
                    imgContainer.appendChild(img);
                    gallery.appendChild(imgContainer);
                });
            }, 500);
        }
    } catch (error) {
        console.error('Error:', error);
        setTimeout(() => {
            status.classList.remove('active');
        }, 500);
    } finally {
        generateBtn.classList.remove('loading');
    }
}

// Add smooth scrolling to gallery when new images are generated
document.getElementById('generate-btn').addEventListener('click', () => {
    setTimeout(() => {
        const gallery = document.getElementById('image-gallery');
        gallery.scrollIntoView({ behavior: 'smooth' });
    }, 100);
});
