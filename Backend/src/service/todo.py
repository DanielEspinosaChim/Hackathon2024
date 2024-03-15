from flask import request, Response
from config.mongodb import mongo  # Importación correcta de la instancia configurada
from bson import ObjectId, json_util, objectid
def create_todo_services():
    data = request.get_json()
    title = data.get('title', None)
    description = data.get('description', None)
    
    if title:
        response = mongo.db.todos.insert_one({'title': title, 'description': description, 'done': False})
        result = {'id': str(response.inserted_id), 'title': title, 'description': description, 'done': False}
        return result
    else:
        return {'message': 'title is required'}, 400

def get_todos_services():
    data = mongo.db.todos.find()
    result = json_util.dumps(data)
    return Response(result, mimetype='application/json')  # Asegúrate de que 'mimetype' sea correcto

def get_todo_services(id):
    data = mongo.db.todos.find_one({'_id': ObjectId(id)})
    result = json_util.dumps(data)
    return Response(result, mimetype='application/json')  # Asegúrate de que 'mimetype' sea correcto

def update_todo_services(id):
    data = request.get_json()
    if len(data) > 0:
        return 'invalid request', 400
    response = mongo.db.todos.update_one({'_id': ObjectId(id)}, {'$set': data})
    
    if response.modified_count >= 1:
        return 'updated successfully', 200
    else:
        return 'no todo found', 404
    
def delete_todo_services(id):
    response = mongo.db.todos.delete_one({'_id': ObjectId(id)})
    if response.deleted_count >= 1:
        return 'deleted successfully', 200
    else:
        return 'no todo found', 404