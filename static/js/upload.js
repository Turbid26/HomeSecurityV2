function removeFace(faceUrl) {
    fetch('/remove_face', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ face: faceUrl })
    }).then(response => response.json()).then(data => {
        if (data.success) location.reload();
    });
}

document.addEventListener("DOMContentLoaded", function () {
    const roleSelect = document.getElementById("roleSelect");
    const guestFields = document.getElementById("guestFields");

    function toggleGuestFields() {
        guestFields.style.display = roleSelect.value === "guest" ? "block" : "none";
    }

    toggleGuestFields();
    roleSelect.addEventListener("change", toggleGuestFields);
});