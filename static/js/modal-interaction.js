document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('product-modal');
    const backdrop = modal.querySelector('.modal-backdrop');
    const panel = modal.querySelector('.modal-panel');
    const closeBtn = modal.querySelector('.modal-close-btn');
    
    const modalImg = document.getElementById('modal-img');
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

    document.body.addEventListener('click', function(e) {
        const trigger = e.target.closest('.product-trigger');
        if (trigger) {
            e.preventDefault();
            e.stopPropagation();
            
            currentProduct = {
                id: parseInt(trigger.dataset.id),
                name: trigger.dataset.name,
                price: parseInt(trigger.dataset.price),
                image: trigger.dataset.image,
                description: trigger.dataset.description || '暫無商品介紹。堅持手工製作，使用天然食材，無添加人工防腐劑。'
            };

            modalImg.src = currentProduct.image;
            modalTitle.textContent = currentProduct.name;
            modalDesc.textContent = currentProduct.description;
            modalPrice.textContent = `NT$${Number(currentProduct.price).toLocaleString()}`;

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
        
        if (existingIndex > -1) {
            cart[existingIndex].quantity = currentQty;
        } else {
            cart.push({
                id: currentProduct.id,
                quantity: currentQty,
                name: currentProduct.name,
                price: currentProduct.price,
                image: currentProduct.image
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