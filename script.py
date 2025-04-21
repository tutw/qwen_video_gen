import logging  # Importa el módulo logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os

# Configuración del sistema de logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),  # Registrar logs en un archivo
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
        # Acceder a la URL
        url = "https://chat.qwen.ai/auth?action=home"
        logging.info(f"Accediendo a la URL: {url}")
        driver.get(url)

        # Confirmar si la página se ha cargado correctamente
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        logging.info("Página cargada correctamente.")

        # Localizar y hacer clic en el botón especificado
        logging.debug("Buscando el botón para hacer clic...")
        initial_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[3]/div/div/div/form/div[3]/div/button'))
        )
        initial_button.click()
        logging.info("Se hizo clic en el botón correctamente.")

        # Obtener credenciales desde los secretos de GitHub Actions
        email = os.environ.get("LOGIN_EMAIL")
        password = os.environ.get("LOGIN_PASSWORD")
        if not email or not password:
            raise ValueError("Las credenciales no están configuradas en las variables de entorno.")

        # Localizar y rellenar el campo de email
        logging.debug("Rellenando el campo de email...")
        email_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[1]/div/div/form/div[2]/div[1]/input'))
        )
        email_field.send_keys(email)
        logging.info("Campo de email rellenado correctamente.")

        # Localizar y rellenar el campo de contraseña
        logging.debug("Rellenando el campo de contraseña...")
        password_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[1]/div/div/form/div[2]/div[2]/span/input'))
        )
        password_field.send_keys(password)
        logging.info("Campo de contraseña rellenado correctamente.")

        # Localizar y hacer clic en el botón de envío
        logging.debug("Haciendo clic en el botón de envío...")
        submit_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[1]/div/div/form/div[4]/button'))
        )
        submit_button.click()
        logging.info("Se hizo clic en el botón de envío correctamente.")

    finally:
        # Cerrar el navegador
        logging.debug("Cerrando el navegador...")
        driver.quit()
        logging.info("Navegador cerrado.")

except Exception as e:
    logging.critical("Error crítico durante la ejecución:", exc_info=True)
