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
