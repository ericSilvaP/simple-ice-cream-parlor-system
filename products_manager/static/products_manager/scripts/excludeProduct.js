const excludeProductButton = document.querySelector(
  '#exclude-product-form > button'
)

function getCSRFToken() {
  return document.cookie
    .split('; ')
    .find((row) => row.startsWith('csrftoken='))
    ?.split('=')[1]
}

excludeProductButton.addEventListener('click', async (e) => {
  e.preventDefault() // impede o submit do form

  if (confirm('Excluir produto?')) {
    e.target.closest('form').submit()
  }
})
