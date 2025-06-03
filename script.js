const links = document.querySelectorAll('.navbar a');
links.forEach(link => {
  if (link.href === window.location.href) link.classList.add('active');
});

const form = document.getElementById('contactForm');
if (form) {
  form.addEventListener('submit', e => {
    e.preventDefault();
    console.log('Formulário enviado:', {
      name: form.name.value,
      email: form.email.value,
      message: form.message.value
    });
    const status = document.getElementById('status');
    if (status) {
      status.textContent = 'Obrigado! Sua mensagem foi recebida.';
      status.style.color = '#0047ab';
    }
    form.reset();
  });
}

document.addEventListener('DOMContentLoaded', () => {
  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        obs.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.fade-in').forEach(el => observer.observe(el));

  const backBtn = document.getElementById('back-to-top');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 300) {
      backBtn.classList.add('visible');
    } else {
      backBtn.classList.remove('visible');
    }
  });
  backBtn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
});










