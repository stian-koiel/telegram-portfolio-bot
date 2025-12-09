import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set. Create .env file with your token!")

# Setup logging
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# In-memory user language storage
user_language = {}


def get_language(user_id: int) -> str:
    """Get user language preference (default: English)."""
    return user_language.get(user_id, "en")


def set_language(user_id: int, lang: str) -> None:
    """Set user language preference."""
    user_language[user_id] = lang


def language_keyboard() -> ReplyKeyboardMarkup:
    """Language selection keyboard."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="English 🇬🇧"),
                KeyboardButton(text="Русский 🇷🇺")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def main_menu_keyboard(lang: str) -> ReplyKeyboardMarkup:
    """Main menu keyboard based on language."""
    if lang == "ru":
        keyboard = [
            [
                KeyboardButton(text="💬 Обо мне"),
                KeyboardButton(text="🛠 Навыки")
            ],
            [
                KeyboardButton(text="📁 Проекты"),
                KeyboardButton(text="📨 Контакты")
            ],
            [
                KeyboardButton(text="🌐 Language / Язык")
            ]
        ]
    else:
        keyboard = [
            [
                KeyboardButton(text="💬 About me"),
                KeyboardButton(text="🛠 Skills")
            ],
            [
                KeyboardButton(text="📁 Projects"),
                KeyboardButton(text="📨 Contacts")
            ],
            [
                KeyboardButton(text="🌐 Language / Язык")
            ]
        ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )


@router.message(CommandStart())
async def cmd_start(message: Message):
    """Handle /start command."""
    await message.answer(
        "Hi! Please choose your language.\n\nПривет! Пожалуйста, выбери язык.",
        reply_markup=language_keyboard()
    )


@router.message(F.text.in_(["English 🇬🇧", "Русский 🇷🇺"]))
async def handle_language_choice(message: Message):
    """Handle language selection."""
    user_id = message.from_user.id

    if message.text == "Русский 🇷🇺":
        set_language(user_id, "ru")
        text = "✅ Русский выбран!\n\nЯ — Telegram-бот-портфолио разработчика.\nВыбирай раздел в меню ниже."
    else:
        set_language(user_id, "en")
        text = "✅ English selected!\n\nI am a portfolio bot for a Python developer.\nChoose a section from the menu below."

    lang = get_language(user_id)
    await message.answer(text, reply_markup=main_menu_keyboard(lang))


@router.message(F.text == "🌐 Language / Язык")
async def change_language(message: Message):
    """Allow language change at any time."""
    await message.answer(
        "Choose your language / Выберите язык:",
        reply_markup=language_keyboard()
    )


async def handle_en(message: Message):
    """Handle English menu buttons."""
    text = message.text

    if text == "💬 About me":
        await message.answer(
            "Hi! I am a Python developer focusing on Telegram bots and web scraping.\n\n"
            "I like building small, practical tools that automate routine tasks and "
            "make data easier to work with.\n\n"
            "GitHub: https://github.com/stian-koiel"
        )

    elif text == "🛠 Skills":
        await message.answer(
            "Here are my main skills:\n"
            "- Python\n"
            "- Telegram Bot API (aiogram)\n"
            "- HTTP requests and APIs\n"
            "- Web scraping (Requests, BeautifulSoup)\n"
            "- Basic automation scripts and data processing"
        )

    elif text == "📁 Projects":
        await message.answer(
            "Some of my projects:\n\n"
            "1) Product List Scraper\n"
            "   Simple web scraper that collects product data from a demo catalog\n"
            "   and saves it to CSV/JSON.\n"
            "   GitHub: https://github.com/stian-koiel/preview-scraper\n\n"
            "2) Telegram Portfolio Bot\n"
            "   This bot you are using now. It shows who I am, my skills and projects.\n"
            "   GitHub: https://github.com/stian-koiel/telegram-portfolio-bot"
        )

    elif text == "📨 Contacts":
        await message.answer(
            "You can reach me here:\n"
            "- Telegram: @aedzakami\n"
            "- Email: hello@vlrevolution.xyz"
        )

    else:
        await message.answer("I did not recognize this command. Please use the buttons in the menu.")


async def handle_ru(message: Message):
    """Handle Russian menu buttons."""
    text = message.text

    if text == "💬 Обо мне":
        await message.answer(
            "Привет! Я Python-разработчик, специализируюсь на Telegram-ботах "
            "и скриптах для парсинга и автоматизации.\n\n"
            "Люблю делать небольшие, но полезные инструменты, которые экономят время "
            "и помогают работать с данными.\n\n"
            "GitHub: https://github.com/stian-koiel"
        )

    elif text == "🛠 Навыки":
        await message.answer(
            "Мои основные навыки:\n"
            "- Python\n"
            "- Telegram Bot API (aiogram)\n"
            "- HTTP-запросы и работа с API\n"
            "- Web scraping (Requests, BeautifulSoup)\n"
            "- Скрипты для автоматизации и обработки данных"
        )

    elif text == "📁 Проекты":
        await message.answer(
            "Некоторые мои проекты:\n\n"
            "1) Product List Scraper\n"
            "   Парсер списка товаров с демо-сайта с выгрузкой в CSV/JSON.\n"
            "   GitHub: https://github.com/stian-koiel/preview-scraper\n\n"
            "2) Telegram Portfolio Bot\n"
            "   Этот бот, который показывает информацию обо мне, моих навыках и проектах.\n"
            "   GitHub: https://github.com/stian-koiel/telegram-portfolio-bot"
        )

    elif text == "📨 Контакты":
        await message.answer(
            "Мои контакты:\n"
            "- Telegram: @aedzakami\n"
            "- Email: hello@vlrevolution.xyz"
        )

    else:
        await message.answer("Я не понял эту команду. Пожалуйста, используй кнопки в меню.")


@router.message()
async def handle_menu(message: Message):
    """Main menu handler - routes to language-specific handlers."""
    user_id = message.from_user.id
    lang = get_language(user_id)

    if lang == "ru":
        await handle_ru(message)
    else:
        await handle_en(message)


async def main():
    """Start the bot."""
    print("🚀 Starting portfolio bot...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
