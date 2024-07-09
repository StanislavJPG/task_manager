document.addEventListener("htmx:configRequest", function(event) {
    let csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    event.detail.headers['X-CSRFToken'] = csrfToken;
});

function openPopup(taskId) {
    var popup = document.getElementById('popupContainer-' + taskId);
    popup.style.display = 'block';
}

function closePopup(taskId) {
    var popup = document.getElementById('popupContainer-' + taskId);
    popup.style.display = 'none';
}

function openPopupDeadline(taskId) {
    var popup = document.getElementById('popupContainer-deadline-' + taskId);
    popup.style.display = 'block';
}

function closePopupDeadline(taskId) {
    var popup = document.getElementById('popupContainer-deadline-' + taskId);
    popup.style.display = 'none';
}

function openPopupTask() {
    var popup = document.getElementById('popupContainer-task');
    popup.style.display = 'block';
}

function closePopupTask() {
    var popup = document.getElementById('popupContainer-task');
    popup.style.display = 'none';
}
