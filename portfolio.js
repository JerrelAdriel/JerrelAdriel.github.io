// Scroll fade-in animation
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.1 });

document.querySelectorAll('.project-card, .skill-group, .contact-card').forEach(el => {
  el.classList.add('fade-in');
  observer.observe(el);
});

// Nav scroll effect
window.addEventListener('scroll', () => {
  document.getElementById('nav').style.background =
    window.scrollY > 50 ? 'rgba(8,8,8,0.98)' : 'rgba(8,8,8,0.85)';
});

// Smooth scroll for nav links
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    e.preventDefault();
    document.querySelector(a.getAttribute('href'))
      ?.scrollIntoView({ behavior: 'smooth' });
  });
});

// ── LIGHTBOX GALLERY ─────────────────────────────
const SCREENSHOTS = {
  'agent-jr': [
    { src: 'assets/screenshots/agent-jr/01-main.png', caption: 'Tampilan Chat Agent-JR' },
  ],
  'brain-tumor': [
    { src: 'assets/screenshots/brain-tumor/01-home.png', caption: 'Landing Page — Modern Dark Theme' },
    { src: 'assets/screenshots/brain-tumor/02-classify.png', caption: 'Halaman Klasifikasi — Drag & Drop Upload' },
  ],
  'lelang': [
    { src: 'assets/screenshots/lelang/01-hero.png', caption: 'Hero Banner — Bulan Ramadhan Promo' },
    { src: 'assets/screenshots/lelang/02-produk.png', caption: 'Grid 12 Produk dengan harga' },
  ],
  'stockop': [
    { src: 'assets/screenshots/stockop/03-peminjaman.png', caption: 'Halaman Peminjaman — 12 data peralatan teknik' },
    { src: 'assets/screenshots/stockop/04-pengambilan.png', caption: 'Halaman Pengambilan — 11 data konsumable' },
    { src: 'assets/screenshots/stockop/01-login.png', caption: 'Login Page (Desktop)' },
    { src: 'assets/screenshots/stockop/02-login-mobile.png', caption: 'Login Page (Mobile — Responsive)' },
  ],
  'jump-game': [
    { src: 'assets/screenshots/jump-game/01-intro.png', caption: 'Welcome Screen — petunjuk kontrol' },
    { src: 'assets/screenshots/jump-game/02-gameplay.png', caption: 'Gameplay — Karakter berlari & loncat' },
    { src: 'assets/screenshots/jump-game/03-gameover.png', caption: 'Game Over — dengan high score localStorage' },
  ],
};

const lightbox = document.getElementById('lightbox');
const lbImg = lightbox.querySelector('.lb-img');
const lbTitle = lightbox.querySelector('.lb-title');
const lbCounter = lightbox.querySelector('.lb-counter');
const lbPrev = lightbox.querySelector('.lb-prev');
const lbNext = lightbox.querySelector('.lb-next');
const lbClose = lightbox.querySelector('.lb-close');

let currentImages = [];
let currentIndex = 0;
let currentTitle = '';

function openLightbox(key, title) {
  currentImages = SCREENSHOTS[key] || [];
  currentTitle = title;
  if (currentImages.length === 0) return;
  currentIndex = 0;
  updateLightbox();
  lightbox.classList.remove('hidden');
  document.body.style.overflow = 'hidden';
}

function updateLightbox() {
  const item = currentImages[currentIndex];
  const src = typeof item === 'string' ? item : item.src;
  const caption = typeof item === 'string' ? '' : (item.caption || '');
  lbImg.src = src;
  lbTitle.textContent = currentTitle + (caption ? ' — ' + caption : '');
  lbCounter.textContent = currentImages.length > 1 ? `${currentIndex + 1} / ${currentImages.length}` : '';
  lbPrev.style.display = currentImages.length > 1 ? '' : 'none';
  lbNext.style.display = currentImages.length > 1 ? '' : 'none';
}

function closeLightbox() {
  lightbox.classList.add('hidden');
  document.body.style.overflow = '';
}

function navigateLightbox(delta) {
  currentIndex = (currentIndex + delta + currentImages.length) % currentImages.length;
  updateLightbox();
}

// Bind triggers
document.querySelectorAll('[data-screenshots]').forEach(el => {
  el.addEventListener('click', (e) => {
    e.preventDefault();
    const key = el.dataset.screenshots;
    const title = el.dataset.title || '';
    openLightbox(key, title);
  });
});

lbClose.addEventListener('click', closeLightbox);
lbPrev.addEventListener('click', () => navigateLightbox(-1));
lbNext.addEventListener('click', () => navigateLightbox(1));
lightbox.addEventListener('click', (e) => {
  if (e.target === lightbox) closeLightbox();
});

document.addEventListener('keydown', (e) => {
  if (lightbox.classList.contains('hidden')) return;
  if (e.key === 'Escape') closeLightbox();
  if (e.key === 'ArrowLeft') navigateLightbox(-1);
  if (e.key === 'ArrowRight') navigateLightbox(1);
});
