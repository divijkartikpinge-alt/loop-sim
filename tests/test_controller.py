from loopsim.controller import PIController
from loopsim.simulation import simulate_room


def _run_room(ki: float) -> tuple[float, float]:
    setpoint = 30.0
    controller = PIController(kp=2.0, ki=ki, output_min=0.0, output_max=20.0)
    _, temperatures = simulate_room(
        controller=controller,
        setpoint=setpoint,
        initial_temperature=20.0,
        ambient_temperature=20.0,
        tau=60.0,
        duration=600.0,
        dt=1.0,
    )
    return setpoint, temperatures[-1]


def test_zero_error_produces_zero_output() -> None:
    controller = PIController(kp=2.0, ki=0.1, output_min=0.0, output_max=20.0)

    assert controller.update(setpoint=25.0, measurement=25.0, dt=1.0) == 0.0


def test_proportional_only_loop_settles_below_setpoint() -> None:
    setpoint, final_temperature = _run_room(ki=0.0)

    assert 20.0 < final_temperature < setpoint - 0.5


def test_integral_action_settles_within_one_percent() -> None:
    setpoint, final_temperature = _run_room(ki=0.05)

    assert abs(final_temperature - setpoint) <= setpoint * 0.01


def test_output_stays_within_limits() -> None:
    controller = PIController(kp=10.0, ki=2.0, output_min=0.0, output_max=5.0)
    outputs = [
        controller.update(setpoint=100.0, measurement=0.0, dt=1.0),
        controller.update(setpoint=-100.0, measurement=0.0, dt=1.0),
    ]

    assert all(0.0 <= output <= 5.0 for output in outputs)


def test_anti_windup_holds_integral_and_reset_clears_it() -> None:
    controller = PIController(kp=1.0, ki=1.0, output_min=0.0, output_max=5.0)
    controller.update(setpoint=1.0, measurement=0.0, dt=1.0)
    stored_error_at_limit = controller.integral_error

    controller.update(setpoint=10.0, measurement=0.0, dt=1.0)
    controller.update(setpoint=10.0, measurement=0.0, dt=1.0)

    assert controller.integral_error == stored_error_at_limit
    controller.reset()
    assert controller.integral_error == 0.0