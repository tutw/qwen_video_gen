#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import uuid
import tempfile
import logging
import subprocess
import atexit
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# Configurar el logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

def kill_chrome_processes():
    """Mata todos los procesos de Chrome de forma más efectiva"""
    logging.info("Cerrando procesos de Chrome...")
    try:
        if os.name == 'nt':  # Windows
            subprocess.run(['taskkill', '/F', '/IM', 'chrome.exe', '/IM', 'chromedriver.exe'], 
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        else:  # Linux/Mac
            subprocess.run(['pkill', '-f', 'chrome'], 
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
            subprocess.run(['pkill', '-f', 'chromedriver'], 
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        time.sleep(1)  # Pequeña pausa para asegurar que los procesos terminen
        logging.info("Procesos de Chrome cerrados correctamente.")
    except Exception as e:
        logging.warning(f"Error al intentar cerrar procesos de Chrome: {e}")

def setup_chrome():
    """Configura y devuelve el driver de Chrome con opciones seguras"""
    # Crear un directorio temporal único para el perfil de Chrome
    unique_dir = Path(tempfile.gettempdir()) / f"chrome_data_{int(time.time())}_{uuid.uuid4().hex}"
    unique_dir.mkdir(parents=True, exist_ok=True)
    
    logging.debug(f"Configurando opciones de Chrome...")
    logging.debug(f"Usando directorio temporal para user-data-dir: {unique_dir}")
    
    # Configurar opciones de Chrome
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument(f'--user-data-dir={str(unique_dir)}')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--mute-audio')
    chrome_options.add_argument('--disable-browser-side-navigation')
    chrome_options.add_argument('--disable-features=NetworkService')
    chrome_options.add_argument('--disable-features=VizDisplayCompositor')
    
    # Opcional: añadir modo headless para entornos CI/CD
    # chrome_options.add_argument('--headless')
    
    # Inicializar el servicio de ChromeDriver
    logging.debug("Inicializando el servicio de ChromeDriver...")
    service = Service(ChromeDriverManager().install())
    
    # Crear una instancia del navegador
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver, unique_dir
    except Exception as e:
        logging.critical(f"Error al inicializar Chrome: {e}")
        # Intentar limpiar recursos antes de re-lanzar la excepción
        try:
            import shutil
            shutil.rmtree(unique_dir, ignore_errors=True)
        except:
            pass
        raise

def main():
    """Función principal del script"""
    driver = None
    temp_dir = None
    
    try:
        logging.info("Iniciando el script...")
        
        # Matar procesos existentes de Chrome para evitar conflictos
        kill_chrome_processes()
        
        # Configurar e iniciar Chrome
        driver, temp_dir = setup_chrome()
        
        # Establecer un timeout para las operaciones de espera
        wait = WebDriverWait(driver, 10)
        
        # Aquí va el resto de tu código que utiliza el driver
        # Por ejemplo:
        driver.get("https://www.example.com")
        logging.info("Página cargada correctamente")
        
        # Esperar a que aparezca un elemento específico
        # wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
        
        # Ejemplo de operación con la página
        # title = driver.title
        # logging.info(f"Título de la página: {title}")
        
        # Aquí puedes continuar con el resto de la lógica de tu script...
        
    except Exception as e:
        logging.critical(f"Error crítico durante la ejecución:")
        logging.exception(e)
        return 1
    finally:
        # Asegurarse de que el driver se cierre correctamente
        if driver:
            logging.info("Cerrando el navegador...")
            try:
                driver.quit()
            except:
                pass
        
        # Limpiar procesos y directorios
        kill_chrome_processes()
        
        # Eliminar el directorio temporal si existe
        if temp_dir and os.path.exists(temp_dir):
            try:
                import shutil
                logging.debug(f"Eliminando directorio temporal: {temp_dir}")
                shutil.rmtree(temp_dir, ignore_errors=True)
            except Exception as e:
                logging.warning(f"Error al eliminar directorio temporal: {e}")
    
    logging.info("Script finalizado correctamente")
    return 0

if __name__ == "__main__":
    # Registrar la función de limpieza para que se ejecute incluso si hay un error fatal
    atexit.register(kill_chrome_processes)
    
    # Ejecutar la función principal
    sys.exit(main())
