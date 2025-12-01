"""
Gestión de conexión a Oracle Database
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

import oracledb
from typing import Optional

from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_SERVICE, LOG_FILE
from src.utils import setup_logger

logger = setup_logger("DatabaseConnection", LOG_FILE)


class DatabaseConnection:
    """Clase para manejar la conexión a Oracle"""
    
    def __init__(self):
        """Inicializa la conexión"""
        self.connection: Optional[oracledb.Connection] = None
        self.cursor: Optional[oracledb.Cursor] = None
    
    def connect(self) -> bool:
        """
        Establece conexión con la base de datos
        
        Returns:
            bool: True si la conexión fue exitosa
        """
        try:
            dsn = f"{DB_HOST}:{DB_PORT}/{DB_SERVICE}"
            
            self.connection = oracledb.connect(
                user=DB_USER,
                password=DB_PASSWORD,
                dsn=dsn
            )
            
            self.cursor = self.connection.cursor()
            logger.info(" Conexión a Oracle exitosa")
            return True
            
        except Exception as e:
            logger.error(f"Error conectando a Oracle: {e}")
            return False
    
    def disconnect(self):
        """Cierra la conexión a la base de datos"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            logger.info(" Desconectado de Oracle")
        except Exception as e:
            logger.error(f"Error al desconectar: {e}")
    
    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.disconnect()
