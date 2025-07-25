// Función para obtener y mostrar los resultados de Steam
async function fetchSteamResults() {
    try {
        const response = await fetch('http://localhost:5000/api/results');
        const data = await response.json();

        const tbody = document.getElementById('scraping-data-body');
        if (tbody) {
            tbody.innerHTML = ""; // Limpia la tabla antes de cargar
            data.forEach(item => {
                tbody.innerHTML += `
                    <tr>
                        <td>${item.game_name}</td>
                        <td>${item.original_price}</td>
                        <td>${item.discount}</td>
                        <td>${item.packages}</td>
                        <td>${item.percentage}</td>
                    </tr>
                `;
            });
        }
    } catch (error) {
        console.error('Error al obtener los resultados:', error);
    }
}

// Llama a la función cuando cargue la página
window.onload = fetchSteamResults;