import hashlib
import re
from datetime import datetime, timezone

from flask import current_app, url_for
from sqlalchemy.exc import IntegrityError

from . import db
from .constants import (
    MAX_LENGTH_CUSTOM_ID, REGEX_FOR_CUSTOM_ID, REGEX_FOR_URL
)
from .exceptions import IncorrectFormatData, NotUniqueData


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, unique=True, nullable=False)
    short = db.Column(db.String(MAX_LENGTH_CUSTOM_ID),
                      unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True,
                          default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        """Возвращение словаря с данными объекта."""
        return dict(
            url=self.original,
            short_link=url_for(
                'redirect_views', _external=True, short_url=self.short),
        )

    @classmethod
    def get_object(cls, **kwargs):
        """Возвращение объекта из базы данных по заданным параметрам.

        Ключевые аргументы:
        **kwargs -- параметры для фильтрации
        """
        return cls.query.filter_by(**kwargs).first()

    @staticmethod
    def validate_original_url(original_url):
        """Проверка корректности введенной ссылки.

        Ключевые аргументы:
        original_url -- исходная ссылка
        """
        if re.fullmatch(REGEX_FOR_URL, original_url) is None:
            raise IncorrectFormatData('Некорректный формат ссылки')
        elif URLMap.get_object(original=original_url):
            raise NotUniqueData('Ссылка уже была создана ранее:')

    @staticmethod
    def validate_custom_id(original_url, custom_id):
        """Проверка корректности введенного идентификатора.

        Ключевые аргументы:
        original_url -- исходная ссылка
        custom_id -- короткий идентификатор
        """
        if not custom_id:
            return URLMap.get_unique_short_id(original_url)
        elif (
            len(custom_id) > MAX_LENGTH_CUSTOM_ID or
            re.fullmatch(REGEX_FOR_CUSTOM_ID, custom_id) is None
        ):
            raise IncorrectFormatData(
                'Указано недопустимое имя для короткой ссылки')
        elif URLMap.get_object(short=custom_id):
            raise NotUniqueData(
                'Предложенный вариант короткой ссылки уже существует.')
        return custom_id

    @staticmethod
    def create_object(data):
        """Создание объект URLMap и сохранение его в базе данных.

        Ключевые аргументы:
        data -- данные для создания объекта"""
        original_url = data.get('url') or data.get('original_link')
        custom_id = URLMap.validate_custom_id(
            original_url, data.get('custom_id'))
        URLMap.validate_original_url(
            original_url)
        url = URLMap(
            original=original_url,
            short=custom_id
        )
        try:
            db.session.add(url)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError('Ошибка сохранения данных')
        return url

    @staticmethod
    def get_unique_short_id(original_url):
        """Генерирует уникальный короткий идентификатор для ссылки.

        Ключевые аргументы:
        original_url -- исходная ссылка
        """
        length_short_url = current_app.config['LENGTH_SHORT_ID']
        url_bytes = original_url.encode('utf-8')
        short_url = hashlib.sha256(url_bytes).hexdigest()[:length_short_url]
        if URLMap.get_object(short=short_url):
            current_app.config['LENGTH_SHORT_ID'] += 1
            short_url = URLMap.get_unique_short_id(original_url)
        return short_url
