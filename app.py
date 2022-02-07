import streamlit as st
import pickle
import pandas as pd
import helper
from PIL import Image
import base64
from ast import literal_eval
import matplotlib.pyplot as plt
from static.load_css import local_css




local_css("static/style.css")

hide_streamlit_style="""
<style>
#MainMenu{visibility:hidden}
footer{visibility:hidden}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

main_title = "<center><div><p class='highlight grey' style='font-size:47px'><span class='bold'>Movies Recommender</span></span></div></center>"
st.markdown(main_title, unsafe_allow_html=True)

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('artifacts/back1.png')

none_poster = Image.open('artifacts/posterNONE.jpg')


gen_movies = pd.read_csv('artifacts/final_clean_data.csv')
general_movie_similarity = pickle.load(open('artifacts/movie_recommender.pkl', 'rb'))


choose_movie = "<span style='color:#edecea'>Choose your movie</span>"
st.markdown(choose_movie, unsafe_allow_html=True)

selected_option = st.selectbox(' ', (gen_movies['title']))
  

if st.button('Search'):
    details = helper.get_info(selected_option)
    imdb_id = details['imdb_id']
    id = 'IMDB - '+ imdb_id
    summary = details['overview']

    cast_images, cast_names = helper.fetch_cast(imdb_id) 

    col1,col2= st.beta_columns([2,1]) 
    with col1:
        st.image('https://image.tmdb.org/t/p/original'+ details['poster_path'])
    with col2:
        movie_name = f"<div><p class='highlight grey' style='font-size:25px'><span class='bold'>{selected_option}</span></div><br>"
        st.markdown(movie_name, unsafe_allow_html=True)
        summary_mk = f"<div><p class='highlight grey' style='font-size:20px'>{summary}</div><br>"
        st.markdown(summary_mk, unsafe_allow_html=True)
        id_mk = f"<div><span class='highlight yellow' style='font-size:17px'><span class='bold'>{id}</span></span></div>"
        st.markdown(id_mk, unsafe_allow_html=True)
    
    st.markdown('<br>', unsafe_allow_html=True)    
    
    for i in literal_eval(str(details['genres'])):
        tags = f"<center><div><span class='highlight grey' style='font-size:18px'><span class='bold'>{i['name']}</span></span></div></center><br>"
        st.markdown(tags, unsafe_allow_html=True)
        #genres = tags

    st.markdown('<br>', unsafe_allow_html=True)

    cast_heading = f"<center><div><p class='highlight grey' style='font-size:30px'><span class='bold'>Cast details</span></div><center>"
    st.markdown(cast_heading, unsafe_allow_html=True)

    act1, act2, act3 = st.beta_columns(3)

    
    with act1:
        st.image(cast_images[0])
        title1= f"<center><div><p class='highlight grey' style='font-size:18px'><span class='bold'>{cast_names[0]}</span></span></div><center>"
        st.markdown(title1,unsafe_allow_html=True)

    with act2:
        st.image(cast_images[1])
        title1= f"<center><div><p class='highlight grey' style='font-size:18px'><span class='bold'>{cast_names[1]}</span></span></div><center>"
        st.markdown(title1,unsafe_allow_html=True)

    with act3:
        st.image(cast_images[2])
        title1= f"<center><div><p class='highlight grey' style='font-size:18px'><span class='bold'>{cast_names[2]}</span></span></div><center>"
        st.markdown(title1,unsafe_allow_html=True)




    #Rating Table
    ratings_table = helper.rating_table(imdb_id)
    try:
        review_table_html = ratings_table.to_html()

        
        st.markdown('<br><br>', unsafe_allow_html=True)
        rating_head = f"<center><div><p class='highlight grey' style='font-size:30px'><span class='bold'>Ratings Score</span></div><center>"
        st.markdown(rating_head, unsafe_allow_html=True)
        
        st.markdown(review_table_html, unsafe_allow_html=True)

        st.markdown('<br><br><br>', unsafe_allow_html=True)
    except:
        pass
     
    


    #create pie chart
    
    review_full = helper.get_reviews(imdb_id)
    if len(review_full)>0:
        print(len(review_full))

        review_full = helper.get_reviews(imdb_id)
        sentiments = f"<center><div><p class='highlight grey' style='font-size:30px'><span class='bold'>Overall sentiments</span></span></div><center>"
        st.markdown(sentiments,unsafe_allow_html=True)
        print(review_full)
        values=review_full['sentiments'].value_counts().values
        labels = review_full['sentiments'].value_counts().index
        fig, ax = plt.subplots()
        colors = ['#77DD77','#FF6961']

                
        plt.pie(values, labels = labels, colors = colors,explode=[0,0.1], autopct='%.0f%%')
        plt.savefig('artifacts/pie.png', transparent=True)
        st.image('artifacts/pie.png')
        st.markdown('<br>', unsafe_allow_html=True)

            #fetch and display reviews
        fetched_revies = helper.top7_reviews(review_full)
        fetched_revies.drop(columns='index', inplace=True)
            
        reviews= f"<center><div><p class='highlight grey' style='font-size:30px'><span class='bold'>Reviews</span></span></div><center>"
        st.markdown(reviews,unsafe_allow_html=True) 
        review_7_html = fetched_revies.to_html()
        st.markdown(review_7_html,unsafe_allow_html=True)  
       
                    

    recomended_movies = helper.movie_recommender(selected_option, gen_movies, general_movie_similarity)
    poster_links = []
    
        
    for movie in recomended_movies:
        link = helper.get_poster(movie)    
        poster_links.append(link)

    st.markdown('<br><br>', unsafe_allow_html=True)
    recommendations= f"<center><div><p class='highlight grey' style='font-size:30px'><span class='bold'>Featured Movies</span></span></div><center>"
    st.markdown(recommendations,unsafe_allow_html=True)  
    
    
    col1, col2, col3, col4, col5 = st.beta_columns(5)

    with col1:
        st.image(poster_links[0])
        title1= f"<center><div><p class='highlight grey' style='font-size:15px'>{recomended_movies[0]}</span></span></div><center>"
        st.markdown(title1,unsafe_allow_html=True)

    with col2:
        st.image(poster_links[1])
        title1= f"<center><div><p class='highlight grey' style='font-size:15px'>{recomended_movies[1]}</span></span></div><center>"
        st.markdown(title1,unsafe_allow_html=True)

    with col3:
        st.image(poster_links[2])
        title1= f"<center><div><p class='highlight grey' style='font-size:15px'>{recomended_movies[2]}</span></span></div><center>"
        st.markdown(title1,unsafe_allow_html=True)

    with col4:
        st.image(poster_links[3])
        title1= f"<center><div><p class='highlight grey' style='font-size:15px'>{recomended_movies[3]}</span></span></div><center>"
        st.markdown(title1,unsafe_allow_html=True)

    with col5:
        st.image(poster_links[4])
        title1= f"<center><div><p class='highlight grey' style='font-size:15px'>{recomended_movies[4]}</span></span></div><center>"
        st.markdown(title1,unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.beta_columns(5)

    with col1:
        st.image(poster_links[5])
        title1= f"<center><div><p class='highlight grey' style='font-size:15px'>{recomended_movies[5]}</span></span></div><center>"
        st.markdown(title1,unsafe_allow_html=True)

    with col2:
        st.image(poster_links[6])
        title1= f"<center><div><p class='highlight grey' style='font-size:15px'>{recomended_movies[6]}</span></span></div><center>"
        st.markdown(title1,unsafe_allow_html=True)

    with col3:
        st.image(poster_links[7])
        title1= f"<center><div><p class='highlight grey' style='font-size:15px'>{recomended_movies[7]}</span></span></div><center>"
        st.markdown(title1,unsafe_allow_html=True)

    with col4:
        st.image(poster_links[8])
        title1= f"<center><div><p class='highlight grey' style='font-size:15px'>{recomended_movies[8]}</span></span></div><center>"
        st.markdown(title1,unsafe_allow_html=True)

    with col5:
        st.image(poster_links[9])
        title1= f"<center><div><p class='highlight grey' style='font-size:15px'>{recomended_movies[9]}</span></span></div><center>"
        st.markdown(title1,unsafe_allow_html=True)


    #movies_images = list(helper.get_all_movies_images(imdb_id))   
    #st.image(movies_images)
    


