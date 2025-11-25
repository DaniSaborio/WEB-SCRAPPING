from bs4 import BeautifulSoup
import re
import logging
import os
import psycopg2
import time
from dotenv import load_dotenv
import csv
from datetime import datetime

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
load_dotenv()

STEAM_DISCOUNTS_URL = "https://store.steampowered.com/search/?specials=1"

# Directorio de exportación (../server_data/exports desde este archivo)
EXPORT_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..",
    "server_data",
    "exports",
)


def extract_steam_game_data_with_bs4(html_content):
    """
    Extrae datos de juegos de Steam de un contenido HTML usando Beautiful Soup.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    extracted_data = []
    games = soup.select("a.search_result_row")

    for game in games:
        game_name_elem = game.select_one(".title")
        game_name = game_name_elem.get_text(strip=True) if game_name_elem else "N/A"

        # Precio original
        price_div = game.select_one(".discount_original_price")
        original_price = None
        if price_div:
            price_text = price_div.get_text(strip=True)
            if "Gratis" in price_text or "Free" in price_text:
                original_price = 0.0
            else:
                prices = re.findall(r"[\d\.,]+", price_text)
                try:
                    if len(prices) >= 1:
                        original_price = float(
                            prices[0].replace(".", "").replace(",", ".")
                        )
                except Exception as e:
                    logging.warning(
                        f"No se pudo convertir el precio para {game_name}: {price_text} ({e})"
                    )
                    original_price = None

        # Descuento y porcentaje
        percentage = ""
        discount = None

        percentage_elem = game.select_one(".discount_pct")
        if percentage_elem:
            percentage = percentage_elem.get_text(strip=True)

        discount_element = game.select_one(".discount_final_price")
        if discount_element:
            discount_text = discount_element.get_text(strip=True)
            try:
                prices_discount = re.findall(r"[\d\.,]+", discount_text)
                if len(prices_discount) >= 1:
                    discount = float(
                        prices_discount[0].replace(".", "").replace(",", ".")
                    )
            except Exception as e:
                logging.warning(
                    f"No se pudo convertir el descuento para {game_name}: {discount_text} ({e})"
                )

        packages_elem = game.select_one(".includes_games_results")
        packages = packages_elem.get_text(strip=True) if packages_elem else "N/A"

        extracted_data.append(
            {
                "game_name": game_name,
                "original_price": original_price,
                "discount": discount,
                "packages": packages,
                "percentage": percentage,
            }
        )

    return extracted_data


def get_discounts_html_with_selenium():
    STEAM_URL = "https://store.steampowered.com/login/"
    STEAM_USERNAME = os.getenv("STEAM_USER")
    STEAM_PASSWORD = os.getenv("STEAM_PASSWORD")

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.binary_location = "/usr/bin/chromium"

    # Usar el chromedriver instalado por el sistema en la imagen
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    html_content = ""
    try:
        # Login
        driver.get(STEAM_URL)
        time.sleep(2)

        username_field = driver.find_element("css selector", 'input[type="text"]')
        password_field = driver.find_element("css selector", 'input[type="password"]')
        username_field.send_keys(STEAM_USERNAME)
        password_field.send_keys(STEAM_PASSWORD)

        sign_in_button = driver.find_element(
            "xpath", '//button[@type="submit" and contains(., "Sign in")]'
        )
        sign_in_button.click()

        time.sleep(15)

        # Ir a la página de descuentos
        driver.get("https://store.steampowered.com/search/?specials=1")
        time.sleep(5)
        html_content = driver.page_source
    except Exception as e:
        logging.error(f"Error navegando con Selenium: {e}")
    finally:
        driver.quit()

    return html_content



def save_data_to_csv(data, directory, filename_prefix="steam_discounts"):
    """
    Guarda la lista de diccionarios en un archivo CSV.
    Crea el directorio si no existe.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        logging.info(f"Directorio de exportación creado: {directory}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(directory, f"{filename_prefix}_{timestamp}.csv")

    if not data:
        logging.warning(
            f"No hay datos para guardar en {file_path}. No se creará el archivo CSV."
        )
        return None

    fieldnames = list(data[0].keys())

    try:
        with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        logging.info(f"Datos exportados exitosamente a: {file_path}")
        return file_path
    except IOError as e:
        logging.error(f"Error al escribir el archivo CSV {file_path}: {e}")
        return None


if __name__ == "__main__":
    # Conexión a PostgreSQL
    conn = psycopg2.connect(
        host=os.getenv("PG_HOST"),
        dbname=os.getenv("PG_DB"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
    )
    cur = conn.cursor()

    # Crear tabla si no existe
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS scrapped_steam (
            id SERIAL PRIMARY KEY NOT NULL,
            game_name VARCHAR(255) NOT NULL,
            original_price NUMERIC(10, 2),
            discount NUMERIC(10, 2),
            packages VARCHAR(20),
            percentage VARCHAR(20) NOT NULL
        )
        """
    )
    conn.commit()

    html_content = get_discounts_html_with_selenium()
    if html_content:
        data = extract_steam_game_data_with_bs4(html_content)

        # Limpiar tabla e insertar nuevos datos
        cur.execute("TRUNCATE TABLE scrapped_steam;")
        for game in data:
            cur.execute(
                """
                INSERT INTO scrapped_steam (game_name, original_price, discount, packages, percentage)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    game["game_name"],
                    game["original_price"],
                    game["discount"],
                    game["packages"],
                    game["percentage"],
                ),
            )
        conn.commit()
        print("Datos guardados en la base de datos.")

        csv_file_path = save_data_to_csv(data, EXPORT_DIR)
        if csv_file_path:
            print(f"Datos también exportados a CSV: {csv_file_path}")
        else:
            print("Falló la exportación a CSV.")

    cur.close()
    conn.close()
