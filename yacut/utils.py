import hashlib

from .models import URLMap


def get_unique_short_id(origin_url):
    """Генерация короткого идентификатора.

    Функция принимает на вход длинную ссылку и
    возвращает короткий идентификатор.
    Если в БД вырастет количество данных, то
    увеличить длину короткого идентификатора."""
    length_short_url = 6
    url_bytes = origin_url.encode('utf-8')
    short_url = hashlib.sha256(url_bytes).hexdigest()[:length_short_url]
    if URLMap.query.filter_by(short=short_url).first() is not None:
        short_url = get_unique_short_id(origin_url + origin_url)
    return short_url
