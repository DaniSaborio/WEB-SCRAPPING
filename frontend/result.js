// frontend/results.js (Código Correcto para Módulo ES6)

// Función para obtener y mostrar los resultados de Steam
export async function fetchSteamResults() { // <<< --- AÑADE 'export' aquí
    console.log("results.js: fetchSteamResults se está ejecutando."); // Añade un log para verificar
    try {
        const response = await fetch('http://localhost:5000/api/results');
        if (!response.ok) {
            throw new Error(`Error HTTP! Estado: ${response.status}`);
        }
        const data = await response.json();
        console.log("results.js: Datos de Steam recibidos:", data);

        const tbody = document.getElementById('scraping-data-body');
        if (tbody) {
            tbody.innerHTML = ""; // Limpia la tabla antes de cargar
            data.forEach(item => {
                tbody.innerHTML += `
                    <tr>
                        <td>${item.game_name || 'N/A'}</td>
                        <td>${item.original_price ? `$${parseFloat(item.original_price).toFixed(2)}` : 'N/A'}</td>
                        <td>${item.discount || 'N/A'}</td>
                        <td>${item.packages || 'N/A'}</td>
                        <td>${item.percentage ? `${item.percentage}%` : 'N/A'}</td>
                    </tr>
                `;
            });
        } else {
            console.error("results.js: Elemento con ID 'scraping-data-body' no encontrado.");
        }
    } catch (error) {
        console.error('results.js: Error al obtener los resultados:', error);
        const tableBody = document.getElementById('scraping-data-body');
        if (tableBody) {
            tableBody.innerHTML = `<tr><td colspan="5" class="text-center text-danger">Error al cargar los datos: ${error.message}</td></tr>`;
        }
    }
}

// <<< --- ELIMINA COMPLETAMENTE ESTA LÍNEA:
// window.onload = fetchSteamResults;