"""
Manejo de archivos Excel
"""
import pandas as pd
from pathlib import Path
from typing import List, Dict

def save_to_excel(data: List[Dict], output_path: Path) -> bool:
    """
    Guarda datos en formato Excel
    
    Args:
        data: Lista de diccionarios con los datos
        output_path: Ruta del archivo de salida
    
    Returns:
        bool: True si se guardó correctamente
    """
    try:
        df = pd.DataFrame(data)
        df.to_excel(output_path, index=False)
        return True
    except Exception as e:
        print(f" Error al guardar Excel: {e}")
        return False

def load_from_excel(input_path: Path) -> pd.DataFrame:
    """
    Carga datos desde Excel
    
    Args:
        input_path: Ruta del archivo Excel
    
    Returns:
        pd.DataFrame: DataFrame con los datos
    """
    try:
        return pd.read_excel(input_path)
    except Exception as e:
        print(f" Error al cargar Excel: {e}")
        return pd.DataFrame()
