import hashlib
import re
from datetime import datetime, timezone

from flask import current_app, url_for
from sqlalchemy.exc import IntegrityError

from . import db
from .constants import (
    MAX_LENGTH_CUSTOM_ID, REGEX_FOR_CUSTOM_ID, REGEX_FOR_URL
)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, unique=True, nullable=False)
    short = db.Column(db.String(MAX_LENGTH_CUSTOM_ID),
                      unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True,
                          default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                'redirect_views', _external=True, short_url=self.short),
        )

    @classmethod
    def get_object(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @staticmethod
    def validate_original_url(original_url):
        if re.fullmatch(REGEX_FOR_URL, original_url) is None:
            raise ValueError('Некорректный формат ссылки')

    @staticmethod
    def create_object(data):
        URLMap.validate_original_url(
            data.get('url') or data.get('original_link'))
        if not data.get('custom_id'):
            data['custom_id'] = URLMap.get_unique_short_id(
                data.get('url') or data.get('original_link'))
        elif (
            len(data['custom_id']) > MAX_LENGTH_CUSTOM_ID or
            re.fullmatch(REGEX_FOR_CUSTOM_ID, data['custom_id']) is None
        ):
            raise ValueError(
                'Указано недопустимое имя для короткой ссылки')
        elif URLMap.get_object(short=data['custom_id']):
            raise ValueError(
                'Предложенный вариант короткой ссылки уже существует.')
        url = URLMap(
            original=data.get('url') or data.get('original_link'),
            short=data['custom_id']
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
        length_short_url = current_app.config['LENGTH_SHORT_ID']
        url_bytes = original_url.encode('utf-8')
        short_url = hashlib.sha256(url_bytes).hexdigest()[:length_short_url]
        if URLMap.get_object(short=short_url):
            current_app.config['LENGTH_SHORT_ID'] += 1
            short_url = URLMap.get_unique_short_id(original_url)
        return short_url
