# src/mission_control.py
# Main mission controller with runtime mission selection

import moderngl_window as mglw
import moderngl

from missions.mission1_grid_blackhole import Mission1GridBlackHole
from missions.mission2_single_beam import Mission2SingleBeam
from missions.mission3_multiple_beams_no_collision import Mission3MultipleBeamsNoCollision
from missions.mission4_multiple_beams import Mission4MultipleBeams
from missions.mission5_units_schwarzschild import Mission5UnitsSchwarzschild
from missions.mission6_fixed_timestep import Mission6FixedTimestep
from missions.mission7_light_bending import Mission7LightBending
from missions.mission8_validation import Mission8Validation
from missions.mission9_redshift import Mission9Redshift

class MissionControl(mglw.WindowConfig):
    """Mission Control for Black Hole Simulation Demo"""
    gl_version = (3, 3)
    title = "SpaceD - Mission Control"
    window_size = (1600, 1000)
    aspect_ratio = 1100 / 800
    resizable = False
    # Store mission number as a class attribute for runtime selection
    selected_mission_number = 1

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ctx.enable(moderngl.BLEND)
        self.ctx._window = self.wnd
        self.w, self.h = self.window_size
        self.active_mission = None
        self._initialize_mission(MissionControl.selected_mission_number)
        print(f"Running: {self.active_mission.get_name() if self.active_mission else 'No mission selected'}")

    def _initialize_mission(self, mission_number):
        """Initialize the selected mission by number"""
        if mission_number == 1:
            self.active_mission = Mission1GridBlackHole(self.ctx, self.w, self.h)
        elif mission_number == 2:
            self.active_mission = Mission2SingleBeam(self.ctx, self.w, self.h)
        elif mission_number == 3:
            self.active_mission = Mission3MultipleBeamsNoCollision(self.ctx, self.w, self.h)
        elif mission_number == 4:
            self.active_mission = Mission4MultipleBeams(self.ctx, self.w, self.h)
        elif mission_number == 5:
            self.active_mission = Mission5UnitsSchwarzschild(self.ctx, self.w, self.h)
        elif mission_number == 6:
            self.active_mission = Mission6FixedTimestep(self.ctx, self.w, self.h)
        elif mission_number == 7:
            self.active_mission = Mission7LightBending(self.ctx, self.w, self.h)
        elif mission_number == 8:
            self.active_mission = Mission8Validation(self.ctx, self.w, self.h)
        elif mission_number == 9:
            self.active_mission = Mission9Redshift(self.ctx, self.w, self.h)
        else:
            print("ERROR: Invalid mission number! (1-7)")
            return
        self.active_mission.initialize()

    def on_render(self, time: float, frame_time: float):
        if not self.active_mission:
            return
        self.active_mission.update(frame_time)
        self.ctx.clear(0.03, 0.04, 0.07, 1.0)
        self.ctx.screen.use()
        self.active_mission.render()

    def key_event(self, key, action, modifiers):
        keys = self.wnd.keys
        if action == keys.ACTION_PRESS and key == keys.ESCAPE:
            self.wnd.close()
            return
        if self.active_mission:
            self.active_mission.handle_key(key, action, modifiers, keys)

    def _print_help(self):
        print("\n" + "="*60)
        print("SpaceDG - Mission Control")
        print("="*60)
        print("Demo Control:")
        print("  1-7       : Jump to specific demo level")
        print("  H         : Show this help")
        print("  ESC       : Exit demo")
        print("\nMission Controls (when active):")
        print("  SPACE     : Pause/unpause animation")
        print("  R         : Reset beams")
        print("  , / .     : Adjust beam spacing (Mission 4)")
        print("\nDemo Levels:")
        print("  1: Grid + Black Hole")
        print("  2: Grid + Single Light Beam")
        print("  3: Grid + Multiple Light Beams")
        print("  4: Grid + Multiple Beams + Collision Detection")
        print("  5: SI Units + Schwarzschild Radius")
        print("  6: Fixed Timestep Physics Loop")
        print("  7: Light Bending Simulation")
        print("  8: Validation Suite")
        print("  9: Red Shift Simulation")
        print("="*60)


def prompt_for_mission():
    print("\nSelect a mission to run:")
    print("  1: Grid + Black Hole")
    print("  2: Grid + Single Light Beam")
    print("  3: Grid + Multiple Light Beams")
    print("  4: Grid + Multiple Beams + Collision Detection")
    print("  5: SI Units + Schwarzschild Radius")
    print("  6: Fixed Timestep Physics Loop")
    print("  7: Light Bending Simulation")
    print("  8: Validation Suite")
    print("  9: Red Shift Simulation")
    print("  0: Exit")
    while True:
        try:
            mission_number = int(input("Enter mission number (0-9): "))
            if 0 <= mission_number <= 9:
                return mission_number
            else:
                print("Please enter a number between 0 and 9.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    while True:
        mission_number = prompt_for_mission()
        if mission_number == 0:
            print("Exiting Mission Control. Goodbye!")
            break
        MissionControl.selected_mission_number = mission_number
        mglw.run_window_config(MissionControl)
