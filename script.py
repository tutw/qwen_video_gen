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
        # Acceder a la URL de inicio
        home_url = "https://chat.qwen.ai/auth?action=home"
        logging.info(f"Accediendo a la URL principal: {home_url}")
        driver.get(home_url)

        # Obtener credenciales desde los secretos de GitHub
        email = os.environ.get("LOGIN_EMAIL")
        password = os.environ.get("LOGIN_PASSWORD")
        if not email or not password:
            raise ValueError("Las credenciales no están configuradas en las variables de entorno.")

        # Completar el formulario de inicio de sesión
        logging.debug("Completando el formulario de inicio de sesión...")
        email_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[1]/div/div/form/div[2]/div[1]/input'))
        )
        email_box.send_keys(email)

        password_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[1]/div/div/form/div[2]/div[2]/span/input'))
        )
        password_box.send_keys(password)

        # Localizar y hacer clic en el botón de inicio de sesión
        logging.debug("Buscando el botón de inicio de sesión...")
        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[3]/div/div/div/form/div[3]/div/button'))
        )
        login_button.click()

        # Esperar a que se complete el inicio de sesión
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "chat-input"))
        )
        logging.info("Inicio de sesión exitoso.")
    except Exception as e:
        logging.error("Error durante la ejecución:", exc_info=True)
        # Guardar el HTML para diagnóstico
        with open("page_source.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)
        logging.info("Se guardó el HTML de la página para depuración.")
    finally:
        # Cerrar el navegador
        logging.debug("Cerrando el navegador...")
        driver.quit()
        logging.info("Navegador cerrado.")

except Exception as e:
    logging.critical("Fallo crítico al iniciar el script:", exc_info=True)
