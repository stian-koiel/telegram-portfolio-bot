# telegram-portfolio-bot

Simple Telegram bot written in Python that works as a portfolio for a developer.  
The bot can show information about me, my skills, projects (with GitHub links) and contacts.  
It also supports two languages: English and Russian.

## Features

- `/start` command with language selection (English / Russian)
- Main menu with:
  - About me
  - Skills
  - Projects (with links to GitHub repositories)
  - Contacts
- Implemented with `aiogram` and `.env` for token management

## Requirements

- Python 3.10+
- Telegram bot token (from @BotFather)
- See `requirements.txt` for Python dependencies

## Setup

1. Clone the repository:

git clone https://github.com/your-username/telegram-portfolio-bot.git
cd telegram-portfolio-bot


2. Create a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

3. Install dependencies:

pip install -r requirements.txt

4. Create a `.env` file based on `.env.example` and paste your bot token:

BOT_TOKEN=your_token_here

5. Run the bot:

python bot.py
Open your bot in Telegram and send `/start` to begin.
