import requests
import re
import datetime
import instaloader
import os

# Initialize Instaloader
L = instaloader.Instaloader()

from django.utils import timezone
from telegram import ParseMode, Update
from telegram import KeyboardButton, ReplyKeyboardMarkup,  InlineKeyboardMarkup, \
     InlineKeyboardButton
from telegram.ext import ConversationHandler, CallbackContext

from users.models import User
from tgbot.handlers.onboarding import static_text
from tgbot.handlers.utils.info import extract_user_data_from_update
from tgbot.handlers.onboarding.keyboards import MAIN_MENU_KEYBOARD, MAIN_KEYBOARD, \
    SETTINGS_KEYBOARD, BACK_TO, MARKS
from tgbot.handlers.onboarding.states import FEEDBACK_STATE, SETTINGS_STATE, INSTA_URL_STATE
from tgbot.main import bot


def start(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)

    update.message.reply_text(
        "«Hi» {}! Kichik Download botga xush kelibsiz \n\n Nima yuklaymiz?".format(u.first_name),
        reply_markup=ReplyKeyboardMarkup(
            MAIN_KEYBOARD,
            one_time_keyboard=False,
            resize_keyboard=True,
        ),
    )
    return ConversationHandler.END


def insta_url(update: Update, context: CallbackContext):

    update.message.reply_text(
        "Instagram URL kiriting"
    )

    return INSTA_URL_STATE


def insta_video(update: Update, context: CallbackContext):
    url = update.message.text
    def get_response(url):
        shortcode = url.split('/')[-2]
        target_dir = f"downloads/{shortcode}"
        os.makedirs(target_dir, exist_ok=True)
        try:
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            L.download_post(post, target=f"downloads/{shortcode}")

            video_path = None
            for filename in os.listdir(target_dir):
                if filename.endswith('.mp4'):
                    video_path = os.path.join(target_dir, f"{shortcode}.mp4")
                    shutil.move(os.path.join(target_dir, filename), video_path)
                    break

            if video_path:
                bot = Bot(token=TOKEN)
                with open(video_path, 'rb') as video_file:
                    update.message.reply_video(video=video_file, width=200, height=300, duration=200)
                update.message.reply_text("Video sent to Telegram!")

        except Exception as e:
            update.message.reply_text(f"An error occurred: {e}")
    get_response(url)

    return ConversationHandler.END


def help(update: Update, context: CallbackContext):
    update.message.reply_text(
        """Buyurtma va boshqa savollar bo'yicha javob olish uchun @pastarobot'ga murojaat qiling, barchasiga javob beramiz :)"""
    )


def settings(update: Update, context: CallbackContext):
    update.message.reply_text(
        "⚙️ Sozlamalar",
        reply_markup=ReplyKeyboardMarkup(
            SETTINGS_KEYBOARD + MAIN_MENU_KEYBOARD,
            one_time_keyboard=False,
            resize_keyboard=True,
        )
    )
    return SETTINGS_STATE


def select_lenguage(update: Update, context: CallbackContext):

    buttons = [
        [InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data="uzb")],
        [InlineKeyboardButton("🇷🇺 Русский", callback_data="rus")],
    ]
    markup = InlineKeyboardMarkup(buttons)
    update.message.reply_text(
        """Iltimos, tilni tanlang
Пожалуйста, выберите язык ⬇️""",
        reply_markup=markup
    )

    return ConversationHandler.END


def feedback(update: Update, context: CallbackContext):
    update.message.reply_text(
        """✅ Bizning Download botni tanlaganingiz uchun rahmat.
Agar Siz bizning xizmatlarimiz sifatini yaxshilashga yordam bersangiz benihoyat hursand bo’lamiz.
Buning uchun 5 ballik tizim asosida bizni baholang""",
        reply_markup=ReplyKeyboardMarkup(
            MARKS + MAIN_MENU_KEYBOARD,
            one_time_keyboard=False,
            input_field_placeholder="Quyidagilardan birini tanlang",
            resize_keyboard=True,
        ),
    )
    return FEEDBACK_STATE


def marking(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Rahmat! Bizning xizmatlarimizni baholaganiz uchun rahmat! 🙏🏻",
        reply_markup=ReplyKeyboardMarkup(
            MAIN_KEYBOARD,
            one_time_keyboard=False,
            resize_keyboard=True,
        ),
    )

    return ConversationHandler.END


def secret_level(update: Update, context: CallbackContext) -> None:
    user_id = extract_user_data_from_update(update)['user_id']
    text = static_text.unlock_secret_room.format(
        user_count=User.objects.count(),
        active_24=User.objects.filter(updated_at__gte=timezone.now() - datetime.timedelta(hours=24)).count()
    )

    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML
    )
