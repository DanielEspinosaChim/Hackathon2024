from flask import Flask, render_template
from dotenv import load_dotenv
import os
from config.mongodb import mongo  # Asegúrate de que esta es la importación correcta
from routes.todo import todo

load_dotenv()
app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

app.register_blueprint(todo, url_prefix='/todo')  # Asegúrate de que '/todo' es correcto

if __name__ == "__main__":
    app.run(debug=True)
