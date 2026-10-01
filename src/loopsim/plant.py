import math


def step_response(t: float, t_start: float, t_final: float, tau: float) -> float:
    """First-order response to a setpoint step at t = 0.

    Assumptions: one time constant, no dead time, constant input,
    plant starts at t_start. Simulated, not measured.
    """
    if tau <= 0:
        raise ValueError("tau must be positive")
    return t_final + (t_start - t_final) * math.exp(-t / tau)
