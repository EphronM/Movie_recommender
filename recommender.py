import pandas as pd
import numpy as np
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

nltk.download('stopwords')

def main():
    stopwords_eng = stopwords.words('english')
    data = pd.read_csv('artifacts/final_clean_data.csv')
    vectorizer = CountVectorizer(max_features=7000, stop_words=stopwords_eng)
    new_tags = vectorizer.fit_transform(data['tags']).toarray()

    similarity = cosine_similarity(new_tags)
    
    pickle.dump(similarity, open('artifacts/recommender_model.pkl', 'wb'))
    pickle.dump(vectorizer, open('artifacts/movie_recommender.pkl', 'wb'))

if __name__ == '__main__':
    main()