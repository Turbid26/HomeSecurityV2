function fetchLiveData() {
    fetch('/live_data')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById("status").innerText = " No data available";
            } else {
                document.getElementById("temp").innerText = `🌡 Temperature: ${data.temperature}°C`;
                document.getElementById("humidity").innerText = `💧 Humidity: ${data.humidity}%`;

                if (data.motion) {
                    document.getElementById("motion").innerHTML = "🚨 Motion Detected!";
                    document.getElementById("motion").style.color = "red";
                } else {
                    document.getElementById("motion").innerHTML = "✅ No Motion";
                    document.getElementById("motion").style.color = "green";
                }
            }
        })
        .catch(error => console.error("Error fetching data:", error));
}

setInterval(fetchLiveData, 3000);