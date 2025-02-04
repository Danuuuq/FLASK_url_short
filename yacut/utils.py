import hashlib

from flask import current_app

from .models import URLMap


def get_unique_short_id(original_url):
    """Генерация короткого идентификатора.

    Функция принимает на вход длинную ссылку и
    возвращает короткий идентификатор.
    Если возникнет коллизия, то увеличиваем
    длину короткого идентификатора."""
    length_short_url = current_app.config['LENGTH_SHORT_ID']
    url_bytes = original_url.encode('utf-8')
    short_url = hashlib.sha256(url_bytes).hexdigest()[:length_short_url]
    if URLMap.query.filter_by(short=short_url).first() is not None:
        current_app.config['LENGTH_SHORT_ID'] += 1
        short_url = get_unique_short_id(original_url)
    return short_url
