# 🌟 Tidal Disruption Event (TDE) Simulator & Black Hole Animation 🕳️

An interactive 2D astrophysical simulation and real-time visualization of a **Tidal Disruption Event (TDE)** using Python, NumPy, and Matplotlib. 

When a star ventures too close to a supermassive black hole, the black hole's immense tidal forces overcome the star's self-gravity, stretching and shredding it apart—a process astrophysicists call **spaghettification**—before sweeping the stellar debris into a glowing accretion disk and consuming it past the event horizon.

---

## ✨ Features

- **Particle-Based Stellar Model**: Simulates a spherical star composed of 1,800 individual particles with orbital velocity vectors.
- **Dynamic Physics Engine**:
  - Newtonian gravity governed by inverse-square law ($a = \frac{G \cdot M}{r^2}$).
  - Tidal disruption triggered at the critical tidal radius ($r_t$).
  - Conservation of angular momentum with tangential velocity boosts inducing accretion disk swirl.
  - Viscous friction simulating energy dissipation and inward spiraling toward the black hole.
  - Event horizon boundary condition where particles crossing $r \le 2.5 \cdot r_{bh}$ are permanently consumed.
- **Multi-Stage Real-Time HUD**:
  - Live elapsed astrophysical time (in hours).
  - Particle state telemetry: **Intact**, **Accretion Disk**, and **Consumed**.
  - Automatic phase detection:
    - `PHASE 1: Approach`
    - `PHASE 2: Spaghettification!`
    - `PHASE 3: Accretion Disk`
    - `PHASE 4: Consumption`
- **Dynamic Heat & Color Mapping**: Accretion disk particles heat up as they plunge closer to the event horizon, visually shifting to brighter, hotter colors.
- **Infinite Looping**: Automatically re-seeds a new star once 90% of the particles have been consumed.

---

## 🔬 Scientific Background

A **Tidal Disruption Event (TDE)** occurs when the tidal forces exerted on an approaching star by a supermassive black hole exceed the star's self-gravity:

$$r_t \approx R_* \left( \frac{M_{\text{BH}}}{M_*} \right)^{1/3}$$

Within this tidal radius ($r_t$):
1. **Disruption & Spaghettification**: Differential gravitational forces pull the near side of the star much harder than the far side, stretching the star into a stream of stellar debris.
2. **Circularization & Disk Formation**: Debris streams collide with themselves via orbital precession, losing kinetic energy through shock heating and forming a swirling, ultra-hot accretion disk.
3. **Accretion**: Magnetic viscosity and turbulent friction transport angular momentum outward, causing mass to spiral inward across the event horizon.

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+**
- Required libraries:
  - `numpy`
  - `matplotlib`

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/dinmuhamedzamish/black-hole-animation.git
   cd black-hole-animation
   ```

2. **Create a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install numpy matplotlib
   ```
   *(or `pip install -r requirements.txt` if using the requirements file)*

---

## 🎮 Running the Simulation

Execute the Python script:

```bash
python black_hole_2.py
```

A high-contrast Matplotlib window will launch displaying:
- **Center**: Supermassive black hole with multi-layered event horizon glow (red, orange, yellow).
- **Cyan Dashed Ring**: The tidal disruption radius ($r = 48.0$).
- **Particles**: Approaching star particles shifting from yellow/dim to blazing hot as the accretion disk forms.

Press <kbd>q</kbd> or close the window to exit the simulation.

---

## ⚙️ Configurable Parameters

You can customize the simulation behavior by adjusting parameters at the top of [`black_hole_2.py`](black_hole_2.py):

| Parameter | Default | Description |
| :--- | :--- | :--- |
| `BLACK_HOLE_MASS` | `1_000_000.0` | Mass of the central supermassive black hole |
| `BLACK_HOLE_RADIUS`| `2.0` | Visual and absorption radius threshold of the black hole |
| `TIDAL_RADIUS` | `48.0` | Radius where tidal forces rip the star into an accretion disk |
| `STAR_RADIUS` | `2.0` | Radius of the initial spherical star |
| `STAR_DISTANCE` | `70.0` | Initial distance of the star from the black hole |
| `NUM_PARTICLES` | `1800` | Total number of particles representing the star |
| `DT` | `0.03` | Simulation time step (lower values increase numerical precision) |
| `FRICTION` | `0.010` | Viscous drag factor driving inward orbital decay in the disk |

---

## 📂 Repository Structure

```text
black-hole-animation/
├── black_hole_2.py      # Core simulation script and Matplotlib animation loop
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## 📜 License

This project is open-source and available under the [MIT License](LICENSE).
