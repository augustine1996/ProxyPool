# -*- coding: utf-8 -*-
from flask import Flask

__all__ = ['app']

app = Flask(__name__)


@app.route('/')
def index_view():
    return "<h3>This is system provide a proxy!</h3>"


@app.route('/<name>/get')
def get_view():
    pass


@app.route('/<name>/count')
def get_count():
    pass
