from datetime import datetime, timezone

from flask import request

from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, unique=True, nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True,
                          default=datetime.now(timezone.utc))

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=request.url.split('api')[0] + self.short
        )
