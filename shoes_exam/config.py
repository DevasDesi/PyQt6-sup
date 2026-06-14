# shoes_exam/config.py
import os

# Определяем путь к папке пакета (где лежит этот файл)
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
UI_DIR = os.path.join(PACKAGE_DIR, 'ui')
RESOURCES_DIR = os.path.join(PACKAGE_DIR, 'resources')

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'shoes_db',
    'charset': 'utf8mb4',
    'cursorclass': 'pymysql.cursors.DictCursor'
}

APP_NAME = "Магазин обуви"   # <-- Название твоего приложения
COMPANY_NAME = "ООO Обувь" # <-- Название компании

# Цвета для подсветки (можно менять)
COLOR_HIGHLIGHT_DISCOUNT = "#2E8B57"   # Скидка > 15%
COLOR_HIGHLIGHT_NO_STOCK = "#ADD8E6"   # Нет на складе
COLOR_TEXT_STRIKE = "red"              # Зачеркнутая цена
COLOR_TEXT_FINAL = "black"             # Итоговая цена

# Пути к ресурсам (подготовь эти файлы заранее!)
LOGO_PATH = "resources/logo.png"       # <-- Логотип компании
PLACEHOLDER_PATH = "resources/picture.png"  # <-- Заглушка для товара без фото