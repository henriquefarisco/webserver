import os
from werkzeug.utils import secure_filename
from flask import current_app, session  # Acessar session para user_id

# Caminho base para os diretórios dos usuários
BASE_UPLOAD_FOLDER = 'uploads'

def get_user_folder():
    user_id = session.get('user_id')
    return os.path.join(BASE_UPLOAD_FOLDER, str(user_id))

def list_directory_contents(path):
    """Listar os conteúdos de um diretório em ordem alfanumérica."""
    directory_path = os.path.join(get_user_folder(), path)
    if not os.path.exists(directory_path):
        return []  # Ou outra lógica para lidar com diretórios não encontrados

    files = []
    with os.scandir(directory_path) as entries:
        for entry in entries:
            files.append({
                'name': entry.name,
                'path': os.path.join(path, entry.name),
                'is_dir': entry.is_dir()
            })

    # Ordena os diretórios antes dos arquivos, ambos alfanumericamente
    files.sort(key=lambda x: (not x['is_dir'], x['name'].lower()))
    return files


def handle_file_upload(file, path):
    """Salvar o arquivo no diretório especificado do usuário."""
    if file:
        filename = secure_filename(file.filename)
        save_path = os.path.join(get_user_folder(), path, filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        file.save(save_path)
        return True
    return False

def create_new_folder(folder_name, path):
    """Criar um novo diretório dentro do diretório do usuário."""
    full_path = os.path.join(get_user_folder(), path, secure_filename(folder_name))
    try:
        os.makedirs(full_path, exist_ok=False)  # False para não sobrescrever diretório existente
        return True
    except FileExistsError:
        return False

