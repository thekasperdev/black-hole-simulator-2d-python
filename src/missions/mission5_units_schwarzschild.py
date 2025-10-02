# =============================================================================
# Mission 5: SI Units & Schwarzschild Radius (Skeleton)
# =============================================================================
# This skeleton provides the structure for using SI units and the Schwarzschild radius in the simulation.
# Implement the logic for unit conversion, black hole radius calculation, and beam management.
# The vertex shader setup from previous missions is available for reuse.
# =============================================================================

import numpy as np
import moderngl
from .mission4_multiple_beams import Mission4MultipleBeams

class Mission5UnitsSchwarzschild(Mission4MultipleBeams):
    """
    Skeleton for Mission 5: Multiple parallel light beams using SI units and Schwarzschild radius.
    """
    # Physical constants (SI units)
    G = 6.67430e-11  # m^3 kg^-1 s^-2
    c = 299_792_458  # m/s

    def get_name(self) -> str:
        return "Mission 5: SI Units & Schwarzschild Radius"

    def initialize(self):
        """
        Set up SI unit world and black hole parameters.
        Reuse the vertex shader setup from previous missions. Implement the rest of the logic.
        """
        # TODO: Convert units and calculate Schwarzschild radius
        pass

    def update(self, dt: float):
        """
        Update multiple particles and implement logic using SI units here.
        """
        # TODO: Move beams and apply SI unit logic
        pass

    def render(self):
        """
        Render the grid background and multiple light beams. Implement rendering logic here.
        """
        # TODO: Draw beams and black hole using OpenGL
        pass

    def handle_key(self, key, action, modifiers, keys):
        """
        Handle keyboard input for Mission 5. Implement controls as needed.
        """
        # TODO: Add keyboard controls for unit management
        pass
