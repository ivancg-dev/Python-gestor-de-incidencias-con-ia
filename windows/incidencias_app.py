import sqlite3

conn = sqlite3.connect("incidencias_app.db")

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
    prioridad TEXT CHECK(prioridad IN ('baja', 'media', 'alta')),
    usuario_id INTEGER,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_resolucion TIMESTAMP DEFAULT NULL,
    
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
);
""")

conn.commit()
conn.close()