/* ===== script.js — Fix Pro Interactive Logic ===== */

// ─── Navbar scroll effect ───────────────────────────────────────
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 40);
});

// ─── Active nav link on scroll ──────────────────────────────────
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-link');

function setActiveNav() {
  const scrollY = window.scrollY + 120;
  sections.forEach(section => {
    const top = section.offsetTop;
    const height = section.offsetHeight;
    if (scrollY >= top && scrollY < top + height) {
      navLinks.forEach(link => link.classList.remove('active'));
      const active = document.querySelector(`.nav-link[href="#${section.id}"]`);
      if (active) active.classList.add('active');
    }
  });
}
window.addEventListener('scroll', setActiveNav, { passive: true });

// ─── Mobile hamburger ────────────────────────────────────────────
const hamburger = document.getElementById('hamburger');
const navLinksEl = document.getElementById('navLinks');

hamburger.addEventListener('click', () => {
  navLinksEl.classList.toggle('open');
  hamburger.classList.toggle('open');
});

// Close mobile nav on link click
navLinksEl.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => {
    navLinksEl.classList.remove('open');
    hamburger.classList.remove('open');
  });
});

// ─── Catalogue tabs ─────────────────────────────────────────────
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

tabBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    const target = btn.dataset.tab;
    tabBtns.forEach(b => b.classList.remove('active'));
    tabContents.forEach(c => c.classList.remove('active'));
    btn.classList.add('active');
    const targetEl = document.getElementById(`${target}-details`);
    if (targetEl) targetEl.classList.add('active');
  });
});

// ─── Scroll reveal ───────────────────────────────────────────────
const revealEls = document.querySelectorAll(
  '.service-card, .rate-card, .gallery-item, .contact-card, .highlight, .gtag, .catalogue-notes'
);

revealEls.forEach(el => el.classList.add('reveal'));

const revealObserver = new IntersectionObserver(
  entries => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        setTimeout(() => entry.target.classList.add('visible'), i * 60);
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
);

revealEls.forEach(el => revealObserver.observe(el));

// ─── Smooth scroll for internal links ───────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', e => {
    const target = document.querySelector(anchor.getAttribute('href'));
    if (target) {
      e.preventDefault();
      const offset = 80;
      const top = target.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: 'smooth' });
    }
  });
});

// ─── Catalogue tab from service card links ───────────────────────
document.querySelectorAll('.service-link[href^="#"]').forEach(link => {
  link.addEventListener('click', e => {
    const href = link.getAttribute('href').replace('#', '').replace('-details', '');
    const matchingTab = document.querySelector(`.tab-btn[data-tab="${href}"]`);
    if (matchingTab) {
      setTimeout(() => matchingTab.click(), 400);
    }
  });
});

// ─── Counter animation for hero stats ───────────────────────────
function animateCounter(el, target, suffix = '') {
  let start = 0;
  const duration = 1800;
  const step = Math.ceil(target / (duration / 16));
  const timer = setInterval(() => {
    start += step;
    if (start >= target) {
      el.textContent = target + suffix;
      clearInterval(timer);
    } else {
      el.textContent = start + suffix;
    }
  }, 16);
}

const statsObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const nums = entry.target.querySelectorAll('.stat-num');
      nums.forEach(num => {
        const text = num.textContent;
        const value = parseInt(text);
        const suffix = text.replace(/[0-9]/g, '');
        if (!isNaN(value)) animateCounter(num, value, suffix);
      });
      statsObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.5 });

const heroStats = document.querySelector('.hero-stats');
if (heroStats) statsObserver.observe(heroStats);

// ─── Section Header reveal ──────────────────────────────────────
const sectionHeaders = document.querySelectorAll('.section-header');
sectionHeaders.forEach(el => el.classList.add('reveal'));
sectionHeaders.forEach(el => revealObserver.observe(el));

// ─── Custom SVG Icon Mapping & Injection ────────────────────────
const ICON_MAPPING = {
  // Top level Services
  "PPRC Piping": `<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path stroke="var(--primary)" d="M3 10h10a4 4 0 0 1 4 4v7" /><path stroke="var(--accent)" d="M11 6h8a2 2 0 0 1 2 2v5" /><circle cx="3" cy="10" r="1" fill="var(--primary)" /><circle cx="19" cy="13" r="1" fill="var(--accent)" /></svg>`,
  "PVC Piping": `<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="20" height="6" rx="1" stroke="var(--primary)" /><rect x="4" y="12" width="16" height="6" rx="1" stroke="var(--accent)" /></svg>`,
  "GI Piping": `<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path stroke="var(--primary)" d="M4 12h16M4 8h16M4 16h16" /><circle cx="12" cy="12" r="5" stroke="var(--accent)" fill="var(--bg)" /></svg>`,
  "Electrical Works": `<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path stroke="var(--primary)" d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" /></svg>`,
  "Profile Lighting": `<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path stroke="var(--primary)" d="M5 3h14c1.1 0 2 .9 2 2v14c0 1.1-.9 2-2 2H5c-1.1 0-2-.9-2-2V5c0-1.1.9-2 2-2z" /><path stroke="var(--accent)" d="M7 12h10" /></svg>`,

  // Rate Cards
  "New Project (Piping Only)": `<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path stroke="var(--primary)" d="M3 3h18v18H3z" /><path stroke="var(--accent)" d="M3 9h18M9 3v18" /><path stroke="var(--primary)" d="M6 14l5-5 5 5" /></svg>`,
  "Bathroom Accessories Installation": `<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path stroke="var(--primary)" d="M4 4h12v4H4zM16 6h4M12 8v8a2 2 0 0 1-2 2H4" /><path stroke="var(--accent)" d="M10 12h.01M6 12h.01M8 15h.01" /></svg>`,
  "Water Tank": `<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="7" ry="2" stroke="var(--primary)" /><path stroke="var(--primary)" d="M5 5v12c0 2.2 3.1 4 7 4s7-1.8 7-4V5" /><path stroke="var(--accent)" d="M5 11h14M5 16h14" /></svg>`,
  "Motor Installation": `<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="8" stroke="var(--primary)" /><path stroke="var(--primary)" d="M12 2v4M12 18v4M2 12h4M18 12h4" /><circle cx="12" cy="12" r="3" stroke="var(--accent)" /></svg>`,
  "Instant Geyser": `<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="6" y="3" width="12" height="18" rx="2" stroke="var(--primary)" /><path stroke="var(--accent)" d="M10 15h4M12 7v4" /><circle cx="12" cy="11" r="2" stroke="var(--accent)" /></svg>`,
  "Standing Geyser": `<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="7" y="2" width="10" height="20" rx="4" stroke="var(--primary)" /><path stroke="var(--accent)" d="M10 8h4M10 16h4" /><circle cx="12" cy="12" r="2" stroke="var(--accent)" /></svg>`,
  "Auto Pressure Pump": `<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="7" stroke="var(--primary)" /><path stroke="var(--primary)" d="M12 5v7l4 4" /><path stroke="var(--accent)" d="M12 12m-2 0a2 2 0 1 0 4 0a2 2 0 1 0 -4 0" /></svg>`,
  "Repairing": `<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path stroke="var(--primary)" d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z" /><path stroke="var(--accent)" d="M18 18h.01M15 15h.01" /></svg>`,
  "Piping (Without Excavation)": `<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path stroke="var(--primary)" d="M2 17h20" /><rect x="4" y="8" width="16" height="5" rx="1" stroke="var(--accent)" /><path stroke="var(--primary)" d="M6 13v4M18 13v4" /></svg>`,
  "Piping (With Excavation)": `<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path stroke="var(--primary)" d="M2 10h20" /><rect x="4" y="14" width="16" height="5" rx="1" stroke="var(--accent)" /><path stroke="var(--primary)" d="M14 6l3 3-8 8-3-3 8-8z" /></svg>`,
  "Mainhole Construction": `<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9" stroke="var(--primary)" /><circle cx="12" cy="12" r="5" stroke="var(--accent)" /><path stroke="var(--primary)" d="M12 3v18M3 12h18" /></svg>`,
  "GI Fitting (Per Feet)": `<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="10" rx="2" stroke="var(--primary)" /><path stroke="var(--accent)" d="M6 7v10M12 7v10M18 7v10" /></svg>`,
  "GI Fitting (Lump Sum)": `<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="14" height="10" rx="2" stroke="var(--primary)" /><circle cx="18" cy="12" r="3" stroke="var(--accent)" /><path stroke="var(--accent)" d="M18 10v4M16 12h4" /></svg>`,
  "Piping (Per Room)": `<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path stroke="var(--primary)" d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" /><path stroke="var(--accent)" d="M9 22V12h6v10" /></svg>`,
  "Per Point (Full Package)": `<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path stroke="var(--primary)" d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .5 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5" /><path stroke="var(--primary)" d="M9 18h6M10 21h4" /><path stroke="var(--accent)" d="M12 2v3M4.9 4.9l2.1 2.1M17 7l2.1-2.1" /></svg>`,
  "Wiring (Per Room / Lump Sum)": `<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path stroke="var(--primary)" d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10 10-4.5 10-10" /><path stroke="var(--accent)" d="M12 6a6 6 0 1 0 6 6" /><circle cx="18" cy="6" r="2" stroke="var(--primary)" /></svg>`,
  "DP Dressing (Normal)": `<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="3" width="16" height="18" rx="2" stroke="var(--primary)" /><path stroke="var(--accent)" d="M8 7h8M8 12h8M8 17h8" /></svg>`,
  "DP Dressing (Heavy)": `<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="3" width="16" height="18" rx="2" stroke="var(--primary)" /><path stroke="var(--accent)" d="M12 7v10M8 12h8" /><path stroke="var(--primary)" d="M12 9l-2 3h4l-2 3" /></svg>`,
  "Fanos (Exhaust Fan)": `<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9" stroke="var(--primary)" /><path stroke="var(--accent)" d="M12 12L8 8M12 12l4 4M12 12l-4 4M12 12l4-4" /><circle cx="12" cy="12" r="2" fill="var(--accent)" /></svg>`,
  "Solar Installation": `<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" stroke="var(--primary)" /><path stroke="var(--primary)" d="M12 3v18M3 12h18" /><circle cx="12" cy="12" r="4" stroke="var(--accent)" fill="var(--bg)" /></svg>`,
  "Solar Ideas / Consultation": `<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path stroke="var(--primary)" d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .5 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5" /><path stroke="var(--primary)" d="M9 18h6M10 21h4" /><rect x="9" y="6" width="6" height="4" stroke="var(--accent)" /></svg>`,
  "Solar Repairing": `<svg class="custom-icon" viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="12" rx="2" stroke="var(--primary)" /><path stroke="var(--accent)" d="M14.7 16.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z" /></svg>`
};

function injectCustomIcons() {
  // 1. Process service-card icons
  document.querySelectorAll('.service-card').forEach(card => {
    const titleEl = card.querySelector('h3');
    if (!titleEl) return;
    const title = titleEl.textContent.trim();
    const iconContainer = card.querySelector('.service-icon');
    if (iconContainer && ICON_MAPPING[title]) {
      iconContainer.innerHTML = ICON_MAPPING[title];
    }
  });

  // 2. Process rate-card icons
  document.querySelectorAll('.rate-card').forEach(card => {
    const titleEl = card.querySelector('h4');
    if (!titleEl) return;
    const title = titleEl.textContent.trim();
    const iconContainer = card.querySelector('.rate-icon');
    if (iconContainer && ICON_MAPPING[title]) {
      iconContainer.innerHTML = ICON_MAPPING[title];
    }
  });
}

// ─── Page load animation ─────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  injectCustomIcons();
  document.body.style.opacity = '0';
  requestAnimationFrame(() => {
    document.body.style.transition = 'opacity 0.5s ease';
    document.body.style.opacity = '1';
  });
});
