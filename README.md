# Winds Collimated by the Motion of Giant Stars in Close Binary Systems

This repository contains the numerical simulations and analysis code used in the research paper:

> **Winds Collimated by the Motion of Giant Stars in Close Binary Systems**  
> Michael Ladyzhensky, 2025

The project studies how the orbital motion of a Wolf–Rayet star in the X-ray binary system **Cygnus X-3** affects the **collimation patterns of stellar winds**. By running 2-D and 3-D simulations while varying the stellar and wind velocities, we investigate how these parameters impact the morphology of the outflow and its spiral / ring-like structures.

---

## Project Overview

The simulations model:

- A Wolf–Rayet star of mass **10 M☉** orbiting a compact object of mass **2.4 M☉**.
- An orbital radius of **0.015 AU**.
- Stellar winds launched from the star’s surface with different speeds relative to the star’s orbital velocity (e.g., half, equal to, or double the stellar velocity). :contentReference[oaicite:1]{index=1}  

Key goals:

- Compute the orbital parameters (semi-major axis, orbital period, and stellar velocity) using **Kepler’s Third Law** and basic two-body dynamics. :contentReference[oaicite:2]{index=2}  
- Launch and track test wind particles as they are emitted from the star along its orbit.
- Visualize **2-D face-on** and **3-D** views of the wind distribution to study collimation patterns and their dependence on stellar and wind velocities. :contentReference[oaicite:3]{index=3}  

    ├── fig1_2d_wind_spiral.png
    ├── fig3_slow_star_winds.png
    ├── fig4_fast_star_winds.png
    ├── fig5_2d_snapshot.png
    └── fig6_3d_snapshot.png
