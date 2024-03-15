from flask import Flask, render_template,  jsonify
from dotenv import load_dotenv
import os
from config.mongodb import mongo  # Asegúrate de que esta es la importación correcta
from routes.todo import todo
from flask_cors import CORS
load_dotenv()
app = Flask(__name__)
CORS(app)
app.config['MONGO_URI'] = 'mongodb+srv://danyespinosachim:hackathon2024@cluster0.dsm2hwk.mongodb.net/hackathondb?retryWrites=true&w=majority&appName=Cluster0'
mongo.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

app.register_blueprint(todo, url_prefix='/todo')  # Asegúrate de que '/todo' es correcto

@app.route('/api/data')
def get_data():
    return jsonify({'data': 'Hello from Flask!'})

if __name__ == "__main__":
    app.run(debug=True)
  
