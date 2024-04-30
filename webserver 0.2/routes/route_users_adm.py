from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from servicos.service_users_adm import listar_usuarios, adicionar_usuario, editar_usuario, suspender_usuario, get_usuario, ativar_usuario, excluir_usuario, alterar_senha_usuario

gerenciador_usuarios_bp = Blueprint('gerenciador_usuarios', __name__)

@gerenciador_usuarios_bp.route('/dashboard/gerenciamento', methods=['GET', 'POST'])
def gerenciamento():
    if 'user_id' not in session or session.get('grupo') != 'Administrador':
        flash('Acesso negado: apenas administradores.')
        return redirect(url_for('login.login'))
    
    if request.method == 'POST':
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        login = request.form['login']
        senha = request.form['senha']
        grupo = request.form['grupo']
        adicionar_usuario(nome, sobrenome, login, senha, grupo)
        flash('Usuário adicionado com sucesso!')
        return redirect(url_for('.gerenciamento'))

    usuarios = listar_usuarios()
    return render_template('gerenciador_usuarios.html', usuarios=usuarios)

@gerenciador_usuarios_bp.route('/dashboard/editar/<int:user_id>', methods=['GET', 'POST'])
def editar(user_id):
    if 'user_id' not in session or session.get('grupo') != 'Administrador':
        flash('Acesso negado: apenas administradores.')
        return redirect(url_for('login.login'))
    
    usuario = get_usuario(user_id)  # Assume que você tem uma função que busca os dados do usuário pelo ID

    if request.method == 'POST':
        nome = request.form['nome']
        login = request.form['login']
        grupo = request.form['grupo']
        editar_usuario(user_id, nome, login, grupo)
        flash('Usuário atualizado com sucesso!')
        return redirect(url_for('.gerenciamento'))

    return render_template('editar_usuario.html', usuario=usuario)

@gerenciador_usuarios_bp.route('/dashboard/suspender/<int:user_id>', methods=['POST'])
def suspender(user_id):
    if 'user_id' not in session or session.get('grupo') != 'Administrador':
        flash('Acesso negado: apenas administradores.')
        return redirect(url_for('login.login'))

    if not suspender_usuario(user_id):
        flash('Não é possível suspender o único administrador ativo.')
    else:
        flash('Usuário suspenso com sucesso!')
    return redirect(url_for('.gerenciamento'))

@gerenciador_usuarios_bp.route('/dashboard/ativar/<int:user_id>', methods=['POST'])
def ativar(user_id):
    if 'user_id' not in session or session.get('grupo') != 'Administrador':
        flash('Acesso negado: apenas administradores.')
        return redirect(url_for('login.login'))

    ativar_usuario(user_id)
    flash('Usuário ativado com sucesso!')
    return redirect(url_for('.gerenciamento'))

@gerenciador_usuarios_bp.route('/dashboard/excluir/<int:user_id>', methods=['POST'])
def excluir(user_id):
    if 'user_id' not in session or session.get('grupo') != 'Administrador':
        flash('Acesso negado: apenas administradores.')
        return redirect(url_for('login.login'))

    excluir_usuario(user_id)
    flash('Usuário excluído com sucesso!')
    return redirect(url_for('.gerenciamento'))

@gerenciador_usuarios_bp.route('/dashboard/alterar-senha/<int:user_id>', methods=['GET'])
def mostrar_alterar_senha(user_id):
    if 'user_id' not in session or session.get('grupo') != 'Administrador':
        flash('Acesso negado: apenas administradores.')
        return redirect(url_for('login.login'))
    return render_template('alterar_senha.html', user_id=user_id)

@gerenciador_usuarios_bp.route('/dashboard/alterar-senha/<int:user_id>', methods=['POST'])
def alterar_senha(user_id):
    if 'user_id' not in session or session.get('grupo') != 'Administrador':
        flash('Acesso negado: apenas administradores.')
        return redirect(url_for('login.login'))

    nova_senha = request.form['nova_senha']
    if alterar_senha_usuario(user_id, nova_senha):
        flash('Senha atualizada com sucesso!')
    else:
        flash('Erro ao atualizar senha.')
    return redirect(url_for('.gerenciamento'))