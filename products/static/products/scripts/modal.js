let modals = document.querySelectorAll('.modal')
const filterButton = document.querySelector('#filter-button-container')
const filterModal = document.querySelector('#filter-modal')

filterButton.addEventListener('click', () => {
  filterModal.classList.toggle('hidden')
})

modals.forEach((modal) => {
  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.classList.toggle('hidden')
    }
  })
})
