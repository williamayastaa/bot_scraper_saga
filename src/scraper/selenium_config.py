"""
Configuración de Selenium WebDriver
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def create_driver(headless: bool = False):
    """
    Crea y configura el driver de Selenium
    
    Args:
        headless: Si True, ejecuta Chrome sin interfaz gráfica
    
    Returns:
        webdriver.Chrome: Driver configurado
    """
    options = Options()
    
    # Configuraciones básicas
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--start-maximized")
    options.add_argument("--remote-allow-origins=*")
    
    # Evita que Chrome se cierre al crashear Python
    options.add_experimental_option("detach", True)
    
    # Modo headless si se solicita
    if headless:
        options.add_argument("--headless")
    
    # Crear driver
    driver = webdriver.Chrome(options=options)
    
    return driver
