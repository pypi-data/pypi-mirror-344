from flask import g
from peewee import PostgresqlDatabase

from amapy_server.configs import Configs
from amapy_server.models.base.base import db_proxy


def get_db(app):
    db_cfg = Configs.shared().DATABASE
    with app.app_context():
        if 'db' not in g:
            postgres_cred = {
                'user': db_cfg['user'],
                'password': db_cfg['password'],
                'host': db_cfg['host'],
                'port': db_cfg['port']
            }
            g.db = PostgresqlDatabase(db_cfg["database"], **postgres_cred)
            db_proxy.initialize(g.db)
        return g.db
