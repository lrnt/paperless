import json

from os import path

from flask import Flask, render_template, request, abort, Response
from flask.views import MethodView

from db import DB, DoesNotExist
from settings import TAG_DEFINITIONS

static_assets_path = path.join(path.dirname(__file__), 'dist')
app = Flask(__name__, static_folder=static_assets_path)
db = DB()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dist/<path:asset_path>')
def send_static(asset_path):
    return send_from_directory(static_assets_path, asset_path)

class DocumentAPI(MethodView):
    def _doc_or_404(self, key):
        try:
            return db.get(key)
        except DoesNotExist:
            abort(404)

    def get(self, key):
        if key is not None:
            document = self._doc_or_404(key)
            with open(document.original_document_path, 'rb') as f:
                return Response(f.read(), mimetype='application/pdf')

        q = request.args.get('q', '')
        t = request.args.getlist('t')
        entries = db.filter(text=q, tags=t)

        return Response(json.dumps([entry.metadata for entry in entries]),
                        mimetype='application/json')

    def patch(self, key):
        document = self._doc_or_404(key)
        document.metadata.update(request.get_json())
        document.write_metadata()
        return Response(json.dumps(document.metadata),
                        mimetype='application/json')


class TagAPI(MethodView):
    def get(self, key):
        tags = {tag: TAG_DEFINITIONS[tag]['color'] for tag in TAG_DEFINITIONS}
        return Response(json.dumps(tags), mimetype='application/json')


if __name__ == '__main__':
    document_view = DocumentAPI.as_view('document_api')
    tag_view = TagAPI.as_view('tag_api')
    app.add_url_rule('/tags/', defaults={'key': None},
                     view_func=tag_view, methods=['GET'])
    app.add_url_rule('/documents/', defaults={'key': None},
                     view_func=document_view, methods=['GET'])
    app.add_url_rule('/documents/<key>', view_func=document_view,
                     methods=['GET', 'PATCH'])
    app.debug = True
    app.run(port=9090)
