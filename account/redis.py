from ast import pattern
from datetime import datetime, timedelta

import pytz
import redis
from django.conf import settings


r = redis.Redis.from_url(settings.CACHES['default']['LOCATION'])


def _get_day(offset=0):
    """Получить день в формате год-месяц-день"""

    day_in_moscow = pytz.timezone('Europe/Moscow').localize(datetime.now())
    previous_day = day_in_moscow - timedelta(days=abs(offset))
    return previous_day.strftime("%Y-%m-%d")

def _increment_learner_action(user, action, expiration_days=365):
    day = _get_day()
    key = f'user:{user}:{day}'
    r.hincrby(key, action, 1)
    r.expire(key, expiration_days * 24 * 60 * 60)

def _get_user_actions_for_day(user_id, day):
    key = f'user:{user_id}:{day}'
    stored_data = r.hgetall(key)

    if stored_data:
        return {field.decode('utf-8'): int(value) for field, value in stored_data.items()}
    
def _get_user_actions_for_all_days(user):
    pattern = f'user:{user}'
    keys = r.keys(pattern)
    result = []

    for key in keys:
        stored_data = r.hgetall(key)
        day = key.decode('utf-8').split(':')[-1]
        if stored_data:
            result[day] = {field.decode('utf-8'): int(value) for field, value in stored_data.items()}

    return result