import logging  # Importa el módulo logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

# Configuración del sistema de logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),  # Registro de logs en un archivo
        logging.StreamHandler()  # Mostrar logs en la consola
    ]
)

logging.info("Iniciando el script...")

try:
    # Configurar opciones de Chrome
    logging.debug("Configurando opciones de Chrome...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ejecución sin interfaz gráfica
    chrome_options.add_argument("--disable-gpu")  # Deshabilitar GPU
    chrome_options.add_argument("--no-sandbox")  # Necesario en entornos de CI/CD
    chrome_options.add_argument("--disable-dev-shm-usage")  # Evitar problemas de memoria compartida

    # Configurar el servicio de ChromeDriver utilizando webdriver-manager
    logging.debug("Inicializando el servicio de ChromeDriver con webdriver-manager...")
    service = Service(ChromeDriverManager().install())

    # Inicializar el navegador Chrome
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Acceder a la URL de inicio de sesión
        login_url = "https://chat.qwen.ai/auth?action=signin"
        logging.info(f"Accediendo a la URL de inicio de sesión: {login_url}")
        driver.get(login_url)

        # Obtener credenciales desde los secretos de GitHub
        email = os.environ.get("LOGIN_EMAIL")
        password = os.environ.get("LOGIN_PASSWORD")
        if not email or not password:
            raise ValueError("Las credenciales no están configuradas en las variables de entorno.")

        # Completar el formulario de inicio de sesión
        logging.debug("Completando el formulario de inicio de sesión...")

        # Localizar el campo de correo electrónico
        email_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "login-email"))
        )
        email_box.send_keys(email)

        # Localizar el campo de contraseña
        password_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="password" and @placeholder="Contraseña"]'))
        )
        password_box.send_keys(password)

        # Localizar y hacer clic en el botón de inicio de sesión
        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#chat-container > div.sticky.top-0.z-40.navbar-bg-mobile.-mb-8.flex.w-full.items-center.px-1\\.5.py-1\\.5 > div > div > div.flex.h-\\[2\\.5rem\\].flex-none.items-center.self-start.text-gray-600.dark\\:text-gray-400 > div > button'))
        )
        login_button.click()

        # Esperar a que se complete el inicio de sesión
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "chat-input"))
        )
        logging.info("Inicio de sesión exitoso.")
    except Exception as e:
        logging.error("Error durante la ejecución:", exc_info=True)
    finally:
        # Cerrar el navegador
        logging.debug("Cerrando el navegador...")
        driver.quit()
        logging.info("Navegador cerrado.")

except Exception as e:
    logging.critical("Fallo crítico al iniciar el script:", exc_info=True)
