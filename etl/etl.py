import pandas as pd
from pymongo import MongoClient
from database import get_database

def etl_process():
    # Ler o arquivo CSV
    df = pd.read_csv('./data/veiculos.csv')

    # Remover linhas vazias ou irrelevantes
    df = df.dropna(subset=['make', 'year', 'model'])

    # Renomear colunas para português
    df.rename(columns={'make': 'montadora', 'year': 'ano', 'model': 'modelo'}, inplace=True)

    # Conectar ao MongoDB
    db = get_database()

    # Agrupar por fabricante e ano
    carros_agrupados = df.groupby(['montadora', 'ano']).apply(lambda x: x.to_dict('records')).reset_index()

    # Inserir no banco de dados
    collection = db['carros']
    collection.delete_many({})  # Limpar coleção antes de inserir novos dados
    for _, row in carros_agrupados.iterrows():
        document = {
            'montadora': row['montadora'],
            'ano': row['ano'],
            'modelos': row[0]  # Lista de modelos
        }
        collection.insert_one(document)

    print("ETL concluído e dados inseridos no MongoDB.")

if __name__ == "__main__":
    etl_process()
