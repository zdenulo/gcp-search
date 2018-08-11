from flask import Flask, render_template, request
from flask.json import jsonify
from spanner_search import SpannerSearch

app = Flask(__name__)

search_client = SpannerSearch()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search')
def search():
    """based on user query it executes search and returns list of item in json"""
    query = request.args.get('query', '')
    results = search_client.search(query)
    return jsonify(results)


@app.route('/upload', methods=['POST'])
def upload():
    """gets list of products and saves into search index"""
    data = request.get_json()
    search_client.insert_bulk(data)
    return 'ok'


@app.route('/delete')
def delete():
    """deletes all items in search"""
    search_client.delete_all()
    return 'ok'


@app.route('/init')
def init():
    """creates database and table for spanner into which data will be uploaded"""
    search_client.init_schema()
    return 'ok'
