document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.btn-primary');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const button = event.target;
            const id = button.getAttribute('data-id');
            const name = button.getAttribute('data-name');
            const price = button.getAttribute('data-price');
            const action = button.getAttribute('data-action');
            if (action === 'add') {
                addToCart(id, name, price, action, button);
            } else if (action === 'remove') {
                removeFromCart(id);
            }
        });
    });
});

function updateCartCount(count) {
    const cartCountElement = document.getElementById('cart-count');
    if (cartCountElement) {
        cartCountElement.textContent = count;
    }
}

function updateTotal() {
    const totalElement = document.getElementById('total');
    let total = 0;
    const cartItems = document.querySelectorAll('#cart-item-{{ item.id }}');
    cartItems.forEach(item => {
        const price = parseFloat(item.querySelector('td:nth-child(3)').textContent);
        total += price;
    });
    totalElement.textContent = total.toFixed(2);
}

function removeFromCart(id) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    if (!csrftoken) {
        console.error('CSRF token not found!');
        return;
    }  
    fetch('/remove_from_cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ product_id: id })
    })
    .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                console.log('Item removed from cart successfully');
                window.location.replace(window.location.origin + '/cart/');
            } else {
                alert(data.error || 'Error removing from cart');
            }
        })
    
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while removing from cart');
    });
}

function addToCart(id, name, price) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const csrfTokenElement = document.getElementById('csrf-token');

    if (!csrftoken) {
        console.error('CSRF token not found!');
        return;
    }
    const csrfToken = csrfTokenInput.value;
    const productData = {
        product_id: id,
        product_name: name,
        product_price: price
    };
    fetch('/add_to_cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(productData)
    })
    .then(response => response.json()
        .then(data => {
            if (response.ok) {
                alert(data.message);
            } else {
                alert(data.error || 'Error adding to cart');
            }
        })
    )
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while adding to cart');
    });
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
