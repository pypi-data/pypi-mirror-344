import sys, os
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath("generated_code"))
from omega_aidas.core.api import app

client = TestClient(app)


def test_status_endpoint():
    resp = client.get("/status")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
