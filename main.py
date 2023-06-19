import os

from environs import Env
import django
import telegram


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from bot.models import Question

if __name__ == '__main__':
    env = Env()
    env.read_env()
    tg_bot_token = env('TG_BOT_TOKEN')
    bot = telegram.Bot(token=tg_bot_token)
    print(bot.get_me())
    # print('Количество пропусков:', Question.objects.count())