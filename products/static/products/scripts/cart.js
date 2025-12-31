const subtotalDiv = document.querySelector('.subtotal-value')

function getTagValue(element) {
  let [integers, cents] = element.textContent.split(',')
  integers = integers.replace('.', '')
  return Number([integers, cents].join('.'))
}

function getCSRFToken() {
  return document.cookie
    .split('; ')
    .find((row) => row.startsWith('csrftoken='))
    ?.split('=')[1]
}

function calculateSubtotal() {
  const prices = document.querySelectorAll('.cart-product')

  const total = [...prices].reduce((sum, product) => {
    const priceSpan = product.querySelector('.cart-price')
    const quantitySpan = product.querySelector('.quantity')

    const price = getTagValue(priceSpan)
    const quantity = Number(quantitySpan.textContent)

    return sum + price * quantity
  }, 0)

  subtotalDiv.textContent = total.toLocaleString('pt-BR')
}

document.querySelectorAll('.plus-product-button').forEach((button) => {
  button.addEventListener('click', () => {
    const product = button.closest('.cart-product')
    const quantitySpan = product.querySelector('.quantity')

    quantitySpan.textContent = Number(quantitySpan.textContent) + 1
    calculateSubtotal()
  })
})

document.querySelectorAll('.minus-product-button').forEach((button) => {
  button.addEventListener('click', async () => {
    const product = button.closest('.cart-product')
    const quantitySpan = product.querySelector('.quantity')
    const productId = product.id[product.id.length - 1]

    const current = Number(quantitySpan.textContent)
    if (current > 1) {
      quantitySpan.textContent = current - 1
      calculateSubtotal()
    } else {
      if (confirm('Excluir produto?')) {
        const response = await fetch(`/cart/remove/${productId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
          },
        })
        if (response.ok) {
          window.location.reload()
        }
      }
    }
  })
})

if (subtotalDiv) calculateSubtotal()
