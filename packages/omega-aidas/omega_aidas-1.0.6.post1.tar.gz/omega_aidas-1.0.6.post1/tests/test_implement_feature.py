import sys, os
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath("generated_code"))
from omega_aidas.core.api import app

client = TestClient(app)


def test_implement_feature():
    payload = {"requirement": "foo"}
    resp = client.post("/implement-feature", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "implementation" in data
    # stub returns the requirement back
    assert data["implementation"]["requirement"] == "foo"
