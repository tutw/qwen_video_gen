import logging  # Importa el módulo logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

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

        # Confirmar si se ha accedido correctamente
        if "home" in driver.current_url:
            logging.info("Acceso exitoso a la URL.")
            print("Acceso exitoso a la URL.")
        else:
            logging.error("No se pudo acceder a la URL correctamente.")
            print("No se pudo acceder a la URL correctamente.")
    finally:
        # Cerrar el navegador
        logging.debug("Cerrando el navegador...")
        driver.quit()
        logging.info("Navegador cerrado.")

except Exception as e:
    logging.critical("Fallo crítico al iniciar el script:", exc_info=True)
