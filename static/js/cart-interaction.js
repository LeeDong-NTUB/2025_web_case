document.addEventListener('DOMContentLoaded', function() {
    initAllCartControls();

    document.body.addEventListener('click', function(e) {
        const addBtn = e.target.closest('.add-to-cart-btn');
        if (addBtn) {
            e.preventDefault();
            e.stopPropagation();
            const wrapper = addBtn.closest('.cart-control-wrapper');
            handleAddToCart(wrapper);
            return;
        }

        const incBtn = e.target.closest('.increase-btn');
        if (incBtn) {
            e.preventDefault();
            e.stopPropagation();
            const wrapper = incBtn.closest('.cart-control-wrapper');
            handleQuantityChange(wrapper, 1);
            return;
        }

        const decBtn = e.target.closest('.decrease-btn');
        if (decBtn) {
            e.preventDefault();
            e.stopPropagation();
            const wrapper = decBtn.closest('.cart-control-wrapper');
            handleQuantityChange(wrapper, -1);
            return;
        }
    });

    window.addEventListener('storage', function() {
        initAllCartControls();
        updateGlobalCartStatus();
    });

    window.addEventListener('cartUpdated', function() {
        initAllCartControls();
        updateGlobalCartStatus();
    });

    updateGlobalCartStatus();
});

function initAllCartControls() {
    const cart = getCart();
    const wrappers = document.querySelectorAll('.cart-control-wrapper');

    wrappers.forEach(wrapper => {
        const id = parseInt(wrapper.dataset.id);
        const item = cart.find(i => i.id === id);

        if (item && item.quantity > 0) {
            toggleControlState(wrapper, true, item.quantity);
        } else {
            toggleControlState(wrapper, false);
        }
    });
}

function handleAddToCart(wrapper) {
    const product = getProductData(wrapper);
    addToCart(product);
    toggleControlState(wrapper, true, 1);
    updateGlobalCartStatus();
}

function handleQuantityChange(wrapper, change) {
    const id = parseInt(wrapper.dataset.id);
    let cart = getCart();
    const itemIndex = cart.findIndex(i => i.id === id);

    if (itemIndex > -1) {
        let newQty = cart[itemIndex].quantity + change;

        if (newQty <= 0) {
            cart.splice(itemIndex, 1);
            saveCart(cart);
            toggleControlState(wrapper, false);
        } else {
            cart[itemIndex].quantity = newQty;
            saveCart(cart);
            toggleControlState(wrapper, true, newQty);
        }
    } else if (change > 0) {
        handleAddToCart(wrapper);
    }
    
    updateGlobalCartStatus();
}

function toggleControlState(wrapper, isQtyMode, qty = 1) {
    const addBtn = wrapper.querySelector('.add-to-cart-btn');
    const qtyControl = wrapper.querySelector('.qty-control');
    const qtyDisplay = wrapper.querySelector('.qty-display');

    if (!addBtn || !qtyControl || !qtyDisplay) return;

    if (isQtyMode) {
        addBtn.classList.add('hidden');
        qtyControl.classList.remove('hidden');
        qtyControl.classList.add('flex');
        qtyDisplay.textContent = qty;
    } else {
        addBtn.classList.remove('hidden');
        qtyControl.classList.add('hidden');
        qtyControl.classList.remove('flex');
    }
}

function getProductData(wrapper) {
    return {
        id: parseInt(wrapper.dataset.id),
        name: wrapper.dataset.name,
        price: parseInt(wrapper.dataset.price),
        image: wrapper.dataset.image
    };
}

function getCart() {
    return JSON.parse(localStorage.getItem('cart')) || [];
}

function saveCart(cart) {
    localStorage.setItem('cart', JSON.stringify(cart));
    window.dispatchEvent(new Event('storage'));
    window.dispatchEvent(new Event('cartUpdated'));
}

function addToCart(product) {
    let cart = getCart();
    const existingItem = cart.find(item => item.id === product.id);

    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: product.id,
            quantity: 1,
            name: product.name,
            price: product.price,
            image: product.image
        });
    }
    saveCart(cart);
}

function updateGlobalCartStatus() {
    const cart = getCart();
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    const cartBtn = document.getElementById('cart-action-btn');
    if (cartBtn) {
        if (totalItems > 0) {
            cartBtn.classList.remove('hidden');
            cartBtn.classList.add('flex');
        } else {
            cartBtn.classList.add('hidden');
            cartBtn.classList.remove('flex');
        }
    }
    const cartCountElement = document.getElementById('cart-count');
    if (cartCountElement) {
        if (totalItems > 0) {
            cartCountElement.textContent = totalItems;
            cartCountElement.classList.remove('hidden');
        } else {
            cartCountElement.classList.add('hidden');
        }
    }
}