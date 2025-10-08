import sqlite3

DB_NAME = "incidencias_app.db"


def create_db():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")

    conn.executescript("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS incidencias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        categoria TEXT NOT NULL,
        estado TEXT CHECK(estado IN ('pendiente', 'cerrado')) DEFAULT 'pendiente',
        prioridad TEXT CHECK(prioridad IN ('baja', 'media', 'alta', 'extrema')),
        usuario_id INTEGER,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        fecha_resolucion TIMESTAMP DEFAULT NULL,
        FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
    );
    """)

    conn.commit()
    conn.close()


# -------------------------------
# Funciones de usuarios
# -------------------------------

def crear_usuario(usuario, email, password_hash):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuarios (usuario, email, password_hash) VALUES (?, ?, ?)",
            (usuario, email, password_hash)
        )
        conn.commit()
        print("✅ Usuario creado correctamente.")
    except sqlite3.IntegrityError:
        print("⚠️ Usuario o correo ya existente.")
    conn.close()


def verificar_usuario(usuario, password_hash):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM usuarios WHERE usuario=? AND password_hash=?",
        (usuario, password_hash)
    )
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


# -------------------------------
# Funciones de incidencias
# -------------------------------

def get_incidencias(estado=None, prioridad=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    sql = """SELECT id, titulo, descripcion, categoria, estado, prioridad, fecha_creacion
             FROM incidencias WHERE 1=1"""
    params = []

    if estado and estado != "Todos":
        sql += " AND estado=?"
        params.append(estado)
    if prioridad and prioridad != "Todos":
        sql += " AND prioridad=?"
        params.append(prioridad)

    cursor.execute(sql, params)
    data = cursor.fetchall()
    conn.close()
    return data


def add_incidencia(titulo, descripcion, categoria, estado, prioridad, usuario_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO incidencias
        (titulo, descripcion, categoria, estado, prioridad, usuario_id)
        VALUES (?, ?, ?, ?, ?, ?)""",
        (titulo, descripcion, categoria, estado, prioridad, usuario_id)
    )
    conn.commit()
    conn.close()


def delete_incidencia(incidencia_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM incidencias WHERE id=?", (incidencia_id,))
    conn.commit()
    conn.close()
