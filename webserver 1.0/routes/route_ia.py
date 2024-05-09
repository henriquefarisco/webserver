from flask import Blueprint, render_template, request

ia_bp = Blueprint('ia', __name__)

@ia_bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Aqui você poderia por exemplo processar dados e retornar resultados de um modelo de IA
        pass
    return render_template('inteligencia_artificial.html')
