import os
from dotenv import load_dotenv
from textblob import TextBlob
import spotipy
from spotify_integration import recomendar_musica, criar_playlist, adicionar_musicas_na_playlist, obter_spotify_client


load_dotenv()

musicas_recomendadas = {}

def carregar_historico():
    if os.path.exists('historico.json'):
        with open('historico.json', 'r') as file:
            return json.load(file)
    return {}

def salvar_historico():
    with open('historico.json', 'w') as file:
        json.dump(musicas_recomendadas, file)

from textblob import TextBlob

def analisar_sentimento(mensagem):
    mensagem = mensagem.lower()
    
    blob = TextBlob(mensagem)
    polaridade = blob.sentiment.polarity  

    palavras_felizes = ["feliz", "alegre", "contente", "animado", "maravilhoso", "incrível", "empolgado"]
    palavras_tristes = ["triste", "deprimido", "ansioso", "preocupado", "nervoso", "frustrado", "cansado", "chateado", "isolado"]
    palavras_neutras = ["ok", "tanto faz", "normal", "indiferente", "neutro"]

    for palavra in palavras_felizes:
        if palavra in mensagem:
            return 'feliz'
    for palavra in palavras_tristes:
        if palavra in mensagem:
            return 'triste'
    for palavra in palavras_neutras:
        if palavra in mensagem:
            return 'neutro'

    if polaridade > 0.1:
        return 'feliz'
    elif polaridade < -0.1:
        return 'triste'
    
    return 'neutro'


def start_chat():
    sp = obter_spotify_client()

    print("\n🎵 MoodTunes v2.0")
    nome = input("\nMoodTunes: Oi! Qual é o seu nome? ")  
    mensagem = input(f"\n{nome}, como você está se sentindo hoje? ")
    humor = analisar_sentimento(mensagem)
    print(f"\nMoodTunes: Parece que você está {humor} hoje, {nome}. Vou preparar uma playlist para você!")
    
    recomendacoes = recomendar_musica(sp, humor, nome)
    playlist_id = criar_playlist(sp, nome, humor)
    resposta_playlist = adicionar_musicas_na_playlist(sp, playlist_id, recomendacoes)
    
    print(f"\n💡 Baseado no seu humor, {nome}, aqui está sua playlist: ")
    print(resposta_playlist)
    
    print(f"\n🎧 Até logo, {nome}! Espero que essa playlist melhore seu dia! 😊")
    feedback = input("Você gostou da playlist? (sim/não): ").strip().lower()
    if feedback == 'não':
        print("\nEntendi, vou tentar novamente!")
        start_chat() 

if __name__ == "__main__":
    start_chat()
