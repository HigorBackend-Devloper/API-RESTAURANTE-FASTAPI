// Interações de interface; dados e autenticação pertencem ao backend futuro.
const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navegacao');
if (menuButton && navigation) {
  menuButton.hidden = false;
  navigation.classList.add('collapsible');
  menuButton.addEventListener('click', () => {
    const open = menuButton.getAttribute('aria-expanded') !== 'true';
    menuButton.setAttribute('aria-expanded', String(open));
    navigation.classList.toggle('is-open', open);
  });
  navigation.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      navigation.classList.remove('is-open');
      menuButton.setAttribute('aria-expanded', 'false');
      menuButton.focus();
    }
  });
}

document.querySelectorAll('[data-password]').forEach((button) => {
  const input = document.getElementById(button.dataset.password);
  if (!input) return;
  button.hidden = false;
  button.addEventListener('click', () => {
    const visible = input.type === 'password';
    input.type = visible ? 'text' : 'password';
    button.textContent = visible ? 'Ocultar senha' : 'Mostrar senha';
    button.setAttribute('aria-pressed', String(visible));
  });
});

document.querySelectorAll('form[data-confirm]').forEach((form) => {
  form.addEventListener('submit', (event) => {
    if (!window.confirm(form.dataset.confirm)) event.preventDefault();
  });
});
