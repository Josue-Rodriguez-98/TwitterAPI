# -----------------------------------------------------------
# Tarea: Análisis de Datos en Twitter
# Sistemas Inteligentes
# Desarrollado por Josué Rodríguez (11641196)
# 2. Emplear expresiones regulares para limpiar el texto removiendo Tags, Caracteres Especiales, URLs, Imágenes (done)
# 2.1 Emplear el algoritmo de Viterbi para segmentar Hashtags
# -----------------------------------------------------------

import tweepy as tw
import re
import os
from dotenv import load_dotenv

#Credenciales para usar el API de Twitter, cargadas desde el archivo .env
load_dotenv()
consumer_key = os.getenv('consumer_key')
consumer_secret = os.getenv('consumer_secret')
access_token = os.getenv('access_token')
access_secret = os.getenv('access_secret')

#Inicializar el API
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tw.API(auth, wait_on_rate_limit=True)

#Bloque de código que remueve Emojis de la cadena (tweet)
def removeEmojis(tweet):
  return tweet.encode('ascii', 'ignore').decode('ascii')
#--------------------------------------------------------

#Bloque de código que remueve líneas en blanco de la cadena (tweet)
def removeEmptyLines(tweet):
  lines = tweet.split('\n')
  nonEmpty = [line for line in lines if line.strip() != '']
  retVal = ''
  for line in nonEmpty:
    retVal += line + '\n'
  return retVal[:len(retVal)-1]
  #--------------------------------------------------------

#Bloque de código que remueve tags, caracteres especiales, urls
def removeTrash(tweet):
  #Expresion regular para quitar usernames
  retVal = re.sub(r'@[\w]+', '', tweet, flags=re.I)
  #Expresión regular para quitar links (aplicando el servicio de enlace de twitter)
  retVal = re.sub(r'https://t.co/[\w]+','', retVal, flags = re.I)
  #Expresión regular para quitar caracteres especiales
  retVal = re.sub(r'[^#a-zA-Z0-9 \n]+','',retVal, flags = re.I)
  #Expresión regular para quitar espacios consecutivos
  retVal = re.sub(r"\s+",' ', retVal, flags = re.I)
  return retVal
#--------------------------------------------------------

#Función que manda a llamar a todos los métodos auxiliares para la limpieza del tweet
def cleanTweet(tweet):
  retVal = removeEmojis(tweet)
  retVal = removeTrash(retVal)
  retVal = removeEmptyLines(retVal)
  return retVal
#---------------------------------------------------------

def main():
  #Palabras claves para nuestros tweets
  query = 'coronavirus OR covid-19 OR #StayAtHome -filter:retweets'
  #Fecha de inicio de nuestros tweets
  date_since = '2020-2-22'
  tweets = tw.Cursor(api.search, q = query, lang = 'en OR es', since = date_since, tweet_mode = 'extended').items(20)
  filteredTweets = []
  count = 1
  for tweet in tweets:
    print(f'##################Tweet #{count}#####################')
    print(f'{tweet.full_text}')
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    filteredText = cleanTweet(tweet.full_text)
    print(f'{filteredText}')
    filteredTweets.append(filteredText)
    count += 1
  #count = 0
  #for txt in filteredTweets:
  #  print(f'{count} -> {txt}\n\n')
  #  count += 1
#---------------------------------------------------------

if '__main__' == __name__:
  main()