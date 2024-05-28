import re

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, \
    ConversationHandler

from tgbot.handlers.onboarding.handlers import start, help, settings, \
    feedback, marking, select_lenguage, insta_url, insta_video
from tgbot.handlers.onboarding.keyboards import SETTINGS, BACK_TO, \
    MAIN_MENU_KEYBOARD, FEEDBACK, VIDEO
from tgbot.handlers.onboarding.states import FEEDBACK_STATE, SETTINGS_STATE, INSTA_URL_STATE


def setup_dispatcher(dp):

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CommandHandler("help", help),
            CommandHandler("settings", settings),

            MessageHandler(Filters.text(SETTINGS), settings),
            MessageHandler(Filters.text(FEEDBACK), feedback),
            MessageHandler(Filters.text(MAIN_MENU_KEYBOARD[0]), start),
            MessageHandler(Filters.text(VIDEO), insta_url)
        ],
        states={
            INSTA_URL_STATE: [
                MessageHandler(
                    Filters.regex('(?:https?:\/\/)?(?:www\.)?instagram\.com\/(?:([a-zA-Z0-9._\-]+)\/?)?(?:([p|reel|tv|stories]+)\/)?([a-zA-Z0-9\-_\.]+)?\/?(?:\?utm_source=[a-zA-Z0-9._\-]+)?'),
                    insta_video
                ),
            ],
            FEEDBACK_STATE: [
                MessageHandler(Filters.regex(
                    '^(😊Hammasi yoqdi ❤️|☺️Yaxshi ⭐️⭐️⭐️⭐️|😐 Yoqmadi ⭐️⭐️⭐️|☹️ Yomon ⭐️⭐️|😤 Juda yomon👎🏻)$'),
                    marking
                ),
            ],
            SETTINGS_STATE: [
                MessageHandler(Filters.regex('^(🌐 Tilni tanlash)$'), select_lenguage),
            ],
        },
        fallbacks=[
            CommandHandler("start", start),
            CommandHandler("help", help),
            MessageHandler(Filters.text(MAIN_MENU_KEYBOARD[0]), start),
        ],
    )
    dp.add_handler(conv_handler)

    return dp