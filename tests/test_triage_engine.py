"""
Unit Tests for IntelligentTriageEngine
"""

import pytest
from modules.triage_engine import (
    IntelligentTriageEngine,
    TriageResult,
    CANDIDATE_LABELS,
    SEVERITY_WEIGHTS,
    _extract_entities,
    _compute_urgency,
    _recommend_units,
)


class TestTriageConstants:
    def test_candidate_labels_defined(self):
        assert len(CANDIDATE_LABELS) == 5
        assert "Fire/Explosion" in CANDIDATE_LABELS
        assert "Critical Medical Trauma" in CANDIDATE_LABELS
        assert "Minor Collision" in CANDIDATE_LABELS
        assert "Hazardous Material Leak" in CANDIDATE_LABELS
        assert "Vehicle Entrapment" in CANDIDATE_LABELS

    def test_severity_weights_valid(self):
        for label in CANDIDATE_LABELS:
            assert label in SEVERITY_WEIGHTS
            assert 0.0 <= SEVERITY_WEIGHTS[label] <= 1.0


class TestEntityExtraction:
    def test_extract_vehicle_counts_digits(self):
        text = "There are 3 cars and 1 truck involved in the collision."
        entities = _extract_entities(text)
        assert "vehicle_count" in entities
        assert "3" in entities["vehicle_count"]
        assert "1" in entities["vehicle_count"]

    def test_extract_vehicle_counts_words(self):
        text = "Two cars and four vans collided near the intersection."
        entities = _extract_entities(text)
        assert "vehicle_count" in entities
        assert "2" in entities["vehicle_count"]
        assert "4" in entities["vehicle_count"]

    def test_extract_casualty_counts(self):
        text = "At least five casualties reported and two people injured."
        entities = _extract_entities(text)
        assert "casualty_count" in entities
        assert "5" in entities["casualty_count"]
        assert "2" in entities["casualty_count"]

    def test_extract_fire_hazards(self):
        text = "Thick black smoke and burning flames visible after an explosion."
        entities = _extract_entities(text)
        assert "fire_mention" in entities
        assert len(entities["fire_mention"]) > 0

    def test_extract_hazmat_hazards(self):
        text = "A chemical tanker has a gas leak and toxic fuel spill."
        entities = _extract_entities(text)
        assert "hazmat_mention" in entities
        assert len(entities["hazmat_mention"]) > 0

    def test_extract_speed_mention(self):
        text = "The vehicle was speeding at 120 km/h before impact."
        entities = _extract_entities(text)
        assert "speed_mention" in entities
        assert "120" in entities["speed_mention"]

    def test_empty_entities_on_plain_text(self):
        text = "Everything is quiet and normal today."
        entities = _extract_entities(text)
        assert entities == {}


class TestUrgencyComputation:
    def test_urgency_bounds(self):
        # Test low urgency
        low_scores = {l: 0.05 for l in CANDIDATE_LABELS}
        low_scores["Minor Collision"] = 0.8
        u_low = _compute_urgency(low_scores, {})
        assert 1.0 <= u_low <= 10.0

        # Test high urgency
        high_scores = {l: 0.02 for l in CANDIDATE_LABELS}
        high_scores["Fire/Explosion"] = 0.92
        entities = {"casualty_count": ["4"], "fire_mention": ["fire"]}
        u_high = _compute_urgency(high_scores, entities)
        assert 1.0 <= u_high <= 10.0
        assert u_high > u_low

    def test_urgency_bonus_applied(self):
        scores = {l: 0.2 for l in CANDIDATE_LABELS}
        u_base = _compute_urgency(scores, {})
        u_with_fire = _compute_urgency(scores, {"fire_mention": ["fire"]})
        u_with_hazmat = _compute_urgency(scores, {"hazmat_mention": ["chemical"]})
        u_with_casualties = _compute_urgency(scores, {"casualty_count": ["3"]})

        assert u_with_fire > u_base
        assert u_with_hazmat > u_base
        assert u_with_casualties > u_base


class TestUnitRecommendations:
    def test_fire_recommendation(self):
        units = _recommend_units("Fire/Explosion", 7.0, {})
        assert any("Fire Engine" in u for u in units)

    def test_medical_recommendation(self):
        units = _recommend_units("Critical Medical Trauma", 7.0, {})
        assert any("Life Support" in u or "Ambulance" in u for u in units)

    def test_entrapment_recommendation(self):
        units = _recommend_units("Vehicle Entrapment", 7.0, {})
        assert any("Heavy Rescue" in u for u in units)

    def test_hazmat_recommendation(self):
        units = _recommend_units("Hazardous Material Leak", 7.0, {})
        assert any("HazMat" in u for u in units)

    def test_minor_collision_recommendation(self):
        units = _recommend_units("Minor Collision", 3.0, {})
        assert any("Ambulance" in u or "Police" in u for u in units)

    def test_critical_helicopter_dispatch(self):
        units = _recommend_units("Critical Medical Trauma", 9.2, {})
        assert any("Trauma Helicopter" in u for u in units)


class TestTriageEngineAnalyze:
    def test_empty_text_raises_value_error(self, triage_engine):
        with pytest.raises(ValueError, match="must not be empty"):
            triage_engine.analyze("")

    def test_whitespace_text_raises_value_error(self, triage_engine):
        with pytest.raises(ValueError, match="must not be empty"):
            triage_engine.analyze("    \n\t  ")

    def test_analyze_explosion_scenario(self, triage_engine):
        statement = "Massive explosion with 3 cars on fire and 2 casualties trapped."
        res = triage_engine.analyze(statement)

        assert isinstance(res, TriageResult)
        assert res.top_label == "Fire/Explosion"
        assert res.urgency_index >= 7.0
        assert len(res.recommended_units) > 0
        assert "vehicle_count" in res.entities
        assert "casualty_count" in res.entities
        assert "fire_mention" in res.entities
        assert abs(sum(res.label_scores.values()) - 1.0) < 0.01

    def test_analyze_minor_crash_scenario(self, triage_engine):
        statement = "Small scratch on the bumper, minor dent in parking lot."
        res = triage_engine.analyze(statement)

        assert isinstance(res, TriageResult)
        assert res.top_label == "Minor Collision"
        assert res.urgency_index < 6.0
