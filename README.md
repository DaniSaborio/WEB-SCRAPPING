# Plataforma de Scraping, Visualización y Análisis LLM de Juegos

Plataforma web integral para hacer scraping de datos de juegos (simulando una tienda tipo Steam), guardarlos en PostgreSQL, visualizarlos en un dashboard moderno y obtener análisis automáticos mediante un LLM. Incluye scheduler para automatizar el scraping y un sistema robusto de logs y manejo de errores.[3][4][5][6]

## Características principales

- **Scraping automatizado:** Extracción de datos de juegos (nombre, precios, descuentos, etc.) desde una fuente web que simula Steam.[7]
- **Persistencia de datos:** Almacenamiento de la información en una base de datos **PostgreSQL** para consultas posteriores.[6]
- **API RESTful:** Endpoints JSON para exponer datos scrapeados y funcionalidades del sistema (scraper, análisis LLM, archivos).[8]
- **Dashboard moderno:** Interfaz web para visualizar resultados, eventos y análisis del mercado de juegos.[4]
- **Gestión de archivos:** Endpoint para listar y descargar archivos CSV exportados por el scraper.[7]
- **Scheduler integrado:** Automatización del scraper cada 30 minutos usando `APScheduler`, ejecutándose en segundo plano junto al servidor Flask.[8]
- **Análisis LLM:** Uso de un Modelo de Lenguaje Grande para ofrecer una opinión y panorama general del mercado basado en los datos más recientes.[9]
- **Registro de eventos:** Logging estructurado de ejecuciones (manuales y programadas), errores y otros eventos relevantes.[3]
- **Resiliencia:** Manejo de excepciones en todo el sistema para evitar caídas y devolver mensajes de error claros.[8]

## Tecnologías utilizadas

- **Backend (Python 3.x):**  
  - **Flask:** API RESTful y servidor del dashboard.[8]
  - **psycopg2:** Conector PostgreSQL para Python.[6]
  - **APScheduler:** Programación de tareas en segundo plano.[3]
  - **OpenAI:** Integración con LLM para análisis de mercado.[9]
  - **Selenium:** Scraping de contenido dinámico.[7]
  - **BeautifulSoup4:** Parsing de HTML y extracción de datos.[6]
  - **python-dotenv:** Gestión de variables de entorno.[10]
  - **subprocess:** Ejecución del script de scraping como proceso independiente.[11]

- **Base de datos:**  
  - **PostgreSQL:** Motor de base de datos relacional.[6]

- **Frontend:**  
  - **HTML5, CSS3, JavaScript (Vanilla JS):** Interfaz del dashboard.[11]
  - **Opcional:** Librerías como Bootstrap, Chart.js o FullCalendar.js si se incorporan al proyecto.[2]

## Estructura del proyecto

```text
WEB-SCRAPPING/
├── backend
│   ├── api
│   │   ├── app.py
│   │   ├── Containerfile
│   │   └── requirements.txt
│   ├── scheduler
│   │   ├── Containerfile
│   │   ├── requirements.txt
│   │   └── scheduler.py
│   └── scrapper
│       ├── Containerfile
│       ├── requirements.txt
│       └── scrapper.py
├── data
│   └── exports
├── docker-compose.yml
├── frontend
│   ├── Containerfile
│   └── public
│       ├── css
│       │   └── styles.css
│       ├── index.html
│       └── js
│           ├── calendar.js
│           ├── files.js
│           ├── main.js
│           └── result.js
├── logs
│   └── scrapper.log
└── README.md
```

## Endpoints de la API

- `GET /`  
  Sirve la página principal del dashboard (`index.html`) del frontend.[8]

- `GET /api/results`  
  Devuelve en JSON todos los resultados de juegos scrapeados desde la tabla `scrapped_steam`.[8]

- `GET /api/events`  
  Devuelve los logs de eventos del sistema desde la tabla `event_logs`, útiles para calendarios o registros de actividad.[3]

- `GET /api/files`  
  Lista los archivos CSV disponibles en `server_data/exports/` con metadatos (nombre, tamaño, última modificación, URL de descarga) en formato JSON.[7]

- `GET /exports/<path:filename>`  
  Permite descargar directamente un archivo específico desde `server_data/exports/`.[7]

  Ejemplo:  

  ```text
  http://localhost:5000/exports/steam_discounts_20250725_103000.csv
  ```

- `POST /api/run_scraper`  
  Lanza manualmente el script de scraping (`scrapper/scrapper.py`); el estado se devuelve en JSON y se loguea en `event_logs`.[3]

- `GET /api/llm_analysis`  
  Genera y devuelve un análisis general del mercado de juegos usando el LLM y los datos más recientes de la base de datos.[9]

## Automatización (scheduler)

El servidor Flask integra un scheduler con `APScheduler` que ejecuta `scrapper/scrapper.py` automáticamente cada 30 minutos en un hilo de fondo. Cada ejecución programada se registra en la tabla `event_logs` con el tipo `"Scraper Run (Scheduled)"`, lo que permite auditar y visualizar la actividad del sistema desde el dashboard.[3][8]
