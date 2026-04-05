const loginForm = document.getElementById("loginForm");
const result = document.getElementById("result");

loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const api = document.getElementById("apiSelect").value;

    let url;
    let body;

    if (api === "fastapi") {
        url = "http://127.0.0.1:8000/users/login"; // cambia al endpoint login de FastAPI
        body = JSON.stringify({ username, password });
    } else {
        url = "http://127.0.0.1:8001/token/"; // endpoint JWT Django
        body = JSON.stringify({ username, password });
    }

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: body
        });

        const data = await response.json();
        result.textContent = JSON.stringify(data, null, 2);

        // Guardar token si quieres usarlo luego
        if (data.access) {
            localStorage.setItem("token", data.access);
        } else if (data.token) {
            localStorage.setItem("token", data.token);
        }

    } catch (error) {
        result.textContent = "Error: " + error;
    }
});