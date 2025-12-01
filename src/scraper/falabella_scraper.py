"""
Scraper para Falabella.com.pe
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from typing import List, Dict

from config import SCRAPER_URL, SCRAPER_TIMEOUT, LOG_FILE
from src.utils import setup_logger

logger = setup_logger("FalabellaScraper", LOG_FILE)


class FalabellaScraper:
    """Clase para hacer scraping de productos en Falabella"""
    
    def __init__(self, driver):
        """
        Inicializa el scraper
        
        Args:
            driver: WebDriver de Selenium
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, SCRAPER_TIMEOUT)
        self.data_total = []
        logger.info(" Scraper inicializado")
    
    def search_product(self, product_name: str) -> bool:
        """
        Busca un producto en Falabella
        
        Args:
            product_name: Nombre del producto a buscar
        
        Returns:
            bool: True si la búsqueda fue exitosa
        """
        try:
            logger.info(f" Navegando a {SCRAPER_URL}")
            self.driver.get(SCRAPER_URL)
            
            # Buscar barra de búsqueda
            search_input = self.wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "SearchBar-module_searchBar__Input__NDqpk")
                )
            )
            
            logger.info(f" Buscando: {product_name}")
            search_input.send_keys(product_name)
            
            # Click en botón de búsqueda
            search_button = self.driver.find_element(
                By.CLASS_NAME, 
                "SearchBar-module_searchIcon__-gxub"
            )
            search_button.click()
            
            # Esperar resultados
            self.wait.until(
                EC.presence_of_element_located((By.ID, "testId-searchResults"))
            )
            
            logger.info(" Búsqueda exitosa")
            return True
            
        except Exception as e:
            logger.error(f" Error en búsqueda: {e}")
            return False
    
    def extract_current_page(self) -> int:
        """
        Extrae productos de la página actual
        
        Returns:
            int: Número de productos extraídos
        """
        try:
            # Esperar que carguen los productos
            self.wait.until(
                EC.presence_of_element_located((By.ID, "testId-searchResults"))
            )
            
            # Obtener productos
            products = self.driver.find_elements(
                By.CLASS_NAME,
                "search-results-4-grid"
            )
            
            count = 0
            for p in products:
                # Extraer datos con manejo de errores
                try:
                    proveedor = p.find_element(By.CLASS_NAME, "pod-title").text
                except:
                    proveedor = ""
                
                try:
                    distribuidor = p.find_element(
                        By.CSS_SELECTOR, 
                        "[id*=testId-pod-displaySellerText]"
                    ).text
                except:
                    distribuidor = ""
                
                try:
                    nombre_producto = p.find_element(
                        By.CLASS_NAME, 
                        "pod-subTitle"
                    ).text
                except:
                    nombre_producto = ""
                
                try:
                    precio_oferta = p.find_element(By.CLASS_NAME, "high").text
                except:
                    precio_oferta = ""
                
                try:
                    precio_normal = p.find_element(By.CLASS_NAME, "medium").text
                except:
                    precio_normal = ""
                
                # Guardar datos
                self.data_total.append({
                    "Proveedor": proveedor,
                    "Distribuidor": distribuidor,
                    "Producto": nombre_producto,
                    "Precio Oferta": precio_oferta,
                    "Precio Normal": precio_normal
                })
                count += 1
            
            logger.info(f" {count} productos extraídos de esta página")
            return count
            
        except Exception as e:
            logger.error(f" Error extrayendo productos: {e}")
            return 0
    
    def has_next_page(self) -> bool:
        """
        Verifica si existe una página siguiente
        
        Returns:
            bool: True si hay página siguiente
        """
        try:
            button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.ID, "testId-pagination-bottom-arrow-right")
                )
            )
            return True
        except:
            return False
    
    def go_to_next_page(self) -> bool:
        """
        Navega a la siguiente página
        
        Returns:
            bool: True si se navegó exitosamente
        """
        try:
            button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.ID, "testId-pagination-bottom-arrow-right")
                )
            )
            
            self.driver.execute_script("arguments[0].click();", button)
            time.sleep(2)
            
            logger.info("  Navegando a siguiente página")
            return True
            
        except Exception as e:
            logger.error(f" No se pudo ir a la siguiente página: {e}")
            return False
    
    def scrape_all_pages(self, product_name: str) -> List[Dict]:
        """
        Realiza scraping de todas las páginas de un producto
        
        Args:
            product_name: Nombre del producto a buscar
        
        Returns:
            List[Dict]: Lista con todos los productos encontrados
        """
        # Buscar producto
        if not self.search_product(product_name):
            logger.error(" No se pudo realizar la búsqueda")
            return []
        
        page_num = 1
        
        # Bucle de paginación
        while True:
            logger.info(f" Procesando página {page_num}")
            self.extract_current_page()
            
            if self.has_next_page():
                if not self.go_to_next_page():
                    break
                page_num += 1
            else:
                logger.info(" No hay más páginas")
                break
        
        logger.info(f" Scraping completo: {len(self.data_total)} productos encontrados")
        return self.data_total
    
    def get_data(self) -> List[Dict]:
        """Retorna los datos recolectados"""
        return self.data_total
    
    def clear_data(self):
        """Limpia los datos almacenados"""
        self.data_total = []
        logger.info("  Datos limpiados")
