import requests
import pytest

BASE_URL = "http://localhost:5000"

# Fixtures for reusable test data
@pytest.fixture(scope="module")
def agent_data():
    """Provides data for creating a new agent."""
    return {'eye_color': "brown", 'name': "Mimoo"}

@pytest.fixture(scope="module")
def lair_data():
    """Provides data for creating a new lair."""
    return {'name': "Bandenhöhle", 'cap': 10}

@pytest.fixture(scope="module")
def team_data():
    """Provides data for creating a new team, assuming lair with ID 0 exists."""
    return {'name': "Räuber Bande", 'lair_id': 0}

# Agent Tests
# ------------

def test_add_agent(agent_data):
    """Test for adding a new agent with valid data."""
    response = requests.post(f"{BASE_URL}/agent", json=agent_data)
    assert response.status_code == 201

def test_create_agent_with_invalid_eye_color():
    """Test for agent creation failure due to invalid eye color."""
    agent_data_invalid = {'name': "Test Agent", 'eye_color': "purple"}
    response = requests.post(f"{BASE_URL}/agent", json=agent_data_invalid)
    assert response.status_code == 422

# Lair Tests
# ------------

def test_add_lair(lair_data):
    """Test for adding a new lair with valid data."""
    response = requests.post(f"{BASE_URL}/lair", json=lair_data)
    assert response.status_code == 201

def test_create_lair_with_invalid_capacity():
    """Test for lair creation failure due to invalid capacity (negative number)."""
    lair_data_invalid = {'name': "Invalid Lair", 'cap': -5}
    response = requests.post(f"{BASE_URL}/lair", json=lair_data_invalid)
    assert response.status_code == 422

# Team Tests
# ------------

def test_create_team_with_valid_data(team_data):
    """Test for creating a team with valid data and ensuring the lair is included in the response."""
    response = requests.post(f"{BASE_URL}/team", json=team_data)
    assert response.status_code == 201
    assert "lair" in response.json()

def test_add_team_with_invalid_lair_id():
    """Test for adding a team with an invalid lair ID, which should fail."""
    team_invalid_lair = {'name': "Räuber Bande", 'lair_id': 999}
    response = requests.post(f"{BASE_URL}/team", json=team_invalid_lair)
    assert response.status_code == 400

def test_add_team_failure(team_data):
    """Test for adding a team with a name that already exists, which should fail."""
    # Assuming the team from `team_data` fixture has already been added
    response = requests.post(f"{BASE_URL}/team", json=team_data)
    assert response.status_code == 400

# Parametrized Test for Various Resources
# ------------

@pytest.mark.parametrize("path, data, expected_status", [
    ("/agent", {'eye_color': "green", 'name': "Agent Green"}, 201),
    ("/lair", {'name': "Mountain Hideout", 'cap': 5}, 201),
    ("/team", {'name': "Mountain Rangers", 'lair_id': 1}, 201),  # Adjust lair_id based on existing lairs
])
def test_create_resources(path, data, expected_status):
    """Test for creating various resources using parametrized data."""
    response = requests.post(f"{BASE_URL}{path}", json=data)
    assert response.status_code == expected_status

# Additional Functional Tests
# ------------

def test_add_agent_to_nonexistent_team():
    """Test for adding an agent to a non-existent team, which should fail."""
    response = requests.post(f"{BASE_URL}/team/9999/agent", json={"agent_id": 0})
    assert response.status_code == 404

def test_update_nonexistent_team():
    """Test for updating a non-existent team, which should fail."""
    update_data = {'name': "Ghost Team", 'lair_id': 0}
    response = requests.put(f"{BASE_URL}/team/9999", json=update_data)
    assert response.status_code == 404

def test_delete_nonexistent_team():
    """Test for deleting a non-existent team, which should fail."""
    response = requests.delete(f"{BASE_URL}/team/9999")
    assert response.status_code == 404

def test_partial_update_team():
    """Test for performing a partial update on a team, only updating the name."""
    update_data = {'name': "Updated Team Name"}
    team_id = 1  # Assuming this team exists
    response = requests.put(f"{BASE_URL}/team/{team_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()['name'] == "Updated Team Name"

def test_team_flee_with_random_choice():
    """Test the team flee functionality with the 'random' option enabled."""
    flee_data = {'random': True}
    team_id = 1  # Assuming this team exists
    response = requests.put(f"{BASE_URL}/team/{team_id}/flee", json=flee_data)
    assert response.status_code == 200
