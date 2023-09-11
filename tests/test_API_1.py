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
def test_dashboard_route_api_request(mock_post, client):
    # Je teste l'API avec le client suivant : 
    client_id = '100066'

    # 2. Je simule une réponse OK et une réponse de l'API 2
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"client_data": {"AGE": {"8": 35}, "ANCIENNETE_CREDIT": {"8": 27.0}, "ANCIENNETE_EMPLOI": {"8": 3}, "CB_SOMME_DUES_RETARD": {"8": 0.0}, "CC_NOMBRE_RETRAIT_MOYEN": {"8": 0.0}, "CC_RATIO_CREDIT": {"8": 0.0}, "CHARGES_ANNUEL": {"8": 28957.5}, "HEURE_APP": {"8": 18}, "NBRE_CONTRAT_ACTIFS": {"8": 3.0}, "NBRE_ENFANT": {"8": 0}, "NBRE_J_RETARD": {"8": 0.0}, "NIVEAU_ETUDE_BAC": {"8": 0}, "NIVEAU_ETUDE_COLLEGE": {"8": 0}, "NIVEAU_ETUDE_ENS_SUP": {"8": 1}, "OCCUPATION_Businessman": {"8": 0}, "OCCUPATION_Commercial associate": {"8": 0}, "OCCUPATION_Maternity leave": {"8": 0}, "OCCUPATION_Pensioner": {"8": 0}, "OCCUPATION_State servant": {"8": 1}, "OCCUPATION_Unemployed": {"8": 0}, "OCCUPATION_Working": {"8": 0}, "POS_PROGRESS_MAX_MIN": {"8": 20.0}, "PROPRIETAIRE_N": {"8": 0}, "PROPRIETAIRE_Y": {"8": 1}, "RATIO_CREDIT_REVENU": {"8": 1.16}, "REVENUS_TOT": {"8": 315000.0}, "SCORE_2_EXT": {"8": 0.8087877917779122}, "SCORE_REGION": {"8": 1}, "SECTEUR_ACTIVITE": {"8": 0.055607766876632055}}, "client_id": "100066", "feat_imp": {"Class_0": {"0": -0.21965016866594606, "1": 0.3880272780737474, "2": 0.9968565391504538, "3": -0.45352238055713967, "4": -0.02353331776153634, "5": 1.2191732320107562, "6": -0.52331869641721, "7": -0.19572911537668342, "8": -0.26924463262944975, "9": 0.0, "10": 0.0, "11": 0.0, "12": 0.33590896349037175, "13": -0.05930569063310236, "14": 0.031305379685963315, "15": -0.1740344540669775, "16": -0.08141216187483694, "17": 0.1477620458783607, "18": 0.1694453119195768, "19": 1.0331728227536987, "20": 0.012132055210571464, "21": -0.14634099719468008, "22": 0.012519760486065191, "23": -0.07039049480564624, "24": 0.05579634868167303, "25": 0.16411725876826155, "26": 0.2606856058247662, "27": -0.14402998853673457, "28": -0.07531855423198505}, "Class_1": {"0": 0.21965016866594606, "1": -0.3880272780737474, "2": -0.9968565391504538, "3": 0.45352238055713967, "4": 0.02353331776153634, "5": -1.2191732320107562, "6": 0.52331869641721, "7": 0.19572911537668342, "8": 0.26924463262944975, "9": 0.0, "10": 0.0, "11": 0.0, "12": -0.33590896349037175, "13": 0.05930569063310236, "14": -0.031305379685963315, "15": 0.1740344540669775, "16": 0.08141216187483694, "17": -0.1477620458783607, "18": -0.1694453119195768, "19": -1.0331728227536987, "20": -0.012132055210571464, "21": 0.14634099719468008, "22": -0.012519760486065191, "23": 0.07039049480564624, "24": -0.05579634868167303, "25": -0.16411725876826155, "26": -0.2606856058247662, "27": 0.14402998853673457, "28": 0.07531855423198505}, "index": {"0": "PROPRIETAIRE_N", "1": "PROPRIETAIRE_Y", "2": "NIVEAU_ETUDE_ENS_SUP", "3": "NIVEAU_ETUDE_BAC", "4": "NIVEAU_ETUDE_COLLEGE", "5": "OCCUPATION_State servant", "6": "OCCUPATION_Working", "7": "OCCUPATION_Commercial associate", "8": "OCCUPATION_Pensioner", "9": "OCCUPATION_Unemployed", "10": "OCCUPATION_Maternity leave", "11": "OCCUPATION_Businessman", "12": "SECTEUR_ACTIVITE", "13": "NBRE_ENFANT", "14": "REVENUS_TOT", "15": "AGE", "16": "ANCIENNETE_EMPLOI", "17": "SCORE_REGION", "18": "HEURE_APP", "19": "SCORE_2_EXT", "20": "CC_NOMBRE_RETRAIT_MOYEN", "21": "POS_PROGRESS_MAX_MIN", "22": "CB_SOMME_DUES_RETARD", "23": "RATIO_CREDIT_REVENU", "24": "CC_RATIO_CREDIT", "25": "NBRE_CONTRAT_ACTIFS", "26": "NBRE_J_RETARD", "27": "CHARGES_ANNUEL", "28": "ANCIENNETE_CREDIT"}}, "score": 88}

    # 3. J'envoie une requête Post 
    response = client.post('/Dashboard/', data={'client_id': client_id})

    # 4. Assertions
    # J'évalue la réponse de la requête post
    assert response.status_code == 200
    assert 'Chargement du dashboard' in response.data.decode('utf-8')

    # Verify that requests.post was called once with the expected arguments
    mock_post.assert_called_once_with(
        'http://127.0.0.1:7000/predict/',
        json={'client_id': client_id}
    )

