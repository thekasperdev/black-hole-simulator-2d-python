# =============================================================================
# Mission 2: Single Light Beam (Skeleton)
# =============================================================================
# This skeleton provides the structure for animating a single light beam.
# Implement the logic for particle movement, rendering, and controls.
# The vertex shader setup is provided.
# =============================================================================

import moderngl
import numpy as np
from .mission1_grid_blackhole import Mission1GridBlackHole

class Mission2SingleBeam(Mission1GridBlackHole):
    """
    Skeleton for Mission 2: Single light particle moving from left to right.
    """
    def get_name(self) -> str:
        return "Mission 2: Single Light Beam"

    def initialize(self):
        """
        Set up shaders and create initial particle.
        The vertex shader below is provided. Implement the rest of the logic.
        """
        # Vertex shader for particle rendering
        self.pt_prog = self.ctx.program(
            vertex_shader="""
            // Vertex Shader: Renders a point for the light beam
            #version 330
            in vec2 in_pos;
            uniform float u_point_size;
            void main() {
                // TODO: Transform coordinates for rendering
                gl_Position = vec4(0.0, 0.0, 0.0, 1.0); // Placeholder
                gl_PointSize = u_point_size;
            }
            """,
            fragment_shader="""
            // Fragment shader: Implement coloring logic here
            #version 330
            out vec4 f_color;
            uniform vec3 u_color;
            void main() {
                // TODO: Color the particle
                f_color = vec4(u_color, 1.0); // Placeholder
            }
            """
        )
        # TODO: Set up VBO/VAO and any other required OpenGL resources

    def update(self, dt: float):
        """
        Update particle position and handle respawning. Implement animation logic here.
        """
        # TODO: Move the particle and respawn if needed
        pass

    def render(self):
        """
        Render the grid background and moving particle. Implement rendering logic here.
        """
        # TODO: Draw the particle using OpenGL
        pass

    def handle_key(self, key, action, modifiers, keys):
        """
        Handle keyboard input for Mission 2. Implement controls as needed.
        """
        # TODO: Add keyboard controls for pausing or resetting
        pass
