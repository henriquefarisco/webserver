from flask import Flask, render_template
from routes.route_login import login_bp
from routes.route_dashboard import dashboard_bp
from routes.route_users_adm import gerenciador_usuarios_bp
from database import init_db
from routes.route_drive import drive_bp
import os
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'
app.config['MAX_CONTENT_LENGTH'] = None
socketio = SocketIO(app)

# Registro dos blueprints
app.register_blueprint(login_bp)
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(gerenciador_usuarios_bp, url_prefix='/')
app.register_blueprint(drive_bp, url_prefix='/drive')

# Assegura que o banco de dados está inicializado
init_db()

def is_directory(path):
    """Verifica se um caminho é um diretório."""
    return os.path.isdir(os.path.join(app.config['UPLOAD_FOLDER'], path))

@socketio.on('connect')
def test_connect():
    emit('my_response', {'data': 'Connected'})

@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')

@app.route('/')
def home():
    return render_template('home.html')  # Deve mostrar a página inicial
app.jinja_env.tests['directory'] = is_directory

if __name__ == '__main__':
    app.run(debug=True)
