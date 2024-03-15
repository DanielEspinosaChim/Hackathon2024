from flask import Blueprint
from service.todo import create_todo_services, get_todos_services, get_todo_services, update_todo_services, delete_todo_services
todo = Blueprint('todo', __name__)

@todo.route('/', methods=['GET'])
def get_todos():
    return get_todos_services()

@todo.route('/<id>', methods=['GET'])
def get_todo(id):
    return get_todo_services(id)

@todo.route('/', methods=['POST'])
def create_todo():
    return create_todo_services()

@todo.route('/<id>', methods=['PUT'])
def update_todo(id):
    return update_todo_services(id)

@todo.route('/<id>', methods=['DELETE'])
def delete_todo(id):
    return delete_todo_services(id)

@todo.route('/test', methods=['GET'])
def test():
    return "Test route within todo Blueprint"