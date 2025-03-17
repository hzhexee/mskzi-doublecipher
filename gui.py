import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QTextEdit, 
                            QMenuBar, QMenu, QMessageBox, QGridLayout, QScrollArea, QSizePolicy)
from PyQt6.QtCore import Qt, QTimer  # Add QTimer here
from PyQt6.QtGui import QFont
from playfair_func import text_prep

class PlayfairDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_step = 0
        self.total_steps = 4
        # Создаем более крупный шрифт для использования в приложении
        self.button_font = QFont()
        self.button_font.setPointSize(12)  # Увеличиваем размер шрифта
        
        # Определяем размеры матрицы как константы класса
        self.matrix_rows = 4
        self.matrix_cols = 8
        
        # Добавляем переменные для хранения данных
        self.key = ""                # Исходный ключ
        self.processed_key = ""      # Обработанный ключ
        self.matrix = None           # Матрица Плейфера
        self.plaintext = ""          # Исходный текст
        self.bigrams = []            # Биграммы
        self.matrix_cells = []       # Ссылки на ячейки матрицы для подсветки
        
        self.initUI()
        
    def initUI(self):
        # Set window properties
        self.setWindowTitle('Шифр Плейфера - Демонстрация')
        self.setGeometry(300, 300, 900, 700)  # Увеличиваем размер окна
        
        # Create central widget and layout
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create input field for key with label
        input_layout = QVBoxLayout()
        key_label = QLabel("Введите слово-ключ:")
        key_label.setFont(self.button_font)  # Увеличиваем шрифт метки
        self.input_text = QTextEdit()
        self.input_text.setFixedHeight(90)  # Увеличиваем высоту поля ввода
        self.input_text.setFont(self.button_font)  # Увеличиваем шрифт текста
        
        # Create a layout for key input area
        key_input_layout = QVBoxLayout()
        key_input_layout.addWidget(key_label)
        key_input_layout.addWidget(self.input_text)
        
        # Add encrypt button
        self.encrypt_btn = QPushButton("Создать таблицу")
        self.encrypt_btn.setFont(self.button_font)  # Увеличиваем шрифт кнопки
        self.encrypt_btn.setMinimumHeight(40)  # Увеличиваем высоту кнопки
        self.encrypt_btn.clicked.connect(self.encrypt_text)
        key_input_layout.addWidget(self.encrypt_btn)
        
        # Create a container for the key input layout
        key_container = QWidget()
        key_container.setLayout(key_input_layout)
        self.key_container = key_container
        
        input_layout.addWidget(key_container)
        
        # Create second input field for text to encrypt (initially hidden)
        self.encrypt_layout = QVBoxLayout()
        encrypt_label = QLabel("Введите текст для шифрования:")
        encrypt_label.setFont(self.button_font)  # Увеличиваем шрифт метки
        self.encrypt_input = QTextEdit()
        self.encrypt_input.setFixedHeight(90)  # Увеличиваем высоту поля ввода
        self.encrypt_input.setFont(self.button_font)  # Увеличиваем шрифт текста
        self.process_btn = QPushButton("Обработать текст")
        self.process_btn.setFont(self.button_font)  # Увеличиваем шрифт кнопки
        self.process_btn.setMinimumHeight(40)  # Увеличиваем высоту кнопки
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
        
        # Добавляем растягивающийся элемент, чтобы прижать все виджеты вверх
        input_layout.addStretch(1)
        
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
        
        # Make the scroll area expand to fill available space
        scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        main_layout.addWidget(scroll_area, 1)  # Add stretch factor of 1
        
        # Create step navigation buttons
        nav_layout = QHBoxLayout()
        self.prev_btn = QPushButton("Предыдущий шаг")
        self.prev_btn.setFont(self.button_font)  # Увеличиваем шрифт кнопки
        self.prev_btn.setMinimumHeight(50)  # Увеличиваем высоту кнопки
        self.prev_btn.clicked.connect(self.previous_step)
        self.prev_btn.setEnabled(False)
        
        self.next_btn = QPushButton("Следующий шаг")
        self.next_btn.setFont(self.button_font)  # Увеличиваем шрифт кнопки
        self.next_btn.setMinimumHeight(50)  # Увеличиваем высоту кнопки
        self.next_btn.clicked.connect(self.next_step)
        
        self.step_label = QLabel("Шаг 1 из 4")
        self.step_label.setFont(self.button_font)  # Увеличиваем шрифт метки
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
        
        # Сбрасываем сохраненные переменные
        self.key = ""
        self.processed_key = ""
        self.matrix = None
        self.plaintext = ""
        self.bigrams = []
        
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
            self.key_container.setVisible(False)  # Hide key input on step 2
        else:
            self.encrypt_container.setVisible(False)
            self.key_container.setVisible(True)  # Show key input on other steps
        
        # Create a text display for the content
        text_display = QTextEdit()
        text_display.setReadOnly(True)
        text_display.setFont(self.button_font)  # Увеличиваем шрифт текста вывода
        text_display.setMinimumHeight(300)  # Увеличиваем минимальную высоту области вывода
        
        # Show different content based on current step
        if self.current_step == 0:
            text_display.setPlainText(
                "Шаг 1: Создание таблицы шифрования\n\n"
                "В этом шаге создается таблица 4x8 на основе ключевого слова.\n"
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
            if self.matrix and self.bigrams:
                # Clear display and set up for animation
                self.reset_demo_display()
                
                # Create step header
                step_header = QLabel("Шаг 3: Шифрование биграмм")
                step_header.setFont(self.button_font)
                self.display_layout.addWidget(step_header)
                
                # Add explanation
                explanation = QLabel(
                    "Каждая пара букв шифруется по правилам:\n"
                    "1. Если буквы в одной строке, берутся буквы справа от каждой\n"
                    "2. Если буквы в одном столбце, берутся буквы снизу от каждой\n"
                    "3. Иначе, буквы на пересечении строк и столбцов исходных букв\n"
                    "В анимации синим отображаются исходные символы, а зеленым - зашифрованные."
                )
                explanation.setFont(self.button_font)
                explanation.setWordWrap(True)
                self.display_layout.addWidget(explanation)
                
                # Display the matrix
                matrix_label = QLabel("Матрица шифрования:")
                matrix_label.setFont(self.button_font)
                self.display_layout.addWidget(matrix_label)
                
                # Create matrix display
                matrix_widget = QWidget()
                grid_layout = QGridLayout(matrix_widget)
                grid_layout.setSpacing(10)

                # Сохраняем матрицу ячеек для подсветки
                self.matrix_cells = []
                for row in range(self.matrix_rows):
                    row_cells = []
                    for col in range(self.matrix_cols):
                        char_label = QLabel("")
                        char_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        char_label.setStyleSheet("border: 2px solid black; padding: 8px; font-weight: bold; font-size: 18px;")
                        char_label.setMinimumSize(40, 40)
                        grid_layout.addWidget(char_label, row, col)
                        row_cells.append(char_label)
                    self.matrix_cells.append(row_cells)

                # Fill grid with characters
                char_index = 0
                for row in range(self.matrix_rows):
                    for col in range(self.matrix_cols):
                        if char_index < len(self.processed_key):
                            self.matrix_cells[row][col].setText(self.processed_key[char_index])
                            char_index += 1
                
                self.display_layout.addWidget(matrix_widget)
                
                # Create animation area
                animation_label = QLabel("Анимация шифрования:")
                animation_label.setFont(self.button_font)
                self.display_layout.addWidget(animation_label)
                
                # Widget to show encryption progress
                self.encryption_display = QTextEdit()
                self.encryption_display.setReadOnly(True)
                self.encryption_display.setFont(self.button_font)
                self.encryption_display.setMinimumHeight(150)
                self.display_layout.addWidget(self.encryption_display)
                
                # Calculate full encrypted text
                from playfair_func import playfair_encrypt
                self.encrypted_text = playfair_encrypt(self.plaintext, self.key)
                
                # Start animation
                self.current_bigram_index = 0
                self.encrypted_bigrams = []
                self.animate_encryption()
            else:
                text_display = QTextEdit()
                text_display.setReadOnly(True)
                text_display.setFont(self.button_font)
                text_display.setPlainText(
                    "Шаг 3: Шифрование биграмм\n\n"
                    "Пожалуйста, сначала заполните данные на шагах 1 и 2."
                )
                self.display_layout.addWidget(text_display)
        elif self.current_step == 3:
            if self.matrix and self.bigrams:
                from playfair_func import playfair_encrypt
                encrypted_text = playfair_encrypt(self.plaintext, self.key)
                
                text_display.setPlainText(
                    "Шаг 4: Результат шифрования\n\n"
                    f"Ключевое слово: {self.key}\n"
                    f"Исходный текст: {self.plaintext}\n"
                    f"Зашифрованный текст: {encrypted_text}"
                )
            else:
                text_display.setPlainText(
                    "Шаг 4: Результат шифрования\n\n"
                    "Пожалуйста, сначала заполните данные на шагах 1 и 2."
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
            
        # Сохраняем исходный ключ
        self.key = text
        
        # Process the text using text_prep
        self.processed_key = text_prep(text)
        
        # Создаем и сохраняем матрицу
        from playfair_func import playfair_matrix
        self.matrix = playfair_matrix(text)
        
        # Create a 4x8 matrix representation
        matrix_rows = 4
        matrix_cols = 8
        
        # Display the processed text info
        info_label = QLabel(f"Обработанный текст: {self.processed_key}")
        info_label.setFont(self.button_font)  # Увеличиваем шрифт информационной метки
        info_label.setWordWrap(True)
        self.display_layout.addWidget(info_label)
        
        # Create a grid layout for the matrix
        matrix_widget = QWidget()
        grid_layout = QGridLayout(matrix_widget)
        grid_layout.setSpacing(10)  # Увеличиваем интервалы между ячейками
        
        # Fill the grid with characters
        char_index = 0
        for row in range(matrix_rows):
            for col in range(matrix_cols):
                if char_index < len(self.processed_key):
                    # Create a label for each character
                    char_label = QLabel(self.processed_key[char_index])
                    char_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    char_label.setStyleSheet("border: 2px solid black; padding: 8px; font-weight: bold; font-size: 18px;")
                    char_label.setMinimumSize(40, 40)  # Увеличиваем размер ячеек
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
            
        # Сохраняем исходный текст
        self.plaintext = text
        
        # Process with bigramm_plaintext and save bigrams
        from playfair_func import bigramm_split
        self.bigrams = bigramm_split(text)
        processed_text = " ".join(self.bigrams)
        
        # Create text display
        text_display = QTextEdit()
        text_display.setReadOnly(True)
        text_display.setPlainText(
            "Шаг 2: Подготовка текста\n\n"
            "Текст разбивается на биграммы (пары букв).\n"
            "Если в паре оказываются одинаковые буквы, между ними вставляется 'Х'.\n"
            "Если количество букв нечетное, в конец добавляется 'Х'.\n\n"
            f"Исходный текст: {self.plaintext}\n"
            f"Текст в биграммах: {processed_text}"
        )
        
        # Add to the display layout
        self.display_layout.addWidget(text_display)

    def animate_encryption(self):
        """Animate the encryption process for each bigram"""
        from PyQt6.QtCore import QTimer
        
        if self.current_bigram_index < len(self.bigrams):
            # Сбросить предыдущие подсветки
            self.reset_highlights()
            
            # Get current bigram
            current_bigram = self.bigrams[self.current_bigram_index]
            
            # Compute the encrypted version of the current bigram
            # Очистим зашифрованный текст от пробелов перед разбиением на биграммы
            clean_encrypted_text = ''.join(self.encrypted_text.split())
            encrypted_bigrams_list = [clean_encrypted_text[i:i+2] for i in range(0, len(clean_encrypted_text), 2)]
            
            if self.current_bigram_index < len(encrypted_bigrams_list):
                encrypted_bigram = encrypted_bigrams_list[self.current_bigram_index]
            else:
                encrypted_bigram = "??"  # На случай ошибки
            
            # Add to encrypted bigrams list
            self.encrypted_bigrams.append(encrypted_bigram)
            
            # Подсвечиваем исходные символы белым
            for char in current_bigram:
                pos = self.find_char_position(char)
                if pos:
                    self.highlight_cell(pos[0], pos[1], "blue")
            
            # Подсвечиваем зашифрованные символы зеленым
            for char in encrypted_bigram:
                pos = self.find_char_position(char)
                if pos:
                    self.highlight_cell(pos[0], pos[1], "green")
            
            # Display the current animation step
            progress_text = (
                f"Шифрование биграммы {self.current_bigram_index + 1} из {len(self.bigrams)}:\n\n"
                f"Текущая биграмма: {current_bigram}\n"
                f"Зашифрованная биграмма: {encrypted_bigram}\n\n"
                f"Прогресс шифрования:\n"
                f"Исходные биграммы: {' '.join(self.bigrams[:self.current_bigram_index + 1])}"
            )
            
            if self.encrypted_bigrams:
                progress_text += f"\nЗашифрованные биграммы: {' '.join(self.encrypted_bigrams)}"
            
            self.encryption_display.setPlainText(progress_text)
            
            # Move to next bigram after delay
            self.current_bigram_index += 1
            QTimer.singleShot(2000, self.animate_encryption)  # 2-second delay
        else:
            # Завершение анимации - сбросим подсветку
            self.reset_highlights()
            
            # Animation complete
            self.encryption_display.setPlainText(
                "Шифрование завершено!\n\n"
                f"Исходные биграммы: {' '.join(self.bigrams)}\n"
                f"Зашифрованные биграммы: {' '.join(self.encrypted_bigrams)}\n"
                f"Зашифрованный текст (слитно): {''.join(self.encrypted_bigrams)}"
            )

    def find_char_position(self, char):
        """Найти позицию символа в матрице"""
        if not self.processed_key or not self.matrix_cells:
            return None
            
        for row in range(len(self.matrix_cells)):
            for col in range(len(self.matrix_cells[row])):
                if self.matrix_cells[row][col].text() == char:
                    return (row, col)
        return None

    def highlight_cell(self, row, col, color):
        """Подсветить ячейку определенным цветом"""
        if 0 <= row < len(self.matrix_cells) and 0 <= col < len(self.matrix_cells[row]):
            self.matrix_cells[row][col].setStyleSheet(
                f"border: 2px solid black; padding: 8px; font-weight: bold; "
                f"font-size: 18px; background-color: {color};"
            )

    def reset_highlights(self):
        """Сбросить все подсветки"""
        for row in range(len(self.matrix_cells)):
            for col in range(len(self.matrix_cells[row])):
                if self.matrix_cells[row][col].text():  # Если ячейка не пуста
                    self.matrix_cells[row][col].setStyleSheet(
                        "border: 2px solid black; padding: 8px; font-weight: bold; font-size: 18px;"
                    )

def main():
    app = QApplication(sys.argv)
    window = PlayfairDemo()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
