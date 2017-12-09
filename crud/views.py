from rest import Crud


def register_all(app):
    for attr in globals().values():
        if isinstance(attr, Crud):
            app.register_blueprint(attr.blue, url_prefix='/' + attr.plural_form)

video = Crud('video', 'v')
from crud.video import load_v
video.load_document = load_v
video.crud()
tag = Crud('tag', 'tags')
tag.crud()