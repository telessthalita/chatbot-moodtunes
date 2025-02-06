import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

musicas_recomendadas = {}

def obter_spotify_client():
    oauth = SpotifyOAuth(
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),  
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),  
        redirect_uri='http://localhost:8888/callback',  
        scope='playlist-modify-public'
    )
    return spotipy.Spotify(auth_manager=oauth)

# spotify_integration.py
def recomendar_musica(sp, humor, nome):
    parametros = {
        'feliz': {'q': 'mood:happy', 'limit': 5}, 
        'triste': {'q': 'mood:happy OR genre:pop OR genre:rock', 'limit': 5},  
        'neutro': {'q': 'mood:calm', 'limit': 5} 
    }
    
    resultados = sp.search(**parametros.get(humor, parametros['neutro']), type='track')

    musicas = [f"{item['name']} - {item['artists'][0]['name']}" for item in resultados['tracks']['items']]
    
    if nome not in musicas_recomendadas:
        musicas_recomendadas[nome] = set()
    
    novas_musicas = [m for m in musicas if m not in musicas_recomendadas[nome]]
    
    if novas_musicas:
        musicas_recomendadas[nome].update(novas_musicas)
    
    return novas_musicas if novas_musicas else ["Já recomendei todas as disponíveis!"]


def criar_playlist(sp, nome_usuario, humor):
    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(user=user_id, name=f"PlayList criada pelo MoodTunes - {nome_usuario}", public=True)
    return playlist['id']

def adicionar_musicas_na_playlist(sp, playlist_id, musicas):
    ids_musicas = []
    for musica in musicas:
        resultado = sp.search(q=musica, type='track', limit=1)
        if resultado['tracks']['items']:
            ids_musicas.append(resultado['tracks']['items'][0]['id'])
    if ids_musicas:
        sp.playlist_add_items(playlist_id, ids_musicas)
        return f"🎶 Sua playlist está pronta! Ouça aqui: https://open.spotify.com/playlist/{playlist_id}"
    return "⚠️ Não foi possível adicionar músicas à playlist."
