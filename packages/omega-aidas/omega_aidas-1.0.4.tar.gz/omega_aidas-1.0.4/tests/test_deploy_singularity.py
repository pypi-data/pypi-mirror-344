import sys, os
from fastapi.testclient import TestClient

# Ensure generated_code is on sys.path
sys.path.insert(0, os.path.abspath("generated_code"))

from omega_aidas.core.api import app

client = TestClient(app)


def test_deploy_singularity_endpoint():
    payload = {"requirement": "secure auth"}
    resp = client.post("/deploy-singularity", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    # Our stub should echo back status and requirement
    assert data["status"] == "success"
    assert data["requirement"] == "secure auth"
