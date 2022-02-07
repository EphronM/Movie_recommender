import pickle
import pandas as pd
import numpy as np
from tmdbv3api import TMDb
from tmdbv3api import Movie
import json
import requests
from urlextract import URLExtract
import re
import json
import bs4 as bs
import urllib.request
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from string import  punctuation
from heapq import nlargest
from PIL import Image
from io import BytesIO


vectorizer = pickle.load(open('artifacts/transform.pkl', 'rb'))
nlp_algo = pickle.load(open('artifacts/nlp_model.pkl', 'rb'))

punctuation = punctuation + '\n'

nltk.download('stopwords')
nltk.download('punkt')
stop_words = stopwords.words('english')


tmdb = TMDb()
tmdb.api_key="12aee6e6e9db1d19c5d8078b2188e3a6"
tmdb_movie = Movie()

def get_info(title):
  info=[]
  result = tmdb_movie.search(title)
  if result:
    movie_id = result[0].id
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=12aee6e6e9db1d19c5d8078b2188e3a6')
    data_json = response.json()
  else:  
    return None
  
  return data_json


def get_poster(title):
    data_json = get_info(title)
    if data_json:
        poster = 'https://image.tmdb.org/t/p/original'+ data_json['poster_path']
    else:
        return None
    return poster



def movie_recommender(selected_moive, new_data,similarity):
    #similarity = make_similarity(new_data)
    movie_index = new_data[new_data['title']==selected_moive].index[0]
    similar_movies = sorted(list(enumerate(similarity[movie_index])),reverse=True, key=lambda x : x[1])[1:11]
    
    movie_list=[]
    for i in similar_movies:
        movie_list.append(list(new_data['title'])[i[0]])
    
    return movie_list


def get_reviews(imdb_id):
  if imdb_id:
    url = f'https://www.imdb.com/title/{imdb_id}/reviews?ref_=tt_ov_rt'

    sauce = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(sauce,'lxml')
    soup_result = soup.find_all("div",{"class":"text show-more__control"})
    reviews = []
    for i in range(len(soup_result)):
      reviews.append(soup_result[i].text)

    full_reviews = pd.DataFrame(reviews,  columns=['reviews'])
     
    if len(full_reviews) >= 1:
      reviews,reviews_status,reviews_list= [],[],[]
      
      for reviews in full_reviews['reviews']:
        reviews= [reviews]
        movie_vector = vectorizer.transform(reviews)
        pred = nlp_algo.predict(movie_vector)
        reviews_status.append('Good' if pred else 'Bad')
          
      full_reviews['sentiments'] = reviews_status
    return full_reviews
  


def top7_reviews(review_full):
  review_full['summary'] = review_full['reviews'].apply(summarizer)
  review_full.dropna(inplace=True)
  review_full.drop(columns=['reviews'], inplace=True)


  return review_full.sample(7).reset_index()
  

def summarizer(review):
  sentances = sent_tokenize(review)
  tokens = word_tokenize(review)

  word_freq={}
  for word in tokens:
    if word.lower() not in punctuation:
      if word.lower() not in stop_words:
        if word not in word_freq.keys():
          word_freq[word]=1
        else:
          word_freq[word]+=1
  
  maximum_freq = max(word_freq.values())
  for word in word_freq.keys():
    word_freq[word] = word_freq[word] / maximum_freq

  sentence_weigth = dict()
  for sent in sentances:
      sent_count_without_stopwords = 0
      for word_weigth in word_freq:
          if not word_weigth in sent.lower():
              pass
          else:
            sent_count_without_stopwords +=1
            if sent in sentence_weigth:
              sentence_weigth[sent] += word_freq[word_weigth]
            else:
              sentence_weigth[sent] = word_freq[word_weigth]

  length = 1

  summary = nlargest(length, sentence_weigth, key=sentence_weigth.get)
  final_summary = [word for word in summary]
  summary = ''.join(final_summary)
  
  if summary:
      if len(summary)<500:
          return summary


def rating_table(id):
  try:
    link = f"https://www.imdb.com/title/{id}/ratings/?ref_=tt_ov_rt"
    data = pd.read_html(link, header=0)[1]
    data.rename(columns={'Unnamed: 0': 'Gender'}, inplace=True)
    return data
  except:
    return None



def get_all_movies_images(imdb):
  extractor = URLExtract() 
  
  url = "https://imdb8.p.rapidapi.com/title/get-images"

  querystring = {"tconst":imdb,"limit":"10"}

  headers = {
      'x-rapidapi-host': "imdb8.p.rapidapi.com",
      'x-rapidapi-key': "7f3de3d2eemsh2291312e476f463p157afbjsn020bbf7037b8"
      }

  response = requests.request("GET", url, headers=headers, params=querystring)
  resizedImages=[]
  for image in set(extractor.find_urls(response.text)):
    try:
      r = requests.get(image)
      img = Image.open(BytesIO(r.content))
      resizedImg = img.resize((225, 230), Image.ANTIALIAS)
      resizedImages.append(resizedImg)
    except:
      pass


  return resizedImages 

def fetch_cast(imdb_id):
  extractor = URLExtract() 
  sauce = urllib.request.urlopen(f'https://www.imdb.com/title/{imdb_id}/fullcredits/').read()
  soup = bs.BeautifulSoup(sauce,'lxml')
  soup_result = soup.find_all("td",{"class":"primary_photo"})
  actors = []

  for i in range(3):
    actors.append(re.findall(r'"(.*?)"', str(soup_result[i]))[2])

  pattern = "[a-zA-Z]{2}\d{7}"
  id  = re.findall(pattern,str(soup_result))[:3]
  url=[]

  for i in id:
    sauce = urllib.request.urlopen(f'https://www.imdb.com/name/{i}').read()
    soup = bs.BeautifulSoup(sauce,'lxml')
    soup_result = soup.find_all("img",{"id":"name-poster"})

    url.append(extractor.find_urls(str(soup_result)).pop())
  return url, actors