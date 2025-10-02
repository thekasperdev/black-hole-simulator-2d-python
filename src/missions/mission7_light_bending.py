# =============================================================================
# Mission 7: Light Bending (Schwarzschild Geodesics) Skeleton
# =============================================================================
# This skeleton provides the structure for integrating Schwarzschild null geodesics in the equatorial plane.
# Implement the logic for geodesic integration, ray management, and rendering.
# The vertex shader setup from previous missions is available for reuse.
# =============================================================================

import numpy as np
from .mission6_fixed_timestep import Mission6FixedTimestep

class Mission7LightBending(Mission6FixedTimestep):
    """
    Skeleton for Mission 7: Light bending in Schwarzschild spacetime (equatorial null geodesics).
    """
    def get_name(self):
        return "Mission 7: Light Bending (Schwarzschild Null Geodesics)"

    def initialize(self):
        """
        Set up Schwarzschild rays and rendering program(s).
        Reuse the vertex shader setup from previous missions. Implement the rest of the logic.
        """
        # TODO: Initialize geodesic rays and set up OpenGL resources
        pass

    def update(self, dt):
        """
        Update ray positions using geodesic integration. Implement logic here.
        """
        # TODO: Integrate geodesics and update rays
        pass

    def render(self):
        """
        Render ray trails and heads, then render the black hole disc. Implement rendering logic here.
        """
        # TODO: Draw geodesic ray trails and heads using OpenGL
        pass

    def handle_key(self, key, action, modifiers, keys):
        """
        Handle keyboard input for Mission 7. Implement controls as needed.
        """
        # TODO: Add keyboard controls for geodesic management
        pass
