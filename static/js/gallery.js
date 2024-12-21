document.addEventListener('DOMContentLoaded', () => {
    const galleryGrid = document.getElementById('gallery-grid');
    const loader = document.getElementById('gallery-loader');
    let page = 1;
    let loading = false;
    let hasMore = true;

    async function loadImages() {
        if (loading || !hasMore) return;
        
        loading = true;
        loader.style.display = 'flex';

        try {
            const response = await fetch(`/api/gallery?page=${page}`);
            const data = await response.json();

            if (data.images.length === 0) {
                hasMore = false;
                loader.style.display = 'none';
                return;
            }

            data.images.forEach(image => {
                const imageContainer = document.createElement('div');
                imageContainer.className = 'gallery-item';
                
                imageContainer.innerHTML = `
                    <img src="${image.path}" alt="${image.prompt || 'AI Generated Image'}" loading="lazy">
                    <div class="gallery-item-overlay">
                        <p class="gallery-item-prompt">${image.prompt || 'AI Generated Image'}</p>
                        <p class="gallery-item-date">${new Date(image.created_at).toLocaleDateString()}</p>
                    </div>
                `;
                
                galleryGrid.appendChild(imageContainer);
            });

            page++;
        } catch (error) {
            console.error('Error loading images:', error);
        } finally {
            loading = false;
            loader.style.display = hasMore ? 'flex' : 'none';
        }
    }

    // Initial load
    loadImages();

    // Infinite scroll
    window.addEventListener('scroll', () => {
        if ((window.innerHeight + window.scrollY) >= document.documentElement.scrollHeight - 500) {
            loadImages();
        }
    });

    // Scroll Progress Bar
    function updateScrollProgress() {
        const scrollProgress = document.querySelector('.scroll-progress-bar');
        const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
        const scrolled = (window.scrollY / scrollHeight) * 100;
        scrollProgress.style.height = `${scrolled}%`;
    }

    // Add scroll event listener
    window.addEventListener('scroll', updateScrollProgress);
    window.addEventListener('resize', updateScrollProgress);

    // Initial progress update
    updateScrollProgress();
});
