from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .validators import ValidateAPIRequest


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    data = ValidateAPIRequest(data)
    if data.valid_data():
        url_obj = URLMap(
            original=data.original_url,
            short=data.short_url
        )
        db.session.add(url_obj)
        db.session.commit()
        return jsonify(url_obj.to_dict()), 201
    raise InvalidAPIUsage(data.error)


@app.route('/api/id/<short_url>/', methods=['GET'])
def get_short_url(short_url):
    url = URLMap.query.filter_by(short=short_url).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url.original}), 200
