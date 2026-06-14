# main_skeleton.py — УНИВЕРСАЛЬНОЕ ПРИЛОЖЕНИЕ PyQt6
# Адаптируй: названия полей, заголовки, количество справочников

import sys
import os

from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QListWidgetItem,
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QLineEdit,
    QComboBox, QDialogButtonBox, QFormLayout, QDoubleSpinBox, QSpinBox,
    QTableWidgetItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from shoes_exam.db_manager import DatabaseManager
from shoes_exam.config import UI_DIR, RESOURCES_DIR, APP_NAME, COMPANY_NAME, LOGO_PATH, PLACEHOLDER_PATH, COLOR_HIGHLIGHT_DISCOUNT, COLOR_HIGHLIGHT_NO_STOCK
from shoes_exam.config import APP_NAME, COMPANY_NAME, LOGO_PATH, PLACEHOLDER_PATH
from shoes_exam.config import UI_DIR, RESOURCES_DIR, APP_NAME, COMPANY_NAME, LOGO_PATH, PLACEHOLDER_PATH, COLOR_HIGHLIGHT_DISCOUNT, COLOR_HIGHLIGHT_NO_STOCK
from shoes_exam.config import COLOR_HIGHLIGHT_DISCOUNT, COLOR_HIGHLIGHT_NO_STOCK, COLOR_TEXT_FINAL, COLOR_TEXT_STRIKE


class ItemCard(QWidget):
    # ============================================================
    # TODO: АДАПТИРУЙ КАРТОЧКУ ПОД СВОИ ПОЛЯ
    # ============================================================
    def __init__(self, item, parent=None):
        super().__init__(parent)
        self.item = item
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # --- ФОТО ---
        self.lbl_photo = QLabel()
        self.lbl_photo.setFixedSize(120, 120)
        self.lbl_photo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_photo.setStyleSheet('border: 1px solid #ccc;')
        photo_path = self.item.get('photo_path') or PLACEHOLDER_PATH
        if os.path.exists(photo_path):
            pixmap = QPixmap(photo_path).scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio)
            self.lbl_photo.setPixmap(pixmap)
        else:
            self.lbl_photo.setText('Фото')
        layout.addWidget(self.lbl_photo)

        # --- ИНФОРМАЦИЯ (центр) ---
        info_layout = QVBoxLayout()

        # TODO: Замени поля под свои (category_name, product_name и т.д.)
        category = self.item.get('category_name') or '—'
        name = self.item.get('product_name') or '—'
        self.lbl_title = QLabel(f'{category} | {name}')
        self.lbl_title.setStyleSheet('font-size: 14px; font-weight: bold;')
        info_layout.addWidget(self.lbl_title)

        # TODO: Добавь/убери поля под свои нужды
        desc = self.item.get('description') or '—'
        info_layout.addWidget(QLabel(f'Описание: {desc}'))

        man = self.item.get('manufacturer_name') or '—'
        info_layout.addWidget(QLabel(f'Производитель: {man}'))

        sup = self.item.get('supplier_name') or '—'
        info_layout.addWidget(QLabel(f'Поставщик: {sup}'))

        # Цена (с зачеркиванием при скидке)
        price = self.item['price']
        discount = self.item['discount'] or 0
        final_price = self.item.get('final_price') or price
        if discount > 0:
            price_text = f"<span style='text-decoration: line-through; color: {COLOR_TEXT_STRIKE};'>Цена: {price} ₽</span>"
            price_text += f" <span style='color: {COLOR_TEXT_FINAL}; font-weight: bold;'>→ {final_price} ₽</span>"
        else:
            price_text = f'Цена: {price} ₽'
        lbl_price = QLabel(price_text)
        lbl_price.setTextFormat(Qt.TextFormat.RichText)
        info_layout.addWidget(lbl_price)

        unit = self.item.get('unit') or 'шт'
        info_layout.addWidget(QLabel(f'Единица измерения: {unit}'))

        qty = self.item.get('quantity_in_stock') or 0
        info_layout.addWidget(QLabel(f'Количество: {qty}'))

        layout.addLayout(info_layout, stretch=1)

        # --- СКИДКА (справа) ---
        discount_layout = QVBoxLayout()
        discount_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_discount = QLabel(f'Действующая\nскидка\n{discount}%')
        lbl_discount.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_discount.setStyleSheet('font-size: 12px; font-weight: bold;')
        discount_layout.addWidget(lbl_discount)
        layout.addLayout(discount_layout)

        # --- ПОДСВЕТКА ---
        self.apply_highlight(discount, qty)

    def apply_highlight(self, discount, qty):
        # Скидка > 15%
        if discount > 15:
            self.setStyleSheet(f'background-color: {COLOR_HIGHLIGHT_DISCOUNT}; color: white;')
        # Нет на складе
        elif qty == 0:
            self.setStyleSheet(f'background-color: {COLOR_HIGHLIGHT_NO_STOCK};')


class LoginWindow(QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.current_user = None
        uic.loadUi(os.path.join(UI_DIR, 'login_skeleton.ui'), self)  # TODO: имя UI-файла
        self.setWindowTitle(f'Авторизация — {APP_NAME}')
        self.btnLogin.clicked.connect(self.do_login)
        self.btnGuest.clicked.connect(self.do_guest)
        self.lineEditPassword.returnPressed.connect(self.do_login)

    def do_login(self):
        login = self.lineEditLogin.text().strip()
        password = self.lineEditPassword.text().strip()
        if not login or not password:
            self.labelError.setText('Введите логин и пароль')
            return
        user = self.db.authenticate(login, password)
        if user:
            self.current_user = user
            self.accept()
        else:
            self.labelError.setText('Неверный логин или пароль')
            self.lineEditPassword.clear()

    def do_guest(self):
        self.current_user = {
            'user_id': 0,
            'full_name': 'Гость',
            'role_name': 'Гость'
        }
        self.accept()


class ItemEditDialog(QDialog):
    # ============================================================
    # TODO: АДАПТИРУЙ ДИАЛОГ РЕДАКТИРОВАНИЯ ПОД СВОИ ПОЛЯ
    # ============================================================
    def __init__(self, categories, item=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Редактирование' if item else 'Добавление')
        self.setMinimumWidth(400)
        self.item = item
        self.setup_ui(categories)

    def setup_ui(self, categories):
        layout = QFormLayout(self)

        # TODO: Добавь/убери поля под свои нужды
        self.edit_name = QLineEdit(self.item.get('product_name', '') if self.item else '')
        layout.addRow('Наименование:*', self.edit_name)

        self.edit_desc = QLineEdit(self.item.get('description', '') if self.item else '')
        layout.addRow('Описание:', self.edit_desc)

        self.combo_category = QComboBox()
        for cat in categories:
            self.combo_category.addItem(cat['category_name'], cat['category_id'])
        if self.item:
            idx = self.combo_category.findText(self.item.get('category_name', ''))
            if idx >= 0:
                self.combo_category.setCurrentIndex(idx)
        layout.addRow('Категория:*', self.combo_category)

        self.spin_price = QDoubleSpinBox()
        self.spin_price.setMaximum(999999.99)
        self.spin_price.setValue(self.item.get('price', 0) if self.item else 0)
        layout.addRow('Цена:*', self.spin_price)

        self.spin_discount = QDoubleSpinBox()
        self.spin_discount.setMaximum(100)
        self.spin_discount.setValue(self.item.get('discount', 0) if self.item else 0)
        layout.addRow('Скидка %:', self.spin_discount)

        self.spin_qty = QSpinBox()
        self.spin_qty.setMaximum(999999)
        self.spin_qty.setValue(self.item.get('quantity_in_stock', 0) if self.item else 0)
        layout.addRow('Количество:', self.spin_qty)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def get_data(self):
        return {
            'product_name': self.edit_name.text().strip(),
            'description': self.edit_desc.text().strip(),
            'category_id': self.combo_category.currentData(),
            'price': self.spin_price.value(),
            'discount': self.spin_discount.value(),
            'quantity_in_stock': self.spin_qty.value(),
        }


class MainWindow(QMainWindow):
    def __init__(self, db, user):
        super().__init__()
        self.db = db
        self.user = user
        self.role = user['role_name']
        uic.loadUi(os.path.join(UI_DIR, 'main_window_skeleton.ui'), self)  # TODO: имя UI-файла
        self.setWindowTitle(f'{APP_NAME} — {self.user["full_name"]}')

        # ФИО и роль в правом верхнем углу
        self.labelUserInfo.setText(f"{self.user['full_name']} | {self.role}")
        self.btnLogout.clicked.connect(self.logout)

        # Настройка видимости по ролям
        self.setup_role_ui()
        self.load_categories()
        self.load_items()

        # Сигналы
        self.btnSearch.clicked.connect(self.load_items)
        self.btnReset.clicked.connect(self.reset_filters)
        self.lineEditSearch.returnPressed.connect(self.load_items)
        self.btnAddProduct.clicked.connect(self.add_item)
        self.btnOrders.clicked.connect(self.show_orders)

    def setup_role_ui(self):
        # Гость и Клиент: только просмотр
        if self.role in ('Гость', 'Клиент'):
            self.filterPanel.setVisible(False)
            self.btnAddProduct.setVisible(False)
            self.btnOrders.setVisible(False)
        # Менеджер: фильтры + заказы
        elif self.role == 'Менеджер':
            self.btnAddProduct.setVisible(False)
            self.tableWidgetOrders.setVisible(True)
        # Администратор: всё
        elif self.role == 'Администратор':
            self.tableWidgetOrders.setVisible(True)

    def load_categories(self):
        categories = self.db.get_categories()
        self.comboBoxCategory.clear()
        self.comboBoxCategory.addItem('Все категории', None)
        for cat in categories:
            self.comboBoxCategory.addItem(cat['category_name'], cat['category_id'])

    def load_items(self):
        # TODO: Адаптируй параметры под свои фильтры
        search = self.lineEditSearch.text().strip() if self.role in ('Менеджер', 'Администратор') else ''
        cat_id = self.comboBoxCategory.currentData() if self.role in ('Менеджер', 'Администратор') else None
        items = self.db.get_items(search, cat_id)

        self.listWidgetProducts.clear()
        for item in items:
            card = ItemCard(item)
            list_item = QListWidgetItem()
            list_item.setSizeHint(card.sizeHint())
            self.listWidgetProducts.addItem(list_item)
            self.listWidgetProducts.setItemWidget(list_item, card)

    def reset_filters(self):
        self.lineEditSearch.clear()
        self.comboBoxCategory.setCurrentIndex(0)
        self.load_items()

    def add_item(self):
        if self.role != 'Администратор':
            return
        categories = self.db.get_categories()
        dialog = ItemEditDialog(categories, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            self.db.add_item(data)
            QMessageBox.information(self, 'Успех', 'Запись добавлена')
            self.load_items()

    def show_orders(self):
        orders = self.db.get_orders()
        self.tableWidgetOrders.setRowCount(len(orders))
        for i, order in enumerate(orders):
            self.tableWidgetOrders.setItem(i, 0, QTableWidgetItem(str(order['order_id'])))
            self.tableWidgetOrders.setItem(i, 1, QTableWidgetItem(order['full_name']))
            self.tableWidgetOrders.setItem(i, 2, QTableWidgetItem(str(order['order_date'])))
            self.tableWidgetOrders.setItem(i, 3, QTableWidgetItem(order['status']))
        self.tableWidgetOrders.setVisible(True)
        self.listWidgetProducts.setVisible(False)

    def logout(self):
        self.close()
        self.login_window = LoginWindow(self.db)
        if self.login_window.exec() == QDialog.DialogCode.Accepted:
            self.new_main = MainWindow(self.db, self.login_window.current_user)
            self.new_main.show()


def main():
    app = QApplication(sys.argv)

    db = DatabaseManager()
    if not db.connect():
        QMessageBox.critical(None, 'Ошибка', 'Не удалось подключиться к базе данных')
        sys.exit(1)

    login = LoginWindow(db)
    if login.exec() != QDialog.DialogCode.Accepted:
        sys.exit(0)

    window = MainWindow(db, login.current_user)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()