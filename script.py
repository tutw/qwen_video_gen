from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import os

# Configurar opciones de Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Ejecutar en modo headless (sin interfaz gráfica)
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")  # Requerido en algunos entornos como servidores
chrome_options.add_argument("--disable-dev-shm-usage")  # Manejo de memoria compartida

# Configurar el servicio de ChromeDriver
chromedriver_path = "chromedriver"  # Asegúrate de que el binario de ChromeDriver esté en tu PATH o especifica la ruta completa
service = Service(chromedriver_path)

# Inicializar el controlador del navegador
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Acceder a la URL
    driver.get("https://chat.qwen.ai/c/07a3d948-a17e-461a-90e6-41675255ec6c")
    print("Accediendo a la página...")
    time.sleep(5)  # Esperar que la página cargue completamente

    # Encontrar la caja de texto donde se escribe el prompt
    prompt_box = driver.find_element(By.TAG_NAME, 'textarea')
    prompt_text = "un gato jugando con una bola de papel"
    print(f"Enviando prompt: {prompt_text}")
    prompt_box.send_keys(prompt_text)
    prompt_box.send_keys(Keys.RETURN)  # Simular presionar Enter
    time.sleep(10)  # Esperar que se genere el video

    # Buscar el enlace al video generado
    video_element = driver.find_element(By.XPATH, '//a[contains(@href, "cdn.qwenlm.ai/output")]')
    video_url = video_element.get_attribute('href')
    print(f"URL del video generado: {video_url}")

    # Guardar la URL en un archivo de texto
    output_file = "video_url.txt"
    with open(output_file, "w") as file:
        file.write(f"URL del video generado: {video_url}\n")
    print(f"URL guardada en {output_file}")

except Exception as e:
    print(f"Ocurrió un error: {e}")

finally:
    # Cerrar el navegador
    driver.quit()
    print("Navegador cerrado.")
