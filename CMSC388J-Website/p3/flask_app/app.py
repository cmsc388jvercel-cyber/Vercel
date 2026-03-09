# 3rd-party packages
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
# from waitress import serve

# stdlib
import os
from datetime import datetime

# local
from forms import SearchForm, MovieReviewForm
from model import MovieClient

app = Flask(__name__)

# TODO: you should fill out these with the appropriate values
app.config['MONGO_URI'] = 'mongodb+srv://388jvmp3:mgsMPcn99NpDh85r@cluster0.n3np1qn.mongodb.net/proj3sampledb?retryWrites=true&w=majority'
app.config['SECRET_KEY'] = "b'\x05\xd3\xdb|\x90\xb5y\xe3\t\x1d\x14\x1c\xe1\xc2\xf5\x9e'"
OMDB_API_KEY = '9b5f8b43'

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

mongo = PyMongo(app)

movie_client = MovieClient(OMDB_API_KEY)

# --- Do not modify this function ---
@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for('query_results', query=form.search_query.data))

    return render_template('index.html', form=form)

@app.route('/search-results/<query>', methods=['GET'])
def query_results(query):
    try:
        results = movie_client.search(query)
        return render_template('query_results.html', results=results)
    except ValueError as e:
        return render_template('query_results.html', error_msg=str(e))

@app.route('/movies/<movie_id>', methods=['GET', 'POST'])
def movie_detail(movie_id):
    try:
        movie = movie_client.retrieve_movie_by_id(movie_id)
    except ValueError as e:
        return render_template('movie_detail.html', error_msg=str(e))
    form = MovieReviewForm()
    if form.validate_on_submit():
        review = {
            'imdb_id': movie_id,
            'commenter': form.name.data,
            'content': form.text.data,
            'date': current_time(),
        }
        mongo.db.reviews.insert_one(review)
        return redirect(url_for('movie_detail',movie_id = movie_id))

    reviews = mongo.db.reviews.find({'imdb_id': movie_id})
    all_reviews = list(reviews)

    return render_template('movie_detail.html', form=form, movie=movie, reviews=all_reviews) 


# Not a view function, used for creating a string for the current time.
def current_time() -> str:
    return datetime.now().strftime('%B %d, %Y at %H:%M:%S')

if __name__ == "__main__":
    serve(app, host="127.0.0.1", port=5007)
