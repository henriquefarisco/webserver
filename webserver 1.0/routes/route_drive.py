from flask import Blueprint, request, redirect, url_for, render_template, send_from_directory, send_file, abort, flash, jsonify, session
from servicos.service_drive import list_directory_contents, handle_file_upload, create_new_folder, get_user_folder
import os
import zipfile
import io
import shutil

drive_bp = Blueprint('drive', __name__, url_prefix='/drive')

def get_user_folder():
    user_id = get_user_id()  # Você precisará implementar esta função
    return os.path.join('uploads', str(user_id))

def get_user_id():
    # Retorna o user_id baseado na sessão do usuário, você deve ajustar conforme sua implementação
    return session.get('user_id')

@drive_bp.route('/', defaults={'subpath': ''})
@drive_bp.route('/<path:subpath>')
def drive_index(subpath):
    files = list_directory_contents(subpath)
    return render_template('drive_index.html', files=files, current_path=subpath)

@drive_bp.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    path = request.form['path']  # Obtém o caminho atual a partir do formulário
    if handle_file_upload(file, path):
        return redirect(url_for('drive.drive_index', subpath=path))
    else:
        return "Falha no upload", 400

@drive_bp.route('/files/<filename>')
def uploaded_file(filename):
    return send_from_directory(get_user_folder(), filename)

@drive_bp.route('/folder', methods=['POST'])
def create_folder():
    folder_name = request.form['folder_name']
    path = request.form['path']  # Obtém o caminho atual a partir do formulário
    if create_new_folder(folder_name, path):
        return redirect(url_for('drive.drive_index', subpath=path))
    else:
        return "Falha ao criar pasta", 400

@drive_bp.route('/upload_folder', methods=['POST'])
def upload_folder():
    files = request.files.getlist('folder')
    base_path = request.form['path']
    errors = []

    for file in files:
        full_path = os.path.join(base_path, file.filename)
        directory = os.path.dirname(full_path)
        if not os.path.exists(os.path.join(get_user_folder(), directory)):
            os.makedirs(os.path.join(get_user_folder(), directory), exist_ok=True)
        if not handle_file_upload(file, directory):
            errors.append(file.filename)

    if errors:
        return "Falha ao enviar os seguintes arquivos: " + ", ".join(errors), 400
    return redirect(url_for('drive.drive_index', subpath=base_path))

@drive_bp.route('/download/<path:path>')
def download(path):
    full_path = os.path.join(get_user_folder(), path)

    if os.path.isdir(full_path):
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(full_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, full_path)
                    zipf.write(file_path, arcname=arcname)
        memory_file.seek(0)
        return send_file(memory_file, download_name=f'{os.path.basename(path)}.zip', as_attachment=True)

    elif os.path.isfile(full_path):
        return send_file(full_path, as_attachment=True)

    else:
        abort(404)

@drive_bp.route('/rename/<path:path>', methods=['POST'])
def rename(path):
    new_name = request.form['new_name']
    old_path = os.path.join(get_user_folder(), path)
    directory = os.path.dirname(path)
    new_path = os.path.join(get_user_folder(), directory, new_name)

    if os.path.exists(new_path):
        return "Erro: um arquivo ou diretório com esse nome já existe.", 400

    os.rename(old_path, new_path)
    return redirect(url_for('drive.drive_index', subpath=directory))

@drive_bp.route('/delete/<path:path>', methods=['POST'])
def delete(path):
    item_path = os.path.join(get_user_folder(), path)
    
    if os.path.exists(item_path):
        try:
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
            flash('Item excluído com sucesso!', 'success')
        except Exception as e:
            flash(f'Erro ao excluir item: {e}', 'error')
        return redirect(url_for('drive.drive_index', subpath=os.path.dirname(path)))
    else:
        flash('Erro: O arquivo ou pasta não existe.', 'error')
        return redirect(url_for('drive.drive_index', subpath=os.path.dirname(path)))

@drive_bp.route('/directory_tree')
def directory_tree():
    user_folder = get_user_folder()
    tree = {}
    for root, dirs, files in os.walk(user_folder):
        for dir in dirs:
            path = os.path.join(root, dir)
            relpath = os.path.relpath(path, user_folder)
            tree[relpath] = {}
    return jsonify(tree)

@drive_bp.route('/move', methods=['POST'])
def move_file():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Nenhum dado JSON fornecido'}), 400

    current_path = data.get('current_path')
    new_path = data.get('new_path')
    if not current_path or not new_path:
        return jsonify({'error': 'Parâmetros necessários estão faltando'}), 400

    user_folder = get_user_folder()
    source_path = os.path.join(user_folder, current_path.strip('/'))
    destination_path = os.path.join(user_folder, new_path.strip('/'))

    # Garantir que o caminho de destino não saia do diretório do usuário
    if not destination_path.startswith(user_folder):
        return jsonify({'error': 'Tentativa de acesso fora do diretório permitido'}), 403

    if os.path.isdir(destination_path):
        destination_path = os.path.join(destination_path, os.path.basename(source_path))

    try:
        shutil.move(source_path, destination_path)
        return jsonify({'message': 'Arquivo movido com sucesso!'}), 200
    except Exception as e:
        print(f"Erro ao mover o arquivo: {e}")
        return jsonify({'error': str(e)}), 500
