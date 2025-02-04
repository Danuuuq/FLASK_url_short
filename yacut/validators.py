import re

from flask import request

from .models import URLMap


def validation_custom_id(custom_id):
    if (
        len(custom_id) > 16 or
        re.fullmatch(r'^[A-Za-z0-9]*$', custom_id) is None
    ):
        return 'Указано недопустимое имя для короткой ссылки'
    if URLMap.query.filter_by(short=custom_id).first() is not None:
        return 'Предложенный вариант короткой ссылки уже существует.'
    return False


def validation_original_url(original_url):
    if re.fullmatch(r'^https?:\/\/.*[.][a-zA-Z]{2}.*$', original_url) is None:
        return 'Неккоректный формат ссылки'
    url = URLMap.query.filter_by(original=original_url).first()
    if url is not None:
        return f'Ссылка уже была создана: {request.url + url.short}'
    return False
