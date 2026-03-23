let modals = document.querySelectorAll('.modal')
const filterButtons = document.querySelectorAll('.filter-button-toggle')
const filterModal = document.querySelector('#filter-modal')

filterButtons.forEach((filterButton) => {
  filterButton.addEventListener('click', () => {
    filterModal.classList.toggle('hidden')
  })
})

modals.forEach((modal) => {
  modal.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.classList.toggle('hidden')
    }
  })
})
