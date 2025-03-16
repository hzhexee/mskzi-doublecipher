def text_prep(text):
    """
    Подготавливает текст для шифра Плейфера:
    - Заменяет 'Ё' на 'Е'
    - Делает все буквы заглавными
    - Возвращает строку в формате: ключевое слово + оставшиеся буквы алфавита
    
    Args:
        text (str): Ключевое слово или фраза
    
    Returns:
        str: Форматированная строка для создания матрицы Плейфера
    """
    # Заменяем 'Ё' на 'Е' и делаем все буквы заглавными
    text = text.upper().replace('Ё', 'Е')
    
    # Создаем русский алфавит без 'Ё'
    alphabet = 'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
    
    # Удаляем повторяющиеся буквы из ключа
    key = ''
    for char in text:
        if char in alphabet and char not in key:
            key += char
    
    # Добавляем оставшиеся буквы алфавита, которых нет в ключе
    for char in alphabet:
        if char not in key:
            key += char
            
    return key

def ciphertext_prep(text):
    text = text.upper().replace('Ё', 'Е')
    text = text.replace(' ', '')
    return text  # Добавлен возврат результата

def bigramm_split(text):
    text = ciphertext_prep(text)
    
    # Сначала обрабатываем повторяющиеся символы
    processed_text = ""
    i = 0
    while i < len(text):
        processed_text += text[i]
        # Если текущий символ совпадает со следующим, добавляем 'Х'
        if i < len(text) - 1 and text[i] == text[i + 1]:
            processed_text += 'Х'
        i += 1
    
    # Теперь добавляем 'Х' в конец, если количество букв нечетное
    if len(processed_text) % 2 != 0:
        processed_text += 'Х'
    
    # Разбиваем на биграммы
    bigramms = []
    for i in range(0, len(processed_text), 2):
        bigramms.append(processed_text[i:i+2])
            
    return bigramms

def bigramm_plaintext(text):
    """
    Преобразует список биграмм в единую текстовую строку с пробелами между биграммами.
    
    Args:
        bigramms (list): Список биграмм ['АБ', 'ВГ', ...]
    
    Returns:
        str: Строка с пробелами между биграммами
    """
    bigramms = bigramm_split(text)
    
    # Объединяем все биграммы в строку с пробелами
    text = ' '.join(bigramms)
    
    return text

def playfair_matrix(text):
    """
    Создает матрицу Плейфера из ключа.
    
    Args:
        text (str): Ключевое слово или фраза
    
    Returns:
        list: Матрица Плейфера
    """
    key = text_prep(text)
    
    # Создаем пустую матрицу 4x8
    matrix = [['' for _ in range(8)] for _ in range(4)]
    
    # Заполняем матрицу буквами из ключа
    i, j = 0, 0
    for char in key:
        matrix[i][j] = char
        j += 1
        if j == 8:  # Изменено с 5 на 8 для соответствия размеру матрицы
            j = 0
            i += 1
    
    return matrix

# test_text = 'Плейфер'
# test_key = text_prep(test_text)
# print(test_key)
# print(playfair_matrix(test_key))

def playfair_encrypt(plaintext, key):
    """
    Шифрует текст методом Плейфера.
    
    Args:
        plaintext (str): Текст для шифрования
        key (str): Ключевое слово или фраза
    
    Returns:
        str: Зашифрованный текст
    """
    # Создаем матрицу Плейфера
    matrix = playfair_matrix(key)
    
    # Разбиваем текст на биграммы
    bigrams = bigramm_split(plaintext)
    
    encrypted_bigrams = []
    
    for bigram in bigrams:
        # Находим позиции букв в матрице
        positions = []
        for char in bigram:
            found = False
            for i in range(4):
                for j in range(8):
                    if matrix[i][j] == char:
                        positions.append((i, j))
                        found = True
                        break
                if found:
                    break
            
            # Если символ не найден в матрице, выведем отладочную информацию
            if not found:
                print(f"Символ '{char}' не найден в матрице!")
                # Используем первый символ матрицы как замену
                positions.append((0, 0))
        
        # Проверяем, что у нас есть обе позиции
        if len(positions) < 2:
            print(f"Предупреждение: для биграммы '{bigram}' найдено меньше 2 позиций")
            continue
            
        row1, col1 = positions[0]
        row2, col2 = positions[1]
        
        # Применяем правила шифрования
        if row1 == row2:  # Буквы в одной строке
            encrypted_bigrams.append(matrix[row1][(col1 + 1) % 8] + matrix[row2][(col2 + 1) % 8])
        elif col1 == col2:  # Буквы в одном столбце
            encrypted_bigrams.append(matrix[(row1 + 1) % 4][col1] + matrix[(row2 + 1) % 4][col2])
        else:  # Буквы образуют прямоугольник
            encrypted_bigrams.append(matrix[row1][col2] + matrix[row2][col1])
    
    # Объединяем зашифрованные биграммы
    return ' '.join(encrypted_bigrams)

# test_text = "ЕХАЛ ГРЕКА ЧЕРЕЗ РЕКУ"
# test_key = "ПЛЕЙФЕР"

# # Отладочный вывод для проверки
# print("Матрица Плейфера:")
# matrix = playfair_matrix(test_key)
# for row in matrix:
#     print(row)
    
# print("\nБиграммы:")
# bigrams = bigramm_split(test_text)
# print(bigrams)

# # Затем вызывайте функцию шифрования
# print("\nРезультат шифрования:")
# print(playfair_encrypt(test_text, test_key))