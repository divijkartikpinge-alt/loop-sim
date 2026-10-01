from math import ceil, exp

from loopsim.controller import PIController


def simulate_room(
    controller: PIController,
    setpoint: float,
    initial_temperature: float,
    ambient_temperature: float,
    tau: float,
    duration: float,
    dt: float,
) -> tuple[list[float], list[float]]:
    """Simulate a room with one time constant and heat input above ambient."""
    if tau <= 0:
        raise ValueError("tau must be positive")
    if dt <= 0:
        raise ValueError("dt must be positive")
    if duration < 0:
        raise ValueError("duration must be non-negative")

    times = [0.0]
    temperatures = [initial_temperature]
    step_count = ceil(duration / dt)

    for index in range(1, step_count + 1):
        current_time = min(index * dt, duration)
        interval = current_time - times[-1]
        control_output = controller.update(
            setpoint, temperatures[-1], interval
        )
        controlled_temperature = ambient_temperature + control_output
        next_temperature = controlled_temperature + (
            temperatures[-1] - controlled_temperature
        ) * exp(-interval / tau)
        times.append(current_time)
        temperatures.append(next_temperature)

    return times, temperatures