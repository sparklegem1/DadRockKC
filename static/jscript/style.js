const hamburger = document.getElementById('hamburger');
const navUL = document.querySelector('.navlist');

hamburger.addEventListener('click', () => {
    navUL.classList.toggle('show');
});