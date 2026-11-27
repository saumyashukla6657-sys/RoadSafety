"""
Unit Tests for app.py UI Helper Functions and Demo Scenarios
"""

import pytest
import pandas as pd
from app import (
    DEMO_SCENARIOS,
    urgency_color,
    render_urgency_gauge,
    render_score_bars,
    render_entities,
    render_hex_dump,
    render_route_segments,
)
from modules.routing_engine import VEHICLE_PROFILES


class TestDemoScenarios:
    def test_demo_scenarios_presence(self):
        assert len(DEMO_SCENARIOS) >= 4
        for sc in DEMO_SCENARIOS:
            assert "text" in sc and len(sc["text"].strip()) > 0
            assert "lat" in sc and 20.0 <= sc["lat"] <= 35.0
            assert "lon" in sc and 68.0 <= sc["lon"] <= 90.0
            assert "vehicle" in sc and sc["vehicle"] in VEHICLE_PROFILES


class TestUIHelperRenderers:
    def test_urgency_color_thresholds(self):
        assert urgency_color(9.5) == "#ff4757"  # Critical
        assert urgency_color(8.0) == "#ff4757"
        assert urgency_color(7.5) == "#ff6b35"  # High
        assert urgency_color(6.0) == "#ff6b35"
        assert urgency_color(5.0) == "#ffd32a"  # Moderate
        assert urgency_color(4.0) == "#ffd32a"
        assert urgency_color(3.2) == "#2ed573"  # Low

    def test_render_urgency_gauge(self):
        html = render_urgency_gauge(8.5)
        assert "urgency-value" in html
        assert "8.50" in html
        assert "CRITICAL" in html

        html_low = render_urgency_gauge(2.5)
        assert "2.50" in html_low
        assert "LOW" in html_low

    def test_render_score_bars(self):
        scores = {
            "Fire/Explosion": 0.75,
            "Minor Collision": 0.25,
        }
        html = render_score_bars(scores)
        assert "score-row" in html
        assert "Fire/Explosion" in html
        assert "75.0%" in html
        assert "Minor Collision" in html
        assert "25.0%" in html

    def test_render_entities_empty(self):
        html = render_entities({})
        assert "No specific entities extracted" in html

    def test_render_entities_populated(self):
        entities = {
            "casualty_count": ["3"],
            "fire_mention": ["fire"],
        }
        html = render_entities(entities)
        assert "entity-tag" in html
        assert "Casualty Count: 3" in html
        assert "Fire Mention: fire" in html

    def test_render_hex_dump(self):
        # 24 bytes = 48 hex chars
        sample_hex = "000102030405060708090A0B0C0D0E0F10111213AABBCCDD"
        html = render_hex_dump(sample_hex)
        assert "hex-dump" in html
        # Last 4 bytes should be styled in red
        assert "color:#ff4757" in html
        assert "AA" in html
        assert "DD" in html

    def test_render_route_segments(self):
        segments = [
            {
                "from": 0,
                "to": 1,
                "road_type": "highway",
                "traffic_level": "clear",
                "distance_km": 0.55,
                "cost": 0.33,
            }
        ]
        html = render_route_segments(segments)
        assert "route-seg" in html
        assert "0→1" in html
        assert "Highway" in html
        assert "Clear" in html
