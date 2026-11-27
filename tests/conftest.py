"""
Shared Pytest Fixtures for GuardianNodes RoadSoS Test Suite
"""

import sys
from pathlib import Path
import pytest

# Ensure root package directory is in sys.path
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.triage_engine import IntelligentTriageEngine
from modules.routing_engine import GraphRoutingEngine
from modules.mesh_simulator import MeshProtocolSimulator


@pytest.fixture
def triage_engine():
    """Returns an IntelligentTriageEngine configured with heuristic fallback (no network call)."""
    engine = IntelligentTriageEngine()
    engine._pipe = None
    # Patch _ensure_pipeline so tests run instantaneously without network requests
    engine._ensure_pipeline = lambda: None
    return engine


@pytest.fixture
def routing_engine():
    """Returns a deterministic GraphRoutingEngine seeded for reproducible tests."""
    return GraphRoutingEngine(seed=42)


@pytest.fixture
def mesh_simulator():
    """Returns a deterministic MeshProtocolSimulator seeded for reproducible tests."""
    return MeshProtocolSimulator(seed=42)
