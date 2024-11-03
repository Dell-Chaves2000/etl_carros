from flask import Blueprint, render_template, request, redirect, url_for
from pymongo import MongoClient
from etl.database import get_database
import math

main = Blueprint('main', __name__)

@main.route("/", methods=['GET', 'POST'])
def index():
    db = get_database()
    collection = db['carros']

    # Obter montadoras e anos do banco para preencher os inputs
    montadoras = collection.distinct('montadora')
    anos = collection.distinct('ano')

    # Variáveis de controle de paginação
    carros_por_pagina = 60  # Máximo de carros por página (15 carros por coluna, 4 colunas)
    max_colunas = 4  # Limite de colunas por página
    pagina_atual = int(request.args.get('pagina', 1))  # Página atual da requisição

    # Inicializar variáveis de montadora e ano para exibição no template
    montadora_selecionado = request.args.get('montadora', None)
    ano_selecionado = request.args.get('ano', None)
    carros_unicos = []
    total_modelos = 0

    # Filtragem dos dados
    if request.method == 'POST':
        montadora_selecionado = request.form.get('montadora')
        ano_selecionado = request.form.get('ano')
        return redirect(url_for('main.index', montadora=montadora_selecionado, ano=ano_selecionado, pagina=1))

    if montadora_selecionado and ano_selecionado:
        # Verifique se o ano está armazenado como string ou int e ajuste a consulta
        try:
            query = {"montadora": montadora_selecionado, "ano": int(ano_selecionado)}
        except ValueError:
            query = {"montadora": montadora_selecionado, "ano": ano_selecionado}

        # Agora vamos buscar todos os documentos que correspondem ao fabricante e ano selecionados
        carros = list(collection.find(query))

        # Iterar sobre os documentos e extrair todos os modelos dos arrays
        for carro in carros:
            for modelo in carro.get('modelos', []):  # Para cada modelo no array 'modelos'
                if 'modelo' in modelo:
                    carros_unicos.append({"modelo": modelo['modelo'], "montadora": carro['montadora'], "ano": carro['ano']})

        # Remover duplicadas
        carros_unicos = list({carro['modelo']: carro for carro in carros_unicos}.values())
        total_modelos = len(carros_unicos)

        # Implementar a paginação
        inicio = (pagina_atual - 1) * carros_por_pagina
        fim = inicio + carros_por_pagina
        modelos_paginados = carros_unicos[inicio:fim]
        total_paginas = math.ceil(total_modelos / carros_por_pagina)

        # Organizar os carros em colunas para exibição
        colunas = []
        num_colunas = max(1, math.ceil(len(modelos_paginados) / 15))  # Cada coluna terá no máximo 15 modelos

        for i in range(num_colunas):
            colunas.append(modelos_paginados[i * 15:(i + 1) * 15])

        # Restringir o número de colunas a 4
        colunas = colunas[:max_colunas]

        # Renderizar a página com os modelos, total de modelos e a paginação
        return render_template(
            'index.html',
            montadoras=montadoras,
            anos=anos,
            colunas=colunas,
            total_modelos=total_modelos,
            pagina_atual=pagina_atual,
            total_paginas=total_paginas,
            montadora_selecionado=montadora_selecionado,
            ano_selecionado=ano_selecionado
        )

    # Exibir a página inicial sem filtro
    return render_template('index.html', montadoras=montadoras, anos=anos)
