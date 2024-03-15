from flask import request
from config.mongodb import mongo  # Importación correcta de la instancia configurada

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
