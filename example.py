#!/usr/bin/env python3
"""
Примеры использования модуля speech2text
"""

from speech2text import SpeechToText


def example_microphone():
    """Пример: распознавание с микрофона"""
    print("=== Пример 1: Распознавание с микрофона ===\n")

    # Создаем объект для русского языка
    stt = SpeechToText(language='ru-RU')

    # Распознаем речь с микрофона
    print("Говорите что-нибудь...")
    text = stt.recognize_from_microphone()

    print(f"\nВы сказали: {text}\n")


def example_file():
    """Пример: распознавание из файла"""
    print("=== Пример 2: Распознавание из файла ===\n")

    # Создаем объект для английского языка
    stt = SpeechToText(language='en-US')

    # Укажите путь к вашему аудио файлу
    audio_file = 'test_audio.wav'

    print(f"Распознавание файла: {audio_file}")
    text = stt.recognize_from_file(audio_file)

    print(f"\nРезультат: {text}\n")


def example_multilingual():
    """Пример: распознавание на разных языках"""
    print("=== Пример 3: Многоязычное распознавание ===\n")

    languages = {
        'ru-RU': 'Русский',
        'en-US': 'Английский',
        'de-DE': 'Немецкий'
    }

    for lang_code, lang_name in languages.items():
        print(f"\nГоворите на языке: {lang_name}")
        stt = SpeechToText(language=lang_code)
        text = stt.recognize_from_microphone(duration=5)  # 5 секунд
        print(f"Распознано ({lang_name}): {text}")


def example_save_to_file():
    """Пример: сохранение результата в файл"""
    print("=== Пример 4: Сохранение результата в файл ===\n")

    stt = SpeechToText(language='ru-RU')

    print("Говорите...")
    text = stt.recognize_from_microphone()

    # Сохраняем результат
    output_file = 'recognized_text.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"\nРезультат сохранен в файл: {output_file}")
    print(f"Текст: {text}\n")


def example_continuous_recognition():
    """Пример: непрерывное распознавание"""
    print("=== Пример 5: Непрерывное распознавание ===\n")

    stt = SpeechToText(language='ru-RU')

    print("Непрерывное распознавание (скажите 'стоп' для завершения)\n")

    while True:
        print("Слушаю...")
        text = stt.recognize_from_microphone()

        print(f"Распознано: {text}")

        # Проверяем команду завершения
        if 'стоп' in text.lower() or 'stop' in text.lower():
            print("\nЗавершение работы...")
            break


if __name__ == '__main__':
    import sys

    examples = {
        '1': ('Распознавание с микрофона', example_microphone),
        '2': ('Распознавание из файла', example_file),
        '3': ('Многоязычное распознавание', example_multilingual),
        '4': ('Сохранение в файл', example_save_to_file),
        '5': ('Непрерывное распознавание', example_continuous_recognition),
    }

    print("Выберите пример для запуска:")
    for key, (description, _) in examples.items():
        print(f"  {key}. {description}")
    print("  0. Выход")

    choice = input("\nВведите номер примера: ").strip()

    if choice == '0':
        print("До свидания!")
        sys.exit(0)

    if choice in examples:
        _, example_func = examples[choice]
        try:
            example_func()
        except KeyboardInterrupt:
            print("\n\nПрервано пользователем")
            sys.exit(0)
        except Exception as e:
            print(f"\nОшибка: {e}")
            sys.exit(1)
    else:
        print("Неверный выбор!")
        sys.exit(1)
