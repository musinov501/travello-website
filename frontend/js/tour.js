document.addEventListener('DOMContentLoaded', function () {
  const searchInput = document.getElementById('searchInput');
  const tourCards = document.querySelectorAll('.hotelCard.tours');
  

  searchInput.addEventListener('input', function () {
    const searchTerm = searchInput.value.toLowerCase().trim();

    tourCards.forEach(card => {
      const title = card.querySelector('h1').textContent.toLowerCase();

      if (searchTerm === '' || title.includes(searchTerm)) {
        card.style.display = '';
      } else {
        card.style.display = 'none';
      }
    });
  });
});
