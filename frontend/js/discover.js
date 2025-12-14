document.addEventListener('DOMContentLoaded', function () {


  const filterSelect = document.getElementById('filter');
  const searchInput = document.getElementById('search');
  const cards = document.querySelectorAll('.hotelCard');
  const tourCard = document.querySelectorAll('.tours');
  const hotelCard = document.querySelectorAll('.hotels');
  const excurCard = document.querySelectorAll('.excursions');


  const lenis = new Lenis({
    autoRaf: true,
    wheelMultiplier: 0.7,
    touchMultiplier: 0.8,
  });


  function filterAndSearch() {
    const selectedFilter = filterSelect.value;
    const searchTerm = searchInput.value.toLowerCase();

    cards.forEach(card => {
      const cardType = Array.from(card.classList).find(cls =>
        ['hotels', 'tours', 'destinations', 'excursions'].includes(cls)
      );

      const cardTitle = card.querySelector('h1').textContent.toLowerCase();

      const matchesFilter = selectedFilter === 'all' || cardType === selectedFilter;
      const matchesSearch = cardTitle.includes(searchTerm);

      card.style.display = matchesFilter && matchesSearch ? 'block' : 'none';
    });
  }

  filterSelect.addEventListener('change', filterAndSearch);
  searchInput.addEventListener('input', filterAndSearch);

  tourCard.forEach(card => {
    card.addEventListener("click", function () {
      window.location.href = './tourDetails.html'
    })
  });

  hotelCard.forEach(card => {
    card.addEventListener("click", function () {
      window.location.href = './hotelDesc.html'
    })
  });

  excurCard.forEach(card => {
    card.addEventListener("click", function () {
      window.location.href = './tourDetails.html'
    })
  });



});