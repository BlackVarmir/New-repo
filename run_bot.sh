#!/bin/bash
# Скрипт для запуска Telegram Speech-to-Text бота

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Telegram Speech-to-Text Bot${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Проверка наличия .env файла
if [ ! -f .env ]; then
    echo -e "${RED}❌ Файл .env не найден!${NC}"
    echo -e "${YELLOW}Создайте файл .env на основе .env.example:${NC}"
    echo -e "  cp .env.example .env"
    echo -e "  nano .env"
    echo ""
    exit 1
fi

# Загрузка переменных окружения из .env
export $(cat .env | grep -v '^#' | xargs)

# Проверка токена
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo -e "${RED}❌ TELEGRAM_BOT_TOKEN не установлен!${NC}"
    echo -e "${YELLOW}Добавьте токен в файл .env:${NC}"
    echo -e "  TELEGRAM_BOT_TOKEN=your_token_here"
    echo ""
    exit 1
fi

# Проверка наличия Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 не установлен!${NC}"
    echo -e "${YELLOW}Установите Python 3:${NC}"
    echo -e "  sudo apt-get install python3 python3-pip"
    echo ""
    exit 1
fi

# Проверка зависимостей
echo -e "${YELLOW}📦 Проверка зависимостей...${NC}"
if ! python3 -c "import telegram" &> /dev/null; then
    echo -e "${YELLOW}⚠️  Зависимости не установлены${NC}"
    echo -e "${YELLOW}Установка зависимостей...${NC}"
    pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Ошибка установки зависимостей!${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ Зависимости установлены${NC}"
fi

echo ""
echo -e "${GREEN}🚀 Запуск бота...${NC}"
echo -e "${YELLOW}Нажмите Ctrl+C для остановки${NC}"
echo ""

# Запуск бота
python3 telegram_bot.py
