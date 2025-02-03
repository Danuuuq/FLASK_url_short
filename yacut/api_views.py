from flask import jsonify, request

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/api/id/', methods=['POST'])
def create_short_url():
    data = request.get_json()
    if 'url' not in data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'custom_id' not in data:
        data['custom_id'] = get_unique_short_id(data['url'])
    url = URLMap(
        origin=data['url'],
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
    return jsonify({'url': url.origin}), 200
