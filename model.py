"""Synthetic filtration comparison at matched fan conditions (standard library only)."""
from dataclasses import dataclass
from math import exp, sqrt
from pathlib import Path
import csv

@dataclass(frozen=True)
class Configuration:
    name: str
    media_resistance: float
    capture_coefficient: float
    loading: float
    capacity: float

@dataclass(frozen=True)
class Result:
    name: str
    airflow: float
    pressure_drop: float
    removal_efficiency: float
    cadr: float
    service_life_proxy: float

def operating_airflow(p_shutoff: float, q_free: float, base_resistance: float, media_resistance: float) -> float:
    """Solve P_shutoff*(1-(Q/Q_free)^2)=(K_base+K_media)*Q^2."""
    if min(p_shutoff, q_free) <= 0 or min(base_resistance, media_resistance) < 0:
        raise ValueError("Fan parameters must be positive and resistances nonnegative")
    return sqrt(p_shutoff / (p_shutoff / q_free**2 + base_resistance + media_resistance))

def evaluate(config: Configuration, *, p_shutoff=250.0, q_free=500.0, base_resistance=0.00035, inlet_concentration=1.0) -> Result:
    if min(config.capture_coefficient, config.loading, config.capacity, inlet_concentration) <= 0:
        raise ValueError("Capture, loading, capacity and concentration must be positive")
    q = operating_airflow(p_shutoff, q_free, base_resistance, config.media_resistance)
    eta = -__import__("math").expm1(-config.capture_coefficient * config.loading / q)
    cadr = q * eta
    pressure = (base_resistance + config.media_resistance) * q**2
    lifetime = config.capacity / (cadr * inlet_concentration)
    return Result(config.name, q, pressure, eta, cadr, lifetime)

EXAMPLES = [
    Configuration("Low-resistance media", 0.00015, 180.0, 1.0, 25000.0),
    Configuration("Balanced media", 0.00045, 300.0, 1.0, 30000.0),
    Configuration("High-loading media", 0.00110, 500.0, 1.0, 45000.0),
]

def main():
    results = [evaluate(c) for c in EXAMPLES]
    out = Path(__file__).with_name("results.csv")
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["configuration", "airflow_normalized", "pressure_drop_normalized", "single_pass_efficiency", "cadr_normalized", "service_life_proxy"])
        for r in results:
            writer.writerow([r.name, *[round(x, 6) for x in (r.airflow, r.pressure_drop, r.removal_efficiency, r.cadr, r.service_life_proxy)]])
    print(f"{'Configuration':25} {'Airflow':>10} {'Removal':>10} {'CADR':>10} {'Life proxy':>12}")
    for r in results:
        print(f"{r.name:25} {r.airflow:10.1f} {r.removal_efficiency:10.1%} {r.cadr:10.1f} {r.service_life_proxy:12.1f}")
    print("Wrote", out)

if __name__ == "__main__":
    main()
