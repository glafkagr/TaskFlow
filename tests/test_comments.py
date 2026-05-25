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

def create_task(client, token, project_id):
    resp = client.post('/api/v1/tasks/',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'My Task', 'project_id': project_id, 'assigned_to': 1}
    )
    return resp.json['id']

def test_create_comment(client):
    token = get_auth_token(client)
    project_id = create_project(client, token)
    task_id = create_task(client, token, project_id)

    response = client.post(f'/api/v1/tasks/{task_id}/comments/',
        headers={'Authorization': f'Bearer {token}'},
        json={'content': 'This is a comment'}
    )
    assert response.status_code == 201
    assert response.json['content'] == 'This is a comment'

def test_get_comments(client):
    token = get_auth_token(client)
    project_id = create_project(client, token)
    task_id = create_task(client, token, project_id)

    client.post(f'/api/v1/tasks/{task_id}/comments/',
        headers={'Authorization': f'Bearer {token}'},
        json={'content': 'First comment'}
    )
    client.post(f'/api/v1/tasks/{task_id}/comments/',
        headers={'Authorization': f'Bearer {token}'},
        json={'content': 'Second comment'}
    )

    response = client.get(f'/api/v1/tasks/{task_id}/comments/',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    assert len(response.json) == 2

def test_update_comment(client):
    token = get_auth_token(client)
    project_id = create_project(client, token)
    task_id = create_task(client, token, project_id)

    create_resp = client.post(f'/api/v1/tasks/{task_id}/comments/',
        headers={'Authorization': f'Bearer {token}'},
        json={'content': 'Original comment'}
    )
    comment_id = create_resp.json['id']

    response = client.put(f'/api/v1/tasks/{task_id}/comments/{comment_id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'content': 'Updated comment'}
    )
    assert response.status_code == 200
    assert response.json['content'] == 'Updated comment'

def test_delete_comment(client):
    token = get_auth_token(client)
    project_id = create_project(client, token)
    task_id = create_task(client, token, project_id)

    create_resp = client.post(f'/api/v1/tasks/{task_id}/comments/',
        headers={'Authorization': f'Bearer {token}'},
        json={'content': 'To delete'}
    )
    comment_id = create_resp.json['id']

    response = client.delete(f'/api/v1/tasks/{task_id}/comments/{comment_id}',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    assert response.json['message'] == 'Comment deleted successfully'
