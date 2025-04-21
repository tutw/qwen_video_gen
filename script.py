#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import uuid
import logging
import subprocess
import atexit
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configurar el logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def kill_chrome_processes():
    """Mata todos los procesos de Chrome de forma más agresiva"""
    logging.info("Cerrando procesos de Chrome...")
    try:
        if os.name == 'nt':  # Windows
            subprocess.run(['taskkill', '/F', '/IM', 'chrome.exe'], 
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
            subprocess.run(['taskkill', '/F', '/IM', 'chromedriver.exe'], 
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        else:  # Linux/Mac
            subprocess.run(['pkill', '-9', '-f', 'chrome'], 
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
            subprocess.run(['pkill', '-9', '-f', 'chromedriver'], 
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        time.sleep(1)  # Pequeña pausa para asegurar que los procesos terminen
        logging.info("Procesos de Chrome cerrados correctamente.")
    except Exception as e:
        logging.warning(f"Error al intentar cerrar procesos de Chrome: {e}")

def main():
    """Función principal del script"""
    driver = None
    
    try:
        logging.info("Iniciando el script...")
        
        # Matar procesos existentes de Chrome para evitar conflictos
        kill_chrome_processes()
        
        # Configurar opciones de Chrome para entorno CI/CD
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')  # Modo headless para CI/CD
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        
        # IMPORTANTE: No usar --user-data-dir en absoluto
        # Esta es la clave para resolver el problema
        
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-browser-side-navigation')
        chrome_options.add_argument('--disable-features=VizDisplayCompositor')
        
        # Inicializar el servicio de ChromeDriver
        service = Service(ChromeDriverManager().install())
        
        # Crear una instancia del navegador
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Establecer un timeout para las operaciones de espera
        wait = WebDriverWait(driver, 10)
        
        # Aquí va el resto de tu código que utiliza el driver
        # Por ejemplo:
        driver.get("https://www.example.com")
        logging.info("Página cargada correctamente")
        
        # EJEMPLO: Login con credenciales desde variables de entorno
        # Asumiendo que estás utilizando las variables LOGIN_EMAIL y LOGIN_PASSWORD
        
        email = os.environ.get('LOGIN_EMAIL')
        password = os.environ.get('LOGIN_PASSWORD')
        
        if email and password:
            # Esto es solo un ejemplo, ajusta según la estructura de tu sitio
            # try:
            #     email_field = wait.until(EC.presence_of_element_located((By.ID, "email")))
            #     email_field.send_keys(email)
            #     
            #     password_field = driver.find_element(By.ID, "password")
            #     password_field.send_keys(password)
            #     
            #     submit_button = driver.find_element(By.ID, "login-button")
            #     submit_button.click()
            #     
            #     # Esperar a que se complete el login
            #     wait.until(EC.presence_of_element_located((By.ID, "dashboard")))
            #     logging.info("Login completado correctamente")
            # except Exception as e:
            #     logging.error(f"Error durante el login: {e}")
        
        # Aquí continúa con el resto de la lógica de tu script...
        
        logging.info("Script ejecutado correctamente")
        
    except Exception as e:
        logging.critical("Error crítico durante la ejecución:")
        logging.exception(e)
        return 1
    finally:
        # Asegurarse de que el driver se cierre correctamente
        if driver:
            try:
                driver.quit()
            except:
                pass
        
        # Limpiar procesos de Chrome
        kill_chrome_processes()
    
    return 0

if __name__ == "__main__":
    # Registrar la función de limpieza para que se ejecute al finalizar
    atexit.register(kill_chrome_processes)
    
    # Ejecutar la función principal
    sys.exit(main())
