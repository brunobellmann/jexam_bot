# JExam Telegram Bot

Telegrambot um aktuelle Prüfungsergebnisse von jExam der TU Dresden abzufragen.

This bot consists of two parts:

1. Node.js app that handles the observed courses for each user.

2. Python script that periodically checks if those courses are online on JExam.

## Deploy to Raspberry Pi

1. Prerequisites

Please install the following packages:

nodejs, git, python3, python3-pip

2. Clone the repository

```bash
git clone https://github.com/brunobellmann/jexam_bot.git
```

3. Setup environment variables

```bash
cd jexam_bot/
```

Copy the .env.example file and edit the settings accordingly:

```bash
cp .env.example .env
vim .env
```

BOT_TOKEN is the API Token of your chatbot you receive from the [botfather](t.me/BotFather) chat in Telegram.

ADMIN_ID is your chat ID, the services will send errors in your private chat. You can find out your chat id by messaging [Telegram Bot Raw](t.me/RawDataBot).

UPDATE_INTERVAL is the amount of seconds until the bot waits for checking the next Update on JExam.

Note: All those environment variables are required to use the bot.

4. Setup the services

```bash
npm install
pip install -r requirements.txt --user
sudo sh install.sh
```

## Stop the services and delete them from autostarting

```bash
sudo sh uninstall.sh
```

## Usage mit Python (auf MacOS):

```bash
brew install python@3.9
pip install requests
pip install -U python-dotenv
```
