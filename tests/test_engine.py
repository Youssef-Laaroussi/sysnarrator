import pytest
from unittest.mock import patch, MagicMock
from sysnarrator.engine import DiagnosticEngine, HealthBreakdown

def test_health_score_calculation():
    engine = DiagnosticEngine()
    breakdown = engine.calculate_health_score()
    assert 0 <= breakdown.score <= 100
    assert breakdown.status_label in ["EXCELLENT", "GOOD", "FAIR", "POOR"]
    assert isinstance(breakdown.penalties, list)

def test_engine_insights_generation():
    engine = DiagnosticEngine()
    insights = engine.analyze_system()
    assert isinstance(insights, list)
    for ins in insights:
        assert ins.severity in ['critical', 'warning', 'info', 'ok']
        assert ins.category
        assert ins.confidence > 0.0
