from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import bcrypt
from database import get_db_connection

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE login = ? AND ativo = 1', (username,)).fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['senha']):
            session['user_id'] = user['id']
            session['username'] = user['nome']
            session['grupo'] = user['grupo']
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash('Usuário suspenso ou credenciais inválidas.', 'error')  # Adiciona a categoria 'error'
    return render_template('login.html')


@login_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login.login'))
