
# Content Based Movie Recommender | Review Sentimental Analysis 

![Python](https://img.shields.io/badge/Python-3.8-blueviolet)
![Framework](https://img.shields.io/badge/Framework-Streamlit-red)
![Frontend](https://img.shields.io/badge/Frontend-HTML/CSS/JS-green)
![API](https://img.shields.io/badge/API-TMDB|IMDB-fcba03)

Movies have always facinated us as the best entertainment platform. It takes us to another diemention created by the directors which makes us emotionaly and mentally attahced. 
Its would be soo helpful for us to get all the released and upcomming movies details at place. 

![image](https://user-images.githubusercontent.com/94764266/152919762-3fd67fbc-3c18-4846-a966-d6cad5b6ede7.png)





## Run this webApp localy

Clone the repository

```bash
git clone https://github.com/EphronM/Movie_recommender-Content-Based.git
```

#### Create a conda environment after opening the repository

```bash
conda create -n movie_env python=3.9 -y
```

```bash
conda activate movie_env
```


#### Installing the required dependencies
```bash
pip install -r requirements.txt
```
#### Run the Python file `recommender.py`
```bash
python recommender.py 
```
This is produce the similarity-model pickle file which is the recommendation model
for the webApp

#### Getting the API key
* login and get your personal API key from https://www.themoviedb.org/. 
* Replace YOUR_API_KEY in both the places (line no. 34 and 42) in file **`helper.py`**

#### All set to run the webApp
```bash
streamlit run app.py
```

## What all does this webapp shows?

![VN20220207_221420 (1)](https://user-images.githubusercontent.com/94764266/152937614-388f1bdc-7bb6-45de-969e-8bc9ae701044.gif)

when searching any movies name, the web App gets you the details such as

* The movie poster along with a short summary and its IMDB ID.
* The genre of the particular movie.
* Top3 cast of the movie with their name and image
* Rating table for categhorised as gender and age respectively.
* Pie Chat of the sentimental Analysis performed on all the collected reviews
* Showcasing the random 7 summarized form of the collected reviews.
* Suggesting the top 10 simmilar movies as recommendation.

The dataset also contains details of the movies yet to release. As the reviews as not available,
sentimental Analysis pie chat, reviews and their coressponding rating table are ommitted. 

![Hnet-image (2)](https://user-images.githubusercontent.com/94764266/152918669-5149d63b-3d48-4504-8b5c-7ed3d9c00df7.gif)


### Data collection

Dataset was collected from `5000 IMDB movies` from kaggle and in addition, webscrapped the movies data using `BeautifulSoup` from `wiki list of movies` for the years 2017-2022.
This includes the movies yet to arrive or postponded due to the pandamic.

### API Reffrences
 - [TMDB](https://www.themoviedb.org/)
 - [IMDb - API dojo](https://rapidapi.com/apidojo/api/imdb8/)

 ### Recommendation Model
 
 ![image](https://user-images.githubusercontent.com/94764266/152920858-97789ea8-50bf-4f96-99ba-168d89326320.png)

 After cleaning and extracting the keyword for coressponding movies titles, the key tags are vectorized using `CountVectorizer`. Based on the `cosine Similarity`
the Similarity score is calculated for each datapoints coressponding to their index. Cosine Similarity gives the most similar movie index based on the their respective tags.

The model is pickled and loaded to the code to reduce the ram utilisation. Finding the Similarity which gives us a matrix of very large dimention (length of the dataset), flooded my ram due to limited hardware.

### Review Summarizer

![image](https://user-images.githubusercontent.com/94764266/152921210-fcfbe6e4-2788-4865-b275-7d71e62288a3.png)

The collected IMDB reiews are mostly of size 9000 words which can not be displayed on the webApp. Calculating the weight of each unique words and scoring each sentence based on the count of weighted words gives us the most important sentence amoung the whole paragraph.
Thus summaring the whole paragraph in a single sentence.

### Sentimental Analysis

![pie](https://user-images.githubusercontent.com/94764266/152921673-29d6ac06-1dff-4b9d-a4ac-470e4610053d.png)

Converting the reviews dataset into TfiD vectors and thus Training a supervised Naive Bayes model to predict the review sentiments.
The Vectorizer model is pickled loaded into the code for transforming and classfiying the collected movie revies.

### Webscrapped data

Using the IMDB ID collected from the API, the rating score, cast details and most of the displaying features are scrapped from IMDB offical website.


### Frontend Design
Implementing css onto the Streamlit using the markdown hacks, helps to costumize the webpage styles and overlook.
This was only possible on `streamlit 0.76.0` and before.







This all about this project. 

Happy coding Focks!!


```bash
Author: EphronM
Email: ephronmartin2016@gmail.com

```
