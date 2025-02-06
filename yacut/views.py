from flask import flash, redirect, render_template

from . import app
from .exceptions import IncorrectFormatData, NotUniqueData
from .models import URLMap
from .forms import URLForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def create_short_url_view():
    form = URLForm()
    if form.validate_on_submit():
        try:
            url = URLMap.create_object(form.data)
        except (ValueError, IncorrectFormatData, NotUniqueData) as error:
            flash(str(error), 'error')
        else:
            flash('Ваша новая ссылка готова:', url.to_dict()['short_link'])
        return render_template('index.html', form=form)
    return render_template('index.html', form=form)


@app.route('/<short_url>')
def redirect_views(short_url):
    url = URLMap.query.filter_by(short=short_url).first_or_404()
    return redirect(url.original)
