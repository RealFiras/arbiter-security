let map;
let marker;

document.addEventListener('DOMContentLoaded', () => {
    map = L.map('map').setView([20, 0], 2);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '© OpenStreetMap', maxZoom: 19
    }).addTo(map);
});

document.getElementById('scanForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = document.getElementById('scanBtn');
    const resultArea = document.getElementById('resultArea');
    const dlBtn = document.getElementById('downloadBtn');

    btn.innerText = "ANALYZING TARGET...";
    btn.disabled = true;
    resultArea.classList.add('hidden');
    dlBtn.style.display = 'none';

    try {
        const res = await fetch('/analyze', {
            method: 'POST', headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ email_text: document.getElementById('emailInput').value })
        });
        
        const data = await res.json();
        
        document.getElementById('verdictBadge').innerText = data.verdict;
        document.getElementById('originIp').innerText = data.origin_ip;
        
        const typeBox = document.getElementById('aiExplanation');
        typeBox.innerHTML = '';
        let i = 0;
        function type() {
            if (i < data.explanation.length) {
                typeBox.innerHTML += data.explanation.charAt(i); i++; setTimeout(type, 5);
            }
        }
        type();
        const geo = data.geo_data;
        if (geo && geo.found) {
            document.getElementById('geoLoc').innerText = `${geo.city}, ${geo.country}`;
            setTimeout(() => {
                map.invalidateSize();
                map.setView([geo.lat, geo.lon], 5);
                if (marker) map.removeLayer(marker);
                marker = L.marker([geo.lat, geo.lon]).addTo(map)
                    .bindPopup(`<b>SOURCE:</b> ${geo.city}, ${geo.country}<br>${geo.isp}`).openPopup();
            }, 100);
        } else {
            document.getElementById('geoLoc').innerText = "CLOAKED / UNKNOWN";
            setTimeout(() => map.invalidateSize(), 100);
        }
        animateGauge(data.risk_score);
        
        const uList = document.getElementById('urlList');
        const uSec = document.getElementById('urlsSection');
        uList.innerHTML = '';
        if (data.extracted_urls.length > 0) {
            uSec.style.display = 'block';
            data.extracted_urls.forEach(u => uList.innerHTML += `<li>🔗 ${u}</li>`);
        } else uSec.style.display = 'none';

        resultArea.classList.remove('hidden');
        dlBtn.style.display = 'block';

    } catch (err) {
        alert("SYSTEM ERROR"); console.error(err);
    } finally {
        btn.innerText = "INITIATE SCAN"; btn.disabled = false;
    }
});

document.getElementById('downloadBtn').addEventListener('click', () => {
    const el = document.getElementById('resultArea');
    html2pdf().set({ margin: 5, filename: 'ARBITER_Report.pdf', image: { type: 'jpeg', quality: 0.98 }, html2canvas: { scale: 2, backgroundColor: '#050a14' }, jsPDF: { unit: 'mm', format: 'a4' } }).from(el).save();
});

function animateGauge(score) {
    const circle = document.querySelector('.circular-progress');
    const val = document.querySelector('.progress-value');
    const label = document.getElementById('riskLabel');
    let clr = score > 60 ? '#ff003c' : (score > 20 ? '#ff9d00' : '#0aff00');
    
    label.innerText = score > 60 ? "CRITICAL THREAT" : (score > 20 ? "SUSPICIOUS" : "SAFE");
    label.style.color = clr;

    let i = 0;
    const interval = setInterval(() => {
        if (i >= score) clearInterval(interval);
        else {
            i++; val.innerText = i + "%";
            circle.style.background = `conic-gradient(${clr} ${i * 3.6}deg, var(--glass-border) 0deg)`;
        }
    }, 10);
}