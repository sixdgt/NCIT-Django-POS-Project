const customCard = document.getElementById('customCard');

customCard.addEventListener('mouseover', () => {
    customCard.style.backgroundColor = '#f0f8ff';
    customCard.style.transition = 'background-color 0.3s ease';
    customCard.innerHTML = "I am changed";
});