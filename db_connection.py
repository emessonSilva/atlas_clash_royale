
from pymongo import MongoClient
import pandas as pd

uri = "mongodb+srv://emessonsilva:uVhLRgl9mqGeGsRZ@clashroyale.ctakw.mongodb.net/?retryWrites=true&w=majority&appName=clashroyale"
client = MongoClient(uri)

# Acessar o banco de dados
db = client['clashroyale']

# Carregar o arquivo CSV de batalhas
battles_df = pd.read_csv('clash_royale_battles.csv')

# Obter a coleção do MongoDB
battles_collection = db['battles']


# Inserir os dados de batalhas no MongoDB
battles_data = battles_df.to_dict(orient='records')
battles_collection.insert_many(battles_data)

# print("Dados inseridos com sucesso!")


