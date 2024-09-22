from pymongo import MongoClient
from datetime import datetime

uri = "mongodb+srv://emessonsilva:uVhLRgl9mqGeGsRZ@clashroyale.ctakw.mongodb.net/?retryWrites=true&w=majority&appName=clashroyale"

# Conectar ao MongoDB Atlas
client = MongoClient(uri) 

# Acesse o banco de dados e a collection
battles_collection = client['clashroyale']['battles']

def calculate_win_loss_percentage_per_battle(card_id):
    """
    Calcula a porcentagem de vitórias e derrotas envolvendo a carta especificada em cada partida.

    """
    # todas as batalhas que envolvem a carta
    battles = battles_collection.find({
        "$or": [
            {"p1c1": card_id}, {"p1c2": card_id}, {"p1c3": card_id}, {"p1c4": card_id},
            {"p1c5": card_id}, {"p1c6": card_id}, {"p1c7": card_id}, {"p1c8": card_id},
            {"p2c1": card_id}, {"p2c2": card_id}, {"p2c3": card_id}, {"p2c4": card_id},
            {"p2c5": card_id}, {"p2c6": card_id}, {"p2c7": card_id}, {"p2c8": card_id}
        ]
    })

    total_battles = 0
    wins = 0

    for battle in battles:
        total_battles += 1
        if battle['vencedor'] == battle['nickname_jogador_1'] and card_id in [battle[f'p1c{i}'] for i in range(1, 9)]:
            wins += 1
        elif battle['vencedor'] == battle['nickname_jogador_2'] and card_id in [battle[f'p2c{i}'] for i in range(1, 9)]:
            wins += 1

    # Calcular a porcentagem de vitórias e derrotas
    if total_battles > 0:
        win_percentage = (wins / total_battles) * 100
        loss_percentage = 100 - win_percentage
    else:
        win_percentage = 0
        loss_percentage = 0

    return win_percentage, loss_percentage

card_id = 13 

win_percentage, loss_percentage = calculate_win_loss_percentage_per_battle(card_id)
print(f"Porcentagem de vitórias: {win_percentage:.2f}%")
print(f"Porcentagem de derrotas: {loss_percentage:.2f}%")
