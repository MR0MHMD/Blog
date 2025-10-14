const slider = document.getElementById('slider');
const slides = slider.querySelector('.slides');
const images = slider.querySelectorAll('.slides img');
const prev = slider.querySelector('.prev');
const next = slider.querySelector('.next');
const dotsContainer = slider.querySelector('.dots');
let index = 0;

images.forEach((_, i) => {
  const dot = document.createElement('div');
  dot.classList.add('dot');
  if (i === 0) dot.classList.add('active');
  dot.addEventListener('click', () => {
    index = i;
    showSlide();
  });
  dotsContainer.appendChild(dot);
});

const dots = dotsContainer.querySelectorAll('.dot');

function showSlide() {
  slides.style.transform = `translateX(${-index * 100}%)`;
  dots.forEach(dot => dot.classList.remove('active'));
  dots[index].classList.add('active');
}

next.addEventListener('click', () => {
  index = (index + 1) % images.length;
  showSlide();
});

prev.addEventListener('click', () => {
  index = (index - 1 + images.length) % images.length;
  showSlide();
});

let startX = 0;
let endX = 0;

slider.addEventListener('touchstart', e => startX = e.touches[0].clientX);
slider.addEventListener('touchend', e => {
  endX = e.changedTouches[0].clientX;
  handleSwipe();
});

slider.addEventListener('mousedown', e => startX = e.clientX);
slider.addEventListener('mouseup', e => {
  endX = e.clientX;
  handleSwipe();
});

function handleSwipe() {
  const diff = startX - endX;
  if (Math.abs(diff) > 50) {
    if (diff > 0) {
      index = (index + 1) % images.length;
    } else {
      index = (index - 1 + images.length) % images.length;
    }
    showSlide();
  }
}