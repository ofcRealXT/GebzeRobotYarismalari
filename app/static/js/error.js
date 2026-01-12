document.addEventListener('DOMContentLoaded', () => {
const statusElement = document.getElementById('access-status');
const portElement = document.getElementById('contact-port');
const text = "REDDEDİLDİ";
let index = 0;

function blinkCursor() {
    statusElement.innerHTML = statusElement.innerHTML === text + '<span class="cursor">_</span>' ? text : text + '<span class="cursor">_</span>';
    setTimeout(blinkCursor, 500);
}
    
    const style = document.createElement('style');
    style.innerHTML = `
        .cursor {
            animation: blink 1s step-end infinite;
        }
        @keyframes blink {
            from, to { opacity: 0; }
            50% { opacity: 1; }
        }
    `;
    document.head.appendChild(style);

    typeText();
    
    portElement.addEventListener('mouseover', () => {
        portElement.textContent = 'ERİŞİLEMİYOR [404]';
        portElement.style.color = '#ff3333';
    });
    portElement.addEventListener('mouseout', () => {
        portElement.textContent = 'KAPALI';
        portElement.style.color = '#ffaa00';
    });
});
