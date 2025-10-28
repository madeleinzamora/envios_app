from flask import Flask, render_template, request, jsonify
import pyodbc

app = Flask(__name__)

# Conexión a SQL Server
conn_str = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=DESKTOP-7T1T0U7\\SQLEXPRESS;"  # Asegúrate de que este nombre coincida con tu instancia
    "Database=RapidExpress;"
    "Trusted_Connection=yes;"
)

@app.route('/')
def index():
    return render_template('formulario.html')

@app.route('/estados')
def obtener_estados():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT id_estado, nombre_estado FROM Estados")
    estados = [{'id': row.id_estado, 'nombre': row.nombre_estado} for row in cursor.fetchall()]
    conn.close()
    return jsonify(estados)

@app.route('/ciudades', methods=['POST'])
def obtener_ciudades():
    id_estado = request.form['id_estado']
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("EXEC sp_ObtenerCiudadesPorEstado ?", id_estado)
    ciudades = [{'id': row.id_ciudad, 'nombre': row.nombre_ciudad} for row in cursor.fetchall()]
    conn.close()
    return jsonify(ciudades)

@app.route('/registrar', methods=['POST'])
def registrar_envio():
    id_cliente = request.form['id_cliente']
    id_ciudad = request.form['id_ciudad']
    descripcion = request.form['descripcion']

    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    resultado = ''
    salida = cursor.execute("{CALL sp_RegistrarEnvio (?, ?, ?, ?)}", id_cliente, id_ciudad, descripcion, resultado)
    conn.commit()
    conn.close()

    return jsonify({'mensaje': resultado})

if __name__ == '__main__':
    app.run(debug=True)
