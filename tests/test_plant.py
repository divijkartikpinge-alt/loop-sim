import pytest
from loopsim.plant import step_response

def test_63_percent_at_tau():
    t_start, t_final, tau = 20.0, 30.0, 120.0
    covered = (step_response(tau, t_start, t_final, tau) - t_start) / (t_final - t_start)
    assert covered == pytest.approx(0.632, abs=1e-3)

def test_starts_at_initial_value():
    assert step_response(0, 20.0, 30.0, 120.0) == pytest.approx(20.0)

def test_rejects_nonpositive_tau():
    with pytest.raises(ValueError):
        step_response(1, 20.0, 30.0, 0)
