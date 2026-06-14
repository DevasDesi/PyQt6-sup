# db_manager_skeleton.py — УНИВЕРСАЛЬНЫЙ КЛАСС РАБОТЫ С БД
# адаптируй SQL-запросы под свои таблицы и поля!

import pymysql
from pymysql.cursors import DictCursor
from config import DB_CONFIG


class DatabaseManager:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=DB_CONFIG['host'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                database=DB_CONFIG['database'],
                charset=DB_CONFIG['charset'],
                cursorclass=DictCursor
            )
            return True
        except Exception as e:
            print(f'Ошибка подключения к БД: {e}')
            return False

    def close(self):
        if self.connection:
            self.connection.close()

    # ============================================================
    # АВТОРИЗАЦИЯ (менять не нужно)
    # ============================================================
    def authenticate(self, login, password):
        with self.connection.cursor() as cursor:
            sql = '''
                SELECT u.user_id, u.full_name, u.login, u.password, r.role_name
                FROM users u
                JOIN roles r ON u.role_id = r.role_id
                WHERE u.login = %s
            '''
            cursor.execute(sql, (login,))
            user = cursor.fetchone()
            if user and user['password'] == password:
                return user
            return None

    # ============================================================
    # TODO: АДАПТИРУЙ ПОЛЯ В SELECT ПОД СВОИ НУЖДЫ
    # ============================================================
    def get_items(self, search_text='', category_id=None):
        # Универсальный метод получения списка с фильтрами
        # Переименуй 'products' и поля под свою таблицу
        with self.connection.cursor() as cursor:
            sql = '''
                SELECT
                    p.product_id,
                    p.product_name,      -- TODO: переименуй под свое поле
                    p.description,
                    p.photo_path,
                    p.unit,
                    p.price,
                    p.discount,
                    ROUND(p.price * (1 - p.discount/100), 2) AS final_price,
                    p.quantity_in_stock,
                    c.category_name,     -- TODO: переименуй справочник
                    m.manufacturer_name, -- TODO: переименуй справочник
                    s.supplier_name      -- TODO: переименуй справочник
                    -- TODO: добавь свои поля
                FROM products p          -- TODO: переименуй таблицу
                LEFT JOIN categories c ON p.category_id = c.category_id
                LEFT JOIN manufacturers m ON p.manufacturer_id = m.manufacturer_id
                LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
                WHERE 1=1
            '''
            params = []
            if search_text:
                sql += ' AND p.product_name LIKE %s'  # TODO: поле для поиска
                params.append(f'%{search_text}%')
            if category_id:
                sql += ' AND p.category_id = %s'
                params.append(category_id)
            sql += ' ORDER BY p.product_name'  # TODO: сортировка
            cursor.execute(sql, params)
            return cursor.fetchall()

    def get_categories(self):
        # TODO: переименуй таблицу если нужно
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT category_id, category_name FROM categories ORDER BY category_name')
            return cursor.fetchall()

    def get_orders(self):
        # TODO: переименуй таблицы под свою область
        with self.connection.cursor() as cursor:
            sql = '''
                SELECT o.order_id, u.full_name, o.order_date, o.status
                FROM orders o
                JOIN users u ON o.user_id = u.user_id
                ORDER BY o.order_date DESC
            '''
            cursor.execute(sql)
            return cursor.fetchall()

    # ============================================================
    # TODO: АДАПТИРУЙ CRUD ПОД СВОИ ПОЛЯ
    # ============================================================
    def add_item(self, data):
        # Универсальное добавление записи
        # TODO: переименуй таблицу и поля
        with self.connection.cursor() as cursor:
            sql = '''
                INSERT INTO products
                (product_name, description, photo_path, category_id, manufacturer_id,
                 supplier_id, unit, price, discount, quantity_in_stock)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(sql, (
                data['product_name'],
                data['description'],
                data.get('photo_path', 'picture.png'),
                data['category_id'],
                data.get('manufacturer_id'),
                data.get('supplier_id'),
                data.get('unit', 'шт'),
                data['price'],
                data.get('discount', 0),
                data.get('quantity_in_stock', 0)
            ))
            self.connection.commit()
            return cursor.lastrowid

    def delete_item(self, item_id):
        # TODO: переименуй таблицу и поле ID
        with self.connection.cursor() as cursor:
            cursor.execute('DELETE FROM products WHERE product_id = %s', (item_id,))
            self.connection.commit()
            return cursor.rowcount > 0

    def update_item(self, item_id, data):
        # TODO: переименуй таблицу и поля
        with self.connection.cursor() as cursor:
            sql = '''
                UPDATE products SET
                    product_name = %s,
                    description = %s,
                    category_id = %s,
                    price = %s,
                    discount = %s,
                    quantity_in_stock = %s
                WHERE product_id = %s
            '''
            cursor.execute(sql, (
                data['product_name'],
                data['description'],
                data['category_id'],
                data['price'],
                data['discount'],
                data['quantity_in_stock'],
                item_id
            ))
            self.connection.commit()
            return cursor.rowcount > 0