from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id
from .validators import validation_custom_id, validation_original_url


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    data = request.get_json(silent=True)
    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    if 'custom_id' not in data:
        data['custom_id'] = get_unique_short_id(data['url'])
    not_valid_custom_id = validation_custom_id(data['custom_id'])
    if not_valid_custom_id:
        raise InvalidAPIUsage(not_valid_custom_id)
    not_valid_original_url = validation_original_url(data['url'])
    if not_valid_original_url:
        raise InvalidAPIUsage(not_valid_original_url)
    url = URLMap(
        original=data['url'],
        short=data['custom_id']
    )
    db.session.add(url)
    db.session.commit()
    return jsonify({
        'url': data['url'],
        'short_link': request.url.split('api')[0] + data['custom_id']
    }), 201


@app.route('/api/id/<short_url>/', methods=['GET'])
def get_short_url(short_url):
    url = URLMap.query.filter_by(short=short_url).first()
    if url is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url.original}), 200
