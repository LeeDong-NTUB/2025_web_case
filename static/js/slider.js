document.addEventListener('DOMContentLoaded', function() {
    const slides = document.querySelectorAll('[data-slide-index]');
    const dots = document.querySelectorAll('[data-dots-index]');
    const prevButton = document.getElementById('prev-button');
    const nextButton = document.getElementById('next-button');
    let currentIndex = 0;
    const slideCount = slides.length;
    
    if (slideCount === 0) return;
    
    function showSlide(index) {
        slides.forEach(slide => {
            slide.classList.remove('opacity-100');
            slide.classList.add('opacity-0', 'hidden');
        });
        
        dots.forEach(dot => {
            dot.classList.remove('bg-white', 'scale-125');
            dot.classList.add('bg-white/50');
        });
        
        slides[index].classList.remove('hidden');
        setTimeout(() => {
            slides[index].classList.remove('opacity-0');
            slides[index].classList.add('opacity-100');
        }, 10);
        
        dots[index].classList.remove('bg-white/50');
        dots[index].classList.add('bg-white', 'scale-125');
        
        currentIndex = index;
    }
    
    function nextSlide() {
        showSlide((currentIndex + 1) % slideCount);
    }
    
    function prevSlide() {
        showSlide((currentIndex - 1 + slideCount) % slideCount);
    }
    
    prevButton.addEventListener('click', prevSlide);
    nextButton.addEventListener('click', nextSlide);
    
    dots.forEach(dot => {
        dot.addEventListener('click', function() {
            const slideIndex = parseInt(this.getAttribute('data-dots-index'));
            showSlide(slideIndex);
        });
    });

    showSlide(0);
    
    // let interval = setInterval(nextSlide, 10000);
    // const sliderContainer = document.getElementById('slider-container');
    // sliderContainer.addEventListener('mouseenter', () => clearInterval(interval));
    // sliderContainer.addEventListener('mouseleave', () => interval = setInterval(nextSlide, 10000));
});