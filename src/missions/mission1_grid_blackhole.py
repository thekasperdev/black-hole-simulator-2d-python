# =============================================================================
# Mission 1: Grid Background and Black Hole Disc (Skeleton)
# =============================================================================
# This skeleton provides the OpenGL vertex shader setup for rendering a grid and black hole disc.
# Implement the logic for initializing, updating, and rendering the mission.
# =============================================================================

import moderngl
import numpy as np
from .base_mission import BaseMission


class Mission1GridBlackHole(BaseMission):
    """
    Skeleton for Mission 1: Display grid background with black hole disc.
    """

    def get_name(self) -> str:
        return "Mission 1: Grid + Black Hole"

    def initialize(self):
        """
        Set up shaders for grid and black hole rendering.
        The vertex shader below is provided. Implement the rest of the logic.
        """
        # Vertex shader for full-screen grid and disc rendering
        self.bg_prog = self.ctx.program(
            vertex_shader="""
            // Vertex Shader: Generates a full-screen triangle for grid/disc rendering
            #version 330
            out vec2 v_uv;
            void main() {
                float x = -1.0 + float((gl_VertexID & 1) << 2);
                float y = -1.0 + float((gl_VertexID & 2) << 1);
                v_uv = vec2(x, y) * 0.5 + 0.5;
                gl_Position = vec4(x, y, 0.0, 1.0);
            }
            """,
            fragment_shader="""
            // Fragment shader: Implement grid/disc coloring logic here
            #version 330
            in vec2 v_uv;
            out vec4 f_color;
            void main() {
                // TODO: Color the grid and black hole disc
                f_color = vec4(0.0, 0.0, 0.0, 1.0); // Placeholder
            }
            """
        )
        # TODO: Set up VAO and any other required OpenGL resources

    def update(self, dt: float):
        """
        Update simulation state. Implement animation or logic as needed.
        """
        # TODO: Animate or update state if needed
        pass

    def render(self):
        """
        Render the grid background and black hole disc.
        Implement the rendering logic using the provided shaders and OpenGL resources.
        """
        # TODO: Draw the grid and disc using OpenGL
        pass

    def handle_key(self, key, action, modifiers, keys):
        """
        Handle keyboard input if needed for Mission 1.
        """
        # TODO: Add keyboard controls if desired
        pass