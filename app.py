import json

import bson
import datetime

import mongoengine
from bson import ObjectId
from flask import Flask
from flask_mongoengine import MongoEngine
from werkzeug.exceptions import BadRequest
from flask import jsonify, request
from controller import *
import requests

app = Flask(__name__)
app.config['MONGODB_DB'] = 'Portal'
app.config[
    'MONGODB_HOST'] = 'mongodb://admin_remine:WinniePooh8@cluster0-shard-00-00-h4vdb.mongodb.net:27017,cluster0-shard-00-01-h4vdb.mongodb.net:27017,cluster0-shard-00-02-h4vdb.mongodb.net:27017/Portal?replicaSet=Cluster0-shard-0&ssl=true&authSource=admin'
app.config['MONGODB_USERNAME'] = 'admin_remine'
app.config['MONGODB_PASSWORD'] = 'WinniePooh8'
db = MongoEngine()
db.init_app(app)


@app.route('/api/news', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        limit = int(request.args.get('limit', 10))
        skip = int(request.args.get('skip', 0))
        lang = request.args.get('lang', 'en')
        tags = request.args.get('tags', None)
        arg_fields = request.args.get('fields', None)
        fields = []
        if tags:
            tags = [x.strip() for x in tags.split(',')]

        if arg_fields:
            fields = [x.strip() for x in arg_fields.split(',')]


        news = get_all_news(limit, skip, lang, tags, fields)
        if news: news_json = json.loads(news.to_json())
        else: news_json = []

        return jsonify({'response': news_json, 'statusCode': 200}), 200

    elif request.method == 'POST':
        payload = request.json.get('payload', None)
        if payload:
            response = add_news(payload)
            return jsonify({'response': response, 'statusCode': 201}), 201
        else:
            raise BadRequest


@app.route('/api/news/<string:news_id>', methods=['GET', 'PUT', 'DELETE'])
def specific_news(news_id):
    if request.method == 'GET':
        news = json.loads(get_news(news_id).to_json())
        return jsonify({'response':news, 'statusCode': 200})
    elif request.method == 'PUT':
        news_json = request.json['payload']
        affected_row = update_news(news_id, news_json)
        if affected_row > 0:
            return jsonify({'response': 'OK', 'statusCode': 200}), 200
        else:
            return jsonify({'response': 'NOT OK', 'statusCode': 404}), 404

    elif request.method == 'DELETE':
        delete_news(news_id)
        return jsonify({'response': 'OK'}), 200


@app.errorhandler(BadRequest)
def gb_bad_request(e):
    return jsonify({'statusCode': 400, 'response': str(e)}), 400


@app.errorhandler(bson.errors.InvalidId)
def gb_not_found(e):
    return jsonify({'statusCode': 404, 'response': 'Not found'}), 404


@app.errorhandler(mongoengine.errors.FieldDoesNotExist)
def gb_not_found(e):
    return jsonify({'statusCode': 404, 'response': str(e)}), 404


@app.errorhandler(mongoengine.errors.ValidationError)
def gb_not_validation_err(e):
    return jsonify({'statusCode': 500, 'response': str(e)}), 500


@app.errorhandler(mongoengine.errors.InvalidQueryError)
def gb_not_invalid(e):
    return jsonify({'statusCode': 500, 'response': str(e)}), 500


def is_valid_id(_id):
    return len(_id) == 24 and _id is not None


def send_request(URL, method, json):
    result = {}
    if method == 'GET':
        result = requests.get(URL, json=json)
    elif method == 'POST':
        result = requests.post(URL, json=json)
    elif method == 'PUT':
        result = requests.put(URL, json=json)
    elif method == 'DELETE':
        result = requests.delete(URL, json=json)
    return jsonify(result.json()), result.status_code


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5003)
