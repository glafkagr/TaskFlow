def test_register(client):
    response = client.post('/api/v1/auth/register', json={
        'username': 'testuser',
        'email': 'test@test.com',
        'password': '123456'
    })
    assert response.status_code == 201
    assert response.json['username'] == 'testuser'

def test_login(client):
    # First register
    client.post('/api/v1/auth/register', json={
        'username': 'testuser',
        'email': 'test@test.com',
        'password': '123456'
    })

    # Then login
    response = client.post('/api/v1/auth/login', json={
        'email': 'test@test.com',
        'password': '123456'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json
