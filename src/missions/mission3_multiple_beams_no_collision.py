# src/missions/mission3_multiple_beams_no_collision.py
# Mission 3: Multiple parallel light beams WITHOUT collision detection

import moderngl
import numpy as np
from .mission2_single_beam import Mission2SingleBeam


class Mission3MultipleBeamsNoCollision(Mission2SingleBeam):
    """Mission 3: Multiple parallel light beams without collision detection"""
    
    def get_name(self) -> str:
        return "Mission 3: Multiple Light Beams"
    
    def initialize(self):
        """Set up shaders and create multiple particles"""
        # Mission 3 specific settings (set before parent init)
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
        """Update multiple particles WITHOUT collision detection"""
        if self.paused or len(self.pos) == 0:
            return
            
        # Move particles
        self.pos[self.alive] += self.vel[self.alive] * dt
        
        # Check if particles went off-screen to the right - respawn them
        for i in range(len(self.pos)):
            if self.alive[i] and self.pos[i, 0] > self.width + 50:
                # Respawn particle on the left with same Y coordinate
                self.pos[i, 0] = -50.0
                # Keep original Y position to maintain beam formation
                self.alive[i] = True
        
        # Only cull particles that have gone too far off-screen vertically
        # NO collision detection with black hole
        onscreen_y = (self.pos[:, 1] >= -50) & (self.pos[:, 1] < self.height + 50)
        self.alive &= onscreen_y
        
        # Rebuild buffer from current alive set
        self.rebuild_vbo()
    
    def handle_key(self, key, action, modifiers, keys):
        """Handle keyboard input for Mission 3"""
        if action == keys.ACTION_PRESS:
            if key == keys.SPACE:
                self.paused = not self.paused
                print(f"Mission 3: Animation {'paused' if self.paused else 'unpaused'}")
            elif key == keys.R:
                self.spawn_multiple_beams()
                self.rebuild_vbo()
                print("Mission 3: Multiple beams reset")
            elif key == keys.COMMA:  # tighten spacing
                self.spacing = max(2, self.spacing - 2)
                self.spawn_multiple_beams()
                self.rebuild_vbo()
                print(f"Mission 3: Spacing decreased to {self.spacing}")
            elif key == keys.PERIOD:  # widen spacing
                self.spacing = min(self.height, self.spacing + 2)
                self.spawn_multiple_beams()
                self.rebuild_vbo()
                print(f"Mission 3: Spacing increased to {self.spacing}")