# Industrial Systems Modeling

A reproducible, **illustrative** engineering decision-support model for comparing gas-phase filtration configurations under matched fan conditions.

## Why this matters

Comparing filters by removal efficiency alone can mislead product decisions. Added media resistance can reduce system airflow. The effective clean-air delivery rate (CADR) combines both:

```
CADR = operating airflow × single-pass removal efficiency
```

This example combines a simplified quadratic fan curve, quadratic system pressure loss, and an illustrative first-order removal relationship to compare configurations on **CADR, pressure drop, and estimated service-life proxy**. It is a teaching/demo model, **not** validated equipment performance, a safety analysis, or a substitute for laboratory testing.

## Run

Python 3.10+ (standard library only):

```bash
python model.py
python -m unittest discover -s tests -v
```

The model writes `results.csv`. All inputs are synthetic and deliberately labeled.

## Engineering approach

- Fan static pressure: `P_fan(Q) = P_shutoff × [1 - (Q/Q_free)^2]`
- System resistance: `P_system(Q) = (K_base + K_media) × Q^2`
- Solve the operating point analytically for the positive airflow
- Illustrative single-pass removal: `eta = 1 - exp(-k × loading / Q)`
- `CADR = Q × eta`
- Service-life proxy: `capacity / (Q × inlet_concentration × eta)`

Units must remain internally consistent; these inputs use an intentionally normalized pressure/airflow scale. The service-life proxy assumes fixed capacity, steady inlet concentration, and ideal capture. Real systems require contaminant-specific breakthrough curves, humidity/temperature effects, competitive adsorption, media shedding, loading variation, and measured fan curves.

## Illustrative decision

The best option depends on operating conditions and constraints. A configuration with higher single-pass efficiency may deliver less clean air if its pressure drop reduces airflow. Evaluate CADR and lifetime alongside energy, noise, manufacturability, and cost.

## Public-data and IP policy

This project contains no employer data, product specifications, supplier information, or confidential test results. Numbers are synthetic and must not be interpreted as EnviroKlenz or other product claims.

## Author

Christopher Hall — [professional background](https://jacksonridgeholdings.com/christopher-hall/)
