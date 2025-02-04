import re

from flask import request

from .models import URLMap
from .utils import get_unique_short_id


class ValidateAPIRequest:

    def __init__(self, data):
        self.original_url = data.get('url')
        self.short_url = data.get('custom_id')
        self.error = None
        self.re_for_url = r'^https?:\/\/.*[.][a-zA-Z]{2}.*$'
        self.re_for_custom_id = r'^[A-Za-z0-9]*$'

    def valid_original_url(self):
        url = URLMap.query.filter_by(original=self.original_url).first()
        if not self.original_url:
            self.error = '\"url\" является обязательным полем!'
        elif re.fullmatch(self.re_for_url, self.original_url) is None:
            self.error = 'Некорректный формат ссылки'
        elif url is not None:
            short_url = request.url.split('api')[0] + url.short
            self.error = f'Ссылка уже была создана: {short_url}'

    def valid_custom_id(self):
        if not self.short_url:
            self.short_url = get_unique_short_id(self.original_url)
        elif (
            len(self.short_url) > 16 or
            re.fullmatch(self.re_for_custom_id, self.short_url) is None
        ):
            self.error = 'Указано недопустимое имя для короткой ссылки'
        elif URLMap.query.filter_by(short=self.short_url).first() is not None:
            self.error = 'Предложенный вариант короткой ссылки уже существует.'

    def valid_data(self):
        self.valid_original_url()
        if self.original_url:
            self.valid_custom_id()
        return True if self.error is None else False
