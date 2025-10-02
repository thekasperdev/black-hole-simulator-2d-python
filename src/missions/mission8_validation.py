# =============================================================================
# Mission 8: Light Bending Validation (Skeleton)
# =============================================================================
# This skeleton provides the structure for validating light bending against analytic formulas.
# Implement the logic for measuring deflection, comparing to analytic results, and rendering.
# The vertex shader setup from previous missions is available for reuse.
# =============================================================================

import numpy as np
from .mission7_light_bending import Mission7LightBending

class Mission8Validation(Mission7LightBending):
    """
    Skeleton for Mission 8: Numeric validation of light bending against analytic formulas.
    """
    def get_name(self):
        return "Mission 8: Light Bending Validation"

    def initialize(self):
        """
        Set up validating rays and rendering program(s).
        Reuse the vertex shader setup from previous missions. Implement the rest of the logic.
        """
        # TODO: Initialize validating rays and set up OpenGL resources
        pass

    def update(self, dt):
        """
        Update ray positions and measure deflection. Implement validation logic here.
        """
        # TODO: Measure deflection and compare to analytic results
        pass

    def render(self):
        """
        Render ray trails and heads, then render the black hole disc. Implement rendering logic here.
        """
        # TODO: Draw validation results using OpenGL
        pass

    def handle_key(self, key, action, modifiers, keys):
        """
        Handle keyboard input for Mission 8. Implement controls as needed.
        """
        # TODO: Add keyboard controls for validation management
        pass
