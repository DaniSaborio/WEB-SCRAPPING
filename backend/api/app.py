from flask import Flask, jsonify, request, send_from_directory
from flask.cli import load_dotenv
from flask_cors import CORS
import psycopg2
import os
import requests
import subprocess
from datetime import datetime

EXPORT_DIR_API = os.environ.get(
    "EXPORT_PATH",
    "/data/exports",
)

FRONTEND_FOLDER = os.environ.get(
    "FRONTEND_FOLDER",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public"),
)

app = Flask(__name__,
            static_folder=FRONTEND_FOLDER,
            static_url_path='/'
           )
CORS(app)

load_dotenv()
DB_NAME = os.getenv('PG_DB')
DB_USER = os.getenv('PG_USER')
DB_PASSWORD = os.getenv('PG_PASSWORD')
DB_HOST = os.getenv('PG_HOST')
DB_PORT = os.getenv('PG_PORT')

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def initialize_database():
    """
    Crea la tabla event_logs si no existe.
    """
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            print("No se pudo conectar a la base de datos para la inicialización.")
            return

        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS event_logs (
                id SERIAL PRIMARY KEY,
                event_type VARCHAR(100) NOT NULL,
                event_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                description TEXT,
                related_id INT,
                related_table VARCHAR(50)
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS scrapped_steam (
                id SERIAL PRIMARY KEY,
                game_name VARCHAR(255) NOT NULL,
                original_price VARCHAR(50),
                discount VARCHAR(50),
                packages VARCHAR(255),
                percentage VARCHAR(10)
            );
        """)
        conn.commit()
        print("Tablas 'event_logs' y 'scrapped_steam' verificadas/creadas exitosamente.")
    except psycopg2.Error as e:
        print(f"Error al inicializar la base de datos (crear tablas): {e}")
    finally:
        if conn:
            conn.close()

# --- Endpoints de la API ---

@app.route('/api/files', methods=['GET'])
def list_exported_files():
    """
    Endpoint para listar los archivos exportados en el directorio EXPORT_DIR_API.
    """
    if not os.path.exists(EXPORT_DIR_API):
        return jsonify({"error": "Directorio de exportación no encontrado en el servidor."}), 404

    files_list = []
    try:
        for filename in os.listdir(EXPORT_DIR_API):
            file_path = os.path.join(EXPORT_DIR_API, filename)
            if os.path.isfile(file_path): 
                file_size = os.path.getsize(file_path) 
                last_modified_timestamp = os.path.getmtime(file_path) 
                last_modified_date = datetime.fromtimestamp(last_modified_timestamp).strftime('%Y-%m-%d %H:%M:%S')

                files_list.append({
                    "name": filename,
                    "size": f"{file_size / 1024:.2f} KB",
                    "last_modified": last_modified_date,
                    "url": f"/exports/{filename}" 
                })

        files_list.sort(key=lambda x: datetime.strptime(x['last_modified'], '%Y-%m-%d %H:%M:%S'), reverse=True)
        return jsonify(files_list), 200

    except Exception as e:
        print(f"Error al listar archivos exportados: {e}")
        return jsonify({"error": "Error interno del servidor al listar archivos."}), 500

# --- ENDPOINT PARA SERVIR ARCHIVOS EXPORTADOS ---

@app.route('/exports/<path:filename>')
def download_exported_file(filename):
    """
    Endpoint para servir (descargar) un archivo específico desde el directorio de exportación.
    """
    try:
        return send_from_directory(EXPORT_DIR_API, filename, as_attachment=True) # as_attachment=True fuerza la descarga
    except FileNotFoundError:
        return jsonify({"error": "Archivo no encontrado."}), 404
    except Exception as e:
        print(f"Error al servir archivo: {e}")
        return jsonify({"error": "Error interno del servidor al servir el archivo."}), 500


@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/api/results', methods=['GET'])
def get_results():
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

        cur = conn.cursor()
        cur.execute("""
            SELECT id, game_name, original_price, discount, packages, percentage
            FROM scrapped_steam
            ORDER BY id DESC;
        """)
        results = cur.fetchall()
        column_names = [desc[0] for desc in cur.description]
        results_list = [dict(zip(column_names, row)) for row in results]
        return jsonify(results_list)

    except psycopg2.Error as e:
        print(f"Error al obtener resultados: {e}")
        return jsonify({"error": "Error interno del servidor al obtener resultados"}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/events', methods=['GET'])
def get_events():
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

        cur = conn.cursor()
        cur.execute("""
            SELECT
                id,
                event_type AS title,
                event_timestamp AS start,
                description
            FROM event_logs
            ORDER BY event_timestamp DESC;
        """)
        events = cur.fetchall()

        column_names = [desc[0] for desc in cur.description]
        events_list = []
        for row in events:
            event_dict = dict(zip(column_names, row))
            events_list.append(event_dict)

        return jsonify(events_list)

    except psycopg2.Error as e:
        print(f"Error al obtener eventos para el calendario: {e}")
        return jsonify({"error": "Error interno del servidor al obtener eventos"}), 500
    finally:
        if conn:
            conn.close()

# --- ENDPOINT PARA EJECUTAR EL SCRAPER ---

@app.route('/api/run_scraper', methods=['POST'])
def run_scraper():
    try:
        resp = requests.post("http://scrapper:8000/run", timeout=5)
        return jsonify({
            "message": "Solicitud enviada al scrapper",
            "scrapper_status_code": resp.status_code,
            "scrapper_response": resp.json() if resp.headers.get("content-type", "").startswith("application/json") else resp.text,
        }), 202
    except Exception as e:
        print(f"Error al llamar al scrapper: {e}")
        return jsonify({"error": "No se pudo contactar al scrapper", "details": str(e)}), 500


if __name__ == '__main__':
    initialize_database()
    app.run(debug=True, host='0.0.0.0', port=5000)
    print("Servidor Flask iniciado en http://localhost:5000")