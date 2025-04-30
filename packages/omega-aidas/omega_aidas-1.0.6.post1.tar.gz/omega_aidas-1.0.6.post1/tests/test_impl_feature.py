import sys, os
from fastapi.testclient import TestClient

# Ensure generated_code is on sys.path
sys.path.insert(0, os.path.abspath("generated_code"))

from omega_aidas.core.impl import CognitiveCore, ImplementationAutomaton


def test_stub_implement_feature():
    core = CognitiveCore()
    impl = ImplementationAutomaton(core)
    out = impl.implement_feature("foo requirement")
    assert isinstance(out, dict)
    assert "implementation" in out
    assert "validation" in out and isinstance(out["validation"], dict)
    assert "quantum_hash" in out
    # implementation should be non‐empty
    assert out["implementation"]
    # validation.success must be True
    assert out["validation"]["success"] is True
