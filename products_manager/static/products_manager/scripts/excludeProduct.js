const excludeProductButton = document.querySelector(
  '#exclude-product-form > button'
)

excludeProductButton.addEventListener('click', () => {
  if (!confirm('Excluir produto?')) {
    window.location.reload()
  }
})
