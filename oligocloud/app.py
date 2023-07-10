import os

import boto3
from flask import Flask, jsonify, make_response, request

app = Flask(__name__)


dynamodb_client = boto3.client('dynamodb')

if os.environ.get('IS_OFFLINE'):
    dynamodb_client = boto3.client(
        'dynamodb', region_name='localhost', endpoint_url='http://localhost:8000'
    )


TASKS_TABLE = os.environ['TASKS_TABLE']


@app.route('/tasks/<string:task_id>')
def get_task(task_id):
    result = dynamodb_client.get_item(
        TableName=TASKS_TABLE, Key={'taskId': {'S': task_id}}
    )
    item = result.get('Item')
    if not item:
        return jsonify({'error': 'Could not find task with provided "taskId"'}), 404

    return jsonify(
        {'taskId': item.get('taskId').get('S'), 'name': item.get('name').get('S')}
    )


@app.route('/tasks', methods=['POST'])
def create_task():
    task_id = request.json.get('taskId')
    name = request.json.get('name')
    if not task_id or not name:
        return jsonify({'error': 'Please provide both "taskId" and "name"'}), 400

    dynamodb_client.put_item(
        TableName=TASKS_TABLE, Item={'taskId': {'S': task_id}, 'name': {'S': name}}
    )

    return jsonify({'taskId': task_id, 'name': name})


@app.errorhandler(404)
def resource_not_found(e):
    return make_response(jsonify(error='Not found!'), 404)
