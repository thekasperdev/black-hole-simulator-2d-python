# src/missions/base_mission.py
# Base class for all simulation missions

from abc import ABC, abstractmethod
import numpy as np
import moderngl


class BaseMission(ABC):
    """Base class for all simulation missions"""
    
    def __init__(self, ctx, width, height):
        """Initialize mission with OpenGL context and screen dimensions"""
        self.ctx = ctx
        self.width = width
        self.height = height
        self.center = np.array([width * 0.5, height * 0.5], dtype=np.float32)
        self.rs_px = min(width, height) * 0.12  # black hole radius
        
    @abstractmethod
    def get_name(self) -> str:
        """Return the mission name for display"""
        pass
    
    @abstractmethod
    def initialize(self):
        """Initialize shaders, buffers, and mission-specific state"""
        pass
    
    @abstractmethod
    def update(self, dt: float):
        """Update simulation state (called every frame)"""
        pass
    
    @abstractmethod
    def render(self):
        """Render the mission (called every frame)"""
        pass
    
    @abstractmethod
    def handle_key(self, key, action, modifiers, keys):
        """Handle keyboard input"""
        pass
    
    def cleanup(self):
        """Optional cleanup when mission is disabled"""
        pass