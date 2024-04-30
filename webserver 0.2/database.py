import sqlite3
import os
import bcrypt

DATABASE_PATH = 'database/users.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists('database'):
        os.mkdir('database')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            sobrenome TEXT NOT NULL,
            login TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            grupo TEXT NOT NULL,
            ativo INTEGER DEFAULT 1
        );
    ''')
    admin_exists = cursor.execute('SELECT COUNT(*) FROM users WHERE grupo = "Administrador"').fetchone()[0]
    if admin_exists == 0:
        print("Nenhum administrador encontrado, adicionando um usuário administrador padrão...")
        hashed_password = bcrypt.hashpw('admin'.encode('utf-8'), bcrypt.gensalt())
        cursor.execute('INSERT INTO users (nome, sobrenome, login, senha, grupo, ativo) VALUES (?, ?, ?, ?, ?, ?)', 
                       ('Admin', 'User', 'admin', hashed_password, 'Administrador', 1))
        conn.commit()
    conn.close()

init_db()
