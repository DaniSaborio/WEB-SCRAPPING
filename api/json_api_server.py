# api/json_api_server.py

from flask import Flask, jsonify, request
from flask.cli import load_dotenv
from flask_cors import CORS # Importa CORS
import psycopg2
import os

app = Flask(__name__)
# Habilitar CORS para todas las rutas.
# En desarrollo, es común permitir todos los orígenes (*).
# En producción, deberías especificar los orígenes permitidos (ej. origins=["http://localhost:8000", "https://tudominio.com"])
CORS(app)


# --- Configuración de la Base de Datos ---
load_dotenv() # Carga las variables de entorno desde el archivo .env
DB_NAME = os.getenv('PG_DB')
DB_USER = os.getenv('PG_USER')
DB_PASSWORD = os.getenv('PG_PASSWORD')
DB_HOST = os.getenv('PG_HOST')
DB_PORT = os.getenv('PG_PORT')

def get_db_connection():
    """Establece y devuelve una conexión a la base de datos PostgreSQL."""
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

# --- Endpoints de la API ---

@app.route('/api/results', methods=['GET'])
def get_results():
    """
    Endpoint para obtener los datos scrapeados de Steam.
    """
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

# Puedes añadir más endpoints aquí para /api/files y /api/events
# siguiendo la misma estructura.

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    print("Servidor Flask iniciado en http://localhost:5000")