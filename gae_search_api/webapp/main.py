import logging

from flask import Flask, render_template, request
from flask.json import jsonify

from google.appengine.ext import deferred

from search_api import SearchAPI

app = Flask(__name__)

search_client = SearchAPI()


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
    """gets data for one product and saves into search index"""
    json_data = request.get_json()
    search_client.insert(json_data)
    return 'ok'


@app.route('/upload_bulk', methods=['POST'])
def upload_bulk():
    """gets list of products and saves into search index"""
    json_data = request.get_json()
    logging.info("received {} items".format(len(json_data)))
    search_client.insert_bulk(json_data)
    return 'ok'


@app.route('/delete')
def delete():
    """deletes all items in search"""
    deferred.defer(search_client.delete_all)
    return 'ok'
