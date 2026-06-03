document.addEventListener('DOMContentLoaded', function() {
    if (event.target && event.target.classList.contains('btn-primary')) {
        const id = event.target.getAttribute('data-id');
        const name = event.target.getAttribute('data-name');
        const price = event.target.getAttribute('data-price');
        addToCart(id, name, price);
    } else if (event.target && event.target.classList.contains('btn-remove')) {
        const id = event.target.getAttribute('data-id');
        const name = event.target.getAttribute('data-name');
        const price = event.target.getAttribute('data-price');
        removeFromCart(id, name, price);
    }
});

function removeFromCart(id, name, price) {
    const csrfTokenElement = document.querySelector('meta[name="csrf-token"]');

    if (!csrfTokenElement) {
        console.error('CSRF token not found!');
        return;
    }
    const csrfToken = csrfTokenElement.value;
    fetch('/remove_from_cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({product_id: id})
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'success' || data.message) {
            console.log('Item removed from cart successfully');
            const row = document.querySelector(`.cart-item[data-id="${id}"]`);
            if (row) {
                row.remove();

                if (data.cart_count !== undefined) {
                    document.getElementById('cart-count').textContent = data.cart_count;
                }
            }

            const tbody = document.querySelector('#cart-table tbody');
            if (tbody && tbody.children.length === 0) {
                tbody.innerHTML = '<tr><td colspan="4">Your cart is empty.</td></tr>';
        } else {
            alert(data.error || 'Error removing from cart');
        }
    }})
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while removing from cart');
    });
}

function removeCartItemFromUI(id) {
    
}

function addToCart(id, name, price) {
    const csrfTokenElement = document.getElementById('csrf-token');

    if (!csrfTokenElement) {
        console.error('CSRF token not found!');
        return;
    }
    const csrfToken = csrfTokenElement.value;
    const productData = {
        product_id: id,
        product_name: name,
        product_price: price
    };
    fetch('/add_to_cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify(productData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while adding to cart');
    });
}

function updateCartCount(count) {
    const cartCountElement = document.getElementById('cart-count');
    if (cartCountElement) {
        cartCountElement.textContent = count;
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
