// frontend/files.js

const API_FILES_URL = 'http://localhost:5000/api/files';

/**
 * Obtiene la lista de archivos exportados desde la API y los muestra en el contenedor.
 * @param {string} elementId El ID del contenedor HTML donde se mostrará la lista de archivos.
 */
export async function fetchAndDisplayFiles(elementId) {
    console.log('files.js: Intentando cargar lista de archivos desde la API...');
    const filesContainer = document.getElementById(elementId);
    if (!filesContainer) {
        console.error(`files.js: Elemento con ID '${elementId}' no encontrado para mostrar archivos.`);
        return;
    }

    filesContainer.innerHTML = '<p>Cargando archivos...</p>';

    try {
        const response = await fetch(API_FILES_URL);
        if (!response.ok) {
            throw new Error(`Error HTTP! Estado: ${response.status}`);
        }
        const files = await response.json();
        console.log('files.js: Archivos recibidos:', files);

        if (files.length === 0) {
            filesContainer.innerHTML = '<p>No hay archivos exportados disponibles.</p>';
            return;
        }

        const ul = document.createElement('ul');
        ul.className = 'list-group'; // Clases de Bootstrap para una lista bonita

        files.forEach(file => {
            const li = document.createElement('li');
            li.className = 'list-group-item d-flex justify-content-between align-items-center';
            li.innerHTML = `
                <div>
                    <strong>${file.name}</strong><br>
                    <small>Tamaño: ${file.size} | Última Modificación: ${file.last_modified}</small>
                </div>
                <a href="http://localhost:5000${file.url}" class="btn btn-sm btn-info" download="${file.name}">Descargar</a>
            `;
            ul.appendChild(li);
        });
        filesContainer.innerHTML = ''; // Limpiar el mensaje de carga
        filesContainer.appendChild(ul);

    } catch (error) {
        console.error('files.js: Error al obtener la lista de archivos:', error);
        filesContainer.innerHTML = `<p class="text-danger">Error al cargar los archivos: ${error.message}</p>`;
    }
}