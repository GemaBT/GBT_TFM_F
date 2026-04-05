// --- Referencias DOM ---
const loginForm = document.getElementById("loginForm");
const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");
const apiSelect = document.getElementById("apiSelect");
const result = document.getElementById("result");
const listUsersBtn = document.getElementById("listUsersBtn");
const changePasswordBtn = document.getElementById("changePasswordBtn");

// --- LOGIN ---
loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const username = usernameInput.value;
    const password = passwordInput.value;

    let url, body;

    if (apiSelect.value === "fastapi") {
        url = "http://localhost:8000/users/usuarios/login";
        body = JSON.stringify({ username, password });
    } else { // Django
        url = "http://127.0.0.1:8001/api/token/";
        body = JSON.stringify({ username, password });
    }

    try {
        const res = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body
        });
        const data = await res.json();
        result.textContent = JSON.stringify(data, null, 2);

        // Guardar token
        const token = data.access || data.token;
        if (token) localStorage.setItem("token", token);

    } catch (err) {
        result.textContent = "Error: " + err;
    }
});

// --- LISTAR USUARIOS ---
listUsersBtn.addEventListener("click", async () => {
    const token = localStorage.getItem("token");
    if (!token) return alert("Primero haz login");

    let url = apiSelect.value === "fastapi"
        ? "http://localhost:8000/users/usuarios"
        : "http://127.0.0.1:8001/usuarios/";

    try {
        const res = await fetch(url, {
            headers: { "Authorization": `Bearer ${token}` }
        });
        const data = await res.json();
        result.textContent = JSON.stringify(data, null, 2);
    } catch (err) {
        result.textContent = "Error: " + err;
    }
});

// --- CAMBIAR CONTRASEÑA ---
changePasswordBtn.addEventListener("click", async () => {
    const old_password = prompt("Contraseña actual:");
    const new_password = prompt("Nueva contraseña:");
    const token = localStorage.getItem("token");
    if (!token) return alert("Primero haz login");

    if (apiSelect.value === "fastapi") {
        const url = "http://localhost:8000/users/usuarios/change-password";
        const body = JSON.stringify({ old_password, new_password });

        try {
            const res = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body
            });
            const data = await res.json();
            result.textContent = JSON.stringify(data, null, 2);
        } catch (err) {
            result.textContent = "Error: " + err;
        }
    } else {
        alert("Django: implementa endpoint de cambio de contraseña");
    }
});