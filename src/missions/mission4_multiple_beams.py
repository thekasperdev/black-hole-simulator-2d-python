# src/missions/mission4_multiple_beams.py
# Mission 4: Multiple parallel light beams

import moderngl
import numpy as np
from .mission3_multiple_beams_no_collision import Mission3MultipleBeamsNoCollision


class Mission4MultipleBeams(Mission3MultipleBeamsNoCollision):
    """Mission 4: Multiple parallel light beams with collision detection"""
    
    def get_name(self) -> str:
        return "Mission 4: Multiple Light Beams"
    
    def initialize(self):
        """Set up shaders and create multiple particles"""
        # Mission 4 specific settings (set before parent init)
        self.spacing = 24  # pixels between beam rows
        
        # Initialize parent class (shaders, etc.) 
        # This will call spawn_particle -> spawn_multiple_beams
        super().initialize()
    
    def spawn_particle(self):
        """Override to spawn multiple beams instead of single particle"""
        self.spawn_multiple_beams()
    
    def spawn_multiple_beams(self):
        """Create multiple parallel light beams"""
        margin = 40
        ys = np.arange(margin, self.height - margin + 1, max(2, self.spacing), dtype=np.int32)
        count_per_beam = 80
        x0 = -200.0  # Start particles off-screen to the left
        
        # Stagger initial x positions so beams appear continuous
        pts = []
        vels = []
        for y in ys:
            for i in range(count_per_beam):
                pts.append([x0 - i * 1.5, float(y)])
                vels.append([self.speed, 0.0])
        
        self.pos = np.array(pts, dtype=np.float32)
        self.vel = np.array(vels, dtype=np.float32)
        self.alive = np.ones(len(self.pos), dtype=bool)
    
    def update(self, dt: float):
        """Update multiple particles with collision detection"""
        if self.paused or len(self.pos) == 0:
            return
            
        # Move particles
        self.pos[self.alive] += self.vel[self.alive] * dt
        
        # Black hole collision detection (particles disappear when they hit)
        to_center = self.pos - self.center
        r2 = (to_center[:, 0] ** 2 + to_center[:, 1] ** 2)
        hit = r2 <= (self.rs_px * self.rs_px)
        
        # Remove particles that hit the black hole (they stay gone)
        self.alive &= ~hit
        
        # Remove particles that went off-screen to the right
        offscreen_right = self.pos[:, 0] > self.width + 50
        self.alive &= ~offscreen_right
        
        # Check if all particles are gone (absorbed or off-screen)
        if not np.any(self.alive):
            # All particles are gone, start a new wave
            self.spawn_multiple_beams()
        
        # Rebuild buffer from current alive set
        self.rebuild_vbo()
    
    def handle_key(self, key, action, modifiers, keys):
        """Handle keyboard input for Mission 4"""
        if action == keys.ACTION_PRESS:
            if key == keys.SPACE:
                self.paused = not self.paused
                print(f"Mission 4: Animation {'paused' if self.paused else 'unpaused'}")
            elif key == keys.R:
                self.spawn_multiple_beams()
                self.rebuild_vbo()
                print("Mission 4: Beams reset")
            elif key == keys.COMMA:  # tighten spacing
                self.spacing = max(2, self.spacing - 2)
                self.spawn_multiple_beams()
                self.rebuild_vbo()
                print(f"Mission 4: Spacing decreased to {self.spacing}")
            elif key == keys.PERIOD:  # widen spacing
                self.spacing = min(self.height, self.spacing + 2)
                self.spawn_multiple_beams()
                self.rebuild_vbo()
                print(f"Mission 4: Spacing increased to {self.spacing}")