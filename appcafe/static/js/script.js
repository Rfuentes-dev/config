document.addEventListener('click', function(event) {
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
    fetch('/remove_from_cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
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
            const row = document.querySelector(`#cart-item-${id}`);
            if (row) {
                const rows = row.getElementsByTagName('td');
                if (rows && rows[2]) {
                    const productPrice = parseFloat(rows[2].textContent.replace('$', '').trim()) || 0;
                    const totalElem = document.getElementById('total');
                    if (totalElem) {
                        const totalActual = parseFloat(totalElem.textContent.replace('$', '').trim()) || 0;
                        const newTotal = Math.max(0, totalActual - productPrice);
                        totalElem.textContent = newTotal.toFixed(2);
                    }
                }
                row.remove();

                if (data.cart_count !== undefined) {
                    const cartCountElem = document.getElementById('cart-count').textContent = data.cart_count;
                    if (cartCountElem) cartCountElem.textContent = data.cart_count;
                }
            }

            const tbody = document.querySelector('table tbody');
            if (tbody && tbody.children.length === 0) {
                tbody.innerHTML = '<tr><td colspan="4">Tu carrito está vacío.</td></tr>';
            }
        } else {
            alert(data.error || 'Error removing from cart');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while removing from cart');
    });
}

function removeCartItemFromUI(id) {
    const row = document.querySelector(`.cart-item[data-id="${id}"]`);
    if (row) {
        row.remove();
    }

    const tbody = document.querySelector('#cart-table tbody');
    if (tbody && tbody.children.length === 0) {
        tbody.innerHTML = '<tr><td colspan="4">Your cart is empty.</td></tr>';
    }
}

function addToCart(id, name, price) {
    fetch('/add_to_cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            product_id: id,
            product_name: name,
            product_price: price
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || 'Network response was not ok');
            });
        }
        return response.json();
    })
    .then(data => {
        console.log('Product added successfully:', data);
        alert('Producto Agregado al Carrito');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error: ' + error.message);
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

function validateCart(event) {
    const tbody = document.querySelector('table tbody');
    const isEmpty = tbody.querySelector('tr td[colspan="4"]') !== null;
            
    if (isEmpty) {
        event.preventDefault();
        alert('El carrito esta vacio. Agregue una orden para confirmar tu pedido.');
        return false;
    }
    return true;
}
