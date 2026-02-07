document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const messageBox = document.getElementById('message-box');
    const submitBtn = document.getElementById('submit-btn');
    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const payload = {
        email: email,
        password: password
    };

    try {
        submitBtn.disabled = true;
        submitBtn.innerText = "Masuk...";

        const response = await fetch('/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (response.ok) {
            localStorage.setItem('access_token', result.data.token);
            localStorage.setItem('user_id', result.data.user_id);
            
            showMessage("Login berhasil! Mengalihkan...", "green");
            
            setTimeout(() => {
                window.location.href = "/chat"; 
            }, 1500);
        } else {
            showMessage(result.message || "Email atau password salah", "red");
            submitBtn.disabled = false;
            submitBtn.innerText = "Masuk";
        }
    } catch (error) {
        console.log("There is an error: ", error);
        showMessage("Terjadi kesalahan koneksi", "red");
        submitBtn.disabled = false;
        submitBtn.innerText = "Masuk";
    }
});

function showMessage(text, color) {
    const messageBox = document.getElementById('message-box');
    messageBox.innerText = text;
    messageBox.style.display = 'block';
    messageBox.style.backgroundColor = color === "green" ? "#d4edda" : "#f8d7da";
    messageBox.style.color = color === "green" ? "#155724" : "#721c24";
}