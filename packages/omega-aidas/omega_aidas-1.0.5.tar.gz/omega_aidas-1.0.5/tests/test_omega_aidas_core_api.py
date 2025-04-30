# tests/test_omega_aidas_core_api.py

import sys, os
import pytest
from fastapi.testclient import TestClient

# Ensure Python can import the generated code
sys.path.insert(0, os.path.abspath("generated_code"))

from omega_aidas.core.api import app  # must match the package path you generated

client = TestClient(app)


def test_deploy_singularity_endpoint_exists():
    resp = client.post("/deploy-singularity", json={"requirement": "test"})
    # Endpoint must exist (not a 404)
    assert resp.status_code != 404, "Endpoint /deploy-singularity not found"
