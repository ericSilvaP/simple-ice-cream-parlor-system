const pricesSpan = document.querySelectorAll('.cart-price')
const subtotalDiv = document.querySelector('.subtotal-value')

function getTagValue(element) {
  let [integers, cents] = element.textContent.split(',')
  integers = integers.replace('.', '')
  return Number([integers, cents].join('.'))
}

const total = [...pricesSpan]
  .map(getTagValue)
  .reduce((sum, value) => sum + value, 0)

subtotalDiv.textContent = total.toLocaleString('pt-br')
