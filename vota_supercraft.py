from RPA.Browser.Selenium import Selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth


import time


def open_browser(headless=False):
    try:
        # Inicializa el navegador
        browser = Selenium()
        chrome_options = Options()
           
      
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        driver  = webdriver.Chrome(chrome_options)

          
        browser.open_available_browser("https://supercraft.es/votar/", headless = headless , options={"arguments": ["--ignore-certificate-errors", "-ignore-certificate-errors"], "capabilities": {"acceptInsecureCerts": True}}, download= False)     
        print("Navegador abierto correctamente en la URL especificada.")

        # Ajusta el tamaño de la ventana para pantallas grandes
        browser.set_window_size(1920, 1080)
        print("Resolución de la ventana ajustada a 1920x1080.")

        # Opcional: Zoom de la página
        browser.execute_javascript("document.body.style.zoom='80%'")
        print("Zoom ajustado al 80%.")

        # Mantén el navegador abierto por 10 segundos para observarlo (opcional)
        browser.wait_until_page_contains("Votar", timeout=10)

       
        browser.click_element("xpath://div/article/section/div/main/a[3]")
        browser.click_element("xpath://div/article/section/div/main/a[4]")
                                              
        
        

     
        
        # Retorna la instancia del navegador por si deseas realizar más acciones
        return browser

    except Exception as e:
        print(f"Error al abrir el navegador: {e}")
        return None


if __name__ == "__main__":
    browser_instance = open_browser(headless=False)
    if browser_instance:
        input("Presiona Enter para cerrar el navegador...")
        browser_instance.close_browser()
