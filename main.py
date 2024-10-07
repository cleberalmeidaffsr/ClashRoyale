import requests
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import timedelta, datetime

load_dotenv()

api = os.getenv("API")
atlas = os.getenv("ATLAS")

headers = {
    "Authorization": f"Bearer {api}"
} 

def adicionarJogador(tag_jogador):
    url = f"https://api.clashroyale.com/v1/players/%23{tag_jogador}"
    
    response = requests.get(url, headers=headers)

    client = MongoClient(atlas)
    db = client['ClashRoyale']  
    collection = db['Jogadores'] 
    
    if response.status_code == 200:
        player_data = response.json()

        player_tag = player_data.get('tag', 'Tag não disponível')
        player_name = player_data.get('name', 'Nome não disponível')
        player_level = player_data.get('expLevel', 'Nível não disponível')
        player_trophies = player_data.get('trophies', 'Troféus não disponíveis')
        player_clan = player_data.get('clan', {}).get('name', 'Sem clã')
        player_wins = player_data.get('wins', 'Vitórias não disponíveis')
        player_losses = player_data.get('losses', 'Derrotas não disponíveis')

        player_document = {
            'playerTag' : player_tag,
            'name' : player_name,
            'level' : player_level,
            'trophies' : player_trophies,
            'clan' : player_clan,
            'wins' : player_wins,
            'losses' : player_losses
        }

        result = collection.update_one(
        {'playerTag' : player_tag},
        {'$set': player_document},
        upsert=True
    )

        if result.upserted_id:
            print(f'Documento inserido com ID: {result.upserted_id}')
        else:
            print(f'Documento atualizado com sucesso!')
    else:
        print(f'Erro: {response.status_code}') 


def adicionarBatalhas(tag_jogador):
    
    url = f"https://api.clashroyale.com/v1/players/%23{tag_jogador}/battlelog"

    response = requests.get(url, headers=headers)

    client = MongoClient(atlas)
    db = client['ClashRoyale']      
    collection = db['Batalhas']

    if response.status_code == 200:

        battle_log = response.json()  
             
        for battle in battle_log:
                
            battle_start_time = battle['battleTime']  
                
            team_1 = battle['team'][0]
            team_2 = battle['opponent'][0]

                
            player_1_trophies = team_1.get('startingTrophies', 'Não disponível')
            player_1_tower_destroys = team_1.get('crowns', 0)
            player_1_deck = team_1.get('cards', [])

                
            player_2_trophies = team_2.get('startingTrophies', 'Não disponível')
            player_2_tower_destroys = team_2.get('crowns', 0)
            player_2_deck = team_2.get('cards', [])

                
            winner = "Jogador 1" if player_1_tower_destroys > player_2_tower_destroys else "Jogador 2" if player_2_tower_destroys > player_1_tower_destroys else "Empate"

                
            battle_start_time = datetime.strptime(battle_start_time, "%Y%m%dT%H%M%S.%fZ")

                
            battle_end_time = battle_start_time + timedelta(minutes=3)

                
            battle_document = {
                'battleStart': battle_start_time,
                'battleEnd': battle_end_time,
                'player1': {
                    'trophies': player_1_trophies,
                    'tower_destroys': player_1_tower_destroys,
                    'deck': [card['name'] for card in player_1_deck]
                },
                'player2': {
                    'trophies': player_2_trophies,
                    'tower_destroys': player_2_tower_destroys,
                    'deck': [card['name'] for card in player_2_deck]
                },
                'winner': winner
            }

                
            result = collection.insert_one(battle_document)

            print(f'Documento de batalha inserido com ID: {result.inserted_id}')

        else:
            print(f"Erro: {response.status_code}")    

# adicionarBatalhas('200VLY909J')
# adicionarJogador('200VLY909J')
