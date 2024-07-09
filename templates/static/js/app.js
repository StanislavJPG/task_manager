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

function valueChange(item){
	return item.checked;
}

function updateTaskStatus(taskId, item) {
    let csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    fetch(`/task/status/pk=${taskId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        body: JSON.stringify({
            checked: valueChange(item)
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log(data); // Результат відповіді від сервера
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    });
}
