from flask import render_template, redirect, url_for, flash, request

from . import app, db
from .models import URLMap
from .forms import URLForm
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def create_short_url_view():
    form = URLForm()
    if form.validate_on_submit():
        breakpoint()
        url = URLMap(
            origin=form.original_link.data,
            short=get_unique_short_id(form.original_link.data)
        )
        db.session.add(url)
        db.session.commit()
        flash(f'Ваша новая ссылка готова:\n{request.url + url.short}')
        return render_template('index.html', form=form)
    return render_template('index.html', form=form)


# @app.route('/<str:short_url>')
# def redirect_views(short_url):
#     url = URLMap.query.get(short=short_url)
#     return redirect(url.origin)
