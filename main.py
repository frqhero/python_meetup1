import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from bot.models import Question

if __name__ == '__main__':
    print('Количество пропусков:', Question.objects.count())