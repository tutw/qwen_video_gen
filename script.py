import logging  # Importa el módulo logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

        # Confirmar si la página se ha cargado correctamente
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        logging.info("Página cargada correctamente.")

        # Localizar y hacer clic en el botón inicial
        logging.debug("Buscando el botón inicial para hacer clic...")
        initial_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[3]/div/div/div/form/div[3]/div/button'))
        )
        initial_button.click()
        logging.info("Se hizo clic en el botón inicial correctamente.")

        # Localizar y rellenar el campo de email y contraseña
        logging.debug("Rellenando credenciales de inicio de sesión...")
        email_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[1]/div/div/form/div[2]/div[1]/input'))
        )
        password_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[1]/div/div/form/div[2]/div[2]/span/input'))
        )
        submit_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[3]/div[1]/div/div/form/div[4]/button'))
        )

        # Obtener credenciales desde los secretos de GitHub Actions
        email = os.environ.get("LOGIN_EMAIL")
        password = os.environ.get("LOGIN_PASSWORD")
        if not email or not password:
            raise ValueError("Las credenciales no están configuradas en las variables de entorno.")

        email_field.send_keys(email)
        password_field.send_keys(password)
        submit_button.click()
        logging.info("Inicio de sesión realizado correctamente.")

        # Hacer clic en el botón para iniciar el proceso
        logging.debug("Buscando el botón para iniciar el proceso de generación...")
        generate_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div/div[4]/div[2]/div[1]/div/div/div/div[1]/div/div[2]/div/div[2]/div[2]/div/div/button[3]'))
        )
        generate_button.click()
        logging.info("Se hizo clic en el botón de generación correctamente.")

        # Rellenar el campo de entrada con el prompt
        logging.debug("Rellenando el campo de entrada con el prompt...")
        chat_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="chat-input"]'))
        )
        chat_input.send_keys("gato jugando con pelota de tennis")
        logging.info("Prompt ingresado correctamente.")

        # Hacer clic en el botón de envío
        logging.debug("Haciendo clic en el botón para enviar el mensaje...")
        send_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="send-message-button"]'))
        )
        send_button.click()
        logging.info("Mensaje enviado correctamente.")

        # Esperar a que se genere la URL del video
        logging.debug("Esperando a que se genere la URL del video...")
        video_url_element = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "http")]'))  # Busca cualquier enlace con "http"
        )
        video_url = video_url_element.get_attribute("href")
        logging.info(f"Video generado: {video_url}")
        print(f"Video generado: {video_url}")

    finally:
        # Cerrar el navegador
        logging.debug("Cerrando el navegador...")
        driver.quit()
        logging.info("Navegador cerrado.")

except Exception as e:
    logging.critical("Error crítico durante la ejecución:", exc_info=True)
