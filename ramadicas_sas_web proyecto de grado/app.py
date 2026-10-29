from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "ramadicas.db"

app = Flask(__name__)
app.secret_key = "cambia-esta-clave-local-antes-de-publicar"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS encuestas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                area TEXT NOT NULL,
                antiguedad TEXT NOT NULL,
                satisfaccion INTEGER NOT NULL CHECK(satisfaccion BETWEEN 1 AND 5),
                herramientas TEXT NOT NULL,
                comentarios TEXT,
                fecha DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

@app.route("/", methods=["GET"])
def index():
    with get_db() as conn:
        total = conn.execute("SELECT COUNT(*) FROM encuestas").fetchone()[0]
        por_area = conn.execute("""
            SELECT area AS etiqueta, COUNT(*) AS cantidad
            FROM encuestas GROUP BY area ORDER BY cantidad DESC
        """).fetchall()
        por_satisfaccion = conn.execute("""
            SELECT CAST(satisfaccion AS TEXT) || ' de 5' AS etiqueta, COUNT(*) AS cantidad
            FROM encuestas GROUP BY satisfaccion ORDER BY satisfaccion
        """).fetchall()
        por_antiguedad = conn.execute("""
            SELECT antiguedad AS etiqueta, COUNT(*) AS cantidad
            FROM encuestas GROUP BY antiguedad ORDER BY cantidad DESC
        """).fetchall()
        recientes = conn.execute("""
            SELECT nombre, area, satisfaccion, fecha
            FROM encuestas ORDER BY id DESC LIMIT 8
        """).fetchall()
    return render_template(
        "index.html",
        total=total,
        por_area=[dict(r) for r in por_area],
        por_satisfaccion=[dict(r) for r in por_satisfaccion],
        por_antiguedad=[dict(r) for r in por_antiguedad],
        recientes=recientes
    )

@app.route("/guardar", methods=["POST"])
def guardar():
    nombre = request.form.get("nombre", "").strip()
    area = request.form.get("area", "").strip()
    antiguedad = request.form.get("antiguedad", "").strip()
    herramientas = request.form.get("herramientas", "").strip()
    comentarios = request.form.get("comentarios", "").strip()
    try:
        satisfaccion = int(request.form.get("satisfaccion", ""))
    except ValueError:
        satisfaccion = 0

    areas_validas = {"Administración", "Operaciones", "Ventas", "Logística", "Tecnología", "Otro"}
    antiguedades_validas = {"Menos de 6 meses", "6 meses a 2 años", "2 a 5 años", "Más de 5 años"}
    herramientas_validas = {"Correo y hojas de cálculo", "Software de gestión", "Sistemas internos", "Otras"}
    if (not nombre or area not in areas_validas or antiguedad not in antiguedades_validas
            or herramientas not in herramientas_validas or not 1 <= satisfaccion <= 5):
        flash("Revisa los campos obligatorios e intenta de nuevo.", "error")
        return redirect(url_for("index"))

    with get_db() as conn:
        conn.execute("""
            INSERT INTO encuestas (nombre, area, antiguedad, satisfaccion, herramientas, comentarios)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nombre, area, antiguedad, satisfaccion, herramientas, comentarios[:1000]))
    flash("¡Encuesta guardada! Las gráficas se actualizaron.", "success")
    return redirect(url_for("index"))

@app.route("/privacidad")
def privacidad():
    return render_template("privacidad.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
