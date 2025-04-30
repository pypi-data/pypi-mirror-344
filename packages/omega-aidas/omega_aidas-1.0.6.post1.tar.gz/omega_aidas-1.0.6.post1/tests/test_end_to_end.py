import sys, os
from fastapi.testclient import TestClient

# Ensure generated code is on the path
sys.path.insert(0, os.path.abspath("generated_code"))

from omega_aidas.core.api import app

client = TestClient(app)


def test_full_workflow():
    # 1) implement-feature
    resp1 = client.post("/implement-feature", json={"requirement": "foo"})
    assert resp1.status_code == 200
    data1 = resp1.json()
    r_id = data1["implementation"]["release_id"]
    assert r_id.startswith("REL-")

    # 2) deploy-singularity
    resp2 = client.post("/deploy-singularity", json={"requirement": "foo"})
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2["status"] == "success"
    assert data2["requirement"] == "foo"

    # 3) monitor
    resp3 = client.post("/monitor", json={"release_id": r_id})
    assert resp3.status_code == 200
    data3 = resp3.json()
    assert data3["release_id"] == r_id
    assert data3["status"] == "healthy"
    assert isinstance(data3["anomalies"], list)
