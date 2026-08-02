const navToggle = document.querySelector('.nav-toggle');
const navMenu = document.querySelector('#nav-menu');
const year = document.querySelector('#year');
const form = document.querySelector('#contact-form');

if (year) year.textContent = new Date().getFullYear();

if (navToggle && navMenu) {
  navToggle.addEventListener('click', () => {
    const isOpen = navMenu.classList.toggle('open');
    navToggle.setAttribute('aria-expanded', String(isOpen));
  });

  navMenu.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      navMenu.classList.remove('open');
      navToggle.setAttribute('aria-expanded', 'false');
    });
  });
}

const attributionKeys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'cta'];
const params = new URLSearchParams(window.location.search);
const currentAttribution = {};
attributionKeys.forEach((key) => {
  const value = params.get(key);
  if (value) currentAttribution[key] = value;
});

if (Object.keys(currentAttribution).length) {
  try {
    window.localStorage.setItem('opsGarageAttribution', JSON.stringify(currentAttribution));
  } catch (error) {
    // Attribution storage is helpful, not required.
  }
}

function readStoredAttribution() {
  try {
    return JSON.parse(window.localStorage.getItem('opsGarageAttribution') || '{}');
  } catch (error) {
    return {};
  }
}

function decorateInternalLink(link) {
  const href = link.getAttribute('href') || '';
  if (!href.startsWith('/intake/') && !href.startsWith('/ops-snapshot/')) return;

  const url = new URL(href, window.location.origin);
  const stored = readStoredAttribution();
  const cta = link.dataset.cta;

  attributionKeys.forEach((key) => {
    if (!url.searchParams.has(key) && stored[key]) url.searchParams.set(key, stored[key]);
  });

  if (cta) url.searchParams.set('cta', cta);
  link.setAttribute('href', `${url.pathname}${url.search}${url.hash}`);
}

document.querySelectorAll('a[href]').forEach((link) => {
  decorateInternalLink(link);
  link.addEventListener('click', () => {
    const cta = link.dataset.cta || link.textContent.trim().slice(0, 60);
    if (!cta) return;
    try {
      window.localStorage.setItem('opsGarageLastCta', JSON.stringify({
        cta,
        href: link.href,
        page: window.location.pathname,
        at: new Date().toISOString()
      }));
    } catch (error) {
      // Ignore storage failures.
    }
  });
});

if (form) {
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const data = new FormData(form);
    const name = encodeURIComponent(data.get('name') || '');
    const email = encodeURIComponent(data.get('email') || '');
    const message = encodeURIComponent(data.get('message') || '');
    const subject = encodeURIComponent('Ops Garage AI build request');
    const body = `Name: ${name}%0AEmail: ${email}%0A%0AWorkflow:%0A${message}`;
    window.location.href = `mailto:frank@opsgarageai.com?subject=${subject}&body=${body}`;
  });
}
