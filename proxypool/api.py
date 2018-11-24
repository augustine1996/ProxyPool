# -*- coding: utf-8 -*-
from flask import Flask, g
from .db import RedisClient

__all__ = ['app']

app = Flask(__name__)


def get_conn():
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


@app.route('/')
def index_view():
    return "<h3>This is system provide a proxy!</h3>"


@app.route('/<name>/get')
def get_view():
    """
    获取一个随机代理
    :return: 随机代理
    """
    conn = get_conn()
    return conn.random() if conn.random() else "代理池已空，请稍后再试"



@app.route('/<name>/count')
def get_count():
    """
    获得当前代理池中代理的总量
    :return: 代理总量
    """
    conn = get_conn()
    return str(conn.count())
