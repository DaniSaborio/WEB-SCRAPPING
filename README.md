# Plataforma de Scraping, Visualización y Análisis LLM de Juegos

Este proyecto es una plataforma web integral diseñada para realizar scraping de datos de juegos (simulando una tienda como Steam), persistir estos datos en una base de datos PostgreSQL, visualizarlos a través de un dashboard moderno, y utilizar un modelo de lenguaje grande (LLM) para generar análisis sobre el panorama del mercado de juegos. Incluye un scheduler para automatizar la ejecución del scraper y una gestión robusta de logs y errores.

## 🌟 Características Principales

* **Scraping Automatizado:** Extracción de datos de juegos (nombre, precios, descuentos, etc.) de una fuente web (simulada por Steam).
* **Persistencia de Datos:** Almacenamiento y gestión de los datos extraídos en una base de datos **PostgreSQL**.
* **API RESTful:** Exposición de los datos recopilados y funcionalidades a través de endpoints API en formato JSON.
* **Dashboard Moderno:** Interfaz de usuario intuitiva para visualizar los resultados del scraping, eventos y análisis.
* **Gestión de Archivos:** Endpoint para listar y descargar archivos CSV exportados por el scraper.
* **Scheduler Integrado:** Automatización de la ejecución del scraper cada 30 minutos utilizando `APScheduler`, ejecutándose en segundo plano con el servidor Flask.
* **Análisis LLM:** Utilización de un Modelo de Lenguaje Grande (LLM) para obtener una opinión y panorama general sobre los datos de juegos extraídos, accesible a través de un endpoint API.
* **Registro de Eventos:** Sistema de logging estructurado para monitorear ejecuciones del scraper (manuales y programadas), errores y otros eventos importantes.
* **Resiliencia:** Manejo adecuado de excepciones en todo el sistema para evitar fallos en tiempo de ejecución y proporcionar mensajes de error claros.

## 🛠️ Tecnologías Utilizadas

* **Backend (Python 3.x):**
    * **Flask:** Microframework web para construir la API RESTful.
    * **Psycopg2:** Adaptador de PostgreSQL para Python.
    * **APScheduler:** Biblioteca para la programación de tareas en segundo plano.
    * **OpenAI:** Para la integración y consumo del Modelo de Lenguaje Grande (LLM).
    * **Selenium:** Para el scraping de contenido dinámico de páginas web.
    * **BeautifulSoup4:** Para el parsing de HTML y extracción de datos.
    * **`python-dotenv`:** Para la gestión segura de variables de entorno.
    * **`subprocess`:** Para ejecutar el script del scraper como un proceso independiente.
* **Base de Datos:**
    * **PostgreSQL:** Sistema de gestión de bases de datos relacionales.
* **Frontend:**
    * **HTML5, CSS3, JavaScript (Vanilla JS):** Base para la interfaz de usuario.
    * **(Opcional):** Si se utilizan librerías/frameworks CSS/JS adicionales (ej. Bootstrap, Chart.js, FullCalendar.js), listarlas aquí.

## 📁 Estructura del Proyecto

WEB-SCRAPPING/

├── .env                               
├── main.py                     
├── requirements.txt           
├── README.md                  
├── api/
│   ├── json_api_server.py      
│   └── scrapper/
│       └── scrapper.py        
├── frontend/
│   ├── index.html             
│   ├── css/                  
│   │   └── style.css
│   └
│   ├── main.js             
│   ├── calendar.js         
│   ├── result.js          
│   └── files.js            
├── llm/
│   ├── llm_selector.py         
│               
├── server_data/
│   └── exports/                
└── logs/                       

## 🚀 Configuración e Instalación

Sigue estos pasos para poner en marcha el proyecto en tu entorno local.

### 1. Clonar el Repositorio


git clone https://github.com/DaniSaborio/WEB-SCRAPPING.git
cd WEB-SCRAPPING


# Instalar dependencias

pip install -r requirements.txt

# Configuración de PostgreSQL
PG_DB=your_database_name
PG_USER=your_username
PG_PASSWORD=your_password
PG_HOST=localhost
PG_PORT=5432


🌐 Endpoints de la API
La aplicación Flask expone los siguientes endpoints:

/ (GET): Sirve la página principal del dashboard (index.html) del frontend.

/api/results (GET): Recupera y devuelve todos los resultados de juegos scrapeados desde la tabla scrapped_steam en formato JSON.

/api/events (GET): Recupera y devuelve los logs de eventos del sistema desde la tabla event_logs en formato JSON, útiles para un calendario o registro de actividad.

/api/files (GET): Lista los archivos CSV exportados disponibles en el directorio server_data/exports/. Devuelve un JSON con metadatos de los archivos (nombre, tamaño, última modificación, URL de descarga).

/exports/<path:filename> (GET): Permite la descarga directa de un archivo específico desde el directorio server_data/exports/.

Ejemplo: http://localhost:5000/exports/steam_discounts_20250725_103000.csv

/api/run_scraper (POST): Dispara manualmente la ejecución del script de scraping (scrapper/scrapper.py). El estado de la ejecución se reporta en la respuesta JSON y se loguea en event_logs.

/api/llm_analysis (GET): Obtiene un análisis y opinión general del mercado de juegos, generada por el LLM, basándose en los datos más recientes scrapeados de la base de datos. Devuelve la opinión del LLM en formato JSON.

⏰ Automatización (Scheduler)
El servidor Flask integra un scheduler (APScheduler) que ejecuta el script de scraping (scrapper/scrapper.py) automáticamente cada 30 minutos en un hilo de fondo. Esto asegura que los datos estén siempre actualizados sin intervención manual. Los logs de estas ejecuciones programadas se registran en la tabla event_logs con el tipo "Scraper Run (Scheduled)".