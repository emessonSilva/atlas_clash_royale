from datetime import datetime
from db_connection import client

# acessa o banco de dados e a collection
battles_collection = client['clashroyale']['battles']


# Consulta para calcular a porcentagem de vitórias e derrotas de uma carta nas batalhas

"""

Primeiro, o $match filtra as batalhas que incluem a carta identificada por card_id, verificando se ela aparece nas cartas dos jogadores. 
O $or permite que a consulta encontre documentos que atendam a pelo menos uma das condições listadas.
Em seguida, o $group agrupa os documentos filtrados, contando o total de batalhas (total_battles) através do $sum, que soma 1 para cada documento que passa pelo filtro. 
As vitórias (wins) são contabilizadas usando o $cond, que verifica se o vencedor da batalha é um dos jogadores que usaram a carta. 
O primeiro $cond utiliza o operador $eq para comparar o campo "$vencedor" com o nome do jogador correspondente. Se essa condição for verdadeira, 
um segundo $cond verifica se a carta está entre as cartas do jogador, utilizando o operador $in. Se a carta estiver presente, soma 1; caso contrário, soma 0. 
Por fim, o $project constrói a saída, excluindo o campo "_id" e calculando as porcentagens de vitórias e derrotas. 
A porcentagem de vitórias é dada por ($wins / $total_battles) * 100, enquanto a de derrotas é calculada subtraindo a porcentagem de vitórias de 100. 

"""

print('Porcentagem de Vitórias e Derrotas por Carta\n')

card_id = 10  

percentages = battles_collection.aggregate([
    {
        "$match": {
            "$or": [
                {"p1c1": card_id}, {"p1c2": card_id}, {"p1c3": card_id}, {"p1c4": card_id},
                {"p1c5": card_id}, {"p1c6": card_id}, {"p1c7": card_id}, {"p1c8": card_id},
                {"p2c1": card_id}, {"p2c2": card_id}, {"p2c3": card_id}, {"p2c4": card_id},
                {"p2c5": card_id}, {"p2c6": card_id}, {"p2c7": card_id}, {"p2c8": card_id}
            ]
        }
    },
    {
        "$group": {
            "_id": None,
            "total_battles": {"$sum": 1},
            "wins": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$vencedor", "$nickname_jogador_1"]},
                        {
                            "$cond": [
                                {"$in": [card_id, ["$p1c1", "$p1c2", "$p1c3", "$p1c4", "$p1c5", "$p1c6", "$p1c7", "$p1c8"]]},
                                1,
                                0
                            ]
                        },
                        {
                            "$cond": [
                                {"$eq": ["$vencedor", "$nickname_jogador_2"]},
                                {
                                    "$cond": [
                                        {"$in": [card_id, ["$p2c1", "$p2c2", "$p2c3", "$p2c4", "$p2c5", "$p2c6", "$p2c7", "$p2c8"]]},
                                        1,
                                        0
                                    ]
                                },
                                0
                            ]
                        }
                    ]
                }
            }
        }
    },
    {
        "$project": {
            "_id": 0,
            "win_percentage": {
                "$multiply": [{"$divide": ["$wins", "$total_battles"]}, 100]
            },
            "loss_percentage": {
                "$subtract": [100, {"$multiply": [{"$divide": ["$wins", "$total_battles"]}, 100]}]
            }
        }
    }
])

result = list(percentages)

if result:
    print(f"Porcentagem de vitórias: {result[0]['win_percentage']:.2f}%")
    print(f"Porcentagem de derrotas: {result[0]['loss_percentage']:.2f}%")
else:
    print(f"Nenhuma batalha encontrada para a carta com ID {card_id}.")

print('----------------------------------------------------------------------------------------------------------------')


# Torres derrubadas pelo jogador 1 nas partidas

"""
Agrupa ($group) os nomes dos jogadores na posição 1 e calcula a média ($avg) de torres derrubada por cada

"""

resultado_torres_jogador_1 = battles_collection.aggregate([
    {
        '$group': {
            '_id': "$nickname_jogador_1",
            'media_torres_jogador_1': { '$avg': "$torres_jogador_1" }
        }
    }
])


print("Torres Derrubadas pelo Jogador 1\n")
for doc in resultado_torres_jogador_1:
    print(doc)

print('----------------------------------------------------------------------------------------------------------------')


# torres derrubadas pelo jogador 2 nas partidas

"""
Agrupa ($group) os nomes dos jogadores na posição 2 e calcula a média ($avg) de torres derrubada por cada

"""

resultado_jogador_2 = battles_collection.aggregate([
    {
        '$group': {
            '_id': "$nickname_jogador_2",
            'media_torres_jogador_2': { '$avg': "$torres_jogador_2" }
        }
    }
])

print("Torres Derrubadas pelo Jogador 2\n")
for doc in resultado_jogador_2:
    print(doc)

print('----------------------------------------------------------------------------------------------------------------')


# Liste os decks completos que produziram mais de X% (parâmetro) de vitórias ocorridas em um intervalo de timestamps (parâmetro)

"""
O código analisa os decks de jogadores com mais de X% de vitórias em um intervalo de tempo específico, definido como 
"2024-09-20 14:00:00" a "2024-09-20 19:00:00", sendo X igual a 70%. Primeiro, ele filtra as batalhas ocorridas nesse período com o comando $match e, 
em seguida, agrupa os resultados pelos decks dos dois jogadores usando $group, calculando o total de batalhas e as vitórias de cada um. 
O código utiliza $project para calcular a porcentagem de vitórias de ambos os jogadores em relação ao total de batalhas. 
Depois, aplica um segundo $match para filtrar os resultados, mostrando apenas os decks que têm porcentagens de vitórias superiores a 
X%. Por fim, o código imprime os decks dos jogadores que atingiram esse critério, incluindo suas respectivas porcentagens de vitória.

"""

print('Decks com Mais de X"%" de Vitórias em Intervalo de Tempo\n')
X = 70
inicio_intervalo = "2024-09-20 14:00:00"
fim_intervalo = "2024-09-20 19:00:00"

resultado = battles_collection.aggregate([
    {
        "$match": {
            "timestamp_batalha": {
                "$gte": inicio_intervalo,
                "$lte": fim_intervalo
            }
        }
    },
    {
        "$group": {
            "_id": {
                "deck_jogador_1": ["$p1c1", "$p1c2", "$p1c3", "$p1c4", "$p1c5", "$p1c6", "$p1c7", "$p1c8"],
                "deck_jogador_2": ["$p2c1", "$p2c2", "$p2c3", "$p2c4", "$p2c5", "$p2c6", "$p2c7", "$p2c8"]
            },
            "total_batalhas": { "$sum": 1 },
            "vitorias_jogador_1": { "$sum": { "$cond": ["$vitoria_jogador_1", 1, 0] } },
            "vitorias_jogador_2": { "$sum": { "$cond": ["$vitoria_jogador_2", 1, 0] } }
        }
    },
    {
        "$project": {
            "deck_jogador_1": "$_id.deck_jogador_1",
            "deck_jogador_2": "$_id.deck_jogador_2",
            "porcentagem_vitorias_jogador_1": {
                "$cond": {
                    "if": { "$gt": ["$total_batalhas", 0] },
                    "then": { "$multiply": [{ "$divide": ["$vitorias_jogador_1", "$total_batalhas"] }, 100] },
                    "else": 0
                }
            },
            "porcentagem_vitorias_jogador_2": {
                "$cond": {
                    "if": { "$gt": ["$total_batalhas", 0] },
                    "then": { "$multiply": [{ "$divide": ["$vitorias_jogador_2", "$total_batalhas"] }, 100] },
                    "else": 0
                }
            }
        }
    },
    {
        "$match": {
            "$or": [
                { "porcentagem_vitorias_jogador_1": { "$gt": X } },
                { "porcentagem_vitorias_jogador_2": { "$gt": X } }
            ]
        }
    }
])

for doc in resultado:
    if doc["porcentagem_vitorias_jogador_1"] > X:
        print(f"Deck Jogador 1: {doc['deck_jogador_1']}, Porcentagem de Vitórias: {doc['porcentagem_vitorias_jogador_1']}")
    if doc["porcentagem_vitorias_jogador_2"] > X:
        print(f"Deck Jogador 2: {doc['deck_jogador_2']}, Porcentagem de Vitórias: {doc['porcentagem_vitorias_jogador_2']}")


print('----------------------------------------------------------------------------------------------------------------')

# top 5 jogares com mais trofeus

"""
o $project seleciona os campos nickname_jogador_1 e trofeus_jogador_1 para o primeiro jogador. O $unionWith une os resultados da primeira projeção com os dados 
do segundo jogador (nickname_jogador_2 e trofeus_jogador_2) da mesma coleção. Com isso, o $group agrupa os resultados pelo nickname e 
calcula o máximo de troféus (max_trofeus) para cada jogador. Por fim, o $sort ordena os resultados em ordem decrescente com base no número máximo de troféus (max_trofeus)
e o $limit limita o resultado a 5 jogadores.

"""

print('Top 5 jogadores com mais troféus\n')

top_players = battles_collection.aggregate([
    {
        "$project": {
            "nickname": "$nickname_jogador_1",
            "trofeus": "$trofeus_jogador_1"
        }
    },
    {
        "$unionWith": {
            "coll": "battles",
            "pipeline": [
                {
                    "$project": {
                        "nickname": "$nickname_jogador_2",
                        "trofeus": "$trofeus_jogador_2"
                    }
                }
            ]
        }
    },
    {
        "$group": {
            "_id": "$nickname",
            "max_trofeus": {"$max": "$trofeus"}
        }
    },
    {
        "$sort": {"max_trofeus": -1}
    },
    {
        "$limit": 5
    }
])

for player in top_players:
    print(player)


print('----------------------------------------------------------------------------------------------------------------')


# Batalha em que o Jogador 2 venceu com menos torres destruídas

"""
o comando find_one busca a batalha em que o Jogador 2 venceu, especificado pela condição { "vitoria_jogador_2": 1 }. 
Em seguida, o comando sort organiza os resultados pela quantidade de torres restantes do Jogador 2, 
usando o campo torres_jogador_2 em ordem crescente, ou seja, a batalha com o menor número de torres restantes aparecerá primeiro.

"""

lowest_tower_win = battles_collection.find_one(
    {"vitoria_jogador_2": 1},
    sort=[("torres_jogador_2", 1)]
)

print('Batalha em que o Jogador 2 venceu com menos torres destruídas\n')
print(lowest_tower_win)


print('----------------------------------------------------------------------------------------------------------------')

# total de batalhas
 
"""
conta o número total de batalhas registradas na collection de batalhas. Ele usa o método distinct("battle_id") 
para obter todos os identificadores únicos de batalha (battle_id) e depois calcula o número total de batalhas usando len(), 
que retorna o tamanho da lista resultante.

"""

total_battles = len(battles_collection.distinct("battle_id"))
print(f'Total de batalhas ocorridas: {total_battles}')

print('----------------------------------------------------------------------------------------------------------------')

# taxa de vitoria na posição do jogador 1

"""
calcula a taxa de vitórias dos jogadores que participaram na posição de Jogador 1. 
Primeiro, ele agrupa ($group) as batalhas por jogador (campo nickname_jogador_1), 
somando o número de vitórias e contando o total de batalhas disputadas. 
Em seguida, ele projeta ($project) os dados, calculando a taxa de vitórias como a divisão entre vitórias e 
batalhas multiplicada por 100. Caso um jogador não tenha batalhas, a taxa é definida como 0. 
Por fim, os jogadores são ordenados ($sort) em ordem decrescente de taxa de vitórias.

"""

print('Taxa de vitoria na posição do jogador 1\n')

taxa_vitorias_posicao_jogador1 = battles_collection.aggregate([
    {
        "$group": {
            "_id": "$nickname_jogador_1",
            "vitorias": {"$sum": "$vitoria_jogador_1"},
            "total_batalhas": {"$sum": 1}
        }
    },
    {
        "$project": {
            "jogador": "$_id",
            "taxa_vitorias": {
                "$cond": {
                    "if": {"$eq": ["$total_batalhas", 0]},
                    "then": 0,
                    "else": {"$multiply": [{"$divide": ["$vitorias", "$total_batalhas"]}, 100]}
                }
            }
        }
    },
    {
        "$sort": {"taxa_vitorias": -1}
    }
])

for resultado in taxa_vitorias_posicao_jogador1:
    print(resultado)

print('----------------------------------------------------------------------------------------------------------------')


# taxa de vitoria na posição do jogador 2

"""
calcula a taxa de vitórias dos jogadores que participaram na posição de Jogador 2. 
Primeiro, ele agrupa ($group) as batalhas por jogador (campo nickname_jogador_2), 
somando o número de vitórias e contando o total de batalhas disputadas. 
Em seguida, ele projeta ($project) os dados, calculando a taxa de vitórias como a divisão entre vitórias e 
batalhas multiplicada por 100. Caso um jogador não tenha batalhas, a taxa é definida como 0. 
Por fim, os jogadores são ordenados ($sort) em ordem decrescente de taxa de vitórias.

"""

print('Taxa de vitoria na posição do jogador 2\n')

taxa_vitorias_posicao_jogador2 = battles_collection.aggregate([
    {
        "$group": {
            "_id": "$nickname_jogador_2",
            "vitorias": {"$sum": "$vitoria_jogador_2"},
            "total_batalhas": {"$sum": 1}
        }
    },
    {
        "$project": {
            "jogador": "$_id",
            "taxa_vitorias": {
                "$cond": {
                    "if": {"$eq": ["$total_batalhas", 0]},
                    "then": 0,
                    "else": {"$multiply": [{"$divide": ["$vitorias", "$total_batalhas"]}, 100]}
                }
            }
        }
    },
    {
        "$sort": {"taxa_vitorias": -1}
    }
])

for resultado in taxa_vitorias_posicao_jogador2:
    print(resultado)



