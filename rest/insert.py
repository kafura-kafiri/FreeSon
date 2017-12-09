from flask import request, render_template
from tools.utility import request_json, str2obj, obj2str, dot_notation
from bson import ObjectId
import datetime


def raw(_id):
    raw_document = {}
    if _id:
        raw_document['_id'] = ObjectId(_id)
    raw_document['_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    return raw_document


def add_insertion(crud):
    @crud.blue.route('/+.html', methods=['GET', 'POST'])
    @crud.blue.route('/<_id>+.html', methods=['GET', 'POST'])
    def create_page(_id=None):
        return render_template(crud.singular_form + '/+.html')

    @crud.blue.route('/+', methods=['GET', 'POST'])
    @crud.blue.route('/<_id>+', methods=['GET', 'POST'])
    def create(_id=None):
        _ = raw(_id)
        default = crud.default
        _json = request_json(request)
        _ = {**_, **default}
        _ = {**_, **_json}
        result = crud.collection.insert_one(str2obj(_))
        _ = crud._on_insert(_)
        return str(result.inserted_id)
    crud.create = create