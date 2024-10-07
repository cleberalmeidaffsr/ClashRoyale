import requests
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

api = os.getenv("API")
atlas = os.getenv("ATLAS")

headers = {
    "Authorization": f"Bearer {api}"
} 

def adicionarJogador(tag_jogador):
    url = f"https://api.clashroyale.com/v1/players/%23{tag_jogador}"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print("Dados obtidos com sucesso!")
    else:
        print(f"Erro: {response.status_code}")
    
    client = MongoClient(atlas)
    db = client['ClashRoyale']  
    collection = db['Jogadores']  

    collection.insert_one(data)
    print("MongoDB Atlas Atualizado.")

    client.close()
    return None 

def adicionarBatalhas(tag_jogador):
    
    url = f"https://api.clashroyale.com/v1/players/%23{tag_jogador}/battlelog"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print("Dados obtidos com sucesso!")
    else:
        print(f"Erro: {response.status_code}")

    client = MongoClient(atlas)
    db = client['ClashRoyale']      
    collection = db['Batalhas']  

    collection.insert_many(data)
    print("MongoDB Atlas Atualizado.")

    client.close()

adicionarJogador("JYQLP2J2P")
adicionarBatalhas("JYQLP2J2P")