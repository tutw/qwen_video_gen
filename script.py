try:
    # Acceder a la URL de inicio de sesión
    login_url = "https://chat.qwen.ai/auth?action=signin"
    logging.info(f"Accediendo a la URL de inicio de sesión: {login_url}")
    driver.get(login_url)

    # Completar el formulario de inicio de sesión
    logging.debug("Completando el formulario de inicio de sesión...")

    # Verifica si el formulario está dentro de un iframe
    try:
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        driver.switch_to.frame(iframe)
        logging.info("Cambiado al iframe con el formulario de inicio de sesión.")
    except Exception:
        logging.info("No se encontró un iframe. Continuando sin cambiar de contexto.")

    # Localizar el campo de correo electrónico
    email_box = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "login-email"))
    )
    email_box.send_keys(email)

    # Localizar el campo de contraseña
    password_box = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//input[@type="password" and @placeholder="Contraseña"]'))
    )
    password_box.send_keys(password)

    # Localizar y hacer clic en el botón de inicio de sesión
    login_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#chat-container > div.sticky.top-0.z-40.navbar-bg-mobile.-mb-8.flex.w-full.items-center.px-1\\.5.py-1\\.5 > div > div > div.flex.h-\\[2\\.5rem\\].flex-none.items-center.self-start.text-gray-600.dark\\:text-gray-400 > div > button'))
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
