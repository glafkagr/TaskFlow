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

def create_project(client, token):
    resp = client.post('/api/v1/projects/',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Test Project'}
    )
    return resp.json['id']

def test_create_task(client):
    token = get_auth_token(client)
    project_id = create_project(client, token)

    response = client.post('/api/v1/tasks/',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'My Task', 'description': 'Do something', 'project_id': project_id}
    )
    assert response.status_code == 201
    assert response.json['title'] == 'My Task'

def test_get_tasks(client):
    token = get_auth_token(client)
    project_id = create_project(client, token)

    client.post('/api/v1/tasks/',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'Task 1', 'project_id': project_id}
    )
    client.post('/api/v1/tasks/',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'Task 2', 'project_id': project_id}
    )

    response = client.get('/api/v1/tasks/',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    assert len(response.json) == 2

def test_update_task_status(client):
    token = get_auth_token(client)
    project_id = create_project(client, token)

    create_resp = client.post('/api/v1/tasks/',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'My Task', 'project_id': project_id}
    )
    task_id = create_resp.json['id']

    response = client.patch(f'/api/v1/tasks/{task_id}/status',
        headers={'Authorization': f'Bearer {token}'},
        json={'status': 'completed'}
    )
    assert response.status_code == 200
    assert response.json['status'] == 'completed'

def test_delete_task(client):
    token = get_auth_token(client)
    project_id = create_project(client, token)

    create_resp = client.post('/api/v1/tasks/',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'To Delete', 'project_id': project_id}
    )
    task_id = create_resp.json['id']

    response = client.delete(f'/api/v1/tasks/{task_id}',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    assert response.json['message'] == 'Task deleted successfully'
