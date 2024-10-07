from datetime import datetime
import os
from db_connection import client
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Acesse o banco de dados e a collection
battles_collection = client['clashroyale']['battles']

# para carregar e redimensionar imagem 
def load_image_from_directory(directory, filename, size=()):
    img_path = os.path.join(directory, filename)  
    img = Image.open(img_path) 
    img = img.resize(size)  
    return ImageTk.PhotoImage(img) 


# CONSULTAS NA INTERFACE

def mostrar_total_batalhas():
    total_battles = len(battles_collection.distinct("battle_id"))  
    messagebox.showinfo("Total de Batalhas", f'Total de batalhas: {total_battles}')

def mostrar_porcentagem_vitorias_derrotas_carta():
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
                "win_percentage": {"$multiply": [{"$divide": ["$wins", "$total_battles"]}, 100]},
                "loss_percentage": {"$subtract": [100, {"$multiply": [{"$divide": ["$wins", "$total_battles"]}, 100]}]}
            }
        }
    ])
    
    result = list(percentages)
    if result:
        win_percentage = f"Porcentagem de vitórias: {result[0]['win_percentage']:.2f}%"
        loss_percentage = f"Porcentagem de derrotas: {result[0]['loss_percentage']:.2f}%"
        messagebox.showinfo("Porcentagem de Vitórias e Derrotas", f'{win_percentage}\n{loss_percentage}')
    else:
        messagebox.showinfo("Porcentagem de Vitórias e Derrotas", f"Nenhuma batalha encontrada para a carta com ID {card_id}.")


def mostrar_torres_derrubadas_jogador_1():
    resultado_torres_jogador_1 = battles_collection.aggregate([
        {'$group': {'_id': "$nickname_jogador_1", 'media_torres_jogador_1': {'$avg': "$torres_jogador_1"}}}
    ])
    resultado = "\n".join([f'{doc["_id"]}: {doc["media_torres_jogador_1"]:.2f}' for doc in resultado_torres_jogador_1])
    messagebox.showinfo("Torres Derrubadas pelo Jogador 1", resultado)


def mostrar_torres_derrubadas_jogador_2():
    resultado_jogador_2 = battles_collection.aggregate([
        {'$group': {'_id': "$nickname_jogador_2", 'media_torres_jogador_2': {'$avg': "$torres_jogador_2"}}}
    ])
    resultado = "\n".join([f'{doc["_id"]}: {doc["media_torres_jogador_2"]:.2f}' for doc in resultado_jogador_2])
    messagebox.showinfo("Torres Derrubadas pelo Jogador 2", resultado)


def mostrar_decks_vitoriosos():
    X = 70
    inicio_intervalo = "2024-09-20 14:00:00"
    fim_intervalo = "2024-09-20 19:00:00"
    
    result = battles_collection.aggregate([
        {"$match": {"timestamp_batalha": {"$gte": inicio_intervalo, "$lte": fim_intervalo}}},
        {"$group": {
            "_id": {"deck_jogador_1": ["$p1c1", "$p1c2", "$p1c3", "$p1c4", "$p1c5", "$p1c6", "$p1c7", "$p1c8"],
                    "deck_jogador_2": ["$p2c1", "$p2c2", "$p2c3", "$p2c4", "$p2c5", "$p2c6", "$p2c7", "$p2c8"]},
            "total_batalhas": {"$sum": 1},
            "vitorias_jogador_1": {"$sum": {"$cond": ["$vitoria_jogador_1", 1, 0]}},
            "vitorias_jogador_2": {"$sum": {"$cond": ["$vitoria_jogador_2", 1, 0]}}
        }},
        {"$project": {
            "deck_jogador_1": "$_id.deck_jogador_1",
            "deck_jogador_2": "$_id.deck_jogador_2",
            "porcentagem_vitorias_jogador_1": {
                "$cond": {
                    "if": {"$gt": ["$total_batalhas", 0]},
                    "then": {"$multiply": [{"$divide": ["$vitorias_jogador_1", "$total_batalhas"]}, 100]},
                    "else": 0
                }
            },
            "porcentagem_vitorias_jogador_2": {
                "$cond": {
                    "if": {"$gt": ["$total_batalhas", 0]},
                    "then": {"$multiply": [{"$divide": ["$vitorias_jogador_2", "$total_batalhas"]}, 100]},
                    "else": 0
                }
            }
        }},
        {"$match": {"$or": [{"porcentagem_vitorias_jogador_1": {"$gt": X}}, {"porcentagem_vitorias_jogador_2": {"$gt": X}}]}
        }
    ])
    
    resultado = ""
    for doc in result:
        if doc["porcentagem_vitorias_jogador_1"] > X:
            resultado += f'Deck Jogador 1: {doc["deck_jogador_1"]}, Porcentagem de Vitórias: {doc["porcentagem_vitorias_jogador_1"]:.2f}%\n'
        if doc["porcentagem_vitorias_jogador_2"] > X:
            resultado += f'Deck Jogador 2: {doc["deck_jogador_2"]}, Porcentagem de Vitórias: {doc["porcentagem_vitorias_jogador_2"]:.2f}%\n'
    
    messagebox.showinfo("Decks com Alta Porcentagem de Vitórias", resultado)


def mostrar_top_5_jogadores():
    top_players = battles_collection.aggregate([
        {"$project": {"nickname": {"$concat": ["$nickname_jogador_1"]}, "trofeus": "$trofeus_jogador_1"}},
        {"$unionWith": {"coll": "battles", "pipeline": [
            {"$project": {"nickname": {"$concat": ["$nickname_jogador_2"]}, "trofeus": "$trofeus_jogador_2"}}
        ]}},
        {"$group": {"_id": "$nickname", "max_trofeus": {"$max": "$trofeus"}}},
        {"$sort": {"max_trofeus": -1}},
        {"$limit": 5}
    ])
    
    resultado = "\n".join([f'{doc["_id"]}: {doc["max_trofeus"]}' for doc in top_players])
    messagebox.showinfo("Top 5 Jogadores com Mais Troféus", resultado)

def mostrar_taxa_vitorias_posicao_jogador_1():
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

    resultado = "\n".join([f'{resultado["jogador"]}: {resultado["taxa_vitorias"]:.2f}%' for resultado in taxa_vitorias_posicao_jogador1])
    messagebox.showinfo("Taxa de Vitórias do Jogador 1", resultado)

def mostrar_taxa_vitorias_posicao_jogador_2():
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

    resultado = "\n".join([f'{resultado["jogador"]}: {resultado["taxa_vitorias"]:.2f}%' for resultado in taxa_vitorias_posicao_jogador2])
    messagebox.showinfo("Taxa de Vitórias do Jogador 2", resultado)



 # Criando a interface gráfica
app = tk.Tk()
app.title("Análise de Batalhas Clash Royale")
app.configure(bg="#083C91") 

cards_frame = tk.Frame(app, bg="#083C91")  
cards_frame.pack(pady=20)

def on_card_click(card_name):
    if card_name == "total_battles":
        mostrar_total_batalhas()
    elif card_name == "porcentagem_vitorias_derrotas":
        mostrar_porcentagem_vitorias_derrotas_carta()
    elif card_name == "torres_jogador_1":
        mostrar_torres_derrubadas_jogador_1()
    elif card_name == "torres_jogador_2":
        mostrar_torres_derrubadas_jogador_2()
    elif card_name == "decks_vitoriosos":
        mostrar_decks_vitoriosos()
    elif card_name == "top_jogadores":
        mostrar_top_5_jogadores()
    elif card_name == "taxa_vitorias_jogador_1":
        mostrar_taxa_vitorias_posicao_jogador_1()
    elif card_name == "taxa_vitorias_jogador_2":
        mostrar_taxa_vitorias_posicao_jogador_2()

image_directory = "images"

cards_info = [
    {"image_filename": "design.png", "name": "total_battles"},
    {"image_filename": "design.png", "name": "porcentagem_vitorias_derrotas"},
    {"image_filename": "design.png", "name": "torres_jogador_1"},
    {"image_filename": "design.png", "name": "torres_jogador_2"},
    {"image_filename": "design.png", "name": "decks_vitoriosos"},
    {"image_filename": "design.png", "name": "top_jogadores"},
    {"image_filename": "design.png", "name": "taxa_vitorias_jogador_1"},
    {"image_filename": "design.png", "name": "taxa_vitorias_jogador_2"},
]

# Adicionando botões no grid
for index, card in enumerate(cards_info):
    img = load_image_from_directory(image_directory, card["image_filename"], size=(250, 300)) 
    
    button = tk.Button(cards_frame, image=img, command=lambda name=card["name"]: on_card_click(name), 
                       bg="#083C91", borderwidth=0)  

    button.image = img 

    # Calcular a posição (linha e coluna) do botão
    row = index // 4  
    column = index % 4  
    button.grid(row=row, column=column, padx=10, pady=10)  

app.mainloop()