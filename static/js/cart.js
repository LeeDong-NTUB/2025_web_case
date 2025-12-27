let cart = JSON.parse(localStorage.getItem('cart')) || [];

function increaseQuantity(productId) {
    const itemIndex = cart.findIndex(item => item.id === productId);
    if (itemIndex > -1) {
        cart[itemIndex].quantity += 1;
        localStorage.setItem('cart', JSON.stringify(cart));
    }
}

function decreaseQuantity(productId) {
    const itemIndex = cart.findIndex(item => item.id === productId);
    if (itemIndex > -1) {
        if (cart[itemIndex].quantity > 1) {
            cart[itemIndex].quantity -= 1;
        } else {
            cart.splice(itemIndex, 1);
        }
        localStorage.setItem('cart', JSON.stringify(cart));
    }
}