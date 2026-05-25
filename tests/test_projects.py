# import pytest
# from app import create_app
# from app.extensions import db

# @pytest.fixture
# def client():
#     app = create_app()
#     app.config['TESTING'] = True
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

#     with app.test_client() as client:
#         with app.app_context():
#             db.create_all()
#         yield client
#         with app.app_context():
#             db.drop_all()

# def get_auth_token(client):
#     """Helper function to get JWT token"""
#     client.post('/api/v1/auth/register', json={
#         'username': 'testuser',
#         'email': 'test@test.com',
#         'password': '123456'
#     })
#     response = client.post('/api/v1/auth/login', json={
#         'email': 'test@test.com',
#         'password': '123456'
#     })
#     return response.json['access_token']

# def test_create_project(client):
#     token = get_auth_token(client)
#     response = client.post('/api/v1/projects/',
#         headers={'Authorization': f'Bearer {token}'},
#         json={'name': 'My Project', 'description': 'Test description'}
#     )
#     assert response.status_code == 201
#     assert response.json['name'] == 'My Project'
#     assert response.json['description'] == 'Test description'

# def test_get_projects(client):
#     token = get_auth_token(client)
#     # Create a project first
#     client.post('/api/v1/projects/',
#         headers={'Authorization': f'Bearer {token}'},
#         json={'name': 'My Project'}
#     )
#     response = client.get('/api/v1/projects/',
#         headers={'Authorization': f'Bearer {token}'}
#     )
#     assert response.status_code == 200
#     assert len(response.json) == 1
#     assert response.json[0]['name'] == 'My Project'

# def test_update_project(client):
#     token = get_auth_token(client)
#     # Create project
#     create_resp = client.post('/api/v1/projects/',
#         headers={'Authorization': f'Bearer {token}'},
#         json={'name': 'Old Name'}
#     )
#     project_id = create_resp.json['id']

#     # Update project
#     response = client.put(f'/api/v1/projects/{project_id}',
#         headers={'Authorization': f'Bearer {token}'},
#         json={'name': 'New Name', 'description': 'Updated'}
#     )
#     assert response.status_code == 200
#     assert response.json['name'] == 'New Name'

# def test_delete_project(client):
#     token = get_auth_token(client)
#     # Create project
#     create_resp = client.post('/api/v1/projects/',
#         headers={'Authorization': f'Bearer {token}'},
#         json={'name': 'To Delete'}
#     )
#     project_id = create_resp.json['id']

#     # Delete project
#     response = client.delete(f'/api/v1/projects/{project_id}',
#         headers={'Authorization': f'Bearer {token}'}
#     )
#     assert response.status_code == 200
#     assert response.json['message'] == 'Project deleted successfully'


def get_auth_token(client):
    client.post('/api/v1/auth/register', json={
        'username': 'testuser',
        'email': 'test@test.com',
        'password': '123456'
    })
    response = client.post('/api/v1/auth/login', json={
        'email': 'test@test.com',
        'password': '123456'
    })
    return response.json['access_token']

def test_create_project(client):
    token = get_auth_token(client)
    response = client.post('/api/v1/projects/',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'My Project', 'description': 'Test description'}
    )
    assert response.status_code == 201
    assert response.json['name'] == 'My Project'

def test_get_projects(client):
    token = get_auth_token(client)
    client.post('/api/v1/projects/',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'My Project'}
    )
    response = client.get('/api/v1/projects/',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    assert len(response.json) == 1

def test_update_project(client):
    token = get_auth_token(client)
    create_resp = client.post('/api/v1/projects/',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Old Name'}
    )
    project_id = create_resp.json['id']

    response = client.put(f'/api/v1/projects/{project_id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'New Name', 'description': 'Updated'}
    )
    assert response.status_code == 200
    assert response.json['name'] == 'New Name'

def test_delete_project(client):
    token = get_auth_token(client)
    create_resp = client.post('/api/v1/projects/',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'To Delete'}
    )
    project_id = create_resp.json['id']

    response = client.delete(f'/api/v1/projects/{project_id}',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    assert response.json['message'] == 'Project deleted successfully'
