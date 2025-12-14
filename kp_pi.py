import sys
import json
import datetime
import os
from typing import Dict, List, Optional
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# Классы для работы с данными (остаются без изменений)
class BodyManagement:
    """Класс для управления учетов тел"""
    
    def __init__(self, data_file="bodies.json"):
        self.data_file = data_file
        self.bodies = self.load_data()
    
    def load_data(self) -> List[Dict]:
        """Загрузка данных из файла"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_data(self):
        """Сохранение данных в файл"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.bodies, f, ensure_ascii=False, indent=2)
    
    def register_body(self, 
                     full_name: str,
                     arrival_date: str,
                     source: str,
                     storage_location: str,
                     documents: List[str],
                     status: str = "поступило") -> Dict:
        """Регистрация нового тела"""
        
        body_id = len(self.bodies) + 1
        
        body_data = {
            "id": body_id,
            "full_name": full_name,
            "arrival_date": arrival_date,
            "source": source,
            "storage_location": storage_location,
            "documents": documents,
            "status": status,
            "preparation_date": None,
            "release_date": None,
            "funeral_service": None,
            "notes": "",
            "registration_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        
        self.bodies.append(body_data)
        self.save_data()
        return body_data
    
    def update_body_status(self, body_id: int, new_status: str, notes: str = ""):
        """Обновление статуса тела"""
        for body in self.bodies:
            if body["id"] == body_id:
                body["status"] = new_status
                if notes:
                    body["notes"] = notes
                if new_status == "подготовлено":
                    body["preparation_date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                elif new_status == "выдано":
                    body["release_date"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                self.save_data()
                return True
        return False
    
    def get_body_by_id(self, body_id: int) -> Optional[Dict]:
        """Получение информации о теле по ID"""
        for body in self.bodies:
            if body["id"] == body_id:
                return body
        return None
    
    def list_bodies(self, status_filter: str = None) -> List[Dict]:
        """Список тел с возможностью фильтрации по статусу"""
        if status_filter:
            return [body for body in self.bodies if body["status"] == status_filter]
        return self.bodies

class SanitaryControl:
    """Класс для контроля санитарных норм"""
    
    def __init__(self, data_file="sanitary.json"):
        self.data_file = data_file
        self.checks = self.load_data()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.checks, f, ensure_ascii=False, indent=2)
    
    def record_check(self, 
                    check_type: str,
                    temperature: float,
                    cleanliness_score: int,
                    inspector: str,
                    notes: str = "") -> Dict:
        """Запись санитарной проверки"""
        
        check_id = len(self.checks) + 1
        
        check_data = {
            "id": check_id,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "check_type": check_type,
            "temperature": temperature,
            "cleanliness_score": cleanliness_score,
            "inspector": inspector,
            "notes": notes,
            "violations": []
        }
        
        self.checks.append(check_data)
        self.save_data()
        return check_data
    
    def add_violation(self, check_id: int, violation: str, corrective_action: str):
        """Добавление нарушения к проверке"""
        for check in self.checks:
            if check["id"] == check_id:
                check["violations"].append({
                    "violation": violation,
                    "corrective_action": corrective_action,
                    "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                })
                self.save_data()
                return True
        return False

class StaffManagement:
    """Класс для управления персоналом"""
    
    def __init__(self, data_file="staff.json"):
        self.data_file = data_file
        self.staff = self.load_data()
        self.schedules = []
    
    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.staff, f, ensure_ascii=False, indent=2)
    
    def add_employee(self,
                    full_name: str,
                    position: str,
                    contact: str,
                    qualifications: List[str]) -> Dict:
        """Добавление сотрудника"""
        
        employee_data = {
            "id": len(self.staff) + 1,
            "full_name": full_name,
            "position": position,
            "contact": contact,
            "qualifications": qualifications,
            "hire_date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "status": "активен"
        }
        
        self.staff.append(employee_data)
        self.save_data()
        return employee_data

class FuneralServiceCoordination:
    """Класс для координации с ритуальными службами"""
    
    def __init__(self, data_file="funeral_services.json"):
        self.data_file = data_file
        self.coordinations = self.load_data()
    
    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def save_data(self):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.coordinations, f, ensure_ascii=False, indent=2)
    
    def register_coordination(self,
                            body_id: int,
                            service_name: str,
                            contact_person: str,
                            contact_phone: str,
                            planned_date: str,
                            documents_needed: List[str]) -> Dict:
        """Регистрация координации с ритуальной службой"""
        
        coordination_data = {
            "id": len(self.coordinations) + 1,
            "body_id": body_id,
            "service_name": service_name,
            "contact_person": contact_person,
            "contact_phone": contact_phone,
            "planned_date": planned_date,
            "documents_needed": documents_needed,
            "documents_provided": [],
            "coordination_date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "status": "в процессе"
        }
        
        self.coordinations.append(coordination_data)
        self.save_data()
        return coordination_data

# Классы для графического интерфейса
class MainWindow(QMainWindow):
    """Главное окно приложения"""
    
    def __init__(self):
        super().__init__()
        
        # Инициализация менеджеров данных
        self.body_manager = BodyManagement()
        self.sanitary_control = SanitaryControl()
        self.staff_manager = StaffManagement()
        self.funeral_coordinator = FuneralServiceCoordination()
        
        self.init_ui()
        self.create_test_data()
    
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        self.setWindowTitle('Система администрирования морга')
        self.setGeometry(100, 100, 1200, 700)
        
        # Установка стиля
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
            }
            QTabWidget::pane {
                border: 1px solid #cccccc;
                background-color: white;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QLabel {
                font-size: 14px;
            }
            QLineEdit, QTextEdit, QComboBox {
                padding: 6px;
                border: 1px solid #cccccc;
                border-radius: 4px;
                font-size: 14px;
            }
            QTableWidget {
                gridline-color: #ddd;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                padding: 8px;
                border: 1px solid #ddd;
            }
        """)
        
        # Создание центрального виджета и основного лэйаута
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Заголовок
        title_label = QLabel('🏥 СИСТЕМА АДМИНИСТРИРОВАНИЯ МОРГА')
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                padding: 20px;
                background-color: white;
                border-bottom: 2px solid #4CAF50;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Создание вкладок
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Создание вкладок
        self.create_body_management_tab()
        self.create_sanitary_control_tab()
        self.create_staff_management_tab()
        self.create_funeral_coordination_tab()
        self.create_reports_tab()
        
        # Статус бар
        self.statusBar().showMessage('Готово к работе')
    
    def create_body_management_tab(self):
        """Вкладка управления телами"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Панель инструментов
        toolbar = QHBoxLayout()
        
        btn_new = QPushButton('➕ Новое тело')
        btn_new.clicked.connect(self.show_new_body_dialog)
        toolbar.addWidget(btn_new)
        
        btn_refresh = QPushButton('🔄 Обновить')
        btn_refresh.clicked.connect(self.refresh_body_table)
        toolbar.addWidget(btn_refresh)
        
        # Фильтр по статусу
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel('Фильтр по статусу:'))
        self.status_filter = QComboBox()
        self.status_filter.addItems(['Все', 'поступило', 'подготовлено', 'выдано'])
        self.status_filter.currentTextChanged.connect(self.refresh_body_table)
        filter_layout.addWidget(self.status_filter)
        filter_layout.addStretch()
        
        layout.addLayout(toolbar)
        layout.addLayout(filter_layout)
        
        # Таблица с телами
        self.body_table = QTableWidget()
        self.body_table.setColumnCount(8)
        self.body_table.setHorizontalHeaderLabels([
            'ID', 'ФИО', 'Дата поступления', 'Источник', 
            'Место хранения', 'Статус', 'Документы', 'Примечания'
        ])
        self.body_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.body_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.body_table.doubleClicked.connect(self.edit_body)
        
        layout.addWidget(self.body_table)
        
        # Кнопка редактирования
        btn_edit = QPushButton('✏️ Редактировать статус')
        btn_edit.clicked.connect(self.edit_body)
        layout.addWidget(btn_edit)
        
        self.tab_widget.addTab(tab, '📋 Управление телами')
        self.refresh_body_table()
    
    def create_sanitary_control_tab(self):
        """Вкладка санитарного контроля"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Панель инструментов
        toolbar = QHBoxLayout()
        
        btn_new_check = QPushButton('➕ Новая проверка')
        btn_new_check.clicked.connect(self.show_new_sanitary_check_dialog)
        toolbar.addWidget(btn_new_check)
        
        btn_refresh = QPushButton('🔄 Обновить')
        btn_refresh.clicked.connect(self.refresh_sanitary_table)
        toolbar.addWidget(btn_refresh)
        
        layout.addLayout(toolbar)
        
        # Таблица с проверками
        self.sanitary_table = QTableWidget()
        self.sanitary_table.setColumnCount(7)
        self.sanitary_table.setHorizontalHeaderLabels([
            'ID', 'Дата', 'Тип проверки', 'Температура', 
            'Оценка чистоты', 'Инспектор', 'Нарушения'
        ])
        self.sanitary_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        layout.addWidget(self.sanitary_table)
        
        # Кнопка добавления нарушения
        btn_add_violation = QPushButton('⚠️ Добавить нарушение')
        btn_add_violation.clicked.connect(self.show_add_violation_dialog)
        layout.addWidget(btn_add_violation)
        
        self.tab_widget.addTab(tab, '🧼 Санитарный контроль')
        self.refresh_sanitary_table()
    
    def create_staff_management_tab(self):
        """Вкладка управления персоналом"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Панель инструментов
        toolbar = QHBoxLayout()
        
        btn_new_employee = QPushButton('➕ Новый сотрудник')
        btn_new_employee.clicked.connect(self.show_new_employee_dialog)
        toolbar.addWidget(btn_new_employee)
        
        btn_refresh = QPushButton('🔄 Обновить')
        btn_refresh.clicked.connect(self.refresh_staff_table)
        toolbar.addWidget(btn_refresh)
        
        layout.addLayout(toolbar)
        
        # Таблица с сотрудниками
        self.staff_table = QTableWidget()
        self.staff_table.setColumnCount(6)
        self.staff_table.setHorizontalHeaderLabels([
            'ID', 'ФИО', 'Должность', 'Контакты', 
            'Дата приема', 'Статус'
        ])
        self.staff_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        layout.addWidget(self.staff_table)
        
        self.tab_widget.addTab(tab, '👥 Управление персоналом')
        self.refresh_staff_table()
    
    def create_funeral_coordination_tab(self):
        """Вкладка координации с ритуальными службами"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Панель инструментов
        toolbar = QHBoxLayout()
        
        btn_new_coordination = QPushButton('➕ Новая координация')
        btn_new_coordination.clicked.connect(self.show_new_coordination_dialog)
        toolbar.addWidget(btn_new_coordination)
        
        btn_refresh = QPushButton('🔄 Обновить')
        btn_refresh.clicked.connect(self.refresh_coordination_table)
        toolbar.addWidget(btn_refresh)
        
        layout.addLayout(toolbar)
        
        # Таблица с координациями
        self.coordination_table = QTableWidget()
        self.coordination_table.setColumnCount(7)
        self.coordination_table.setHorizontalHeaderLabels([
            'ID', 'ID тела', 'Ритуальная служба', 'Контактное лицо', 
            'Запланированная дата', 'Статус', 'Документы'
        ])
        self.coordination_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        layout.addWidget(self.coordination_table)
        
        self.tab_widget.addTab(tab, '⚰️ Координация с ритуальными службами')
        self.refresh_coordination_table()
    
    def create_reports_tab(self):
        """Вкладка отчетов"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Кнопки генерации отчетов
        report_buttons = QGridLayout()
        
        btn_bodies_report = QPushButton('📊 Отчет по телам')
        btn_bodies_report.clicked.connect(self.generate_bodies_report)
        report_buttons.addWidget(btn_bodies_report, 0, 0)
        
        btn_sanitary_report = QPushButton('📋 Отчет по проверкам')
        btn_sanitary_report.clicked.connect(self.generate_sanitary_report)
        report_buttons.addWidget(btn_sanitary_report, 0, 1)
        
        btn_statistics = QPushButton('📈 Общая статистика')
        btn_statistics.clicked.connect(self.show_statistics)
        report_buttons.addWidget(btn_statistics, 1, 0)
        
        btn_daily_report = QPushButton('📅 Ежедневный отчет')
        btn_daily_report.clicked.connect(self.generate_daily_report)
        report_buttons.addWidget(btn_daily_report, 1, 1)
        
        layout.addLayout(report_buttons)
        
        # Область для вывода отчетов
        self.report_text = QTextEdit()
        self.report_text.setReadOnly(True)
        layout.addWidget(self.report_text)
        
        self.tab_widget.addTab(tab, '📄 Отчеты')
    
    def refresh_body_table(self):
        """Обновление таблицы тел"""
        self.body_table.setRowCount(0)
        
        status_filter = self.status_filter.currentText()
        if status_filter == 'Все':
            bodies = self.body_manager.list_bodies()
        else:
            bodies = self.body_manager.list_bodies(status_filter)
        
        for body in bodies:
            row = self.body_table.rowCount()
            self.body_table.insertRow(row)
            
            documents = ', '.join(body.get('documents', []))
            
            self.body_table.setItem(row, 0, QTableWidgetItem(str(body['id'])))
            self.body_table.setItem(row, 1, QTableWidgetItem(body['full_name']))
            self.body_table.setItem(row, 2, QTableWidgetItem(body['arrival_date']))
            self.body_table.setItem(row, 3, QTableWidgetItem(body['source']))
            self.body_table.setItem(row, 4, QTableWidgetItem(body['storage_location']))
            self.body_table.setItem(row, 5, QTableWidgetItem(body['status']))
            self.body_table.setItem(row, 6, QTableWidgetItem(documents))
            self.body_table.setItem(row, 7, QTableWidgetItem(body.get('notes', '')))
        
        self.body_table.resizeColumnsToContents()
        self.statusBar().showMessage(f'Загружено записей: {len(bodies)}')
    
    def refresh_sanitary_table(self):
        """Обновление таблицы санитарных проверок"""
        self.sanitary_table.setRowCount(0)
        
        for check in self.sanitary_control.checks:
            row = self.sanitary_table.rowCount()
            self.sanitary_table.insertRow(row)
            
            violations = str(len(check.get('violations', [])))
            
            self.sanitary_table.setItem(row, 0, QTableWidgetItem(str(check['id'])))
            self.sanitary_table.setItem(row, 1, QTableWidgetItem(check['date']))
            self.sanitary_table.setItem(row, 2, QTableWidgetItem(check['check_type']))
            self.sanitary_table.setItem(row, 3, QTableWidgetItem(str(check['temperature'])))
            self.sanitary_table.setItem(row, 4, QTableWidgetItem(str(check['cleanliness_score'])))
            self.sanitary_table.setItem(row, 5, QTableWidgetItem(check['inspector']))
            self.sanitary_table.setItem(row, 6, QTableWidgetItem(violations))
        
        self.sanitary_table.resizeColumnsToContents()
    
    def refresh_staff_table(self):
        """Обновление таблицы сотрудников"""
        self.staff_table.setRowCount(0)
        
        for employee in self.staff_manager.staff:
            row = self.staff_table.rowCount()
            self.staff_table.insertRow(row)
            
            self.staff_table.setItem(row, 0, QTableWidgetItem(str(employee['id'])))
            self.staff_table.setItem(row, 1, QTableWidgetItem(employee['full_name']))
            self.staff_table.setItem(row, 2, QTableWidgetItem(employee['position']))
            self.staff_table.setItem(row, 3, QTableWidgetItem(employee['contact']))
            self.staff_table.setItem(row, 4, QTableWidgetItem(employee['hire_date']))
            self.staff_table.setItem(row, 5, QTableWidgetItem(employee['status']))
        
        self.staff_table.resizeColumnsToContents()
    
    def refresh_coordination_table(self):
        """Обновление таблицы координаций"""
        self.coordination_table.setRowCount(0)
        
        for coord in self.funeral_coordinator.coordinations:
            row = self.coordination_table.rowCount()
            self.coordination_table.insertRow(row)
            
            docs = ', '.join(coord.get('documents_needed', []))
            
            self.coordination_table.setItem(row, 0, QTableWidgetItem(str(coord['id'])))
            self.coordination_table.setItem(row, 1, QTableWidgetItem(str(coord['body_id'])))
            self.coordination_table.setItem(row, 2, QTableWidgetItem(coord['service_name']))
            self.coordination_table.setItem(row, 3, QTableWidgetItem(coord['contact_person']))
            self.coordination_table.setItem(row, 4, QTableWidgetItem(coord['planned_date']))
            self.coordination_table.setItem(row, 5, QTableWidgetItem(coord['status']))
            self.coordination_table.setItem(row, 6, QTableWidgetItem(docs))
        
        self.coordination_table.resizeColumnsToContents()
    
    def show_new_body_dialog(self):
        """Диалог регистрации нового тела"""
        dialog = QDialog(self)
        dialog.setWindowTitle('Регистрация нового тела')
        dialog.setModal(True)
        dialog.resize(500, 400)
        
        layout = QVBoxLayout(dialog)
        
        # Поля формы
        form_layout = QFormLayout()
        
        self.body_name_input = QLineEdit()
        form_layout.addRow('ФИО:', self.body_name_input)
        
        self.body_arrival_input = QLineEdit()
        self.body_arrival_input.setText(datetime.datetime.now().strftime("%Y-%m-%d"))
        form_layout.addRow('Дата поступления:', self.body_arrival_input)
        
        self.body_source_input = QComboBox()
        self.body_source_input.addItems(['Больница', 'Полиция', 'СК', 'Частное лицо', 'Другое'])
        form_layout.addRow('Источник:', self.body_source_input)
        
        self.body_location_input = QComboBox()
        self.body_location_input.addItems(['Холодильная камера 1', 'Холодильная камера 2', 
                                          'Холодильная камера 3', 'Временное хранение'])
        form_layout.addRow('Место хранения:', self.body_location_input)
        
        self.body_docs_input = QTextEdit()
        self.body_docs_input.setMaximumHeight(80)
        form_layout.addRow('Документы (каждый с новой строки):', self.body_docs_input)
        
        self.body_notes_input = QTextEdit()
        self.body_notes_input.setMaximumHeight(60)
        form_layout.addRow('Примечания:', self.body_notes_input)
        
        layout.addLayout(form_layout)
        
        # Кнопки
        button_layout = QHBoxLayout()
        btn_save = QPushButton('Сохранить')
        btn_save.clicked.connect(lambda: self.save_new_body(dialog))
        btn_cancel = QPushButton('Отмена')
        btn_cancel.clicked.connect(dialog.reject)
        
        button_layout.addWidget(btn_save)
        button_layout.addWidget(btn_cancel)
        layout.addLayout(button_layout)
        
        dialog.exec_()
    
    def save_new_body(self, dialog):
        """Сохранение нового тела"""
        name = self.body_name_input.text().strip()
        arrival = self.body_arrival_input.text().strip()
        source = self.body_source_input.currentText()
        location = self.body_location_input.currentText()
        notes = self.body_notes_input.toPlainText().strip()
        
        docs_text = self.body_docs_input.toPlainText().strip()
        documents = [doc.strip() for doc in docs_text.split('\n') if doc.strip()]
        
        if not name:
            QMessageBox.warning(self, 'Ошибка', 'Поле "ФИО" обязательно для заполнения')
            return
        
        body = self.body_manager.register_body(
            name, arrival, source, location, documents, "поступило"
        )
        
        if body:
            QMessageBox.information(self, 'Успешно', f'Тело зарегистрировано! ID: {body["id"]}')
            dialog.accept()
            self.refresh_body_table()
    
    def edit_body(self):
        """Редактирование статуса тела"""
        selected = self.body_table.selectedItems()
        if not selected:
            QMessageBox.warning(self, 'Внимание', 'Выберите запись для редактирования')
            return
        
        body_id = int(self.body_table.item(selected[0].row(), 0).text())
        body = self.body_manager.get_body_by_id(body_id)
        
        if not body:
            QMessageBox.warning(self, 'Ошибка', 'Запись не найдена')
            return
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f'Редактирование тела ID: {body_id}')
        dialog.setModal(True)
        dialog.resize(400, 300)
        
        layout = QVBoxLayout(dialog)
        
        form_layout = QFormLayout()
        
        # Информация о теле
        info_label = QLabel(f'ФИО: {body["full_name"]}\n'
                           f'Дата поступления: {body["arrival_date"]}\n'
                           f'Текущий статус: {body["status"]}')
        form_layout.addRow('Информация:', info_label)
        
        # Статус
        self.status_combo = QComboBox()
        self.status_combo.addItems(['поступило', 'подготовлено', 'выдано'])
        self.status_combo.setCurrentText(body['status'])
        form_layout.addRow('Новый статус:', self.status_combo)
        
        # Примечания
        self.edit_notes_input = QTextEdit()
        self.edit_notes_input.setPlainText(body.get('notes', ''))
        self.edit_notes_input.setMaximumHeight(100)
        form_layout.addRow('Примечания:', self.edit_notes_input)
        
        layout.addLayout(form_layout)
        
        # Кнопки
        button_layout = QHBoxLayout()
        btn_save = QPushButton('Сохранить')
        btn_save.clicked.connect(lambda: self.save_body_edit(body_id, dialog))
        btn_cancel = QPushButton('Отмена')
        btn_cancel.clicked.connect(dialog.reject)
        
        button_layout.addWidget(btn_save)
        button_layout.addWidget(btn_cancel)
        layout.addLayout(button_layout)
        
        dialog.exec_()
    
    def save_body_edit(self, body_id, dialog):
        """Сохранение изменений тела"""
        new_status = self.status_combo.currentText()
        notes = self.edit_notes_input.toPlainText().strip()
        
        if self.body_manager.update_body_status(body_id, new_status, notes):
            QMessageBox.information(self, 'Успешно', 'Статус обновлен')
            dialog.accept()
            self.refresh_body_table()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Не удалось обновить статус')
    
    def show_new_sanitary_check_dialog(self):
        """Диалог новой санитарной проверки"""
        dialog = QDialog(self)
        dialog.setWindowTitle('Новая санитарная проверка')
        dialog.setModal(True)
        dialog.resize(400, 300)
        
        layout = QVBoxLayout(dialog)
        
        form_layout = QFormLayout()
        
        self.check_type_input = QComboBox()
        self.check_type_input.addItems(['Ежедневная', 'Еженедельная', 'Внеплановая', 'Специальная'])
        form_layout.addRow('Тип проверки:', self.check_type_input)
        
        self.temperature_input = QDoubleSpinBox()
        self.temperature_input.setRange(-10, 30)
        self.temperature_input.setValue(4.0)
        self.temperature_input.setSingleStep(0.5)
        form_layout.addRow('Температура (°C):', self.temperature_input)
        
        self.cleanliness_input = QSpinBox()
        self.cleanliness_input.setRange(1, 10)
        self.cleanliness_input.setValue(8)
        form_layout.addRow('Оценка чистоты (1-10):', self.cleanliness_input)
        
        self.inspector_input = QLineEdit()
        form_layout.addRow('Инспектор:', self.inspector_input)
        
        self.check_notes_input = QTextEdit()
        self.check_notes_input.setMaximumHeight(80)
        form_layout.addRow('Примечания:', self.check_notes_input)
        
        layout.addLayout(form_layout)
        
        button_layout = QHBoxLayout()
        btn_save = QPushButton('Сохранить')
        btn_save.clicked.connect(lambda: self.save_new_check(dialog))
        btn_cancel = QPushButton('Отмена')
        btn_cancel.clicked.connect(dialog.reject)
        
        button_layout.addWidget(btn_save)
        button_layout.addWidget(btn_cancel)
        layout.addLayout(button_layout)
        
        dialog.exec_()
    
    def save_new_check(self, dialog):
        """Сохранение новой проверки"""
        check_type = self.check_type_input.currentText()
        temperature = self.temperature_input.value()
        cleanliness = self.cleanliness_input.value()
        inspector = self.inspector_input.text().strip()
        notes = self.check_notes_input.toPlainText().strip()
        
        if not inspector:
            QMessageBox.warning(self, 'Ошибка', 'Поле "Инспектор" обязательно для заполнения')
            return
        
        check = self.sanitary_control.record_check(
            check_type, temperature, cleanliness, inspector, notes
        )
        
        if check:
            QMessageBox.information(self, 'Успешно', f'Проверка записана! ID: {check["id"]}')
            dialog.accept()
            self.refresh_sanitary_table()
    
    def show_add_violation_dialog(self):
        """Диалог добавления нарушения"""
        selected = self.sanitary_table.selectedItems()
        if not selected:
            QMessageBox.warning(self, 'Внимание', 'Выберите проверку для добавления нарушения')
            return
        
        check_id = int(self.sanitary_table.item(selected[0].row(), 0).text())
        
        dialog = QDialog(self)
        dialog.setWindowTitle(f'Добавление нарушения для проверки ID: {check_id}')
        dialog.setModal(True)
        dialog.resize(400, 200)
        
        layout = QVBoxLayout(dialog)
        
        form_layout = QFormLayout()
        
        self.violation_input = QTextEdit()
        self.violation_input.setMaximumHeight(60)
        form_layout.addRow('Нарушение:', self.violation_input)
        
        self.corrective_action_input = QTextEdit()
        self.corrective_action_input.setMaximumHeight(60)
        form_layout.addRow('Корректирующее действие:', self.corrective_action_input)
        
        layout.addLayout(form_layout)
        
        button_layout = QHBoxLayout()
        btn_save = QPushButton('Сохранить')
        btn_save.clicked.connect(lambda: self.save_violation(check_id, dialog))
        btn_cancel = QPushButton('Отмена')
        btn_cancel.clicked.connect(dialog.reject)
        
        button_layout.addWidget(btn_save)
        button_layout.addWidget(btn_cancel)
        layout.addLayout(button_layout)
        
        dialog.exec_()
    
    def save_violation(self, check_id, dialog):
        """Сохранение нарушения"""
        violation = self.violation_input.toPlainText().strip()
        corrective_action = self.corrective_action_input.toPlainText().strip()
        
        if not violation or not corrective_action:
            QMessageBox.warning(self, 'Ошибка', 'Все поля обязательны для заполнения')
            return
        
        if self.sanitary_control.add_violation(check_id, violation, corrective_action):
            QMessageBox.information(self, 'Успешно', 'Нарушение добавлено')
            dialog.accept()
            self.refresh_sanitary_table()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Не удалось добавить нарушение')
    
    def show_new_employee_dialog(self):
        """Диалог добавления сотрудника"""
        dialog = QDialog(self)
        dialog.setWindowTitle('Новый сотрудник')
        dialog.setModal(True)
        dialog.resize(400, 300)
        
        layout = QVBoxLayout(dialog)
        
        form_layout = QFormLayout()
        
        self.emp_name_input = QLineEdit()
        form_layout.addRow('ФИО:', self.emp_name_input)
        
        self.emp_position_input = QComboBox()
        self.emp_position_input.addItems(['Патологоанатом', 'Санитар', 'Администратор', 
                                         'Водитель', 'Охранник', 'Другое'])
        form_layout.addRow('Должность:', self.emp_position_input)
        
        self.emp_contact_input = QLineEdit()
        form_layout.addRow('Контакты:', self.emp_contact_input)
        
        self.emp_qualifications_input = QTextEdit()
        self.emp_qualifications_input.setMaximumHeight(80)
        form_layout.addRow('Квалификации (каждая с новой строки):', self.emp_qualifications_input)
        
        layout.addLayout(form_layout)
        
        button_layout = QHBoxLayout()
        btn_save = QPushButton('Сохранить')
        btn_save.clicked.connect(lambda: self.save_new_employee(dialog))
        btn_cancel = QPushButton('Отмена')
        btn_cancel.clicked.connect(dialog.reject)
        
        button_layout.addWidget(btn_save)
        button_layout.addWidget(btn_cancel)
        layout.addLayout(button_layout)
        
        dialog.exec_()
    
    def save_new_employee(self, dialog):
        """Сохранение нового сотрудника"""
        name = self.emp_name_input.text().strip()
        position = self.emp_position_input.currentText()
        contact = self.emp_contact_input.text().strip()
        
        quals_text = self.emp_qualifications_input.toPlainText().strip()
        qualifications = [q.strip() for q in quals_text.split('\n') if q.strip()]
        
        if not name or not contact:
            QMessageBox.warning(self, 'Ошибка', 'Поля "ФИО" и "Контакты" обязательны')
            return
        
        employee = self.staff_manager.add_employee(name, position, contact, qualifications)
        
        if employee:
            QMessageBox.information(self, 'Успешно', f'Сотрудник добавлен! ID: {employee["id"]}')
            dialog.accept()
            self.refresh_staff_table()
    
    def show_new_coordination_dialog(self):
        """Диалог новой координации"""
        dialog = QDialog(self)
        dialog.setWindowTitle('Новая координация с ритуальной службой')
        dialog.setModal(True)
        dialog.resize(500, 300)
        
        layout = QVBoxLayout(dialog)
        
        form_layout = QFormLayout()
        
        # ID тела
        self.coord_body_id_input = QSpinBox()
        self.coord_body_id_input.setRange(1, 9999)
        form_layout.addRow('ID тела:', self.coord_body_id_input)
        
        # Ритуальная служба
        self.coord_service_input = QLineEdit()
        form_layout.addRow('Ритуальная служба:', self.coord_service_input)
        
        # Контактное лицо
        self.coord_contact_person_input = QLineEdit()
        form_layout.addRow('Контактное лицо:', self.coord_contact_person_input)
        
        # Телефон
        self.coord_phone_input = QLineEdit()
        form_layout.addRow('Телефон:', self.coord_phone_input)
        
        # Планируемая дата
        self.coord_date_input = QLineEdit()
        self.coord_date_input.setText(datetime.datetime.now().strftime("%Y-%m-%d"))
        form_layout.addRow('Планируемая дата:', self.coord_date_input)
        
        # Необходимые документы
        self.coord_docs_input = QTextEdit()
        self.coord_docs_input.setMaximumHeight(60)
        self.coord_docs_input.setPlainText("Свидетельство о смерти\nПаспорт\nДоверенность")
        form_layout.addRow('Необходимые документы:', self.coord_docs_input)
        
        layout.addLayout(form_layout)
        
        button_layout = QHBoxLayout()
        btn_save = QPushButton('Сохранить')
        btn_save.clicked.connect(lambda: self.save_new_coordination(dialog))
        btn_cancel = QPushButton('Отмена')
        btn_cancel.clicked.connect(dialog.reject)
        
        button_layout.addWidget(btn_save)
        button_layout.addWidget(btn_cancel)
        layout.addLayout(button_layout)
        
        dialog.exec_()
    
    def save_new_coordination(self, dialog):
        """Сохранение новой координации"""
        body_id = self.coord_body_id_input.value()
        service = self.coord_service_input.text().strip()
        contact_person = self.coord_contact_person_input.text().strip()
        phone = self.coord_phone_input.text().strip()
        planned_date = self.coord_date_input.text().strip()
        
        docs_text = self.coord_docs_input.toPlainText().strip()
        documents_needed = [doc.strip() for doc in docs_text.split('\n') if doc.strip()]
        
        if not service or not contact_person or not phone:
            QMessageBox.warning(self, 'Ошибка', 'Заполните все обязательные поля')
            return
        
        # Проверяем, существует ли тело с таким ID
        body = self.body_manager.get_body_by_id(body_id)
        if not body:
            QMessageBox.warning(self, 'Ошибка', f'Тело с ID {body_id} не найдено')
            return
        
        coordination = self.funeral_coordinator.register_coordination(
            body_id, service, contact_person, phone, planned_date, documents_needed
        )
        
        if coordination:
            QMessageBox.information(self, 'Успешно', f'Координация зарегистрирована! ID: {coordination["id"]}')
            dialog.accept()
            self.refresh_coordination_table()
    
    def generate_bodies_report(self):
        """Генерация отчета по телам"""
        bodies = self.body_manager.list_bodies()
        
        report = "📊 ОТЧЕТ ПО ТЕЛАМ\n"
        report += "=" * 50 + "\n\n"
        
        report += f"Всего тел в системе: {len(bodies)}\n"
        report += f"Дата генерации: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        # Статистика по статусам
        statuses = {}
        for body in bodies:
            status = body['status']
            statuses[status] = statuses.get(status, 0) + 1
        
        report += "📈 СТАТИСТИКА ПО СТАТУСАМ:\n"
        for status, count in statuses.items():
            report += f"  • {status}: {count} тел\n"
        
        report += "\n📋 ПОСЛЕДНИЕ 10 ПОСТУПЛЕНИЙ:\n"
        recent_bodies = sorted(bodies, key=lambda x: x.get('registration_date', ''), reverse=True)[:10]
        
        for body in recent_bodies:
            report += f"\nID: {body['id']}\n"
            report += f"  ФИО: {body['full_name']}\n"
            report += f"  Дата поступления: {body['arrival_date']}\n"
            report += f"  Статус: {body['status']}\n"
            report += f"  Место хранения: {body['storage_location']}\n"
        
        self.report_text.setPlainText(report)
        self.tab_widget.setCurrentIndex(4)  # Переход на вкладку отчетов
    
    def generate_sanitary_report(self):
        """Генерация отчета по санитарным проверкам"""
        checks = self.sanitary_control.checks
        
        report = "🧼 ОТЧЕТ ПО САНИТАРНЫМ ПРОВЕРКАМ\n"
        report += "=" * 50 + "\n\n"
        
        report += f"Всего проверок: {len(checks)}\n"
        report += f"Дата генерации: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        # Последние 10 проверок
        recent_checks = sorted(checks, key=lambda x: x['date'], reverse=True)[:10]
        
        report += "📋 ПОСЛЕДНИЕ 10 ПРОВЕРОК:\n"
        for check in recent_checks:
            report += f"\nID: {check['id']}\n"
            report += f"  Дата: {check['date']}\n"
            report += f"  Тип: {check['check_type']}\n"
            report += f"  Температура: {check['temperature']}°C\n"
            report += f"  Оценка чистоты: {check['cleanliness_score']}/10\n"
            report += f"  Инспектор: {check['inspector']}\n"
            report += f"  Нарушений: {len(check.get('violations', []))}\n"
        
        # Статистика по нарушениям
        total_violations = sum(len(check.get('violations', [])) for check in checks)
        report += f"\n⚠️ ВСЕГО НАРУШЕНИЙ: {total_violations}\n"
        
        self.report_text.setPlainText(report)
        self.tab_widget.setCurrentIndex(4)
    
    def show_statistics(self):
        """Показать общую статистику"""
        bodies_count = len(self.body_manager.bodies)
        checks_count = len(self.sanitary_control.checks)
        staff_count = len(self.staff_manager.staff)
        coord_count = len(self.funeral_coordinator.coordinations)
        
        # Статистика по статусам тел
        status_stats = {}
        for body in self.body_manager.bodies:
            status = body['status']
            status_stats[status] = status_stats.get(status, 0) + 1
        
        report = "📈 ОБЩАЯ СТАТИСТИКА\n"
        report += "=" * 50 + "\n\n"
        
        report += f"📊 ОСНОВНЫЕ ПОКАЗАТЕЛИ:\n"
        report += f"  • Зарегистрировано тел: {bodies_count}\n"
        report += f"  • Проведено санитарных проверок: {checks_count}\n"
        report += f"  • Сотрудников в системе: {staff_count}\n"
        report += f"  • Координаций с ритуальными службами: {coord_count}\n\n"
        
        report += "📋 СТАТУСЫ ТЕЛ:\n"
        for status, count in status_stats.items():
            percentage = (count / bodies_count * 100) if bodies_count > 0 else 0
            report += f"  • {status}: {count} ({percentage:.1f}%)\n"
        
        report += f"\n📅 СИСТЕМА АКТИВНА С: {self.get_system_start_date()}\n"
        
        self.report_text.setPlainText(report)
        self.tab_widget.setCurrentIndex(4)
    
    def generate_daily_report(self):
        """Генерация ежедневного отчета"""
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Тела, поступившие сегодня
        todays_bodies = [b for b in self.body_manager.bodies 
                        if b['arrival_date'].startswith(today)]
        
        # Проверки за сегодня
        todays_checks = [c for c in self.sanitary_control.checks 
                        if c['date'].startswith(today)]
        
        report = f"📅 ЕЖЕДНЕВНЫЙ ОТЧЕТ НА {today}\n"
        report += "=" * 50 + "\n\n"
        
        report += f"📊 СВОДКА ЗА ДЕНЬ:\n"
        report += f"  • Поступило тел: {len(todays_bodies)}\n"
        report += f"  • Проведено проверок: {len(todays_checks)}\n\n"
        
        if todays_bodies:
            report += "📋 ТЕЛА, ПОСТУПИВШИЕ СЕГОДНЯ:\n"
            for body in todays_bodies:
                report += f"  • ID: {body['id']}, ФИО: {body['full_name']}, Источник: {body['source']}\n"
        else:
            report += "📋 ТЕЛА, ПОСТУПИВШИЕ СЕГОДНЯ: нет\n"
        
        if todays_checks:
            report += "\n🧼 ПРОВЕРКИ ЗА СЕГОДНЯ:\n"
            for check in todays_checks:
                violations = len(check.get('violations', []))
                report += f"  • {check['date'][11:]}, Тип: {check['check_type']}, Нарушений: {violations}\n"
        
        self.report_text.setPlainText(report)
        self.tab_widget.setCurrentIndex(4)
    
    def get_system_start_date(self):
        """Получение даты начала работы системы"""
        dates = []
        
        if self.body_manager.bodies:
            dates.extend([b.get('registration_date', '') for b in self.body_manager.bodies])
        if self.sanitary_control.checks:
            dates.extend([c['date'] for c in self.sanitary_control.checks])
        
        if dates:
            valid_dates = [d for d in dates if d]
            if valid_dates:
                return min(valid_dates)[:10]
        
        return datetime.datetime.now().strftime("%Y-%m-%d")
    
    def create_test_data(self):
        """Создание тестовых данных при первом запуске"""
        if not os.path.exists("bodies.json"):
            # Тестовые тела
            test_bodies = [
                {
                    "full_name": "Иванов Иван Иванович",
                    "arrival_date": "2024-01-15",
                    "source": "Городская больница №1",
                    "storage_location": "Холодильная камера 3",
                    "documents": ["Направление из больницы", "Паспорт"],
                    "status": "поступило"
                },
                {
                    "full_name": "Петров Петр Петрович",
                    "arrival_date": "2024-01-14",
                    "source": "Полиция",
                    "storage_location": "Холодильная камера 2",
                    "documents": ["Протокол осмотра", "Паспорт"],
                    "status": "подготовлено"
                }
            ]
            
            for body_data in test_bodies:
                self.body_manager.register_body(**body_data)
            
            # Тестовая проверка
            self.sanitary_control.record_check(
                "Ежедневная", 4.5, 8, "Сидоров А.И.", "Все в норме"
            )
            
            # Тестовый сотрудник
            self.staff_manager.add_employee(
                "Смирнов Алексей Владимирович",
                "Патологоанатом",
                "+7-999-123-45-67",
                ["Высшая категория", "Стаж 15 лет"]
            )
            
            QMessageBox.information(self, 'Тестовые данные', 
                                  'Созданы тестовые данные для демонстрации работы системы')
            self.refresh_body_table()
            self.refresh_sanitary_table()
            self.refresh_staff_table()

def main():
    """Запуск приложения"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # Установка иконки приложения
    app.setWindowIcon(QIcon.fromTheme('applications-science'))
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()