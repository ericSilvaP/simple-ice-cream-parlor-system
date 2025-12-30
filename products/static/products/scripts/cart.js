const pricesSpan = document.querySelectorAll('.cart-price')
const subtotalDiv = document.querySelector('.subtotal-value')

// let subtotal = prices.reduce((p1, p2) => p1 + p2)
function getTagValue(element) {
  return element.textContent.replace(',', '.')
  // }
  // for (let priceSpan of pricesSpan) {
  //   Number(priceSpan.textContent).
}
console.log(pricesSpan)
