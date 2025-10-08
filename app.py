from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# --- CONEXIÓN CON MYSQL ---
def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin123",
        database="cloud"
    )


# --- RUTAS DE USUARIOS ---
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(usuarios)


@app.route('/usuarios', methods=['POST'])
def crear_usuario():
    datos = request.json
    nombre = datos.get('nombre')
    celular = datos.get('celular')
    correo = datos.get('correo')

    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO usuarios (nombre, celular, correo) VALUES (%s, %s, %s)",
                   (nombre, celular, correo))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Usuario creado correctamente"}), 201


@app.route('/usuarios/<int:id_usuario>', methods=['PUT'])
def actualizar_usuario(id_usuario):
    datos = request.json
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE usuarios SET nombre=%s, celular=%s, correo=%s WHERE id=%s",
        (datos['nombre'], datos['celular'], datos['correo'], id_usuario)
    )
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Usuario actualizado correctamente"})


@app.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
def eliminar_usuario(id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id=%s", (id_usuario,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Usuario eliminado correctamente"})


# --- RUTAS DE MASCOTAS ---
@app.route('/mascotas', methods=['GET'])
def obtener_mascotas():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("""
        SELECT m.id, m.nombre, m.raza, m.vacunado, m.motivo_consulta, u.nombre AS dueño
        FROM mascotas m
        JOIN usuarios u ON m.id_usuario = u.id
    """)
    mascotas = cursor.fetchall()
    cursor.close()
    conexion.close()
    return jsonify(mascotas)


@app.route('/mascotas', methods=['POST'])
def crear_mascota():
    datos = request.json
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO mascotas (nombre, raza, vacunado, motivo_consulta, id_usuario)
        VALUES (%s, %s, %s, %s, %s)
    """, (datos['nombre'], datos['raza'], datos['vacunado'], datos['motivo_consulta'], datos['id_usuario']))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Mascota registrada correctamente"}), 201


@app.route('/mascotas/<int:id_mascota>', methods=['PUT'])
def actualizar_mascota(id_mascota):
    datos = request.json
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE mascotas
        SET nombre=%s, raza=%s, vacunado=%s, motivo_consulta=%s
        WHERE id=%s
    """, (datos['nombre'], datos['raza'], datos['vacunado'], datos['motivo_consulta'], id_mascota))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Mascota actualizada correctamente"})


@app.route('/mascotas/<int:id_mascota>', methods=['DELETE'])
def eliminar_mascota(id_mascota):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM mascotas WHERE id=%s", (id_mascota,))
    conexion.commit()
    cursor.close()
    conexion.close()
    return jsonify({"mensaje": "Mascota eliminada correctamente"})

if __name__ == '__main__':
    app.run(debug=True)
