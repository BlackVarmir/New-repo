#!/usr/bin/env python3
"""
Telegram Bot для распознавания речи (Speech to Text)

Бот принимает голосовые сообщения и аудио файлы,
распознает речь и отправляет текст обратно пользователю.
"""

import os
import sys
import logging
import tempfile
from pathlib import Path
import speech_recognition as sr
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
from telegram.constants import ChatAction

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Доступные языки для распознавания
LANGUAGES = {
    'ru': {'name': '🇷🇺 Русский', 'code': 'ru-RU'},
    'en': {'name': '🇺🇸 English', 'code': 'en-US'},
    'de': {'name': '🇩🇪 Deutsch', 'code': 'de-DE'},
    'fr': {'name': '🇫🇷 Français', 'code': 'fr-FR'},
    'es': {'name': '🇪🇸 Español', 'code': 'es-ES'},
    'it': {'name': '🇮🇹 Italiano', 'code': 'it-IT'},
    'pt': {'name': '🇧🇷 Português', 'code': 'pt-BR'},
    'ja': {'name': '🇯🇵 日本語', 'code': 'ja-JP'},
    'zh': {'name': '🇨🇳 中文', 'code': 'zh-CN'},
    'ko': {'name': '🇰🇷 한국어', 'code': 'ko-KR'},
}

# Директория для временных файлов (кросс-платформенная)
TEMP_DIR = Path(tempfile.gettempdir()) / 'telegram_speech2text'
TEMP_DIR.mkdir(parents=True, exist_ok=True)


class SpeechRecognitionBot:
    """Класс для работы телеграм бота"""

    def __init__(self, token: str):
        """
        Инициализация бота

        Args:
            token: Токен телеграм бота
        """
        self.token = token
        self.recognizer = sr.Recognizer()
        # Хранилище языков пользователей (в реальном проекте использовать БД)
        self.user_languages = {}

    def get_user_language(self, user_id: int) -> str:
        """Получить язык пользователя (по умолчанию русский)"""
        return self.user_languages.get(user_id, 'ru-RU')

    def set_user_language(self, user_id: int, language: str):
        """Установить язык пользователя"""
        self.user_languages[user_id] = language

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user = update.effective_user
        welcome_message = f"""
👋 Привет, {user.first_name}!

Я бот для распознавания речи. Отправь мне:
🎤 Голосовое сообщение
🎵 Аудио файл (MP3, WAV, FLAC)

И я преобразую его в текст!

📝 Доступные команды:
/start - Начать работу
/help - Помощь
/language - Выбрать язык распознавания

🌍 Текущий язык: {LANGUAGES.get(self.get_user_language(user.id)[:2], {}).get('name', 'Русский')}
        """
        await update.message.reply_text(welcome_message)

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help"""
        help_message = """
📖 **Инструкция по использованию**

**Как использовать:**
1️⃣ Отправьте голосовое сообщение в чат
2️⃣ Или отправьте аудио файл
3️⃣ Дождитесь распознавания
4️⃣ Получите текст!

**Поддерживаемые форматы:**
• Голосовые сообщения Telegram (OGG)
• MP3
• WAV
• FLAC

**Команды:**
/start - Начать работу с ботом
/help - Показать эту справку
/language - Выбрать язык распознавания

**Поддерживаемые языки:**
🇷🇺 Русский
🇺🇸 Английский
🇩🇪 Немецкий
🇫🇷 Французский
🇪🇸 Испанский
🇮🇹 Итальянский
🇧🇷 Португальский
🇯🇵 Японский
🇨🇳 Китайский
🇰🇷 Корейский

**Советы:**
✅ Говорите четко и не слишком быстро
✅ Избегайте фонового шума
✅ Оптимальная длина записи: 3-30 секунд

❓ Вопросы? Напишите разработчику!
        """
        await update.message.reply_text(help_message, parse_mode='Markdown')

    async def language_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /language - показать клавиатуру выбора языка"""
        keyboard = []
        # Создаем клавиатуру с языками (по 2 кнопки в ряд)
        lang_items = list(LANGUAGES.items())
        for i in range(0, len(lang_items), 2):
            row = []
            for j in range(2):
                if i + j < len(lang_items):
                    lang_key, lang_data = lang_items[i + j]
                    row.append(
                        InlineKeyboardButton(
                            lang_data['name'],
                            callback_data=f"lang_{lang_key}"
                        )
                    )
            keyboard.append(row)

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            '🌍 Выберите язык для распознавания речи:',
            reply_markup=reply_markup
        )

    async def language_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик выбора языка из клавиатуры"""
        query = update.callback_query
        await query.answer()

        # Получаем выбранный язык
        lang_key = query.data.replace('lang_', '')

        if lang_key in LANGUAGES:
            user_id = update.effective_user.id
            lang_code = LANGUAGES[lang_key]['code']
            lang_name = LANGUAGES[lang_key]['name']

            self.set_user_language(user_id, lang_code)

            await query.edit_message_text(
                f'✅ Язык распознавания изменен на: {lang_name}\n\n'
                f'Теперь отправьте голосовое сообщение или аудио файл!'
            )
        else:
            await query.edit_message_text('❌ Ошибка выбора языка')

    async def recognize_audio(self, audio_path: str, language: str) -> str:
        """
        Распознавание речи из аудио файла

        Args:
            audio_path: Путь к аудио файлу
            language: Код языка для распознавания

        Returns:
            str: Распознанный текст или сообщение об ошибке
        """
        try:
            # Конвертация в WAV если нужно
            file_path = Path(audio_path)
            if file_path.suffix.lower() in ['.ogg', '.mp3', '.m4a']:
                try:
                    from pydub import AudioSegment
                    # Определяем формат
                    if file_path.suffix.lower() == '.ogg':
                        audio = AudioSegment.from_ogg(audio_path)
                    elif file_path.suffix.lower() == '.mp3':
                        audio = AudioSegment.from_mp3(audio_path)
                    else:
                        audio = AudioSegment.from_file(audio_path)

                    # Конвертируем в WAV
                    wav_path = file_path.with_suffix('.wav')
                    audio.export(str(wav_path), format='wav')
                    audio_path = str(wav_path)
                except Exception as e:
                    logger.error(f"Error converting audio: {e}")
                    return f"❌ Ошибка конвертации аудио: {str(e)}"

            # Распознавание
            with sr.AudioFile(audio_path) as source:
                audio_data = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio_data, language=language)
                return text

        except sr.UnknownValueError:
            return "❌ Не удалось распознать речь. Попробуйте говорить четче или выберите другой язык."
        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {e}")
            return f"❌ Ошибка сервиса распознавания: {str(e)}"
        except Exception as e:
            logger.error(f"Recognition error: {e}")
            return f"❌ Ошибка: {str(e)}"

    async def handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик голосовых сообщений"""
        user = update.effective_user
        language = self.get_user_language(user.id)

        # Отправляем статус "печатает..."
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action=ChatAction.TYPING
        )

        try:
            # Скачиваем голосовое сообщение
            voice = update.message.voice
            file = await context.bot.get_file(voice.file_id)

            # Сохраняем временно
            file_path = TEMP_DIR / f"{user.id}_{voice.file_id}.ogg"
            await file.download_to_drive(file_path)

            logger.info(f"User {user.id} sent voice message, language: {language}")

            # Сообщаем о начале распознавания
            status_msg = await update.message.reply_text(
                "🎤 Распознаю голосовое сообщение..."
            )

            # Распознаем
            text = await self.recognize_audio(str(file_path), language)

            # Удаляем статусное сообщение
            await status_msg.delete()

            # Отправляем результат
            if text.startswith('❌'):
                await update.message.reply_text(text)
            else:
                response = f"📝 **Распознанный текст:**\n\n{text}"
                await update.message.reply_text(response, parse_mode='Markdown')

            # Удаляем временные файлы
            file_path.unlink(missing_ok=True)
            file_path.with_suffix('.wav').unlink(missing_ok=True)

        except Exception as e:
            logger.error(f"Error handling voice message: {e}")
            await update.message.reply_text(
                f"❌ Произошла ошибка при обработке голосового сообщения:\n{str(e)}"
            )

    async def handle_audio(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик аудио файлов"""
        user = update.effective_user
        language = self.get_user_language(user.id)

        # Отправляем статус "печатает..."
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action=ChatAction.TYPING
        )

        try:
            # Скачиваем аудио файл
            audio = update.message.audio
            file = await context.bot.get_file(audio.file_id)

            # Определяем расширение
            file_name = audio.file_name or f"audio_{audio.file_id}"
            file_path = TEMP_DIR / f"{user.id}_{file_name}"

            await file.download_to_drive(file_path)

            logger.info(f"User {user.id} sent audio file: {file_name}, language: {language}")

            # Сообщаем о начале распознавания
            status_msg = await update.message.reply_text(
                f"🎵 Распознаю аудио файл `{file_name}`...",
                parse_mode='Markdown'
            )

            # Распознаем
            text = await self.recognize_audio(str(file_path), language)

            # Удаляем статусное сообщение
            await status_msg.delete()

            # Отправляем результат
            if text.startswith('❌'):
                await update.message.reply_text(text)
            else:
                response = f"📝 **Распознанный текст:**\n\n{text}"
                await update.message.reply_text(response, parse_mode='Markdown')

            # Удаляем временные файлы
            file_path.unlink(missing_ok=True)
            file_path.with_suffix('.wav').unlink(missing_ok=True)

        except Exception as e:
            logger.error(f"Error handling audio file: {e}")
            await update.message.reply_text(
                f"❌ Произошла ошибка при обработке аудио файла:\n{str(e)}"
            )

    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик документов (для аудио файлов отправленных как документы)"""
        document = update.message.document

        # Проверяем, что это аудио файл
        audio_extensions = ['.mp3', '.wav', '.flac', '.ogg', '.m4a', '.aac']
        file_name = document.file_name or ''

        if not any(file_name.lower().endswith(ext) for ext in audio_extensions):
            await update.message.reply_text(
                "❌ Пожалуйста, отправьте аудио файл с расширением: MP3, WAV, FLAC, OGG, M4A"
            )
            return

        # Обрабатываем как аудио
        user = update.effective_user
        language = self.get_user_language(user.id)

        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id,
            action=ChatAction.TYPING
        )

        try:
            file = await context.bot.get_file(document.file_id)
            file_path = TEMP_DIR / f"{user.id}_{file_name}"
            await file.download_to_drive(file_path)

            logger.info(f"User {user.id} sent audio document: {file_name}, language: {language}")

            status_msg = await update.message.reply_text(
                f"🎵 Распознаю аудио файл `{file_name}`...",
                parse_mode='Markdown'
            )

            text = await self.recognize_audio(str(file_path), language)

            await status_msg.delete()

            if text.startswith('❌'):
                await update.message.reply_text(text)
            else:
                response = f"📝 **Распознанный текст:**\n\n{text}"
                await update.message.reply_text(response, parse_mode='Markdown')

            file_path.unlink(missing_ok=True)
            file_path.with_suffix('.wav').unlink(missing_ok=True)

        except Exception as e:
            logger.error(f"Error handling audio document: {e}")
            await update.message.reply_text(
                f"❌ Произошла ошибка при обработке файла:\n{str(e)}"
            )

    def run(self):
        """Запуск бота"""
        logger.info("Starting Speech Recognition Bot...")

        # Создаем приложение
        application = Application.builder().token(self.token).build()

        # Регистрируем обработчики команд
        application.add_handler(CommandHandler("start", self.start_command))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("language", self.language_command))

        # Регистрируем обработчик выбора языка
        application.add_handler(CallbackQueryHandler(self.language_callback, pattern='^lang_'))

        # Регистрируем обработчики сообщений
        application.add_handler(MessageHandler(filters.VOICE, self.handle_voice))
        application.add_handler(MessageHandler(filters.AUDIO, self.handle_audio))
        application.add_handler(MessageHandler(filters.Document.ALL, self.handle_document))

        # Запускаем бота
        logger.info("Bot is running...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    """Главная функция"""
    # Получаем токен из переменной окружения
    token = os.getenv('TELEGRAM_BOT_TOKEN')

    if not token:
        print("❌ Ошибка: Не указан TELEGRAM_BOT_TOKEN")
        print("Установите переменную окружения:")
        print("  export TELEGRAM_BOT_TOKEN='your_token_here'")
        print("\nИли создайте файл .env с содержимым:")
        print("  TELEGRAM_BOT_TOKEN=your_token_here")
        sys.exit(1)

    # Создаем и запускаем бота
    bot = SpeechRecognitionBot(token)
    bot.run()


if __name__ == '__main__':
    main()
