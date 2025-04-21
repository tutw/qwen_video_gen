import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configurar el sistema de logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),  # Registrar en un archivo
        logging.StreamHandler()  # Mostrar en consola
    ]
)

logging.info("Iniciando el script...")

try:
    # Configurar opciones de Chrome
    logging.debug("Configurando opciones de Chrome...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ejecución sin interfaz gráfica
    chrome_options.add_argument("--disable-gpu")  # Deshabilitar GPU
    chrome_options.add_argument("--no-sandbox")  # Necesario en entornos como GitHub Actions
    chrome_options.add_argument("--disable-dev-shm-usage")  # Evitar problemas de memoria compartida

    # Configurar ChromeDriver con webdriver-manager
    logging.debug("Inicializando el navegador Chrome con webdriver-manager...")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    try:
        # Acceder a la URL
        url = "https://chat.qwen.ai/c/07a3d948-a17e-461a-90e6-41675255ec6c"
        logging.info(f"Accediendo a la URL: {url}")
        driver.get(url)
        time.sleep(5)  # Esperar que la página cargue completamente

        # Encontrar la caja de texto donde se escribe el prompt
        logging.debug("Buscando la caja de texto para el prompt...")
        prompt_box = driver.find_element(By.TAG_NAME, 'textarea')
        prompt_text = "un gato jugando con una bola de papel"
        logging.info(f"Enviando prompt: {prompt_text}")
        prompt_box.send_keys(prompt_text)
        prompt_box.send_keys(Keys.RETURN)
        time.sleep(10)  # Esperar que se genere el video

        # Buscar el enlace al video generado
        logging.debug("Buscando el enlace del video generado...")
        video_element = driver.find_element(By.XPATH, '//a[contains(@href, "cdn.qwenlm.ai/output")]')
        video_url = video_element.get_attribute('href')
        logging.info(f"URL del video generado: {video_url}")

        # Guardar la URL en un archivo de texto
        output_file = "video_url.txt"
        logging.debug(f"Guardando la URL en el archivo: {output_file}")
        with open(output_file, "w") as file:
            file.write(f"URL del video generado: {video_url}\n")
        logging.info(f"URL guardada correctamente en {output_file}")

    except Exception as e:
        logging.error("Ocurrió un error durante la ejecución principal:", exc_info=True)

    finally:
        # Cerrar el navegador
        logging.debug("Cerrando el navegador...")
        driver.quit()
        logging.info("Navegador cerrado.")

except Exception as e:
    logging.critical("Fallo crítico al iniciar el script:", exc_info=True)
