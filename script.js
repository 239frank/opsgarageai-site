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

if (form) {
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const data = new FormData(form);
    const name = encodeURIComponent(data.get('name') || '');
    const email = encodeURIComponent(data.get('email') || '');
    const message = encodeURIComponent(data.get('message') || '');
    const subject = encodeURIComponent('Ops Garage AI build request');
    const body = `Name: ${name}%0AEmail: ${email}%0A%0AWorkflow:%0A${message}`;
    window.location.href = `mailto:hello@opsgarageai.com?subject=${subject}&body=${body}`;
  });
}
