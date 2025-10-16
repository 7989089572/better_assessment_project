import pytest
from backend.app import create_app
from backend.extensions import db
from backend.config import TestConfig

@pytest.fixture
def app():
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_and_list_comments(client):
    rv = client.post('/api/comments', json={'task_id':1, 'author':'Alice', 'content':'First comment'})
    assert rv.status_code == 201
    rv = client.get('/api/comments?task_id=1')
    assert rv.status_code == 200
    data = rv.get_json()
    assert len(data) == 1

def test_update_comment(client):
    rv = client.post('/api/comments', json={'task_id':2, 'author':'Bob', 'content':'Hi'})
    cid = rv.get_json()['id']
    rv = client.put(f'/api/comments/{cid}', json={'author':'Bobby','content':'Updated'})
    assert rv.status_code == 200
    assert rv.get_json()['content'] == 'Updated'

def test_delete_comment(client):
    rv = client.post('/api/comments', json={'task_id':3, 'author':'Sam', 'content':'Temp'})
    cid = rv.get_json()['id']
    rv = client.delete(f'/api/comments/{cid}')
    assert rv.status_code == 200
