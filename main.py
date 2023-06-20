import os

from environs import Env
from telegram import ReplyKeyboardMarkup, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from bot.models import Question

MAIN_MENU = 'Добро пожаловать!'

ABOUT_BUTTON = 'Что я могу?'
ABOUT_MENU_MARKUP = InlineKeyboardMarkup([[
    InlineKeyboardButton(ABOUT_BUTTON, callback_data=ABOUT_BUTTON)
]])


def start(update, context):
    reply_keyboard = [['Boy', 'Girl', 'Other']]
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Hi'
        )
    )


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


def menu(update, context):
    context.bot.send_message(
        update.message.from_user.id,
        MAIN_MENU,
        parse_mode=ParseMode.HTML,
        reply_markup=ABOUT_MENU_MARKUP
    )


def button_tap(update, context):
    data = update.callback_query.data
    text = 'Ничего'

    update.callback_query.answer()
    update.callback_query.message.edit_text(
        text,
        ParseMode.HTML,
        reply_markup=None
    )


if __name__ == '__main__':
    env = Env()
    env.read_env()
    tg_bot_token = env('TG_BOT_TOKEN')
    updater = Updater(token=tg_bot_token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    caps_handler = CommandHandler('caps', caps)
    dispatcher.add_handler(caps_handler)

    dispatcher.add_handler(CommandHandler("menu", menu))
    dispatcher.add_handler(CallbackQueryHandler(button_tap))

    updater.start_polling()
    # print('Количество пропусков:', Question.objects.count())