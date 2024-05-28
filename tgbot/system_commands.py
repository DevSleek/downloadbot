from typing import Dict
from telegram import Bot, BotCommand

bot = Bot(dtb.settings.TELEGRAM_TOKEN)


def set_up_commands(bot_instance: Bot) -> None:

    commands = [
        BotCommand("start", "Menu menu"),
        BotCommand("help", "Help"),
        BotCommand("settings", "Settings"),
    ]
    bot_instance.set_my_commands(commands)


set_up_commands(bot)
