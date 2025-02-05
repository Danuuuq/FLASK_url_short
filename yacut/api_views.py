from flask import jsonify, request

from . import app
from .error_handlers import InvalidAPIUsage
from .models import URLMap


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if not data.get('url'):
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    try:
        url = URLMap.create_object(data)
    except ValueError as error:
        raise InvalidAPIUsage(str(error))
    return jsonify(url.to_dict()), 201


@app.route('/api/id/<short_url>/', methods=['GET'])
def get_short_url(short_url):
    url = URLMap.get_object(short=short_url)
    if not url:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url.original}), 200
