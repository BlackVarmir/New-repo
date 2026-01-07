# Speech to Text (Speech2Text)

Программа для преобразования речи в текст на Python с поддержкой множества языков.

## 🚀 Два способа использования

### 1. 🤖 Telegram Bot (Рекомендуется)
**Самый простой способ!** Используйте готового Telegram бота для распознавания голосовых сообщений.

👉 **[Инструкция по запуску Telegram бота](BOT_README.md)**

**Быстрый старт:**
```bash
# 1. Получите токен у @BotFather в Telegram
# 2. Создайте .env файл
cp .env.example .env
# 3. Добавьте токен в .env
# 4. Запустите бота
./run_bot.sh
```

### 2. 💻 Консольная программа
Используйте программу через командную строку для распознавания с микрофона или из файлов.

---

## Возможности

- 🎤 Распознавание речи с микрофона в реальном времени
- 📁 Распознавание речи из аудио файлов (WAV, FLAC, MP3)
- 🤖 **Telegram бот** для удобного использования
- 🌍 Поддержка множества языков (русский, английский, немецкий и др.)
- 💾 Сохранение результатов в текстовый файл
- 🆓 Использует бесплатный Google Speech Recognition API

## Установка

### 1. Установка Python зависимостей

```bash
pip install -r requirements.txt
```

### 2. Установка системных зависимостей

#### На Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install portaudio19-dev python3-pyaudio ffmpeg
```

#### На macOS:
```bash
brew install portaudio ffmpeg
```

#### На Windows:
- Скачайте и установите [FFmpeg](https://ffmpeg.org/download.html)
- PyAudio может потребовать установки через wheel файл

## Использование

### Распознавание с микрофона

Распознавание на русском языке (по умолчанию):
```bash
python speech2text.py -m
```

Распознавание на английском языке:
```bash
python speech2text.py -m -l en-US
```

Запись с ограничением по времени (10 секунд):
```bash
python speech2text.py -m -d 10
```

### Распознавание из файла

Распознавание из WAV файла:
```bash
python speech2text.py -f audio.wav
```

Распознавание из MP3 файла на английском:
```bash
python speech2text.py -f audio.mp3 -l en-US
```

### Сохранение результата в файл

```bash
python speech2text.py -m -o result.txt
python speech2text.py -f audio.wav -o result.txt
```

## Параметры командной строки

```
-m, --microphone          Распознавание речи с микрофона
-f, --file FILE           Путь к аудио файлу (WAV, FLAC, MP3)
-l, --language LANG       Язык распознавания (по умолчанию: ru-RU)
-d, --duration SECONDS    Длительность записи с микрофона в секундах
-o, --output FILE         Сохранить результат в файл
```

## Поддерживаемые языки

| Код языка | Язык |
|-----------|------|
| `ru-RU` | Русский |
| `en-US` | Английский (США) |
| `en-GB` | Английский (Великобритания) |
| `de-DE` | Немецкий |
| `fr-FR` | Французский |
| `es-ES` | Испанский |
| `it-IT` | Итальянский |
| `ja-JP` | Японский |
| `zh-CN` | Китайский (упрощенный) |
| `ko-KR` | Корейский |

Полный список языков доступен в [документации Google Cloud Speech-to-Text](https://cloud.google.com/speech-to-text/docs/languages).

## Примеры использования

### Пример 1: Быстрое распознавание с микрофона
```bash
# Говорите после сообщения "Говорите..."
python speech2text.py -m
```

### Пример 2: Транскрипция аудио файла
```bash
# Распознать русскую речь из файла и сохранить результат
python speech2text.py -f interview.wav -o transcript.txt
```

### Пример 3: Многоязычное распознавание
```bash
# Английский
python speech2text.py -m -l en-US -o english.txt

# Немецкий
python speech2text.py -m -l de-DE -o german.txt
```

## Использование в коде Python

```python
from speech2text import SpeechToText

# Создание объекта распознавания
stt = SpeechToText(language='ru-RU')

# Распознавание с микрофона
text = stt.recognize_from_microphone()
print(text)

# Распознавание из файла
text = stt.recognize_from_file('audio.wav')
print(text)
```

## Решение проблем

### Ошибка: "No module named 'pyaudio'"
Установите PyAudio:
```bash
# Ubuntu/Debian
sudo apt-get install python3-pyaudio

# Или через pip
pip install pyaudio
```

### Ошибка: "ALSA lib ... Unknown PCM" (Linux)
Это предупреждение ALSA, можно игнорировать или настроить ALSA конфигурацию.

### Микрофон не работает
Проверьте, что микрофон подключен и работает:
```bash
# Linux
arecord -l

# Проверьте права доступа к микрофону
```

### Ошибка при работе с MP3
Убедитесь, что установлены pydub и ffmpeg:
```bash
pip install pydub
# И установите ffmpeg как указано выше
```

## Требования

- Python 3.6+
- Интернет соединение (для Google Speech Recognition API)
- Микрофон (для распознавания в реальном времени)

## 📁 Структура проекта

```
.
├── speech2text.py          # Основная программа для командной строки
├── telegram_bot.py         # Telegram бот
├── example.py              # Примеры использования
├── run_bot.sh              # Скрипт запуска бота
├── requirements.txt        # Python зависимости
├── .env.example            # Пример конфигурации
├── README.md               # Основная документация
└── BOT_README.md           # Документация по Telegram боту
```

## 🔗 Полезные ссылки

- 📖 [Документация Telegram бота](BOT_README.md)
- 🤖 [Создание бота в Telegram](https://core.telegram.org/bots#6-botfather)
- 🗣️ [Google Speech Recognition API](https://cloud.google.com/speech-to-text)
- 📚 [Поддерживаемые языки](https://cloud.google.com/speech-to-text/docs/languages)

## Лицензия

MIT License

## Автор

Created with Claude AI Assistant
