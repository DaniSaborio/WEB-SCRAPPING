// frontend/main.js
import { fetchAndDisplayFiles } from './files.js'; // <<< --- Importa la nueva función
import { init as initCalendarModule } from './calendar.js';
import { fetchSteamResults } from './result.js';
// Si tienes un módulo para archivos, impórtalo también:
// import { init as initFilesModule } from './files.js'; 

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM Content Loaded - Initializing modules...');
    
    // Inicializar módulos existentes
    initCalendarModule('calendar');
    fetchSteamResults();
    // if (typeof initFilesModule === 'function') { // Ejemplo si tienes initFilesModule
    //     initFilesModule();
    // }

    // <<< --- AQUI SE AGREGA LA LLAMADA A fetchAndDisplayFiles ---
    fetchAndDisplayFiles('files-list-container'); 
    // -----------------------------------------------------------

    // --- Lógica para el botón del Scraper ---
    const runScraperBtn = document.getElementById('run-scraper-btn');
    const scraperStatusDiv = document.getElementById('scraper-status');

    if (runScraperBtn && scraperStatusDiv) {
        runScraperBtn.addEventListener('click', async () => {
            runScraperBtn.disabled = true; // Deshabilitar botón para evitar múltiples clics
            scraperStatusDiv.classList.remove('d-none', 'alert-success', 'alert-danger');
            scraperStatusDiv.classList.add('alert-info');
            scraperStatusDiv.textContent = 'Ejecutando scraper... por favor espere.';

            try {
                // Realizar la petición al nuevo endpoint de Flask
                const response = await fetch('http://localhost:5000/api/run_scraper', {
                    method: 'POST', // Usamos POST para acciones
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                const data = await response.json();

                if (response.ok) {
                    scraperStatusDiv.classList.remove('alert-info');
                    scraperStatusDiv.classList.add('alert-success');
                    scraperStatusDiv.textContent = `Scraper ejecutado con éxito: ${data.message}`;
                    // Opcional: Volver a cargar los resultados de Steam después de ejecutar el scraper
                    await fetchSteamResults(); 
                    // También recargar la lista de archivos después de una ejecución exitosa del scraper
                    await fetchAndDisplayFiles('files-list-container'); // <<< --- AGREGADO AQUÍ TAMBIÉN
                } else {
                    scraperStatusDiv.classList.remove('alert-info');
                    scraperStatusDiv.classList.add('alert-danger');
                    scraperStatusDiv.textContent = `Error al ejecutar scraper: ${data.error || 'Error desconocido'}`;
                }
            } catch (error) {
                console.error('Error de red o del servidor al ejecutar scraper:', error);
                scraperStatusDiv.classList.remove('alert-info');
                scraperStatusDiv.classList.add('alert-danger');
                scraperStatusDiv.textContent = `Error de conexión: ${error.message}`;
            } finally {
                runScraperBtn.disabled = false; // Habilitar el botón de nuevo
                // Opcional: Ocultar el mensaje de estado después de un tiempo
                setTimeout(() => {
                    scraperStatusDiv.classList.add('d-none');
                }, 5000); 
            }
        });
    } else {
        console.warn("Botón 'run-scraper-btn' o 'scraper-status' no encontrado en el DOM.");
    }
});