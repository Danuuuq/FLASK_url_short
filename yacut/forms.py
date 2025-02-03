from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, URLField, SubmitField
from wtforms.validators import (
    DataRequired, Length, Optional, URL, ValidationError, Regexp
)

from .models import URLMap


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, 256),
            URL(message='Указанна неккоректная ссылка')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[
            Length(1, 16, 'Максимальная длина 16 символов'),
            Optional(),
            Regexp('^[A-Za-z0-9]*$',
                   message='Допустимы только символы латиницы и цифры')]
    )
    submit = SubmitField('Создать')

    def validate_original_link(form, field):
        if URLMap.query.filter_by(origin=field.data).first() is not None:
            breakpoint()
            url = URLMap.query.filter_by(origin=field.data).first()
            raise ValidationError(
                f'Ссылка уже была создана: {request.url + url.short}'
            )

    def validate_custom_id(form, field):
        if URLMap.query.filter_by(short=field.data).first() is not None:
            raise ValidationError(
                'Предложенный вариант короткой ссылки уже существует.'
            )
