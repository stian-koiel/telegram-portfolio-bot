import logging
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set. Please create a .env file based on .env.example")

# Configure logging for easier debugging
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Simple in-memory storage for user language preferences.
# For a production bot you would use a database or a proper storage backend.
user_language = {}  # user_id -> "en" or "ru"


def get_language(user_id: int) -> str:
    """
    Return the language code for a given user.
    Defaults to English ("en") if the user did not choose yet.
    """
    return user_language.get(user_id, "en")


def set_language(user_id: int, lang: str) -> None:
    """Save the language preference for a user in the in-memory storage."""
    user_language[user_id] = lang


def language_keyboard() -> ReplyKeyboardMarkup:
    """
    Keyboard shown on /start to allow the user to choose a language.
    """
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("English 🇬🇧"), KeyboardButton("Русский 🇷🇺"))
    return kb


def main_menu_keyboard(lang: str) -> ReplyKeyboardMarkup:
    """
    Build the main menu keyboard depending on the selected language.
    """
    kb = ReplyKeyboardMarkup(resize_keyboard=True)

    if lang == "ru":
        kb.add(
            KeyboardButton("💬 Обо мне"),
            KeyboardButton("🛠 Навыки"),
        )
        kb.add(
            KeyboardButton("📁 Проекты"),
            KeyboardButton("📨 Контакты"),
        )
        kb.add(KeyboardButton("🌐 Language / Язык"))
    else:
        kb.add(
            KeyboardButton("💬 About me"),
            KeyboardButton("🛠 Skills"),
        )
        kb.add(
            KeyboardButton("📁 Projects"),
            KeyboardButton("📨 Contacts"),
        )
        kb.add(KeyboardButton("🌐 Language / Язык"))

    return kb


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    """
    Handle the /start command:
    - Ask the user to choose a language.
    - Show a short welcome text.
    """
    text = (
        "Hi! Please choose your language.\n\n"
        "Привет! Пожалуйста, выбери язык."
    )
    await message.answer(text, reply_markup=language_keyboard())


@dp.message_handler(lambda m: m.text in ["English 🇬🇧", "Русский 🇷🇺"])
async def handle_language_choice(message: types.Message):
    """
    Handle user language choice from the language keyboard.
    """
    user_id = message.from_user.id

    if message.text == "Русский 🇷🇺":
        set_language(user_id, "ru")
        text = (
            "Отлично! Я — Telegram‑бот‑портфолио разработчика.\n\n"
            "Выбирай раздел в меню ниже."
        )
    else:
        set_language(user_id, "en")
        text = (
            "Great! I am a portfolio bot for a Python developer.\n\n"
            "Please choose a section from the menu below."
        )

    lang = get_language(user_id)
    await message.answer(text, reply_markup=main_menu_keyboard(lang))


@dp.message_handler()
async def handle_menu(message: types.Message):
    """
    Handle all text messages after the user chooses a language.
    We use the text of the message and current language to decide what to answer.
    """
    user_id = message.from_user.id
    lang = get_language(user_id)
    text = message.text

    # Allow the user to switch language at any time
    if text == "🌐 Language / Язык":
        await message.answer(
            "Choose your language / Выберите язык:",
            reply_markup=language_keyboard(),
        )
        return

    if lang == "ru":
        await handle_ru(message)
    else:
        await handle_en(message)


async def handle_en(message: types.Message):
    """
    Handle main menu buttons and commands in English.
    """
    text = message.text

    if text == "💬 About me":
        about = (
            "Hi! I am a Python developer focusing on Telegram bots and web scraping.\n\n"
            "I like building small, practical tools that automate routine tasks and "
            "make data easier to work with.\n\n"
            "GitHub: https://github.com/your-username"
        )
        await message.answer(about)

    elif text == "🛠 Skills":
        skills = (
            "Here are my main skills:\n"
            "- Python\n"
            "- Telegram Bot API (aiogram)\n"
            "- HTTP requests and APIs\n"
            "- Web scraping (Requests, BeautifulSoup)\n"
            "- Basic automation scripts and data processing"
        )
        await message.answer(skills)

    elif text == "📁 Projects":
        projects = (
            "Some of my projects:\n\n"
            "1) Product List Scraper\n"
            "   Simple web scraper that collects product data from a demo catalog\n"
            "   and saves it to CSV/JSON.\n"
            "   GitHub: https://github.com/your-username/product-list-scraper\n\n"
            "2) Telegram Portfolio Bot\n"
            "   This bot you are using now. It shows who I am, my skills and projects.\n"
            "   GitHub: https://github.com/your-username/telegram-portfolio-bot"
        )
        await message.answer(projects)

    elif text == "📨 Contacts":
        contacts = (
            "You can reach me here:\n"
            "- Telegram: @your_telegram\n"
            "- Email: your_email@example.com\n"
            "- Freelance profile: link to your profile (when ready)"
        )
        await message.answer(contacts)

    else:
        # Default fallback if text does not match any known button
        await message.answer(
            "I did not recognize this command. "
            "Please use the buttons in the menu."
        )


async def handle_ru(message: types.Message):
    """
    Handle main menu buttons and commands in Russian.
    """
    text = message.text

    if text == "💬 Обо мне":
        about = (
            "Привет! Я Python‑разработчик, специализируюсь на Telegram‑ботах "
            "и скриптах для парсинга и автоматизации.\n\n"
            "Люблю делать небольшие, но полезные инструменты, которые экономят время "
            "и помогают работать с данными.\n\n"
            "GitHub: https://github.com/your-username"
        )
        await message.answer(about)

    elif text == "🛠 Навыки":
        skills = (
            "Мои основные навыки:\n"
            "- Python\n"
            "- Telegram Bot API (aiogram)\n"
            "- HTTP‑запросы и работа с API\n"
            "- Web scraping (Requests, BeautifulSoup)\n"
            "- Скрипты для автоматизации и обработки данных"
        )
        await message.answer(skills)

    elif text == "📁 Проекты":
        projects = (
            "Некоторые мои проекты:\n\n"
            "1) Product List Scraper\n"
            "   Парсер списка товаров с демо‑сайта с выгрузкой в CSV/JSON.\n"
            "   GitHub: https://github.com/your-username/product-list-scraper\n\n"
            "2) Telegram Portfolio Bot\n"
            "   Этот бот, который показывает информацию обо мне, моих навыках и проектах.\n"
            "   GitHub: https://github.com/your-username/telegram-portfolio-bot"
        )
        await message.answer(projects)

    elif text == "📨 Контакты":
        contacts = (
            "Мои контакты:\n"
            "- Telegram: @your_telegram\n"
            "- Email: your_email@example.com\n"
            "- Профиль на фрилансе: ссылка (когда будет готова)"
        )
        await message.answer(contacts)

    else:
        await message.answer(
            "Я не понял эту команду. Пожалуйста, используй кнопки в меню."
        )


if __name__ == "__main__":
    # Start long-polling to receive updates from Telegram
    executor.start_polling(dp, skip_updates=True)
