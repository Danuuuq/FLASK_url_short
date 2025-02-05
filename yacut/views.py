from flask import abort, flash, redirect, render_template, request

from . import app
from .models import URLMap
from .forms import URLForm


@app.route('/', methods=['GET', 'POST'])
def create_short_url_view():
    form = URLForm()
    if form.validate_on_submit():
        try:
            url = URLMap.create_object(form.data)
        except ValueError:
            abort(500)
        flash('Ваша новая ссылка готова:', request.url + url.short)
        return render_template('index.html', form=form)
    return render_template('index.html', form=form)


@app.route('/<short_url>')
def redirect_views(short_url):
    url = URLMap.query.filter_by(short=short_url).first_or_404()
    return redirect(url.original)
