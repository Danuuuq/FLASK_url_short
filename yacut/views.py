from flask import render_template, redirect, url_for, flash, request

from . import app, db
from .models import URLMap
from .forms import URLForm
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def create_short_url_view():
    form = URLForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data
        if len(custom_id) == 0:
            custom_id = get_unique_short_id(form.original_link.data)
        url = URLMap(
            origin=form.original_link.data,
            short=custom_id
        )
        db.session.add(url)
        db.session.commit()
        flash('Ваша новая ссылка готова:', request.url + url.short)
        return render_template('index.html', form=form)
    return render_template('index.html', form=form)


@app.route('/<short_url>')
def redirect_views(short_url):
    url = URLMap.query.filter_by(short=short_url).first()
    return redirect(url.origin)
