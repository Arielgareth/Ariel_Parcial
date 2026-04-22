from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def crear_db():
    con = sqlite3.connect("inventario.db")
    cursor = con.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        categoria TEXT NOT NULL,
        precio REAL NOT NULL,
        stock INTEGER NOT NULL
    )
    """)

    con.commit()
    con.close()

crear_db()

def get_db():
    return sqlite3.connect("inventario.db")

# LISTAR
@app.route("/")
def index():
    con = get_db()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    con.close()
    return render_template("index.html", productos=productos)

# FORMULARIO NUEVO
@app.route("/nuevo")
def nuevo():
    return render_template("form.html")

# GUARDAR
@app.route("/guardar", methods=["POST"])
def guardar():
    nombre = request.form["nombre"]
    categoria = request.form["categoria"]
    precio = request.form["precio"]
    stock = request.form["stock"]

    con = get_db()
    cursor = con.cursor()
    cursor.execute("INSERT INTO productos (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)",
                   (nombre, categoria, precio, stock))
    con.commit()
    con.close()
    return redirect("/")

# EDITAR
@app.route("/editar/<int:id>")
def editar(id):
    con = get_db()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM productos WHERE id=?", (id,))
    producto = cursor.fetchone()
    con.close()
    return render_template("form.html", producto=producto)

# ACTUALIZAR
@app.route("/actualizar/<int:id>", methods=["POST"])
def actualizar(id):
    nombre = request.form["nombre"]
    categoria = request.form["categoria"]
    precio = request.form["precio"]
    stock = request.form["stock"]

    con = get_db()
    cursor = con.cursor()
    cursor.execute("""
        UPDATE productos 
        SET nombre=?, categoria=?, precio=?, stock=? 
        WHERE id=?
    """, (nombre, categoria, precio, stock, id))
    con.commit()
    con.close()
    return redirect("/")

# ELIMINAR
@app.route("/eliminar/<int:id>")
def eliminar(id):
    con = get_db()
    cursor = con.cursor()
    cursor.execute("DELETE FROM productos WHERE id=?", (id,))
    con.commit()
    con.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)