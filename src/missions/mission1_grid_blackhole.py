# src/missions/mission1_grid_blackhole.py
# Mission 1: Basic grid background and black hole disc

import moderngl
import numpy as np
from .base_mission import BaseMission


class Mission1GridBlackHole(BaseMission):
    """Mission 1: Display grid background with black hole disc - Foundation for all missions"""
    
    def get_name(self) -> str:
        return "Mission 1: Grid + Black Hole"
    
    def initialize(self):
        """Set up shaders for grid and black hole rendering"""
        self.setup_background_rendering()
    
    def setup_background_rendering(self):
        """Initialize grid and black hole rendering - can be called by inheriting missions"""
        # Background (grid + disc) full-screen quad
        self.bg_prog = self.ctx.program(
            vertex_shader="""
            #version 330
            out vec2 v_uv;
            void main() {
                // Generate a full-screen triangle using gl_VertexID
                float x = -1.0 + float((gl_VertexID & 1) << 2);
                float y = -1.0 + float((gl_VertexID & 2) << 1);
                v_uv = vec2(x, y) * 0.5 + 0.5;
                gl_Position = vec4(x, y, 0.0, 1.0);
            }""",
            fragment_shader="""
            #version 330
            in vec2 v_uv;
            out vec4 f_color;
            uniform vec2 u_center;
            uniform float u_rsPx;
            uniform float u_grid_gap;

            void main() {
                vec2 frag = vec2(gl_FragCoord.x, gl_FragCoord.y);
                float r = length(frag - u_center);

                // Grid lines: draw a faint line when modulo < 1 pixel
                float gx = (mod(frag.x, u_grid_gap) < 1.0) ? 1.0 : 0.0;
                float gy = (mod(frag.y, u_grid_gap) < 1.0) ? 1.0 : 0.0;
                float grid = max(gx, gy);

                vec3 bg = vec3(0.03, 0.04, 0.07);
                vec3 grid_col = vec3(0.12, 0.14, 0.20);
                vec3 col = mix(bg, grid_col, grid);

                // Black hole disc
                if (r <= u_rsPx) { col = vec3(0.0); }

                f_color = vec4(col, 1.0);
            }"""
        )
        
        # Set shader uniforms
        self.bg_prog["u_center"].value = tuple(self.center)
        self.bg_prog["u_rsPx"].value = float(self.rs_px)
        self.bg_prog["u_grid_gap"].value = 24.0
        
        # Create VAO for background rendering
        self.bg_vao = self.ctx.vertex_array(self.bg_prog, [])
    
    def update(self, dt: float):
        """No animation in Mission 1 - just static background"""
        pass
    
    def render_background(self):
        """Render grid background with black hole disc - can be called by inheriting missions"""
        self.bg_vao.render(mode=moderngl.TRIANGLES, vertices=3)
    
    def render(self):
        """Render grid background with black hole disc"""
        # Just render the background - main controller handles screen clearing
        self.render_background()
    
    def handle_key(self, key, action, modifiers, keys):
        """Mission 1 has no interactive controls"""
        pass