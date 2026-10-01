import argparse
import sys
from pathlib import Path


def _simulate(ki: float) -> tuple[list[float], list[float]]:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
    from loopsim.controller import PIController
    from loopsim.simulation import simulate_room

    controller = PIController(kp=2.0, ki=ki, output_min=0.0, output_max=20.0)
    times, temperatures = simulate_room(
        controller=controller,
        setpoint=30.0,
        initial_temperature=20.0,
        ambient_temperature=20.0,
        tau=60.0,
        duration=600.0,
        dt=1.0,
    )
    return times, temperatures


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot simulated P and PI responses.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("pi_response.png"),
        help="image output path (default: pi_response.png)",
    )
    args = parser.parse_args()

    import matplotlib.pyplot as plt

    p_times, p_temperatures = _simulate(ki=0.0)
    pi_times, pi_temperatures = _simulate(ki=0.05)
    setpoint = 30.0

    figure, axis = plt.subplots()
    axis.plot(p_times, [setpoint] * len(p_times), "--", label="Setpoint")
    axis.plot(p_times, p_temperatures, label="P-only response")
    axis.plot(pi_times, pi_temperatures, label="PI response")
    axis.set_xlabel("Time (s)")
    axis.set_ylabel("Room temperature (°C)")
    axis.set_title("Simulated first-order room response")
    axis.text(0.99, 0.02, "simulated", transform=axis.transAxes, ha="right")
    axis.legend()
    axis.grid(True, alpha=0.3)
    figure.tight_layout()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(args.output, dpi=150)
    plt.close(figure)
    print(f"Saved plot to {args.output}")


if __name__ == "__main__":
    main()