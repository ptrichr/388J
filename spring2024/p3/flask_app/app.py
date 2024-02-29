# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo

# stdlib
import os
from datetime import datetime

# local
from flask_app.forms import SearchForm, MovieReviewForm
from flask_app.model import MovieClient

# don't change the name
app = Flask(__name__)

# TODO: you should fill out these with the appropriate values
app.config['MONGO_URI'] = 'mongodb+srv://petrichor:QpssdcS6BuHsIKsV@388j.lvoyrb1.mongodb.net/388J?retryWrites=true&w=majority' 
app.config['SECRET_KEY'] = b';\xe1\xce\x00A\x8e_g\x88I"\xab\'\xce\x06\xb9'
OMDB_API_KEY = '30a9894d' 

# DO NOT REMOVE OR MODIFY THESE 4 LINES (required for autograder to work)
if os.getenv('MONGO_URI'):
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')
if os.getenv('OMDB_API_KEY'):
    OMDB_API_KEY = os.getenv('OMDB_API_KEY')

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

# don't change the name
mongo = PyMongo(app)

# don't change the name 
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
        res = movie_client.search(query)
        return render_template('query_results.html', results=res)
    except ValueError as e:
        return render_template('query_results.html', error_msg=e)
@app.route('/movies/<movie_id>', methods=['GET', 'POST'])
def movie_detail(movie_id):
    try:
        movie_data = movie_client.retrieve_movie_by_id(movie_id)
    except ValueError as e:
        return render_template("movie_detail.html", error_msg=e)
    
    form = MovieReviewForm()
    # p3_reviews is the mongo database collection
    if form.validate_on_submit():
        review = {
            'imdb_id': movie_id,
            'commenter': form.name.data,
            'content': form.text.data,
            'date': current_time()
        }
        # insert into mongo
        mongo.db.reviews.insert_one(review)
        return redirect(url_for('movie_detail', movie_id=movie_id))
        
    reviews_from_db = list(mongo.db.reviews.find({'imdb_id': movie_id}))
            
    return render_template('movie_detail.html', 
                           movie=movie_data, 
                           form=form, 
                           reviews=reviews_from_db)

# Not a view function, used for creating a string for the current time.
def current_time() -> str:
    return datetime.now().strftime('%B %d, %Y at %H:%M:%S')