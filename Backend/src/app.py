from flask import Flask, jsonify, request
from flask_cors import CORS
import mariadb
import sys

app = Flask(__name__)
CORS(app, origins=["http://localhost:8080"])

# Configurar la conexión a MariaDB
config = {
    'host': '10.17.166.53',
    'port': 3306,
    'user': 'poncho',
    'password': 'poncho',
    'database': 'Hackaton'
}

@app.route('/login', methods=['POST'])
def login():
    credentials = request.json
    usuario = credentials.get('usuario')
    contrasena = credentials.get('contrasena')

    if not usuario or not contrasena:
        return jsonify({"message": "Usuario y contraseña son necesarios"}), 400

    try:
        conn = mariadb.connect(**config)
        cur = conn.cursor()
        
        # Cambia la consulta para seleccionar el ID_Profesor y el Nombre
        cur.execute("SELECT ID_Profesor, Nombre FROM Profesor WHERE Usuario = ? AND Contrasena = ?", (usuario, contrasena,))
        teacher = cur.fetchone()
        
        
        cur.execute("SELECT Nombre FROM Administrador WHERE Usuario = ? AND Contrasena = ?", (usuario, contrasena,))
        administrator = cur.fetchone()

        if teacher:
            profesor_id, teacher_name = teacher  # Desempaqueta correctamente el resultado de la consulta
            return jsonify({
                "message": "Login successful",
                "role": "Teacher",
                "name": teacher_name,
                "profesor_id": profesor_id
            }), 200
        elif administrator:
            # Obtener el nombre del administrador desde la consulta SQL
            admin_name = administrator[0]
            return jsonify({"message": "Login successful", "role": "Administrator", "name": admin_name}), 200
        else:
            return jsonify({"message": "Usuario o contraseña inválidos"}), 401

    except mariadb.Error as e:
        print(f"Error conectando a MariaDB: {e}")
        return jsonify({"message": "Error de conexión a la base de datos"}), 500
    finally:
        cur.close()
        conn.close()

                
@app.route('/api/data')
def get_api_data():
    # Mensaje de prueba para esta ruta
    return jsonify({"message": "Datos desde Flask por /api/data!"})

@app.route('/')
def get_root():
    try:
        # Conexión a la base de datos
        conn = mariadb.connect(**config)
        cur = conn.cursor()

        # Ejecución de una consulta SQL
        cur.execute("SELECT * FROM Administrador;")  # Asegúrate de que esta consulta sea relevante para tu base de datos
        rows = cur.fetchall()

        # Convertir los resultados en una lista de diccionarios
        results = []
        for row in rows:
            # Ajusta esto según la estructura de tu tabla
            results.append({"columna1": row[0], "columna2": row[1], "columna3": row[2]})

        cur.close()
        conn.close()

        return jsonify(results)
    except mariadb.Error as e:
        print(f"Error conectando a MariaDB: {e}")
        sys.exit(1)
        
@app.route('/api/asignaturas', methods=['GET'])
def get_asignaturas():
    try:
        conn = mariadb.connect(**config)
        cur = conn.cursor()

        cur.execute("SELECT Nombre FROM Asignatura;")
        asignaturas = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return jsonify([asignatura[0] for asignatura in asignaturas])
    except mariadb.Error as e:
        print(f"Error conectando a MariaDB: {e}")
        return jsonify({"message": "Error de conexión a la base de datos"}), 500

@app.route('/api/aulas', methods=['GET'])
def get_aulas():
    try:
        conn = mariadb.connect(**config)
        cur = conn.cursor()

        cur.execute("SELECT Nombre FROM Aula;")
        aulas = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return jsonify([aula[0] for aula in aulas])
    except mariadb.Error as e:
        print(f"Error conectando a MariaDB: {e}")
        return jsonify({"message": "Error de conexión a la base de datos"}), 500
    
@app.route('/api/disponibilidad', methods=['POST'])
def update_availability():
    data = request.json
    print("Received data:", data)  # Log the data to the console
    
    # Extracting 'profesor_id' from the received data
    profesor_id = data.get('profesor_id')
    if profesor_id is None:
        print("Error: 'profesor_id' is required.")
        return jsonify({"message": "'profesor_id' is required"}), 400
    
    # Attempt to convert 'profesor_id' to an integer
    try:
        profesor_id = int(profesor_id)
    except ValueError as e:
        print(f"Error converting 'profesor_id' to int: {e}")
        return jsonify({"message": "'profesor_id' must be an integer"}), 400
    
    # Extracting 'disponibilidad' and 'nombramiento' from the received data
    disponibilidad = data.get('disponibilidad')
    nombramiento = data.get('nombramiento')

    # Checking if 'disponibilidad' is a dictionary
    if not isinstance(disponibilidad, dict):
        print("Error: 'disponibilidad' must be a dictionary.")
        return jsonify({"message": "'disponibilidad' must be a dictionary"}), 400

    # Checking if 'nombramiento' is provided
    if nombramiento is None:
        print("Error: 'nombramiento' is None.")
        return jsonify({"message": "'nombramiento' is required"}), 400

    # Connecting to the database and updating availability
    try:
        conn = mariadb.connect(**config)
        cur = conn.cursor()

        # Deleting existing entries for the professor in the 'Disponibilidad' table
        delete_query = "DELETE FROM Disponibilidad WHERE profesor_id = ?"
        cur.execute(delete_query, (profesor_id,))

        # Inserting new availability data into the 'Disponibilidad' table
        for day, hours in disponibilidad.items():
            for hour_range in hours:
                start_time, end_time = hour_range.split(" - ")
                insert_query = """
                INSERT INTO Disponibilidad (profesor_id, dia, hora_inicio, hora_fin) 
                VALUES (?, ?, ?, ?)
                """
                cur.execute(insert_query, (profesor_id, day, start_time, end_time))
        
        # Updating 'nombramiento' if necessary (you need to update this with the correct table and column names)
        # Assuming that the 'nombramiento' column exists in a table that is related to 'profesor_id'
        update_nombramiento_query = """
        UPDATE Profesor 
        SET Horas_Nombramiento = ? 
        WHERE ID_Profesor = ?
        """
        cur.execute(update_nombramiento_query, (nombramiento, profesor_id))

        conn.commit()
        return jsonify({"message": "Disponibilidad y nombramiento actualizados correctamente"}), 200
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        return jsonify({"message": "Database connection error"}), 500
    finally:
        cur.close()
        conn.close()



if __name__ == '__main__':
    app.run(debug=True)
