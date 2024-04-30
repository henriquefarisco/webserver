from database import get_db_connection
import bcrypt

def listar_usuarios():
    conn = get_db_connection()
    usuarios = conn.execute('SELECT id, nome, login, grupo FROM users').fetchall()
    conn.close()
    return usuarios

def adicionar_usuario(nome, sobrenome, login, senha, grupo):
    hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    conn = get_db_connection()
    conn.execute('INSERT INTO users (nome, sobrenome, login, senha, grupo) VALUES (?, ?, ?, ?, ?)',
                 (nome, sobrenome, login, hashed_senha, grupo))
    conn.commit()
    conn.close()

def editar_usuario(user_id, nome, login, grupo):
    conn = get_db_connection()
    conn.execute('UPDATE users SET nome = ?, login = ?, grupo = ? WHERE id = ?', (nome, login, grupo, user_id))
    conn.commit()
    conn.close()

def suspender_usuario(user_id):
    conn = get_db_connection()
    # Verifica quantos administradores ativos existem
    admin_count = conn.execute('SELECT COUNT(*) FROM users WHERE grupo = "Administrador" AND ativo = 1').fetchone()[0]
    usuario = conn.execute('SELECT grupo FROM users WHERE id = ?', (user_id,)).fetchone()

    if usuario['grupo'] == 'Administrador' and admin_count <= 1:
        conn.close()
        return False  # Não permitir suspensão se for o único administrador ativo

    conn.execute('UPDATE users SET ativo = 0 WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    return True

def get_usuario(user_id):
    conn = get_db_connection()
    usuario = conn.execute('SELECT id, nome, login, grupo FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return usuario

def ativar_usuario(user_id):
    conn = get_db_connection()
    conn.execute('UPDATE users SET ativo = 1 WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()

def excluir_usuario(user_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()

def alterar_senha_usuario(user_id, nova_senha):
    hashed_senha = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt())
    try:
        conn = get_db_connection()
        conn.execute('UPDATE users SET senha = ? WHERE id = ?', (hashed_senha, user_id))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False
