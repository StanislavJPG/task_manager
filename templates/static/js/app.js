const csrfToken = document.currentScript.dataset.csrftoken;

htmx.on('htmx:configRequest', (event) => {
  if (csrfToken) {
    evt.detail.headers['x-csrftoken'] = csrfToken;
  }
});