from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from dotenv import load_dotenv

load_dotenv()
# Configuración
STEAM_URL = "https://store.steampowered.com/login/"
STEAM_USERNAME = os.getenv('STEAM_USER')
STEAM_PASSWORD = os.getenv('STEAM_PASSWORD')

# --- VERIFICACIÓN CRÍTICA DE LAS VARIABLES DE ENTORNO ---


# Configuración del navegador
chrome_options = Options()

# Inicializar WebDriver

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    driver.get(STEAM_URL)

    # Espera inicial para que la página cargue, esencial cuando no usamos WebDriverWait
    time.sleep(2)

    # --- Localizar campos de texto y contraseña ---
    username_field = driver.find_element('css selector', 'input[type="text"]')
    password_field = driver.find_element("css selector", 'input[type="password"]')

    username_field.send_keys(STEAM_USERNAME)
    password_field.send_keys(STEAM_PASSWORD)

    # --- Localizar el botón de Sign in ---
    sign_in_button = driver.find_element("xpath", '//button[@type="submit" and text()="Sign in"]')
    sign_in_button.click()

    # Espera después de intentar iniciar sesión para observar el resultado
    time.sleep(25)
    #ENTRAR A DESCUENTOS
    more_button = driver.find_element('xpath', '//div[contains(@class, "responsive_content_dive") and contains(text(), "Más")]')
    more_button.click()
    #FILTRAR POR JUEGOS RPG Y ACCCION 

    time.sleep(10)
except Exception as e:
    print(f"Ocurrió un error durante el intento de inicio de sesión: {e}")

finally:
    # Asegura que el navegador se cierre
    if driver:
        driver.quit()

        #//*[@id="home_specialoffers"]/span/a/div/div
        #//*[@id="responsive_page_template_content"]/div[3]/div[1]/div/div/div/div[2]/div/form/div[4]/button