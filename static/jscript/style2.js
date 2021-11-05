const hamburger = document.querySelector('#hamburger');
const navUL = document.querySelector('.navlist');

hamburger.addEventListener('click', () => {
    console.log('hi');
    navUL.classList.toggle('show');
});