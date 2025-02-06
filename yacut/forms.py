from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import (
    DataRequired, Length, Optional, Regexp, URL, ValidationError
)

from .constants import (
    MAX_LENGTH_CUSTOM_ID, MAX_LENGTH_ORIGINAL_URL,
    MIN_LENGTH_FIELDS, REGEX_FOR_CUSTOM_ID
)
from .models import URLMap


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(MIN_LENGTH_FIELDS, MAX_LENGTH_ORIGINAL_URL),
            URL(message='Указанна некорректная ссылка')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(MIN_LENGTH_FIELDS, MAX_LENGTH_CUSTOM_ID,
                   f'Максимальная длина {MAX_LENGTH_CUSTOM_ID} символов'),
            Optional(),
            Regexp(REGEX_FOR_CUSTOM_ID,
                   message='Допустимы только символы латиницы и цифры')]
    )
    submit = SubmitField('Создать')

    def validate_original_link(form, field):
        url = URLMap.get_object(original=field.data)
        if url:
            raise ValidationError(
                f'Ссылка уже была создана: {request.url + url.short}'
            )

    def validate_custom_id(form, field):
        if URLMap.get_object(short=field.data):
            raise ValidationError(
                'Предложенный вариант короткой ссылки уже существует.'
            )
