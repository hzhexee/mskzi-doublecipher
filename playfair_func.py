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
    
    # Добавляем 'Х' в конец, если количество букв нечетное
    if len(text) % 2 != 0:
        text += 'Х'
    
    bigramms = []
    i = 0
    
    while i < len(text):
        # Если текущий символ совпадает со следующим
        if i < len(text) - 1 and text[i] == text[i + 1]:
            bigramms.append(text[i] + 'Х')
            i += 1
        else:
            bigramms.append(text[i:i+2])
            i += 2
            
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
