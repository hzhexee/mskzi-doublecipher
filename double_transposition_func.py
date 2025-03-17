import random

def text_prep(text):
    """
    Подготавливает текст для шифрования:
    - Заменяет 'Ё' на 'Е'
    - Делает все буквы заглавными

    Args:
        text (str): Ключевое слово или фраза
    
    Returns:
        str: Форматированная строка
    """
    # Заменяем 'Ё' на 'Е' и делаем все буквы заглавными
    return text.upper().replace('Ё', 'Е')


def double_transposition_encrypt(plaintext, key1, key2):
    """
    Шифрует текст методом двойной перестановки.
    
    Args:
        plaintext (str): Текст для шифрования
        key1 (str): Первый ключ
        key2 (str): Второй ключ
    
    Returns:
        str: Зашифрованный текст
    """
    # Подготовка текста
    text = text_prep(plaintext)
    
    # Подготовка ключей
    key1 = text_prep(key1)
    key2 = text_prep(key2)
    
    # Определение размеров матрицы
    cols = len(key1)
    rows = len(key2)
    
    # Вычисляем общий размер матрицы
    matrix_size = cols * rows
    
    # Список специальных символов для заполнения
    special_chars = ['@', '#', '$', '%', '&', '*', '!', '?', '+', '=', '<', '>', '^', '~']
    
    # Дополняем текст, если его длина меньше размера матрицы
    if len(text) < matrix_size:
        padding_length = matrix_size - len(text)
        padding = ''.join(random.choice(special_chars) for _ in range(padding_length))
        text += padding
    
    # Создаем исходную матрицу, заполняя ее по строкам
    matrix = []
    for i in range(0, len(text), cols):
        row = text[i:i+cols]
        # Дополняем последнюю строку, если она неполная
        if len(row) < cols:
            padding_length = cols - len(row)
            padding = ''.join(random.choice(special_chars) for _ in range(padding_length))
            row += padding
        matrix.append(list(row))
    
    # Создаем матрицу перестановки для каждого ключа
    permutation1 = get_key_permutation(key1)

    permutation2 = get_key_permutation(key2)
    
        
    
def get_key_permutation(key):
    """
    Возвращает список индексов перестановки для заданного ключа.
    
    Args:
        key (str): Ключ для перестановки
    
    Returns:
        list: Список с индексами исходных позиций в порядке сортировки
    """
    # Создаем список пар (символ, позиция)
    indexed_key = [(char, i) for i, char in enumerate(key, 1)]
    
    # Сортируем по символам
    sorted_indexed_key = sorted(indexed_key, key=lambda x: x[0])
    
    # Извлекаем исходные позиции в новом порядке
    permutation = [orig_pos for _, orig_pos in sorted_indexed_key]
    
    return permutation


# Тест шифрования
plaintext = 'АБВГДЕЙКА'
key1 = 'КЛЮЧ'
key2 = 'секрет'
ciphertext = double_transposition_encrypt(plaintext, key1, key2)
print(ciphertext)  # Ожидаемый результат: 'ЙГКАБДВЕА'