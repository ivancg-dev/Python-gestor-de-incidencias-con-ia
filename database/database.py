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
        prioridad TEXT CHECK(prioridad IN ('leve', 'medio', 'grave', 'extremo')),
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

def get_incidencias(estado=None, prioridad=None, fecha_desde=None, fecha_hasta=None):
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
    if fecha_desde:
        sql += " AND date(fecha_creacion) >= date(?)"
        params.append(fecha_desde)
    if fecha_hasta:
        sql += " AND date(fecha_creacion) <= date(?)"
        params.append(fecha_hasta)

    cursor.execute(sql, params)
    data = cursor.fetchall()
    conn.close()
    return data


def get_titulos_y_prioridades(estado=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    sql = """SELECT titulo, prioridad FROM incidencias WHERE 1=1"""
    params = []

    if estado and estado != "Todos":
        sql += " AND estado=?"
        params.append(estado)

    cursor.execute(sql, params)
    data = cursor.fetchall()
    conn.close()
    return data


def get_titulos_y_estados(estado=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    sql = """SELECT titulo, estado FROM incidencias WHERE 1=1"""
    params = []

    if estado and estado != "Todos":
        sql += " AND estado=?"
        params.append(estado)

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
    conn.close()  # ✅ corregido: ya no hay texto sin comentar


def update_estado_incidencia(incidencia_id, nuevo_estado):
    import sqlite3
    from datetime import datetime

    conn = sqlite3.connect("incidencias_app.db")
    cursor = conn.cursor()

    if nuevo_estado.lower() == "cerrado":
        fecha_cierre = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            UPDATE incidencias
            SET estado = ?, fecha_resolucion = ?
            WHERE id = ?
        """, (nuevo_estado, fecha_cierre, incidencia_id))
    else:
        # Si cambia a otro estado, borra la fecha de resolución
        cursor.execute("""
            UPDATE incidencias
            SET estado = ?, fecha_resolucion = NULL
            WHERE id = ?
        """, (nuevo_estado, incidencia_id))

    conn.commit()
    conn.close()


def get_datos_para_graficas(fecha_desde=None, fecha_hasta=None):
    """Devuelve datos filtrados por fechas para generar gráficas."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    sql = """SELECT categoria, estado, fecha_creacion, fecha_resolucion
             FROM incidencias WHERE 1=1"""
    params = []

    if fecha_desde:
        sql += " AND date(fecha_creacion) >= date(?)"
        params.append(fecha_desde)
    if fecha_hasta:
        sql += " AND date(fecha_creacion) <= date(?)"
        params.append(fecha_hasta)

    cursor.execute(sql, params)
    data = cursor.fetchall()
    conn.close()
    return data
