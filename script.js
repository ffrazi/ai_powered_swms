function saveToDatabase() {
    let name = document.getElementById("name").value;
    let email = document.getElementById("email").value;
    let phone = document.getElementById("phone").value;
    let area = document.getElementById("area").value;

    if (!name || !email || !phone || !area) {
        alert("Please fill all fields");
        return;
    }

    let formData = { name, email, phone, area };

    fetch("http://127.0.0.1:5000/add_user", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
    })
    .then(response => response.json())
    .then(data => {
        console.log("Response:", data);
        alert(data.message);  // Show success or error message
    })
    .catch(error => console.error("Error:", error));
}