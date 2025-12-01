"""
Configuración centralizada del proyecto
"""
import os
from pathlib import Path
import configparser

# Directorios base
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = BASE_DIR / "config.ini"

# Crear directorios si no existen
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Leer configuración
config = configparser.ConfigParser()

if CONFIG_FILE.exists():
    config.read(CONFIG_FILE)
else:
    print("Archivo config.ini no encontrado. Usando valores por defecto.")
    print("Copia config.ini.example a config.ini y configura tus credenciales.")

# Configuración de base de datos
DB_USER = config.get("DATABASE", "user", fallback="SYSTEM")
DB_PASSWORD = config.get("DATABASE", "password", fallback="")
DB_HOST = config.get("DATABASE", "host", fallback="localhost")
DB_PORT = config.get("DATABASE", "port", fallback="1521")
DB_SERVICE = config.get("DATABASE", "service_name", fallback="xepdb1")

# Configuración del scraper
SCRAPER_URL = config.get("SCRAPER", "url", fallback="https://www.falabella.com.pe/falabella-pe")
SCRAPER_TIMEOUT = config.getint("SCRAPER", "timeout", fallback=10)
SCRAPER_HEADLESS = config.getboolean("SCRAPER", "headless", fallback=False)

# Rutas de salida
OUTPUT_EXCEL = DATA_DIR / "productos.xlsx"
LOG_FILE = LOGS_DIR / "scraper.log"
