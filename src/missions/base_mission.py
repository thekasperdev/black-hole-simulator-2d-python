# =============================================================================
# BaseMission: Abstract base class for all simulation missions
# =============================================================================
# Purpose:
#   - Provides a common interface and shared fields for all missions in the simulator.
#   - All missions (Mission1 through Mission9) inherit from BaseMission and implement
#     the required methods for initialization, updating, rendering, and input handling.
# Guidance for Participants:
#   - Use this class as a template for your own missions.
#   - Override the abstract methods to provide mission-specific logic.
#   - Use self.center and self.rs_px for black hole placement and rendering.
#   - The cleanup() method is optional and can be used to release resources when switching missions.
# Implementation Notes:
#   - Each mission builds on the previous, introducing new physical effects, rendering features,
#     or user controls.
#   - See comments in each mission file for specific instructions and implementation details.
#   - This solution branch is designed to help you understand the structure and progression of the hackathon tasks.
# =============================================================================

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