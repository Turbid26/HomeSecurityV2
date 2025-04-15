function fetchAlerts() {
    fetch('/get_alerts')
    .then(response => response.json())
    .then(data => {
        let container = document.querySelector('.alert-container');
        container.innerHTML = ''; // Uncomment this to clear previous alerts if needed

        data.forEach(alert => {
            let colorClass = alert.type === 'temperature' ? 'red' : 'yellow';
            let alertItem = `
                <div class="alert-item">
                    <div class="alert-info">
                        <span class="alert-icon ${colorClass}"></span> ${alert.message}
                    </div>
                    <div class="alert-time">${alert.timestamp}</div>
                </div>
            `;
            container.innerHTML += alertItem;
        });
    });
}

fetchAlerts();
setInterval(fetchAlerts, 10000);