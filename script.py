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
import xml.etree.ElementTree as ET

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
        login_url = "https://chat.qwen.ai/login"
        logging.info(f"Accediendo a la URL de inicio de sesión: {login_url}")
        driver.get(login_url)

        # Obtener credenciales de las variables de entorno
        email = os.environ.get("LOGIN_EMAIL")
        password = os.environ.get("LOGIN_PASSWORD")
        if not email or not password:
            raise ValueError("Las credenciales no están configuradas en las variables de entorno.")

        # Completar el formulario de inicio de sesión
        logging.debug("Completando el formulario de inicio de sesión...")
        email_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "login_email"))
        )
        email_box.send_keys(email)

        password_box = driver.find_element(By.ID, "login_password")
        password_box.send_keys(password)
        password_box.send_keys(Keys.RETURN)

        # Esperar a que el inicio de sesión sea exitoso
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//textarea"))
        )
        logging.info("Inicio de sesión exitoso.")

        # Acceder a la URL principal
        url = "https://chat.qwen.ai/c/07a3d948-a17e-461a-90e6-41675255ec6c"
        logging.info(f"Accediendo a la URL principal: {url}")
        driver.get(url)
        time.sleep(5)  # Esperar que la página cargue completamente

        # Encontrar la caja de texto donde se escribe el prompt
        logging.debug("Buscando la caja de texto para el prompt...")
        prompt_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "textarea"))
        )
        prompt_text = "un gato jugando con una bola de papel"
        logging.info(f"Enviando prompt: {prompt_text}")
        prompt_box.send_keys(prompt_text)
        prompt_box.send_keys(Keys.RETURN)
        time.sleep(10)  # Esperar que se genere el video

        # Buscar el enlace al video generado con espera dinámica
        try:
            logging.debug("Buscando el enlace del video generado...")
            video_element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "cdn.qwenlm.ai/output")]'))
            )
            video_url = video_element.get_attribute('href')
            logging.info(f"URL del video generado: {video_url}")
        except Exception as e:
            logging.error("No se pudo encontrar el enlace al video generado:", exc_info=True)
            with open("page_source.html", "w", encoding="utf-8") as file:
                file.write(driver.page_source)  # Guarda el HTML completo de la página
            video_url = None

        # Crear un archivo XML si se encontró la URL
        if video_url:
            output_file = "url.xml"
            logging.debug(f"Creando el archivo XML en: {output_file}")
            root = ET.Element("VideoData")
            prompt_element = ET.SubElement(root, "Prompt")
            prompt_element.text = prompt_text
            url_element = ET.SubElement(root, "URL")
            url_element.text = video_url
            tree = ET.ElementTree(root)
            with open(output_file, "wb") as file:
                tree.write(file, encoding="utf-8", xml_declaration=True)
            logging.info(f"Archivo XML creado correctamente en {output_file}")

    except Exception as e:
        logging.error("Ocurrió un error durante la ejecución principal:", exc_info=True)

    finally:
        # Cerrar el navegador
        logging.debug("Cerrando el navegador...")
        driver.quit()
        logging.info("Navegador cerrado.")

except Exception as e:
    logging.critical("Fallo crítico al iniciar el script:", exc_info=True)
