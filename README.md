# loop-sim
Simulated control-loop experiments: first-order plant, then PI controller, saturation and dead time.
All data is simulated, not measured. Run the tests with `pytest`.
Limits: single time constant, no real building data yet.

## PI controller

The discrete PI controller combines proportional response with accumulated error,
limits its output, and uses conditional integration to prevent windup. It assumes
fixed non-negative gains, positive time steps, a direct-acting controller, and a
first-order room with one time constant. All responses are simulated, not measured.

Run `python scripts/plot_pi_response.py` from the repository root to save
`pi_response.png`; use `--output path/to/image.png` to choose another image path.