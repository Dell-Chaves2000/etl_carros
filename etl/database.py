from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

def get_database():
    # Conectar ao MongoDB
    CONNECTION_STRING = os.getenv("MONGO_URI")
    client = MongoClient(CONNECTION_STRING)
    return client['carros_db']
