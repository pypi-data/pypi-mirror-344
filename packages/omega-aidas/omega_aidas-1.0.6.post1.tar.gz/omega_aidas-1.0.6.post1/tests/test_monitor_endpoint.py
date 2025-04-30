import sys, os
import pytest
from fastapi.testclient import TestClient

# Ensure generated_code is on sys.path
sys.path.insert(0, os.path.abspath("generated_code"))

from omega_aidas.core.api import app

client = TestClient(app)


def test_monitor_endpoint_monitors_stub():
    # Given a dummy release_id
    payload = {"release_id": "R123"}
    resp = client.post("/monitor", json=payload)
    assert resp.status_code == 200
    data = resp.json()

    # Our stub returns either a dict from ops.monitor, or {"monitored": release_id}
    assert "monitored" in data
    assert data["monitored"] == "R123"
