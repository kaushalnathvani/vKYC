from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from sqlalchemy.pool import NullPool
import configparser


class DBManager:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.db_config = self.get_db_config()

    def get_db_config(self):
        config = configparser.ConfigParser()
        CONFIG_FILE = 'config.ini'
        CONFIG_PATH = 'config'
        config.read(os.path.join(CONFIG_PATH, CONFIG_FILE))
        el = dict(config.items("pg_config"))

        config = {
            'type': el.get('type', 'postgres'),
            'host': el.get('host', 'localhost'),
            'port': int(el.get('port', 5432)),
            'db_name': el.get('db_name', ''),
            'user': el.get('user', ''),
            'passwd': el.get('passwd', ''),
            'charset': 'utf8',
            'schema': el.get('schema', 'public'),
            'secret_key': el.get('secret_key', ''),
        }

        return config

    def get_session(self, dbconfig=None):
        if dbconfig is None:
            db_config = self.db_config
        else:
            db_config = dbconfig

        conn_str = (
                'postgresql://%(user)s:%(passwd)s@%(host)s:%(port)d/%(db_name)s' % db_config)
        engine = create_engine(conn_str, poolclass=NullPool)
        engine.dialect.supports_sane_rowcount = engine.dialect.supports_sane_multi_rowcount = False

        # db_session = scoped_session(sessionmaker(
        #     autocommit=False,
        #     autoflush=True,
        #     expire_on_commit=False,
        #     bind=engine
        # ))

        Session = sessionmaker(bind=engine)
        conn = engine.connect()
        session = Session(bind=conn)

        return session

    def close_session(self, session):
        try:
            session.close()
        except Exception as e:
            print('Error:',e)
            pass
