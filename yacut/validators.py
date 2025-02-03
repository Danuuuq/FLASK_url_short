from wtforms.validators import ValidationError

from .models import URLMap


class Unique(object):
    def __init__(self, message):
        if not message:
            message = 'Данные уже содержатся в базе данных'
        self.message = message

    def __call__(self, form, field):
        if URLMap.query.filter_by(origin=field.data).first() is not None:
            raise ValidationError(self.message)
