"""
Punto de entrada principal de la aplicación
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from config import OUTPUT_EXCEL, LOG_FILE
from src.scraper import FalabellaScraper, create_driver
from src.database import insert_products, list_tables
from src.utils import save_to_excel, setup_logger

logger = setup_logger("Main", LOG_FILE)


def main():
    """Función principal"""
    
    print("=" * 60)
    print(" BOT SCRAPER FALABELLA".center(60))
    print("=" * 60)
    print()
    
    # Solicitar producto
    product_name = input(" Introduce el producto que deseas scrapear: ").strip()
    
    if not product_name:
        print(" Debes ingresar un nombre de producto")
        return
    
    logger.info(f" Iniciando scraping de: {product_name}")
    
    # Crear driver
    driver = None
    try:
        print("\n Iniciando navegador...")
        driver = create_driver(headless=False)
        
        # Crear scraper
        scraper = FalabellaScraper(driver)
        
        # Realizar scraping
        print(" Buscando productos...\n")
        data = scraper.scrape_all_pages(product_name)
        
        if not data:
            print("  No se encontraron productos")
            return
        
        print(f"\n Total productos encontrados: {len(data)}")
        
        # Guardar en Excel
        print(f"\n Guardando en Excel: {OUTPUT_EXCEL}")
        if save_to_excel(data, OUTPUT_EXCEL):
            print(" Excel guardado correctamente")
        else:
            print(" Error guardando Excel")
        
        # Guardar en Oracle
        print("\n  Guardando en Oracle Database...")
        if insert_products(data):
            print(" Datos insertados en Oracle correctamente")
        else:
            print(" Error insertando en Oracle")
        
        print("\n Proceso completado exitosamente")
        
    except KeyboardInterrupt:
        print("\n\n  Proceso interrumpido por el usuario")
        logger.warning("Proceso interrumpido por usuario")
        
    except Exception as e:
        print(f"\n Error inesperado: {e}")
        logger.error(f"Error inesperado: {e}", exc_info=True)
        
    finally:
        if driver:
            print("\n Cerrando navegador...")
            driver.quit()
        
        print("\n" + "=" * 60)
        print(" ¡Hasta luego!")
        print("=" * 60)


if __name__ == "__main__":
    main()
