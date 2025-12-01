"""
Consultas SQL para Oracle
"""
import sys
from pathlib import Path

# Agregar el directorio raíz al PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

import datetime
from typing import List, Dict
import pandas as pd

from config import LOG_FILE
from src.utils import setup_logger
from .connection import DatabaseConnection

logger = setup_logger("DatabaseQueries", LOG_FILE)


def insert_products(data: List[Dict]) -> bool:
    """
    Inserta productos en la base de datos
    
    Args:
        data: Lista de diccionarios con datos de productos
    
    Returns:
        bool: True si se insertó correctamente
    """
    try:
        with DatabaseConnection() as db:
            if not db.connection:
                return False
            
            # Fecha de importación
            fecha_importacion = datetime.datetime.now()
            
            # Query parametrizada
            sql = """
                INSERT INTO productos_saga (
                    proveedor,
                    distribuidor,
                    producto,
                    precio_oferta,
                    precio_normal,
                    import_time
                )
                VALUES (:1, :2, :3, :4, :5, :6)
            """
            
            # Preparar registros
            registros = [
                (
                    row["Proveedor"],
                    row["Distribuidor"],
                    row["Producto"],
                    row["Precio Oferta"],
                    row["Precio Normal"],
                    fecha_importacion
                )
                for row in data
            ]
            
            # Insertar todos de una vez
            db.cursor.executemany(sql, registros)
            db.connection.commit()
            
            logger.info(f"✅ {len(registros)} productos insertados en Oracle")
            return True
            
    except Exception as e:
        logger.error(f"Error insertando productos: {e}")
        return False


def get_all_products() -> pd.DataFrame:
    """
    Obtiene todos los productos de la base de datos
    
    Returns:
        pd.DataFrame: DataFrame con los productos
    """
    try:
        with DatabaseConnection() as db:
            if not db.connection:
                return pd.DataFrame()
            
            query = "SELECT * FROM productos_saga ORDER BY import_time DESC"
            df = pd.read_sql(query, db.connection)
            
            logger.info(f"{len(df)} productos recuperados de Oracle")
            return df
            
    except Exception as e:
        logger.error(f" Error obteniendo productos: {e}")
        return pd.DataFrame()


def list_tables() -> List[str]:
    """
    Lista todas las tablas del usuario
    
    Returns:
        List[str]: Lista de nombres de tablas
    """
    try:
        with DatabaseConnection() as db:
            if not db.connection:
                return []
            
            db.cursor.execute(
                "SELECT table_name FROM user_tables WHERE table_name LIKE '%SAGA%'"
            )
            
            tables = [row[0] for row in db.cursor]
            logger.info(f" {len(tables)} tablas encontradas")
            return tables
            
    except Exception as e:
        logger.error(f" Error listando tablas: {e}")
        return []
