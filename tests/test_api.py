def test_health_check(client):
    response = client.get('/api/v1/test')
    assert response.status_code == 200
    assert response.json['message'] == 'API works'

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
