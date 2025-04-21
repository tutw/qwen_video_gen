import logging
import tempfile  # Para crear directorios temporales de forma única
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configuración de logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),  # Guardar en archivo
        logging.StreamHandler()  # Mostrar en consola
    ]
)

logging.info("Iniciando el script...")

try:
    # Configuración de Chrome
    logging.debug("Configurando opciones de Chrome...")
    chrome_options = Options()
    # Descomentar la siguiente línea para ejecutar en modo headless
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Crear un directorio temporal único para evitar conflictos de `user-data-dir`
    user_data_dir = tempfile.mkdtemp()
    logging.debug(f"Usando directorio temporal para user-data-dir: {user_data_dir}")
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

    # Inicializar el servicio de ChromeDriver
    logging.debug("Inicializando el servicio de ChromeDriver...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Acceso a la página
        url = "https://chat.qwen.ai/auth?action=home"
        logging.info(f"Accediendo a la URL: {url}")
        driver.get(url)

        # Esperar a que se cargue la página
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        logging.info("Página cargada correctamente.")

        # Botón inicial
        logging.debug("Buscando el botón inicial para hacer clic...")
        initial_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[3]/div/div/div/form/div[3]/div/button'))
        )
        initial_button.click()
        logging.info("Se hizo clic en el botón inicial correctamente.")

        # Rellenar el campo de entrada con el prompt
        logging.debug("Rellenando el campo de entrada con el prompt...")
        chat_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="chat-input"]'))
        )
        chat_input.send_keys("gato jugando con pelota de tennis")
        logging.info("Prompt ingresado correctamente.")

        # Esperar a que el botón de envío aparezca
        logging.debug("Esperando a que el botón de envío esté disponible...")
        send_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="send-message-button"]'))
        )
        send_button.click()
        logging.info("Mensaje enviado correctamente.")

    finally:
        # Cerrar el navegador
        logging.debug("Cerrando el navegador...")
        driver.quit()
        logging.info("Navegador cerrado.")

except Exception as e:
    logging.critical("Error crítico durante la ejecución:", exc_info=True)
