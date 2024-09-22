
from pymongo import MongoClient
import pandas as pd

uri = "mongodb+srv://emessonsilva:uVhLRgl9mqGeGsRZ@clashroyale.ctakw.mongodb.net/?retryWrites=true&w=majority&appName=clashroyale"
client = MongoClient(uri)

# Acessar o banco de dados
db = client['clashroyale']

# Carregar o arquivo CSV de cartas
cards_df = pd.read_csv('cardlist.csv')

# Carregar o arquivo CSV de batalhas
battles_df = pd.read_csv('clash_royale_battles.csv')

# Obter as coleções MongoDB
cards_collection = db['cards']
battles_collection = db['battles']

# Inserir os dados de cartas no MongoDB
cards_data = cards_df.to_dict(orient='records')
cards_collection.insert_many(cards_data)

# Inserir os dados de batalhas no MongoDB
battles_data = battles_df.to_dict(orient='records')
battles_collection.insert_many(battles_data)

print("Dados inseridos com sucesso!")
