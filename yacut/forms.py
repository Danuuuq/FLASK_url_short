from flask_wtf import FlaskForm
from wtforms import StringField, URLField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, URL

from .validators import Unique


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
            Unique('Предложенный вариант короткой ссылки уже существует.')]
    )
    submit = SubmitField('Создать')
