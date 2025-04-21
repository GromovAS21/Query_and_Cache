from datetime import datetime, time, timedelta

default_limit = 5

def get_cache_expiration():
    """
    Возвращает время до истечения кэша (до 14:11 текущего дня).

    Returns:
        Время до истечения кэша.
    """
    now = datetime.now()
    expiration_time = time(14, 11)

    if now.time() < expiration_time:  # Если сейчас время до 14:11,
        expiration_datetime = datetime.combine(now.date(), expiration_time)
    else:  # Если сейчас время после 14:11
        expiration_datetime = datetime.combine(now.date(), expiration_time)
        expiration_datetime += timedelta(days=1)

    return expiration_datetime - now