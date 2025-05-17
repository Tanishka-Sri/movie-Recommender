from turtle import color

import streamlit as st
import pickle
import pandas as pd
import base64

# Page config
st.set_page_config(page_title="Custom Streamlit UI", layout="centered")

#def fetch_poster(movie_id):
   # response = requests.get('https://api.themoviedb.org/3/movie/{
     #            }?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    #data = response.json()


# Function to encode local image to base64
def get_base64_image(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Get the image as base64
img_base64 = get_base64_image("background.jpg")
# Inject the base64 image into CSS
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    
    </style>
""", unsafe_allow_html=True)


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    for i in movies_list:
        movie_id = i[0]
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.markdown("<h1 style='text-align: center; color: #FFD700;'>FILMOPHILE</h1>", unsafe_allow_html=True)

st.header("Get ready to jam!!")
selected_movie_name = st.selectbox(
    "How would you like to be contacted?",
    movies['title'].values)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    for i in recommendations:
        st.markdown(f"<p style='color:#FFC0CB; font-size:20px; font-weight:bold; text-align:center;'>{i}</p>", unsafe_allow_html=True)
