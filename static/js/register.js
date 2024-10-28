document.getElementById('register').addEventListener('submit', async (event) => {
    event.preventDefault(); // Previene que el formulario recargue la página

    const nombre = document.getElementById('nombre').value;
    const razonSocial = document.getElementById('razon_social').value;
    const ruc = document.getElementById('RUC').value;
    const email = document.getElementById('correo').value;
    const numero = document.getElementById('numero_contacto').value;
    const password = document.getElementById('contrasena').value;

    // Creamos un objeto con los datos a enviar
    const empresaData = {
        nombre,
        razon_social: razonSocial,
        RUC: ruc,
        correo: email,
        numero_contacto: numero,
        contrasena: password
    };

    try {
        // Hacer fetch al backend Flask
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(empresaData)
        });

        const result = await response.json();

        if (response.ok && result.success) {
            localStorage.setItem('authToken', result.token);
            window.location.href = '/dashboard';
        } else {
            alert(result.message || 'Error en el registro.');
        }
    } catch (error) {
        console.error('Error al enviar los datos:', error);
    }
});
