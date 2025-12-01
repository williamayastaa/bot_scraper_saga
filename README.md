# 🤖 Bot Scraper Falabella

Bot automatizado para extraer información de productos desde Falabella.com.pe y almacenarla en Oracle Database.

## 🚀 Características

- ✅ Web scraping con Selenium
- ✅ Paginación automática
- ✅ Almacenamiento en Oracle DB
- ✅ Exportación a Excel
- ✅ Sistema de logs
- ✅ Manejo de errores robusto

## 📋 Requisitos

- Python 3.8+
- Chrome/Chromium instalado
- Oracle Database 11g+

## 🔧 Instalación

1. Instalar dependencias:
```bash
pip install -r requirements.txt
```

2. Configurar credenciales:
```bash
cp config.ini.example config.ini
# Editar config.ini con tus credenciales
```

## 🎯 Uso

```bash
python src/main.py
```

El bot te pedirá el nombre del producto a buscar.

## 📁 Estructura del Proyecto

- `src/scraper/` - Lógica de web scraping
- `src/database/` - Gestión de base de datos
- `src/utils/` - Utilidades compartidas
- `config/` - Configuraciones
- `data/` - Archivos Excel generados
- `logs/` - Registros de ejecución

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor abre un issue primero.

## 📝 Licencia

MIT License
