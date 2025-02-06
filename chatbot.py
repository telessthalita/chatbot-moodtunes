import os
from dotenv import load_dotenv
from textblob import TextBlob
from spotify_integration import obter_spotify_client, recomendar_musica, criar_playlist, adicionar_musicas_na_playlist

load_dotenv()

sp = obter_spotify_client()

historico = {}
musicas_recomendadas = {}

def analisar_sentimento(mensagem):
    blob = TextBlob(mensagem)
    sentimento = blob.sentiment.polarity  
    if sentimento > 0.3:  
        return 'feliz'
    elif sentimento < -0.3: 
        return 'triste'
    
    palavras_felizes = ["feliz", "animado", "empolgado", "maravilhoso", "muito bem"]
    palavras_tristes = ["triste", "deprimido", "ansioso", "frustrado", "sofrendo", "isolado"]

    for palavra in palavras_felizes:
        if palavra in mensagem.lower():
            return 'feliz'
    for palavra in palavras_tristes:
        if palavra in mensagem.lower():
            return 'triste'
    
    return 'neutro'


def start_chat():  
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

if __name__ == "__main__":
    start_chat()
