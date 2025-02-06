import spotipy  
from spotipy.oauth2 import SpotifyClientCredentials  

# Suas credenciais (substitua com as suas)  
client_id = 'SEU_CLIENT_ID'  
client_secret = 'SEU_CLIENT_SECRET'  

# Conectar ao Spotify  
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))  

def recomendar_musica(humor):  
    if humor == 'feliz':  
        resultados = sp.search(q='mood:happy', limit=5, type='track')  
    elif humor == 'triste':  
        resultados = sp.search(q='mood:sad', limit=5, type='track')  
    else:  
        resultados = sp.search(q='mood:calm', limit=1, type='track')  

    musica = resultados['tracks']['items'][0]['name']  
    artista = resultados['tracks']['items'][0]['artists'][0]['name']  
    return f"{musica} - {artista}"  

def start_chat():  
    nome = input("Chatbot: Oi! Qual é o seu nome? ")  
    humor = input("Chatbot: Como você está se sentindo hoje (feliz, triste, neutro)? ")  
    musica = recomendar_musica(humor)  
    print(f"Chatbot: Recomendo esta música para você: {musica}")  

start_chat()  