import { fetchAndDisplayFiles } from './files.js';
import { init as initCalendarModule } from './calendar.js';
import { fetchSteamResults } from './result.js';

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM Content Loaded - Initializing modules...');
    
    initCalendarModule('calendar');
    fetchSteamResults();
    fetchAndDisplayFiles('files-list-container'); 

    const runScraperBtn = document.getElementById('run-scraper-btn');
    const scraperStatusDiv = document.getElementById('scraper-status');

    if (runScraperBtn && scraperStatusDiv) {
        runScraperBtn.addEventListener('click', async () => {
            runScraperBtn.disabled = true; 
            scraperStatusDiv.classList.remove('d-none', 'alert-success', 'alert-danger');
            scraperStatusDiv.classList.add('alert-info');
            scraperStatusDiv.textContent = 'Ejecutando scraper... por favor espere.';

            try {
                const response = await fetch('http://localhost:5000/api/run_scraper', {
                    method: 'POST', 
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });

                const data = await response.json();

                if (response.ok) {
                    scraperStatusDiv.classList.remove('alert-info');
                    scraperStatusDiv.classList.add('alert-success');
                    scraperStatusDiv.textContent = `Scraper ejecutado con éxito: ${data.message}`;
                    await fetchSteamResults(); 
                    await fetchAndDisplayFiles('files-list-container'); 
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
                runScraperBtn.disabled = false; 
                setTimeout(() => {
                    scraperStatusDiv.classList.add('d-none');
                }, 5000); 
            }
        });
    } else {
        console.warn("Botón 'run-scraper-btn' o 'scraper-status' no encontrado en el DOM.");
    }
});