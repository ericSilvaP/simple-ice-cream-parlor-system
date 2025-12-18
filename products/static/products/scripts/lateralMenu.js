const latMenu = document.getElementById('lateral-menu')
const burgerMenu = document.querySelector('.burger-menu-container')

burgerMenu.addEventListener('click', () => {
  latMenu.classList.toggle('display-none')
})
