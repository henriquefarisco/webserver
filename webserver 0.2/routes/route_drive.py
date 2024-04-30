from flask import Blueprint, request, redirect, url_for, render_template, send_from_directory, send_file, abort, flash
from servicos.service_drive import list_directory_contents, handle_file_upload, create_new_folder, get_user_folder
import os
import zipfile
import io
import shutil


drive_bp = Blueprint('drive', __name__, url_prefix='/drive')

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
        # Ajusta o caminho para incluir a estrutura de diretórios da pasta enviada
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
        # Se for um diretório, compacte e envie como ZIP
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
        # Se for um arquivo, envie diretamente
        return send_file(full_path, as_attachment=True)

    else:
        # Se o caminho não existir
        abort(404)


@drive_bp.route('/rename/<path:path>', methods=['POST'])
def rename(path):
    new_name = request.form['new_name']
    old_path = os.path.join(get_user_folder(), path)
    directory = os.path.dirname(path)  # Use path instead of old_path to get the relative directory
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
                shutil.rmtree(item_path)  # Excluir pasta, mesmo se tiver conteúdo
            else:
                os.remove(item_path)  # Excluir arquivo
            flash('Item excluído com sucesso!', 'success')
        except Exception as e:
            flash(f'Erro ao excluir item: {e}', 'error')
        return redirect(url_for('drive.drive_index', subpath=os.path.dirname(path)))
    else:
        flash('Erro: O arquivo ou pasta não existe.', 'error')
        return redirect(url_for('drive.drive_index', subpath=os.path.dirname(path)))