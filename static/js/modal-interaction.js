document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('product-modal');
    const backdrop = modal.querySelector('.modal-backdrop');
    const panel = modal.querySelector('.modal-panel');
    const closeBtn = modal.querySelector('.modal-close-btn');
    
    const sliderTrack = document.getElementById('modal-slider-track');
    const prevImgBtn = document.getElementById('modal-prev-img');
    const nextImgBtn = document.getElementById('modal-next-img');
    const dotsContainer = document.getElementById('modal-slider-dots');

    const modalTitle = document.getElementById('modal-title');
    const modalDesc = document.getElementById('modal-desc');
    const modalPrice = document.getElementById('modal-price');
    const modalQtyDisplay = document.getElementById('modal-qty');
    
    const modalIncreaseBtn = document.getElementById('modal-increase');
    const modalDecreaseBtn = document.getElementById('modal-decrease');
    const modalCartBtn = document.getElementById('modal-cart-btn');
    const modalDeleteBtn = document.getElementById('modal-delete-btn');

    let currentProduct = {};
    let currentQty = 1;
    let currentImgIndex = 0;
    let productImages = [];

    document.body.addEventListener('click', function(e) {
        const trigger = e.target.closest('.product-trigger');
        if (trigger) {
            e.preventDefault();
            e.stopPropagation();
            
            const imagesStr = trigger.dataset.images || '';
            productImages = imagesStr.split('|').filter(url => url.trim() !== '');
            
            if (productImages.length === 0) {
                 productImages = [trigger.dataset.image];
            }

            currentProduct = {
                id: parseInt(trigger.dataset.id),
                name: trigger.dataset.name,
                price: parseInt(trigger.dataset.price),
                originalPrice: parseInt(trigger.dataset.originalPrice),
                isSale: trigger.dataset.isSale === 'true',
                images: productImages, 
                description: trigger.dataset.description || '暫無商品介紹。堅持手工製作，使用天然食材，無添加人工防腐劑。'
            };

            initSlider();

            modalTitle.textContent = currentProduct.name;
            modalDesc.textContent = currentProduct.description;

            if (currentProduct.isSale) {
                modalPrice.innerHTML = `
                    <span class="text-[#d63031]">NT$${Number(currentProduct.price).toLocaleString()}</span>
                    <span class="text-base text-gray-400 line-through font-normal">NT$${Number(currentProduct.originalPrice).toLocaleString()}</span>
                `;
            } else {
                modalPrice.innerHTML = `
                    <span class="text-[#a97659]">NT$${Number(currentProduct.price).toLocaleString()}</span>
                `;
            }

            initModalState();

            modal.classList.remove('hidden');
            setTimeout(() => {
                backdrop.classList.remove('opacity-0');
                panel.classList.remove('opacity-0', 'scale-95');
                panel.classList.add('opacity-100', 'scale-100');
            }, 10);
            
            document.body.style.overflow = 'hidden';
        }
    });

    function initSlider() {
        currentImgIndex = 0;
        sliderTrack.innerHTML = '';
        dotsContainer.innerHTML = '';
        sliderTrack.style.transform = `translateX(0%)`;

        productImages.forEach((url, index) => {
            const imgDiv = document.createElement('div');
            imgDiv.className = 'w-full h-full flex-shrink-0';
            imgDiv.innerHTML = `<img src="${url}" alt="Product Image ${index+1}" class="w-full h-full object-cover">`;
            sliderTrack.appendChild(imgDiv);
        });

        if (productImages.length > 1) {
            prevImgBtn.classList.remove('hidden');
            nextImgBtn.classList.remove('hidden');
            
            productImages.forEach((_, index) => {
                const dot = document.createElement('button');
                dot.className = `w-2.5 h-2.5 rounded-full transition-colors ${index === 0 ? 'bg-[#7b6a63]' : 'bg-[#d4bcb0]/50 hover:bg-[#d4bcb0]'}`;
                dot.addEventListener('click', (e) => {
                    e.stopPropagation();
                    goToSlide(index);
                });
                dotsContainer.appendChild(dot);
            });
        } else {
            prevImgBtn.classList.add('hidden');
            nextImgBtn.classList.add('hidden');
        }
    }

    function updateSlider() {
        sliderTrack.style.transform = `translateX(-${currentImgIndex * 100}%)`;
        
        Array.from(dotsContainer.children).forEach((dot, index) => {
            if (index === currentImgIndex) {
                dot.className = 'w-2.5 h-2.5 rounded-full transition-colors bg-[#7b6a63]';
            } else {
                dot.className = 'w-2.5 h-2.5 rounded-full transition-colors bg-[#d4bcb0]/50 hover:bg-[#d4bcb0]';
            }
        });
    }

    function goToSlide(index) {
        currentImgIndex = index;
        if (currentImgIndex < 0) currentImgIndex = productImages.length - 1;
        if (currentImgIndex >= productImages.length) currentImgIndex = 0;
        updateSlider();
    }
    prevImgBtn.onclick = (e) => {
        e.stopPropagation();
        goToSlide(currentImgIndex - 1);
    };

    nextImgBtn.onclick = (e) => {
        e.stopPropagation();
        goToSlide(currentImgIndex + 1);
    };


    function initModalState() {
        const cart = JSON.parse(localStorage.getItem('cart')) || [];
        const existingItem = cart.find(item => item.id === currentProduct.id);
        
        if (existingItem) {
            currentQty = existingItem.quantity;
            modalCartBtn.querySelector('span').textContent = "更新購物車";
        } else {
            currentQty = 1;
            modalCartBtn.querySelector('span').textContent = "加入購物車";
        }
        modalQtyDisplay.textContent = currentQty;
    }

    function closeModal() {
        backdrop.classList.add('opacity-0');
        panel.classList.remove('opacity-100', 'scale-100');
        panel.classList.add('opacity-0', 'scale-95');
        
        setTimeout(() => {
            modal.classList.add('hidden');
            document.body.style.overflow = '';
        }, 300);
    }

    closeBtn.addEventListener('click', closeModal);
    backdrop.addEventListener('click', closeModal);

    modalIncreaseBtn.addEventListener('click', () => {
        currentQty++;
        modalQtyDisplay.textContent = currentQty;
    });

    modalDecreaseBtn.addEventListener('click', () => {
        if (currentQty > 1) {
            currentQty--;
            modalQtyDisplay.textContent = currentQty;
        }
    });

    modalCartBtn.addEventListener('click', () => {
        let cart = JSON.parse(localStorage.getItem('cart')) || [];
        const existingIndex = cart.findIndex(item => item.id === currentProduct.id);
        
        const thumbImage = currentProduct.images.length > 0 ? currentProduct.images[0] : '';

        if (existingIndex > -1) {
            cart[existingIndex].quantity = currentQty;
        } else {
            cart.push({
                id: currentProduct.id,
                quantity: currentQty,
                name: currentProduct.name,
                price: currentProduct.price,
                image: thumbImage
            });
        }
        
        saveAndClose(cart, `已將 ${currentProduct.name} 加入購物車`);
    });

    modalDeleteBtn.addEventListener('click', () => {
        let cart = JSON.parse(localStorage.getItem('cart')) || [];
        const existingIndex = cart.findIndex(item => item.id === currentProduct.id);
        
        if (existingIndex > -1) {
            cart.splice(existingIndex, 1);
            saveAndClose(cart, `已從購物車移除 ${currentProduct.name}`);
        } else {
            closeModal();
        }
    });

    function saveAndClose(cart, msg) {
        localStorage.setItem('cart', JSON.stringify(cart));
        window.dispatchEvent(new Event('storage'));
        window.dispatchEvent(new Event('cartUpdated'));
        
        if (typeof showNotification === 'function') {
            showNotification(msg);
        }
        
        closeModal();
    }
});