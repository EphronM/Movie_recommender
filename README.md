
# Content Based Movie Recommender | Review Sentimental Analysis 
![Python](https://img.shields.io/badge/Python-3.8-blueviolet)
![Framework](https://img.shields.io/badge/Framework-Streamlit-red)
![Frontend](https://img.shields.io/badge/Frontend-HTML/CSS/JS-green)
![API](https://img.shields.io/badge/API-TMDB|IMDB-fcba03)

Movies have always facinated us as the best entertainment platform. It takes us to another diemention created by the directors which makes us emotionaly and mentally attahced. 
Its would be soo helpful for us to get all the released and upcomming movies details at place. 



## What all does this webapp shows?
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

### Data collection

Dataset was collected from `5000 IMDB movies` from kaggle and in addition, webscrapped the movies data using `BeautifulSoup` from `wiki list of movies` for the years 2017-2022.
This includes the movies yet to arrive or postponded due to the pandamic.

### API Reffrences
 - [TMDB](https://www.themoviedb.org/)
 - [IMDb - API dojo](https://rapidapi.com/apidojo/api/imdb8/)

 ### Recommendation Model

 After cleaning and extracting the keyword for coressponding movies titles, the key tags are vectorized using `CountVectorizer`. Based on the `cosine Similarity`
the Similarity score is calculated for each datapoints coressponding to their index. Cosine Similarity gives the most similar movie index based on the their respective tags.

The model is pickled and loaded to the code to reduce the ram utilisation. Finding the Similarity which gives us a matrix of very large dimention (length of the dataset), flooded my ram due to limited hardware.

### Review Summarizer

The collected IMDB reiews are mostly of size 9000 words which can not be displayed on the webApp. Calculating the weight of each unique words and scoring each sentence based on the count of weighted words gives us the most important sentence amoung the whole paragraph.
Thus summaring the whole paragraph in a single sentence.

### Sentimental Analysis

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
