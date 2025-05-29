// function fetchLiveData() {
//     fetch('/live_data')
//         .then(response => response.json())
//         .then(data => {
//             if (data.error) {
//                 document.getElementById("status").innerText = " No data available";
//             } else {
//                 document.getElementById("temp").innerText = `🌡 Temperature: ${data.temperature}°C`;
//                 document.getElementById("humidity").innerText = `💧 Humidity: ${data.humidity}%`;

//                 if (data.motion) {
//                     document.getElementById("motion").innerHTML = "🚨 Motion Detected!";
//                     document.getElementById("motion").style.color = "red";
//                 } else {
//                     document.getElementById("motion").innerHTML = "✅ No Motion";
//                     document.getElementById("motion").style.color = "green";
//                 }
//             }
//         })
//         .catch(error => console.error("Error fetching data:", error));
// }

// setInterval(fetchLiveData, 3000);

document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('startRecording');
    const stopBtn = document.getElementById('stopRecording');

    // Prevent duplicate binding
    if (startBtn && !startBtn.dataset.bound) {
        startBtn.dataset.bound = true;
        startBtn.addEventListener('click', () => {
            fetch('/start_recording', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            })
            .then(res => res.json())
            .then(data => {
                console.log("[DEBUG] Start recording response:", data);
                alert(data.status);
            });
        });
    }

    if (stopBtn && !stopBtn.dataset.bound) {
        stopBtn.dataset.bound = true;
        stopBtn.addEventListener('click', () => {
            fetch('/stop_recording', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            })
            .then(res => res.json())
            .then(data => {
                console.log("[DEBUG] Stop recording response:", data);
                alert(data.status);
            });
        });
    }
});
