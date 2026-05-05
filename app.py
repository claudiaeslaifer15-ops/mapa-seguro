from flask import Flask, render_template, request, jsonify, redirect
import sqlite3

app = Flask(__name__)

# 🔥 CREAR BASE DE DATOS SI NO EXISTE
def init_db():
    conn = sqlite3.connect('datos.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reportes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lat REAL,
            lng REAL,
            tipo TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# 🏠 RUTA PRINCIPAL
@app.route('/')
def index():
    return render_template('index.html')


# 💾 GUARDAR REPORTE
@app.route('/guardar', methods=['POST'])
def guardar():
    data = request.get_json()

    lat = data['lat']
    lng = data['lng']
    tipo = data['tipo']

    conn = sqlite3.connect('datos.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO reportes (lat, lng, tipo) VALUES (?, ?, ?)",
        (lat, lng, tipo)
    )

    conn.commit()
    conn.close()

    return jsonify({"mensaje": "Reporte guardado correctamente"})


# 📊 OBTENER REPORTES
@app.route('/reportes')
def reportes():
    conn = sqlite3.connect('datos.db')
    cursor = conn.cursor()

    cursor.execute("SELECT lat, lng, tipo FROM reportes")
    datos = cursor.fetchall()

    conn.close()

    lista = []
    for d in datos:
        lista.append({
            "lat": d[0],
            "lng": d[1],
            "tipo": d[2]
        })

    return jsonify(lista)


# 🔐 PANEL ADMIN
@app.route('/admin')
def admin():
    conn = sqlite3.connect('datos.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reportes")
    datos = cursor.fetchall()

    conn.close()

    return render_template('admin.html', datos=datos)


# ❌ ELIMINAR UNO
@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    conn = sqlite3.connect('datos.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM reportes WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return redirect('/admin')


# 🧹 LIMPIAR TODO
@app.route('/limpiar', methods=['POST'])
def limpiar():
    conn = sqlite3.connect('datos.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM reportes")

    conn.commit()
    conn.close()

    return redirect('/admin')


# 🚀 EJECUTAR APP
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)