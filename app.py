from flask import Flask, request, render_template
import pickle
import pandas as pd
import requests
from itertools import zip_longest

app = Flask(__name__)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_poster = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

movies_dict = pickle.load(open('model/movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

@app.route('/index', methods=['POST'])
@app.route('/find_movie')
def home():
    if request.method == 'POST':
        movie_title = request.form.get('Movie_title')
        names, posters = recommend(movie_title)
        return render_template('recmmended.html', names=names, posters=posters, zip=zip)
    return render_template('index.html', movies=movies['title'].values)

if __name__ == '__main__':
    app.run(debug=True)
