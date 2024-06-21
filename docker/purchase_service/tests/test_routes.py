import pytest
from unittest.mock import Mock

def test_health(client):
    response = client.get('/api/purchase/')
    assert response.status_code == 200