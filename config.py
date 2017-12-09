from pymongo import MongoClient
from gridfs import GridFS
import pymongo


def configure(app):
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = 'very secret key'
    app.config['TESTING'] = True

    from tools.trans import trans, update
    update()
    app.jinja_env.globals.update(_=trans)
    import html
    app.jinja_env.globals.update(unescape=lambda x: html.unescape(x))

    @app.after_request
    def after_request(response):
        response.headers.add('Accept-Ranges', 'bytes')
        return response


client = MongoClient('localhost:27017')
db_name = 'FREESON'
db = client[db_name]
fs = GridFS(client[db_name + '_FS'])

v = db['V']
v.drop_indexes()
v.create_index([('x', pymongo.TEXT)])

tags = db['TAGS']
tags.drop_indexes()