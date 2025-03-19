import random
import re
import math

def sanitize_text(text):
    """
    Подготавливает текст для шифрования:
    - Заменяет 'Ё' на 'Е'
    - Делает все буквы заглавными
    - Удаляет все специальные символы (оставляет только буквы)

    Args:
        text (str): Ключевое слово или фраза
    
    Returns:
        str: Форматированная строка
    """
    # Сначала сделаем текст заглавным и заменим 'Ё' на 'Е'
    text = text.upper().replace('Ё', 'Е')
    
    # Удалим все символы, кроме букв (латинских и кириллических)
    text = re.sub(r'[^A-ZА-Я]', '', text)
    
    return text


def transpose_text(text, key):
    """Выполняет перестановку символов текста по ключу"""
    num_cols = len(key)
    num_rows = math.ceil(len(text) / num_cols)
    matrix = [[''] * num_cols for _ in range(num_rows)]

    # Заполняем матрицу по строкам
    idx = 0
    for r in range(num_rows):
        for c in range(num_cols):
            if idx < len(text):
                matrix[r][c] = text[idx]
                idx += 1

    # Считываем столбцы в порядке ключа
    sorted_indices = sorted(range(len(key)), key=lambda x: key[x])
    ciphertext = ''.join(matrix[r][c] for c in sorted_indices for r in range(num_rows))
    return ciphertext, matrix, sorted_indices

def create_permutation_key(keyword):
    """Создает порядок перестановки на основе ключевого слова"""
    sorted_chars = sorted(list(set(keyword)))  # Убираем дубликаты, сортируем
    return [sorted_chars.index(c) for c in keyword]

def format_matrix(matrix, key_len):
    """
    Форматирует матрицу для визуального представления.
    
    Args:
        matrix (list): Двумерный список символов
        key_len (int): Длина ключа (количество столбцов)
    
    Returns:
        str: Отформатированная строка матрицы
    """
    result = []
    
    # Добавляем заголовок с номерами столбцов
    header = '   | ' + ' '.join(f"{i+1:^3}" for i in range(key_len))
    result.append(header)
    
    # Добавляем разделительную линию
    separator = '---+' + '----' * key_len
    result.append(separator)
    
    # Добавляем строки матрицы
    for i, row in enumerate(matrix):
        # Дополняем ряд пустыми строками, если он короче длины ключа
        while len(row) < key_len:
            row.append(' ')
        row_str = f"{i+1:2} | " + ' '.join(f"{c:^3}" for c in row)
        result.append(row_str)
    
    return '\n'.join(result)

def visualize_double_transposition(text, key1, key2):
    """
    Визуализирует процесс шифрования методом двойной перестановки.
    
    Args:
        text (str): Текст для шифрования
        key1 (str): Первый ключ
        key2 (str): Второй ключ
    
    Returns:
        str: Текстовое представление процесса шифрования
    """
    result = []
    
    key1_perm = create_permutation_key(key1)
    key2_perm = create_permutation_key(key2)
    
    result.append(f"Исходный текст: {text}")
    result.append(f"Первый ключ: {key1}")
    result.append(f"Второй ключ: {key2}\n")
    
    # Показываем перестановки ключей
    result.append(f"Перестановка для первого ключа:")
    result.append(f"Символы ключа:  {' '.join(key1)}")
    result.append(f"Индексы ключа:  {' '.join(str(i) for i in key1_perm)}\n")
    
    result.append(f"Перестановка для второго ключа:")
    result.append(f"Символы ключа:  {' '.join(key2)}")
    result.append(f"Индексы ключа:  {' '.join(str(i) for i in key2_perm)}\n")
    
    # Первая перестановка
    intermediate, matrix1, sorted_indices1 = transpose_text(text, key1_perm)
    
    # Визуализируем исходную матрицу
    result.append("Исходная матрица (заполнение по строкам):")
    result.append(format_matrix(matrix1, len(key1_perm)))
    
    # Визуализируем порядок считывания столбцов
    result.append("\nПорядок считывания столбцов:")
    result.append(f"Исходные индексы:  {' '.join(str(i+1) for i in range(len(key1_perm)))}")
    result.append(f"Порядок считывания: {' '.join(str(i+1) for i in sorted_indices1)}\n")
    
    result.append(f"Результат первой перестановки: {intermediate}\n")
    
    # Вторая перестановка
    num_cols2 = len(key2_perm)
    num_rows2 = math.ceil(len(intermediate) / num_cols2)
    
    # Создаем матрицу для второй перестановки
    matrix2 = [[''] * num_cols2 for _ in range(num_rows2)]
    idx = 0
    for r in range(num_rows2):
        for c in range(num_cols2):
            if idx < len(intermediate):
                matrix2[r][c] = intermediate[idx]
                idx += 1
    
    result.append("Матрица для второй перестановки:")
    result.append(format_matrix(matrix2, len(key2_perm)))
    
    # Получаем финальный шифртекст и индексы перестановки
    ciphertext, _, sorted_indices2 = transpose_text(intermediate, key2_perm)
    
    # Визуализируем порядок считывания столбцов для второй перестановки
    result.append("\nПорядок считывания столбцов (вторая перестановка):")
    result.append(f"Исходные индексы:  {' '.join(str(i+1) for i in range(len(key2_perm)))}")
    result.append(f"Порядок считывания: {' '.join(str(i+1) for i in sorted_indices2)}\n")
    
    result.append(f"Результат двойной перестановки: {ciphertext}")
    
    return '\n'.join(result)

def dt_resultOnly(text, key1, key2):
    key1_perm = create_permutation_key(key1)
    key2_perm = create_permutation_key(key2)
    
    intermediate, _, _ = transpose_text(text, key1_perm)
    
    num_cols2 = len(key2_perm)
    num_rows2 = math.ceil(len(intermediate) / num_cols2)
    
    matrix2 = [[''] * num_cols2 for _ in range(num_rows2)]
    idx = 0
    for r in range(num_rows2):
        for c in range(num_cols2):
            if idx < len(intermediate):
                matrix2[r][c] = intermediate[idx]
                idx += 1
    
    ciphertext, _, _ = transpose_text(intermediate, key2_perm)
    
    return ciphertext

# Test input
plaintext = "АБВГДЕЙКА"
key1 = "КЛЮЧ"
key2 = "СЕКРЕТ"
ciphertext = dt_resultOnly(plaintext, key1, key2)
print(ciphertext)