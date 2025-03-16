import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QTextEdit, 
                            QMenuBar, QMenu, QMessageBox, QGridLayout, QScrollArea)
from PyQt6.QtCore import Qt
from playfair_func import text_prep, bigramm_plaintext

class PlayfairDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_step = 0
        self.total_steps = 4
        self.initUI()
        
    def initUI(self):
        # Set window properties
        self.setWindowTitle('Шифр Плейфера - Демонстрация')
        self.setGeometry(300, 300, 800, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create input field for key with label
        input_layout = QVBoxLayout()
        key_label = QLabel("Введите слово-ключ:")
        self.input_text = QTextEdit()
        input_layout.addWidget(key_label)
        input_layout.addWidget(self.input_text)
        
        # Add encrypt button
        self.encrypt_btn = QPushButton("Создать таблицу")
        self.encrypt_btn.clicked.connect(self.encrypt_text)
        input_layout.addWidget(self.encrypt_btn)
        
        # Create second input field for text to encrypt (initially hidden)
        self.encrypt_layout = QVBoxLayout()
        encrypt_label = QLabel("Введите текст для шифрования:")
        self.encrypt_input = QTextEdit()
        self.process_btn = QPushButton("Обработать текст")
        self.process_btn.clicked.connect(self.process_text)
        
        self.encrypt_layout.addWidget(encrypt_label)
        self.encrypt_layout.addWidget(self.encrypt_input)
        self.encrypt_layout.addWidget(self.process_btn)
        
        # Create a container for the encrypt layout
        encrypt_container = QWidget()
        encrypt_container.setLayout(self.encrypt_layout)
        encrypt_container.setVisible(False)
        self.encrypt_container = encrypt_container
        
        input_layout.addWidget(encrypt_container)
        main_layout.addLayout(input_layout)
        
        # Create demo display area - use a scrollable widget container instead of just a QTextEdit
        display_widget = QWidget()
        self.display_layout = QVBoxLayout(display_widget)
        
        # Create a scroll area to contain the display widget
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(display_widget)
        
        # Store references
        self.display_widget = display_widget
        self.demo_display = scroll_area
        
        main_layout.addWidget(scroll_area)
        
        # Create step navigation buttons
        nav_layout = QHBoxLayout()
        self.prev_btn = QPushButton("Предыдущий шаг")
        self.prev_btn.clicked.connect(self.previous_step)
        self.prev_btn.setEnabled(False)
        
        self.next_btn = QPushButton("Следующий шаг")
        self.next_btn.clicked.connect(self.next_step)
        
        self.step_label = QLabel("Шаг 1 из 4")
        self.step_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        nav_layout.addWidget(self.prev_btn)
        nav_layout.addWidget(self.step_label)
        nav_layout.addWidget(self.next_btn)
        
        main_layout.addLayout(nav_layout)
        
        # Set the central widget
        self.setCentralWidget(central_widget)
        
        # Initial display
        self.update_display()
    
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # Menu menu
        menu_menu = menubar.addMenu("Меню")
        
        # Add actions to Menu
        new_action = menu_menu.addAction("Новый")
        new_action.triggered.connect(self.new_demo)
        
        exit_action = menu_menu.addAction("Выход")
        exit_action.triggered.connect(self.close)
        
        # Help menu
        help_menu = menubar.addMenu("Справка")
        
        # Add actions to Help
        about_action = help_menu.addAction("О программе")
        about_action.triggered.connect(self.show_about)
        
        help_action = help_menu.addAction("Помощь")
        help_action.triggered.connect(self.show_help)
    
    def new_demo(self):
        self.input_text.clear()
        self.encrypt_input.clear()  # Clear the encryption input as well
        self.current_step = 0
        self.update_display()
        self.prev_btn.setEnabled(False)
        self.next_btn.setEnabled(True)
    
    def show_about(self):
        QMessageBox.information(
            self,
            "О программе",
            "Демонстрация работы шифра Плейфера\n"
            "Учебный проект\n"
            "© 2023"
        )
    
    def show_help(self):
        QMessageBox.information(
            self,
            "Помощь",
            "Шифр Плейфера — ручная симметричная техника шифрования, использующая биграммы.\n\n"
            "Пошаговая демонстрация:\n"
            "1. Создание таблицы шифрования\n"
            "2. Подготовка текста\n"
            "3. Шифрование биграмм\n"
            "4. Результат шифрования"
        )
    
    def next_step(self):
        if self.current_step < self.total_steps - 1:
            self.current_step += 1
            self.update_display()
            self.prev_btn.setEnabled(True)
            if self.current_step == self.total_steps - 1:
                self.next_btn.setEnabled(False)
    
    def previous_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.update_display()
            self.next_btn.setEnabled(True)
            if self.current_step == 0:
                self.prev_btn.setEnabled(False)
    
    def reset_demo_display(self):
        """Reset the demo display to its original state without custom layouts"""
        # Clear the current layout
        while self.display_layout.count():
            item = self.display_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def update_display(self):
        # Reset the demo display first to ensure we can set text
        self.reset_demo_display()
        
        self.step_label.setText(f"Шаг {self.current_step + 1} из {self.total_steps}")
        
        # Show/hide appropriate input fields based on step
        if self.current_step == 1:  # Step 2
            self.encrypt_container.setVisible(True)
        else:
            self.encrypt_container.setVisible(False)
        
        # Get the input text
        text = self.input_text.toPlainText()
        
        # Create a text display for the content
        text_display = QTextEdit()
        text_display.setReadOnly(True)
        
        # Show different content based on current step
        if self.current_step == 0:
            text_display.setPlainText(
                "Шаг 1: Создание таблицы шифрования\n\n"
                "В этом шаге создается таблица 5x5 на основе ключевого слова.\n"
                "Буквы Е и Ё обычно объединяются в одну ячейку.\n\n"
                "Пример таблицы будет показан здесь."
            )
        elif self.current_step == 1:
            text_display.setPlainText(
                "Шаг 2: Подготовка текста\n\n"
                "Текст разбивается на биграммы (пары букв).\n"
                "Если в паре оказываются одинаковые буквы, между ними вставляется 'Х'.\n"
                "Если количество букв нечетное, в конец добавляется 'Х'.\n\n"
                "Используйте поле ввода выше для обработки текста."
            )
        elif self.current_step == 2:
            text_display.setPlainText(
                "Шаг 3: Шифрование биграмм\n\n"
                "Каждая пара букв шифруется по правилам:\n"
                "1. Если буквы в одной строке, берутся буквы справа от каждой\n"
                "2. Если буквы в одном столбце, берутся буквы снизу от каждой\n"
                "3. Иначе, буквы на пересечении строк и столбцов исходных букв\n\n"
                "Процесс шифрования будет показан здесь."
            )
        elif self.current_step == 3:
            text_display.setPlainText(
                "Шаг 4: Результат шифрования\n\n"
                f"Исходный текст: {text}\n"
                "Зашифрованный текст будет показан здесь."
            )
        
        # Add the text display to the layout
        self.display_layout.addWidget(text_display)
    
    def encrypt_text(self):
        # Reset the demo display first
        self.reset_demo_display()
        
        # Get input text
        text = self.input_text.toPlainText()
        if not text:
            QMessageBox.warning(self, "Предупреждение", "Введите текст для шифрования!")
            return
            
        # Process the text using text_prep
        processed_text = text_prep(text)
        
        # Create a 4x8 matrix representation
        matrix_rows = 4
        matrix_cols = 8
        
        # Display the processed text info
        info_label = QLabel(f"Обработанный текст: {processed_text}")
        info_label.setWordWrap(True)
        self.display_layout.addWidget(info_label)
        
        # Create a grid layout for the matrix
        matrix_widget = QWidget()
        grid_layout = QGridLayout(matrix_widget)
        grid_layout.setSpacing(5)
        
        # Fill the grid with characters
        char_index = 0
        for row in range(matrix_rows):
            for col in range(matrix_cols):
                if char_index < len(processed_text):
                    # Create a label for each character
                    char_label = QLabel(processed_text[char_index])
                    char_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    char_label.setStyleSheet("border: 1px solid black; padding: 5px; font-weight: bold; font-size: 14px;")
                    char_label.setMinimumSize(30, 30)
                    grid_layout.addWidget(char_label, row, col)
                    char_index += 1
        
        # Add the matrix widget to the display layout
        self.display_layout.addWidget(matrix_widget)
    
    def process_text(self):
        """Process the text to encrypt using bigramm_plaintext"""
        # Reset the demo display first
        self.reset_demo_display()
        
        # Get the text to encrypt
        text = self.encrypt_input.toPlainText()
        if not text:
            QMessageBox.warning(self, "Предупреждение", "Введите текст для шифрования!")
            return
            
        # Process with bigramm_plaintext
        processed_text = bigramm_plaintext(text)
        
        # Create text display
        text_display = QTextEdit()
        text_display.setReadOnly(True)
        text_display.setPlainText(
            "Шаг 2: Подготовка текста\n\n"
            "Текст разбивается на биграммы (пары букв).\n"
            "Если в паре оказываются одинаковые буквы, между ними вставляется 'Х'.\n"
            "Если количество букв нечетное, в конец добавляется 'Х'.\n\n"
            f"Исходный текст: {text}\n"
            f"Текст в биграммах: {processed_text}"
        )
        
        # Add to the display layout
        self.display_layout.addWidget(text_display)


def main():
    app = QApplication(sys.argv)
    window = PlayfairDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
