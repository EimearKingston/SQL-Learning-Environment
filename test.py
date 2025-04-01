from app import *
from flask import Flask 
import pytest 
@pytest.fixture
def client():
    
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def db():
    
    with app.app_context():
        db = get_db("movies.sqlite")  
        yield db 
def test_index_route():
    response = app.test_client().get('/')

    assert response.status_code == 200
    assert 'text/html' in response.content_type 
def test_sign_up_route():
    response = app.test_client().get('/sign_up')

    assert response.status_code == 200
    assert 'text/html' in response.content_type 
def test_login_route():
    response = app.test_client().get('/login')

    assert response.status_code == 200
    assert 'text/html' in response.content_type 
def test_teacher_sign_up_route():
    response = app.test_client().get('/teacher_sign_up')

    assert response.status_code == 200
    assert 'text/html' in response.content_type 
def test_teacher_login_route():
    response = app.test_client().get('/teacher_login')

    assert response.status_code == 200
    assert 'text/html' in response.content_type 
def test_workbooks_route(): 
    response = app.test_client().get('/index1')

    assert response.status_code == 200
    assert 'text/html' in response.content_type 
def test_workbook_route(): 
    workbook_id = 1
    response = app.test_client().get(f'/workbook/{workbook_id}')

    assert response.status_code == 200
    assert 'text/html' in response.content_type 
def test_question_route(): 
    question_id = 1 
    workbook_id = 1
    response = app.test_client().get(f'/workbook/{workbook_id}/question/{question_id}')

    assert response.status_code == 200
    assert 'text/html' in response.content_type 
def test_upload_route():
    response = app.test_client().get('/upload')

    assert response.status_code == 200
    assert 'text/html' in response.content_type 

def test_incorrect_query(client, db):
    
    data = {"query": "SELET * FROM movies"}  
    response = client.post("/workbook/1/question/0", data=data)
    json_data = response.get_json() 
    print(response)
    assert response.status_code == 200  
    if json_data.get("error"):  
        assert "SQLite Error" in json_data["error"]
