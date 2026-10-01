class PIController:
    """Discrete direct-acting PI controller with fixed gains and positive time steps."""

    def __init__(
        self,
        kp: float,
        ki: float,
        output_min: float,
        output_max: float,
    ) -> None:
        if kp < 0 or ki < 0:
            raise ValueError("controller gains must be non-negative")
        if output_min >= output_max:
            raise ValueError("output_min must be less than output_max")
        self.kp = kp
        self.ki = ki
        self.output_min = output_min
        self.output_max = output_max
        self.integral_error = 0.0

    def update(self, setpoint: float, measurement: float, dt: float) -> float:
        """Return a bounded control output and conditionally integrate the error."""
        if dt <= 0:
            raise ValueError("dt must be positive")

        error = setpoint - measurement
        candidate_integral = self.integral_error + error * dt
        unconstrained_output = self.kp * error + self.ki * candidate_integral
        output = min(max(unconstrained_output, self.output_min), self.output_max)

        pushing_past_high_limit = (
            unconstrained_output >= self.output_max and error > 0
        )
        pushing_past_low_limit = (
            unconstrained_output <= self.output_min and error < 0
        )
        if not pushing_past_high_limit and not pushing_past_low_limit:
            self.integral_error = candidate_integral

        return output

    def reset(self) -> None:
        """Clear the accumulated error."""
        self.integral_error = 0.0