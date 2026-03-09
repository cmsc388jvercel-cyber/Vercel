import random
from datetime import datetime

from flask_app.app import mongo, movie_client

def get_reviews_for_movie_from_db(movie_id):
    reviews = mongo.db.reviews.find({'imdb_id': movie_id})
    return list(reviews)

def insert_review(imdb_id, commenter, content, date):
    mongo.db.reviews.insert_one({
        'imdb_id': imdb_id,
        'commenter': commenter,
        'content': content,
        'date': date
    })

def current_time_date_only() -> str:
    return datetime.now().strftime('%B %d, %Y')