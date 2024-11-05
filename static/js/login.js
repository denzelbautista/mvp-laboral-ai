document.getElementById('loginForm').addEventListener('submit', async function (event) {
    event.preventDefault(); // Evita el envío tradicional del formulario

    // Captura los valores de los campos
    const correo = document.getElementById('correo').value;
    const contrasena = document.getElementById('contrasena').value;

    try {
        // Enviar solicitud POST al endpoint de login
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ correo, contrasena })
        });

        const result = await response.json();

        if (response.ok && result.success) {
            // Si el inicio de sesión es exitoso, guarda el token en localStorage
            localStorage.setItem('authToken', result.token);

            // Redirecciona al dashboard
            window.location.href = '/dashboard';
        } else {
            // Muestra el mensaje de error
            alert(result.message || 'Error en el registro.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Hubo un problema al iniciar sesión. Intenta de nuevo.');
    }
});