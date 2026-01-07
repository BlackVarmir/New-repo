#!/usr/bin/env python3
"""
Speech to Text Program
Программа для преобразования речи в текст

Поддерживает:
- Распознавание речи с микрофона в реальном времени
- Распознавание речи из аудио файлов (WAV, FLAC, MP3)
- Поддержка множества языков (русский, английский и др.)
"""

import speech_recognition as sr
import argparse
import sys
from pathlib import Path


class SpeechToText:
    """Класс для работы с распознаванием речи"""

    def __init__(self, language='ru-RU'):
        """
        Инициализация распознавателя речи

        Args:
            language: Язык распознавания (по умолчанию ru-RU для русского)
        """
        self.recognizer = sr.Recognizer()
        self.language = language

    def recognize_from_microphone(self, duration=None):
        """
        Распознавание речи с микрофона

        Args:
            duration: Длительность записи в секундах (None = до тишины)

        Returns:
            str: Распознанный текст
        """
        with sr.Microphone() as source:
            print("Настройка микрофона на фоновый шум...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Говорите...")

            try:
                if duration:
                    audio = self.recognizer.record(source, duration=duration)
                else:
                    audio = self.recognizer.listen(source)

                print("Распознавание...")
                text = self.recognizer.recognize_google(audio, language=self.language)
                return text

            except sr.WaitTimeoutError:
                return "Ошибка: Превышено время ожидания"
            except sr.UnknownValueError:
                return "Ошибка: Не удалось распознать речь"
            except sr.RequestError as e:
                return f"Ошибка сервиса распознавания: {e}"

    def recognize_from_file(self, audio_file):
        """
        Распознавание речи из аудио файла

        Args:
            audio_file: Путь к аудио файлу (WAV, FLAC, MP3)

        Returns:
            str: Распознанный текст
        """
        audio_path = Path(audio_file)

        if not audio_path.exists():
            return f"Ошибка: Файл {audio_file} не найден"

        # Проверка формата файла
        supported_formats = ['.wav', '.flac', '.mp3']
        if audio_path.suffix.lower() not in supported_formats:
            return f"Ошибка: Поддерживаются только форматы: {', '.join(supported_formats)}"

        try:
            # Для MP3 требуется конвертация через pydub
            if audio_path.suffix.lower() == '.mp3':
                try:
                    from pydub import AudioSegment
                    sound = AudioSegment.from_mp3(audio_file)
                    sound.export("/tmp/temp.wav", format="wav")
                    audio_file = "/tmp/temp.wav"
                except ImportError:
                    return "Ошибка: Для работы с MP3 установите: pip install pydub ffmpeg-python"

            with sr.AudioFile(audio_file) as source:
                print(f"Загрузка аудио файла: {audio_path.name}")
                audio = self.recognizer.record(source)

                print("Распознавание...")
                text = self.recognizer.recognize_google(audio, language=self.language)
                return text

        except sr.UnknownValueError:
            return "Ошибка: Не удалось распознать речь"
        except sr.RequestError as e:
            return f"Ошибка сервиса распознавания: {e}"
        except Exception as e:
            return f"Ошибка: {e}"


def main():
    """Основная функция программы"""
    parser = argparse.ArgumentParser(
        description='Speech to Text - Программа распознавания речи',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  %(prog)s -m                    # Распознавание с микрофона (русский язык)
  %(prog)s -m -l en-US           # Распознавание с микрофона (английский язык)
  %(prog)s -f audio.wav          # Распознавание из файла
  %(prog)s -f audio.mp3 -l en-US # Распознавание из MP3 файла (английский)

Поддерживаемые языки:
  ru-RU - Русский
  en-US - Английский (США)
  en-GB - Английский (Великобритания)
  de-DE - Немецкий
  fr-FR - Французский
  es-ES - Испанский
  и другие...
        """
    )

    # Выбор источника
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument('-m', '--microphone', action='store_true',
                            help='Распознавание речи с микрофона')
    source_group.add_argument('-f', '--file', type=str,
                            help='Путь к аудио файлу (WAV, FLAC, MP3)')

    # Параметры
    parser.add_argument('-l', '--language', type=str, default='ru-RU',
                      help='Язык распознавания (по умолчанию: ru-RU)')
    parser.add_argument('-d', '--duration', type=int, default=None,
                      help='Длительность записи с микрофона в секундах')
    parser.add_argument('-o', '--output', type=str, default=None,
                      help='Сохранить результат в файл')

    args = parser.parse_args()

    # Создание объекта распознавания
    stt = SpeechToText(language=args.language)

    # Выполнение распознавания
    if args.microphone:
        result = stt.recognize_from_microphone(duration=args.duration)
    else:
        result = stt.recognize_from_file(args.file)

    # Вывод результата
    print("\n" + "="*50)
    print("РЕЗУЛЬТАТ:")
    print("="*50)
    print(result)
    print("="*50 + "\n")

    # Сохранение в файл если указано
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"Результат сохранен в файл: {args.output}")
        except Exception as e:
            print(f"Ошибка при сохранении в файл: {e}", file=sys.stderr)
            return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
