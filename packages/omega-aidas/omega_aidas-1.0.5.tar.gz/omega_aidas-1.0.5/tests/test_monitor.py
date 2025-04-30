import sys, os
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath("generated_code"))
from omega_aidas.core.api import app

client = TestClient(app)


def test_monitor_endpoint():
    payload = {"release_id": "R123"}
    resp = client.post("/monitor", json=payload)
    assert resp.status_code == 200
    assert resp.json().get("monitored") == "R123"
