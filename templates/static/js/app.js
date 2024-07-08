document.addEventListener("htmx:configRequest", function(event) {
    let csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    event.detail.headers['X-CSRFToken'] = csrfToken;
});

function openPopup() {
    var popup = document.getElementById('popupContainer');
    popup.style.display = 'block';
}

function closePopup() {
    var popup = document.getElementById('popupContainer');
    popup.style.display = 'none';
}

function openPopupDeadline() {
    var popup = document.getElementById('popupContainer-deadline');
    popup.style.display = 'block';
}

function closePopupDeadline() {
    var popup = document.getElementById('popupContainer-deadline');
    popup.style.display = 'none';
}
