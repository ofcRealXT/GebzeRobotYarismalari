const days = document.getElementById('days');

if (days) { // sadece geri sayım öğeleri varsa çalıştır
    const targetDate = new Date('2026-06-01T09:00:00');

    function updateCountdown() {
        const now = new Date();
        const diff = Math.max(0, targetDate - now);

        days.textContent = String(Math.floor(diff / (1000 * 60 * 60 * 24))).padStart(2, '0');
        document.getElementById('hours').textContent = String(Math.floor((diff / (1000 * 60 * 60)) % 24)).padStart(2, '0');
        document.getElementById('minutes').textContent = String(Math.floor((diff / (1000 * 60)) % 60)).padStart(2, '0');
        document.getElementById('seconds').textContent = String(Math.floor((diff / 1000) % 60)).padStart(2, '0');
    }

    updateCountdown();
    setInterval(updateCountdown, 1000);
}

const slider = document.getElementById('auto-slider');
const cards = slider ? slider.querySelectorAll('.slider-card') : [];
let currentIndex = 0;
const slideInterval = 2500; 

if (slider && cards.length > 0) {
    function nextSlide() {
        currentIndex++;
        if (currentIndex >= cards.length) {
            currentIndex = 0;
        }

        const scrollAmount = currentIndex * (cards[0].offsetWidth + 30);
        
        slider.scrollTo({
            left: scrollAmount,
            behavior: 'smooth'
        });
    }


    setInterval(nextSlide, slideInterval);
}

// --------------------------------------------------------

document.querySelectorAll('.faq-question').forEach(btn => {
    btn.addEventListener('click', () => {
        const item = btn.parentElement;
        item.classList.toggle('active');

        // diğer tüm FAQ öğelerinin açık durumunu kapat
        document.querySelectorAll('.faq-item').forEach(i => {
            if(i !== item) i.classList.remove('active');
        });
    });
});
