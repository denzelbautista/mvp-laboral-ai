// Validar el token JWT
function validateAuthToken() {
    const token = localStorage.getItem("authToken");
  
    if (!token) {
      // Redirigir al login si no hay token
      window.location.href = "/login";
    } else {
      try {
        // Decodificar el payload del JWT
        const payload = JSON.parse(atob(token.split(".")[1]));
        const now = Math.floor(Date.now() / 1000);
  
        if (payload.exp < now) {
          // Si el token está expirado
          alert("Tu sesión ha expirado. Por favor, inicia sesión nuevamente.");
          localStorage.removeItem("authToken");
          window.location.href = "/login";
        } else {
          // Mostrar el contenido del dashboard si el token es válido
          document.querySelector(".main-wrapper").style.display = "block";
        }
      } catch (error) {
        console.error("Token inválido:", error);
        window.location.href = "/login";
      }
    }
  }
  
  // Datos de ejemplo para la tabla
  const jobs = [
    {
      title: "Desarrollador web",
      candidates: 56,
      publishDate: "01/04/2024",
      endDate: "28/04/2024",
    },
    {
      title: "Analista de datos",
      candidates: 10,
      publishDate: "21/04/2024",
      endDate: "10/05/2024",
    },
    {
      title: "Experto en redes",
      candidates: "+100",
      publishDate: "10/03/2024",
      endDate: "03/04/2024",
    },
    {
      title: "Desarrollador android",
      candidates: 8,
      publishDate: "02/01/2024",
      endDate: "10/02/2024",
    },
    {
      title: "Desarrollador IO's",
      candidates: 3,
      publishDate: "20/12/2023",
      endDate: "15/01/2024",
    },
  ];
  
  // Renderizar empleos en la tabla
  function renderJobs() {
    const tbody = document.getElementById("jobsTableBody");
    tbody.innerHTML = jobs
      .map(
        (job) => `
        <tr>
          <td>${job.title}</td>
          <td>${job.candidates}</td>
          <td>${job.publishDate}</td>
          <td>${job.endDate}</td>
          <td>
            <i class="fas fa-file-alt action-icon" title="Ver detalles"></i>
            <i class="fas fa-download action-icon" title="Descargar"></i>
            <i class="fas fa-pause action-icon" title="Pausar"></i>
            <i class="fas fa-trash action-icon" title="Eliminar"></i>
          </td>
        </tr>
      `
      )
      .join("");
  }
  
  // Validar token al cargar la página y renderizar la tabla
  document.addEventListener("DOMContentLoaded", () => {
    validateAuthToken();
    renderJobs();
  });
  