# black-hole-simulator-2d-python
Black Hole Simulator 2D in Python - TechSync 2025

## Overview
This project simulates the physics and visualization of a black hole in 2D, with interactive missions that demonstrate concepts such as light bending, redshift, and collision detection. Each mission builds on the previous, adding new features and complexity.

## Features
- Interactive mission selection and runtime switching
- Real-time OpenGL rendering using moderngl
- Missions include:
  1. Grid + Black Hole: Visualizes a static grid and black hole disc
  2. Single Light Beam: Animates a single light beam
  3. Multiple Light Beams: Animates several parallel beams
  4. Multiple Beams + Collision Detection
  5. SI Units + Schwarzschild Radius
  6. Fixed Timestep Physics Loop
  7. Light Bending Simulation
  8. Validation Suite
  9. Red Shift Simulation

## Installation
1. Ensure you have Python 3.8+ installed.
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the simulator from the command line:
```bash
python src/mission_control.py
```
You will be prompted to select a mission (1-9). Follow on-screen instructions for controls and mission switching.

## Controls
- `1-9`: Jump to specific mission
- `H`: Show help
- `ESC`: Exit demo
- `SPACE`: Pause/unpause animation
- `R`: Reset beams
- `,` / `.`: Adjust beam spacing (Mission 4)

## Mission Details
- **Mission 1:** Grid + Black Hole — Foundation for all missions, static visualization.
- **Mission 2:** Single Light Beam — Adds dynamic simulation with a moving light beam.
- **Mission 3:** Multiple Light Beams — Multiple beams, no collisions.
- **Mission 4:** Multiple Beams + Collision Detection — Adds collision logic.
- **Mission 5:** SI Units + Schwarzschild Radius — Introduces physical units.
- **Mission 6:** Fixed Timestep Physics Loop — Demonstrates physics loop control.
- **Mission 7:** Light Bending Simulation — Simulates gravitational lensing.
- **Mission 8:** Validation Suite — For testing and validation.
- **Mission 9:** Red Shift Simulation — Visualizes redshift effects.