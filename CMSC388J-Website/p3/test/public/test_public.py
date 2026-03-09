from bs4 import BeautifulSoup
from flask.testing import FlaskClient

from ..util import *

# Secret key set (5)
def test_secret_key_set(client: FlaskClient):
    secret = client.application.config['SECRET_KEY']
    assert len(secret) > 0

'''
Tests for search form
10 - search form rendered with input validators (5 + 5)
5 - search form input validation errors shown on page 
15 - query results show up after using search form
'''

# Search form rendered (5)
def test_search_form_rendered(client: FlaskClient):
    res = client.get('/')
    assert res.status_code == 200

    soup = BeautifulSoup(res.data, features='html.parser')
    field = soup.find(attrs={'name': 'search_query'})
    assert field is not None, 'no search_query field'

# Search form has correct input validators (5)
def test_search_form_has_input_validators(client: FlaskClient):
    res = client.get('/')
    assert res.status_code == 200

    soup = BeautifulSoup(res.data, features='html.parser')
    field = soup.find(attrs={'name': 'search_query'})
    assert field is not None, 'no search_query field'

    assert field['minlength'] == '1'
    assert field['maxlength'] == '30'
    assert field['required'] is not None

# Search form validators show errors on page (5)
def test_search_form_validators_show_errors(client: FlaskClient):
    res = client.post('/', data={
        'search_query': 'a' * 31
    }, follow_redirects=True)
    assert res.status_code == 200 
    
    soup = BeautifulSoup(res.data, features='html.parser')
    error_elems = soup.find_all(string=lambda t: 'Field must be between' in t)
    assert len(error_elems) == 1

# Search form shows results (15)
def test_search_form_shows_results(client: FlaskClient):
    res = client.post('/', data={
        'search_query': 'dune',
    }, follow_redirects=True)
    assert res.status_code == 200

    soup = BeautifulSoup(res.data, features='html.parser')
    a_elems = soup.find_all('a', href=True)
    found_movie = False
    for elem in a_elems:
        if 'tt1160419' in elem['href'] and 'Dune' in elem.text:
            found_movie = True
    assert found_movie

'''
Tests for review form
10 - Review form rendered with input validators
5 - Review form input validator errors shown on page
5 - Review form has multi-line input for review
10 - reviews are shown after submitting review form
15 - Reviews are shown per movie (unique per movie)
'''

# Review form rendered (5)
def test_review_form_rendered(client: FlaskClient):
    res = client.get('/movies/tt1160419')
    assert res.status_code == 200

    soup = BeautifulSoup(res.data, features='html.parser')
    name_field = soup.find(attrs={'name': 'name'})
    text_field = soup.find(attrs={'name': 'text'})
    assert name_field is not None, 'no name field'
    assert text_field is not None, 'no text field'

# Review form has correct validators (5)
def test_review_form_has_input_validators(client: FlaskClient):
    res = client.get('/movies/tt1160419')
    assert res.status_code == 200

    soup = BeautifulSoup(res.data, features='html.parser')
    name_field = soup.find(attrs={'name': 'name'})
    text_field = soup.find(attrs={'name': 'text'})
    assert name_field is not None, 'no name field'
    assert text_field is not None, 'no text field'

    assert name_field['minlength'] == '1'
    assert name_field['maxlength'] == '50'
    assert name_field['required'] is not None

    assert text_field['minlength'] == '1'
    assert text_field['maxlength'] == '500'
    assert text_field['required'] is not None

# Review form validators show errors on page (5)
def test_review_form_validators_show_errors(client: FlaskClient):
    res = client.post('/movies/tt1160419', data={
        'name': 'a' * 51,
        'text': 'b' * 501
    }, follow_redirects=True)
    assert res.status_code == 200 
    
    soup = BeautifulSoup(res.data, features='html.parser')
    error_elems = soup.find_all(string=lambda t: 'Field must be between' in t)
    assert len(error_elems) == 2

# Review form has multi-line input for review (5)
def test_review_form_uses_multiline_input(client: FlaskClient):
    res = client.get('/movies/tt1160419')
    assert res.status_code == 200

    soup = BeautifulSoup(res.data, features='html.parser')
    name_field = soup.find(attrs={'name': 'name'})
    text_field = soup.find(attrs={'name': 'text'})
    assert name_field is not None, 'no name field'
    assert text_field is not None, 'no text field'

    assert text_field.name == 'textarea'

# Review shows up on page after submitting form (10)
def test_review_shows_up_on_page(client: FlaskClient):
    name, text = 'testuser 2', 'awesome movie 2'
    res = client.post('/movies/tt1160419', data={
        'name': name,
        'text': text
    }, follow_redirects=True)
    assert res.status_code == 200 

    soup = BeautifulSoup(res.data, features='html.parser') 
    assert soup.find(string=lambda t: name in t), 'did not find name'
    assert soup.find(string=lambda t: text in t), 'did not find text'

# Reviews are shown per movie (unique per movie) (15)
def test_review_only_show_up_on_one_movie(client: FlaskClient):
    name, text = 'testuser 3', 'awesome movie 3'
    res = client.post('/movies/tt1160419', data={
        'name': name,
        'text': text
    }, follow_redirects=True)
    assert res.status_code == 200  

    res2 = client.get('/movies/tt0117060') # different movie
    assert res.status_code == 200

    soup = BeautifulSoup(res2.data, features='html.parser')
    assert not soup.find(string=lambda t: name in t), 'found name'
    assert not soup.find(string=lambda t: text in t), 'found text'

'''
Tests for MongoDB
15 - Reviews are inserted to MongoDB
15 - Reviews are read from MongoDB
'''
    
# Review form inserts to database (15)
def test_review_form_adds_to_database(client: FlaskClient):
    res = client.post('/movies/tt1160419', data={
        'name': 'testuser 1',
        'text': 'awesome movie 1'
    }, follow_redirects=True)
    assert res.status_code == 200

    reviews = get_reviews_for_movie_from_db('tt1160419')
    expected_review = {
        'imdb_id': 'tt1160419',
        'commenter': 'testuser 1',
        'content': 'awesome movie 1',
    }
    found_review = False
    for review in reviews:
        if expected_review.items() <= review.items():
            # need to check date separately because time may not be same 
            if current_time_date_only() == review['date'].split(' at ')[0]:
                found_review = True
    assert found_review

# Reviews are read from database (15)
def test_using_mongodb_to_show_reviews(client: FlaskClient):
    imdb_id = 'tt0816692'
    name = 'testuser 4'
    text = 'awesome movie 4'
    date = current_time_date_only()
    insert_review(imdb_id, name, text, date) 

    res = client.get(f'/movies/{imdb_id}')
    assert res.status_code == 200

    soup = BeautifulSoup(res.data, features='html.parser')
    assert soup.find(string=lambda t: name in t), 'did not find name'
    assert soup.find(string=lambda t: text in t), 'did not find text'