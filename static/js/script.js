// ========== PARTICLE CANVAS ==========
(function initParticles() {
    const canvas = document.getElementById('particles');
    const ctx = canvas.getContext('2d');
    let particles = [];
    let animFrame;

    function resize() {
        canvas.width  = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resize);
    resize();

    class Particle {
        constructor() { this.reset(); }
        reset() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.size = Math.random() * 1.5 + 0.3;
            this.speedX = (Math.random() - 0.5) * 0.3;
            this.speedY = (Math.random() - 0.5) * 0.3;
            this.opacity = Math.random() * 0.4 + 0.1;
            this.color = Math.random() > 0.5 ? '99,179,237' : '159,122,234';
        }
        update() {
            this.x += this.speedX;
            this.y += this.speedY;
            if (this.x < 0 || this.x > canvas.width || this.y < 0 || this.y > canvas.height) {
                this.reset();
            }
        }
        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(${this.color},${this.opacity})`;
            ctx.fill();
        }
    }

    for (let i = 0; i < 80; i++) particles.push(new Particle());

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles.forEach(p => { p.update(); p.draw(); });
        // Draw connecting lines
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 100) {
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.strokeStyle = `rgba(99,179,237,${0.05 * (1 - dist / 100)})`;
                    ctx.lineWidth = 0.5;
                    ctx.stroke();
                }
            }
        }
        animFrame = requestAnimationFrame(animate);
    }
    animate();
})();

// ========== NAVBAR SCROLL ==========
window.addEventListener('scroll', () => {
    const nav = document.getElementById('navbar');
    nav.classList.toggle('scrolled', window.scrollY > 50);
});

// ========== PROGRESS STEPS ==========
function updateProgressSteps(activeSection) {
    document.querySelectorAll('.step').forEach(step => {
        const n = parseInt(step.dataset.step);
        step.classList.remove('active', 'done');
        if (n < activeSection) step.classList.add('done');
        else if (n === activeSection) step.classList.add('active');
    });
    document.querySelectorAll('.step-line').forEach((line, idx) => {
        line.classList.toggle('done', idx + 1 < activeSection);
    });
}

// Intersection Observer for step progress
const sectionObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const sec = parseInt(entry.target.dataset.section);
            updateProgressSteps(sec);
        }
    });
}, { threshold: 0.4 });
document.querySelectorAll('.form-card').forEach(c => sectionObserver.observe(c));

// ========== CREDIT SCORE LIVE UPDATE ==========
const creditInput = document.getElementById('credit_score');
const creditFill  = document.getElementById('creditFill');
const creditBadge = document.getElementById('creditBadge');

function updateCreditMeter(score) {
    const pct = ((score - 300) / 550) * 100;
    creditFill.style.width = Math.max(0, Math.min(100, pct)) + '%';
    let label = 'Poor', color = '#fc8181';
    if (score >= 740) { label = 'Excellent'; color = '#68d391'; }
    else if (score >= 670) { label = 'Good';      color = '#9ae6b4'; }
    else if (score >= 580) { label = 'Fair';       color = '#f6ad55'; }
    else if (score >= 500) { label = 'Poor';       color = '#fc8181'; }
    else                   { label = 'Very Poor';  color = '#fc8181'; }
    creditBadge.textContent = label;
    creditBadge.style.background = color + '22';
    creditBadge.style.color = color;
    creditBadge.style.borderColor = color + '44';
}
creditInput.addEventListener('input', () => updateCreditMeter(parseInt(creditInput.value) || 300));
updateCreditMeter(720);

// ========== DTI LIVE UPDATE ==========
const dtiInput = document.getElementById('debt_to_income');
const dtiFill  = document.getElementById('dtiFill');
const dtiBadge = document.getElementById('dtiBadge');

function updateDTI(val) {
    const pct = Math.min(val * 100, 100);
    dtiFill.style.width = pct + '%';
    let label = 'Good', color = '#68d391';
    if (val > 0.5)        { label = 'High';     color = '#fc8181'; }
    else if (val > 0.36)  { label = 'Moderate'; color = '#f6ad55'; }
    dtiBadge.textContent = label;
    dtiBadge.style.background = color + '22';
    dtiBadge.style.color = color;
    dtiBadge.style.borderColor = color + '44';
}
dtiInput.addEventListener('input', () => updateDTI(parseFloat(dtiInput.value) || 0));
updateDTI(0.35);

// ========== INCOME HINT ==========
const incomeInput = document.getElementById('annual_income');
const incomeHint  = document.getElementById('income-hint');
incomeInput.addEventListener('input', () => {
    const monthly = Math.round((parseFloat(incomeInput.value) || 0) / 12);
    incomeHint.textContent = '≈ $' + monthly.toLocaleString() + ' / month';
});

// ========== TOAST ==========
function showToast(msg, duration = 3000) {
    const toast = document.getElementById('toast');
    toast.textContent = msg;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), duration);
}

// ========== MODAL HELPERS ==========
function openModal() {
    const modal = document.getElementById('resultModal');
    modal.classList.add('show');
    document.body.style.overflow = 'hidden';
}
function closeModal() {
    const modal = document.getElementById('resultModal');
    modal.classList.remove('show');
    document.body.style.overflow = '';
}
window.closeModal = closeModal;

document.getElementById('resultModal').addEventListener('click', function(e) {
    if (e.target === this) closeModal();
});

// ========== LOADING STEPS ANIMATION ==========
function animateLoadingSteps() {
    const steps = ['step1','step2','step3'];
    const delays = [300, 700, 1100];
    steps.forEach((id, i) => {
        const el = document.getElementById(id);
        if (!el) return;
        el.classList.remove('active','done');
        setTimeout(() => {
            el.classList.add('active');
            el.querySelector('i').className = 'fas fa-circle-notch fa-spin';
        }, delays[i]);
        setTimeout(() => {
            el.classList.remove('active');
            el.classList.add('done');
            el.querySelector('i').className = 'fas fa-check-circle';
        }, delays[i] + 400);
    });
}

// ========== FORM SUBMIT ==========
document.getElementById('loanForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const btn = document.getElementById('submitBtn');
    const formData = new FormData(e.target);
    const data = Object.fromEntries(formData.entries());

    // Button loading state
    btn.disabled = true;
    btn.classList.add('loading');
    btn.querySelector('.btn-text').innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Analyzing...';

    // Show modal loader
    document.getElementById('loaderState').classList.remove('hidden');
    document.getElementById('resultState').classList.add('hidden');
    openModal();
    animateLoadingSteps();

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        const result = await response.json();

        // Wait for step animations to finish
        setTimeout(() => {
            document.getElementById('loaderState').classList.add('hidden');
            document.getElementById('resultState').classList.remove('hidden');
            renderResult(result, data);
        }, 1600);

    } catch (err) {
        setTimeout(() => {
            document.getElementById('loaderState').classList.add('hidden');
            document.getElementById('resultState').classList.remove('hidden');
            renderError(err.message);
        }, 1000);
    } finally {
        setTimeout(() => {
            btn.disabled = false;
            btn.classList.remove('loading');
            btn.querySelector('.btn-text').innerHTML = '<i class="fas fa-microchip"></i> Analyze My Application';
        }, 1700);
    }
});

// ========== RENDER RESULT ==========
function renderResult(result, formData) {
    const iconWrap    = document.getElementById('resultIconWrap');
    const resultIcon  = document.getElementById('resultIcon');
    const resultBadge = document.getElementById('resultBadge');
    const statusText  = document.getElementById('statusText');
    const msgText     = document.getElementById('msgText');
    const probFill    = document.getElementById('probFill');
    const probPercent = document.getElementById('probPercent');
    const ripple      = document.querySelector('.result-ripple');
    const factors     = document.getElementById('factorsGrid');

    if (!result.success) { renderError(result.error || 'Unknown error'); return; }

    const approved = result.prediction === 1;
    const pct      = approved ? result.probability * 100 : (1 - result.probability) * 100;

    if (approved) {
        resultIcon.style.background = 'rgba(104,211,145,0.15)';
        resultIcon.style.border     = '2px solid #68d391';
        resultIcon.innerHTML        = '<i class="fas fa-check" style="color:#68d391"></i>';
        ripple.style.borderColor    = '#68d391';
        resultBadge.textContent     = 'APPROVED';
        resultBadge.style.background= 'rgba(104,211,145,0.12)';
        resultBadge.style.color     = '#68d391';
        resultBadge.style.border    = '1px solid rgba(104,211,145,0.3)';
        statusText.style.color      = '#68d391';
        probFill.style.background   = 'linear-gradient(90deg, #38a169, #68d391)';
        probPercent.style.color     = '#68d391';
    } else {
        resultIcon.style.background = 'rgba(252,129,129,0.15)';
        resultIcon.style.border     = '2px solid #fc8181';
        resultIcon.innerHTML        = '<i class="fas fa-times" style="color:#fc8181"></i>';
        ripple.style.borderColor    = '#fc8181';
        resultBadge.textContent     = 'DECLINED';
        resultBadge.style.background= 'rgba(252,129,129,0.12)';
        resultBadge.style.color     = '#fc8181';
        resultBadge.style.border    = '1px solid rgba(252,129,129,0.3)';
        statusText.style.color      = '#fc8181';
        probFill.style.background   = 'linear-gradient(90deg, #c53030, #fc8181)';
        probPercent.style.color     = '#fc8181';
    }

    statusText.textContent = result.status;
    msgText.textContent    = result.message;

    // Animate probability bar
    probFill.style.width = '0%';
    probPercent.textContent = '0%';
    requestAnimationFrame(() => {
        setTimeout(() => {
            probFill.style.width = pct + '%';
            animateCounter(probPercent, 0, Math.round(pct), 1200, '%');
        }, 100);
    });

    // Key factors grid
    factors.innerHTML = '';
    const items = [
        { label: 'Credit Score',  value: formData.credit_score  || '—' },
        { label: 'Annual Income', value: '$' + Number(formData.annual_income || 0).toLocaleString() },
        { label: 'DTI Ratio',     value: (parseFloat(formData.debt_to_income || 0) * 100).toFixed(0) + '%' },
        { label: 'Loan Amount',   value: '$' + Number(formData.loan_amount || 0).toLocaleString() },
    ];
    items.forEach((item, i) => {
        const div = document.createElement('div');
        div.className = 'factor-item';
        div.style.animationDelay = (i * 0.08) + 's';
        div.innerHTML = `<div class="factor-label">${item.label}</div><div class="factor-value">${item.value}</div>`;
        factors.appendChild(div);
    });

    showToast(approved ? '✅ Application Approved!' : '❌ Application Declined');
}

function renderError(msg) {
    const resultIcon  = document.getElementById('resultIcon');
    const resultBadge = document.getElementById('resultBadge');
    const statusText  = document.getElementById('statusText');
    const msgText     = document.getElementById('msgText');
    const probFill    = document.getElementById('probFill');
    const probPercent = document.getElementById('probPercent');

    resultIcon.style.background = 'rgba(246,173,85,0.15)';
    resultIcon.style.border     = '2px solid #f6ad55';
    resultIcon.innerHTML        = '<i class="fas fa-exclamation-triangle" style="color:#f6ad55"></i>';
    resultBadge.textContent     = 'ERROR';
    resultBadge.style.background= 'rgba(246,173,85,0.12)';
    resultBadge.style.color     = '#f6ad55';
    resultBadge.style.border    = '1px solid rgba(246,173,85,0.3)';
    statusText.textContent      = 'Error';
    statusText.style.color      = '#f6ad55';
    msgText.textContent         = msg || 'Something went wrong. Please check your inputs.';
    probFill.style.width        = '0%';
    probPercent.textContent     = '—';
    document.getElementById('factorsGrid').innerHTML = '';
    showToast('⚠️ An error occurred. Please try again.');
}

// ========== COUNTER ANIMATION ==========
function animateCounter(el, from, to, duration, suffix='') {
    const start = performance.now();
    function update(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const ease = 1 - Math.pow(1 - progress, 3);
        el.textContent = Math.round(from + (to - from) * ease) + suffix;
        if (progress < 1) requestAnimationFrame(update);
    }
    requestAnimationFrame(update);
}

// ========== CARD ENTRANCE ANIMATIONS ==========
const cardObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.form-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(30px)';
    card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    cardObserver.observe(card);
});
