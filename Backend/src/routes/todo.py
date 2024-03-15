from flask import Blueprint
from service.todo import create_todo_services
todo = Blueprint('todo', __name__)

@todo.route('/', methods=['GET'])
def get_todos():
    return 'get all todos'

@todo.route('/<int:id>', methods=['GET'])
def get_todo(id):
    return f'get todo by id {id}'

@todo.route('/', methods=['POST'])
def create_todo():
    return create_todo_services()

@todo.route('/<int:id>', methods=['PUT'])
def update_todo(id):
    return f'update todo with id {id}'

@todo.route('/<int:id>', methods=['DELETE'])
def delete_todo(id):
    return f'delete todo with id {id}'

@todo.route('/test', methods=['GET'])
def test():
    return "Test route within todo Blueprint"