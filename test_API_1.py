import pytest
from API_1 import app  
from unittest.mock import patch

@pytest.fixture
#Je crée un test 'client'
def client():
    with app.test_client() as client:
        yield client
    
def test_welcome_route(client):
    response = client.get('/')
    assert response.status_code == 200  # Je teste si j'obtiens un code 200

@patch('API_1.requests.post')
def test_dashboard_route_api_request(client):
    # Je teste l'API avec le client suivant : 
    client_id = '100066'
    input_data = {'client_id': client_id}
    response = client.post('/Dashboard/', data=input_data)
    assert response.status_code == 200
    data_recu = response.json()
    assert 'client_id' in data_recu
    assert 'score' in data_recu
    assert 'feat_imp' in data_recu
    assert 'client_data' in data_recu
