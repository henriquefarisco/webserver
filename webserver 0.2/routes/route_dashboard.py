from flask import Blueprint, render_template, session, redirect, url_for

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login.login'))  # Redireciona para o login se não estiver logado
    return render_template('dashboard.html', grupo=session.get('grupo'))
