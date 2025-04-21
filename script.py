from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Configurar el controlador del navegador (asegúrate de tener el controlador adecuado para tu navegador)
driver = webdriver.Chrome()  # O usa otro controlador como Firefox, Edge, etc.

try:
    # Accede a la URL
    driver.get("https://chat.qwen.ai/c/07a3d948-a17e-461a-90e6-41675255ec6c")
    time.sleep(5)  # Espera que la página cargue completamente (ajusta el tiempo si es necesario)

    # Encuentra la caja de texto donde se escribe el prompt
    prompt_box = driver.find_element(By.TAG_NAME, 'textarea')  # Ajusta el selector si es necesario
    prompt_box.send_keys("un gato jugando con una bola de papel")
    prompt_box.send_keys(Keys.RETURN)  # Simula presionar Enter
    time.sleep(10)  # Espera que se genere el video (ajusta el tiempo según lo necesario)

    # Encuentra el último video generado
    video_element = driver.find_element(By.XPATH, '//a[contains(@href, "cdn.qwenlm.ai/output")]')  # Selector XPath para encontrar el enlace del video
    video_url = video_element.get_attribute('href')

    print("URL del video generado:", video_url)

finally:
    # Cierra el navegador
    driver.quit()
