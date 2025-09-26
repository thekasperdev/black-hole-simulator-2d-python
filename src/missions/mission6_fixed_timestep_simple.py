# src/missions/mission6_fixed_timestep_simple.py
# Mission 6: Rays with fixed timestep and trails, building on Mission 5
# - Uses visual time scaling and fixed substeps for smooth, slow motion.
# - Rays are simple straight-line (no GR bending) for now, stored in SI units (metres).
# - Rendering converts metres -> pixels using self.pixels_per_metre and offsets by self.center.

import numpy as np
import moderngl
from .mission5_units_schwarzschild import Mission5UnitsSchwarzschild

class Ray:
    """
    Ray expressed in Cartesian coordinates (metres) relative to the black hole centre at (0,0).
    Simple straight-line propagation: x += vx * dt, y += vy * dt.
    Stores a finite-length trail of recent positions (metres).
    """
    def __init__(self, pos_m, dir_vec_m_s, rs_m, c_m_s, max_trail=500):
        # positions in metres (relative to BH centre)
        self.x = float(pos_m[0])
        self.y = float(pos_m[1])
        # velocity in m/s (cartesian)
        self.vx = float(dir_vec_m_s[0])
        self.vy = float(dir_vec_m_s[1])
        # polar quantities (for checks/diagnostics)
        self.r = float(np.sqrt(self.x * self.x + self.y * self.y))
        self.phi = float(np.arctan2(self.y, self.x))
        # trail: list of np.array([x, y]) in metres
        self.trail = [np.array([self.x, self.y], dtype=np.float32)]
        # limits and flags
        self.alive = True
        self.rs = float(rs_m)      # Schwarzschild radius in metres
        self.c = float(c_m_s)      # speed of light in m/s
        self.max_trail = int(max_trail)

    def step(self, dt_s):
        """
        Advance the ray by dt_s seconds (straight-line).
        Append to trail and clamp trail length.
        """
        if not self.alive:
            return
        # advance cartesian coordinates
        self.x += self.vx * float(dt_s)
        self.y += self.vy * float(dt_s)
        # update polar
        self.r = np.sqrt(self.x * self.x + self.y * self.y)
        self.phi = np.arctan2(self.y, self.x)
        # append to trail
        self.trail.append(np.array([self.x, self.y], dtype=np.float32))
        # clamp trail length to avoid uncontrolled memory growth
        if len(self.trail) > self.max_trail:
            # drop oldest entries
            del self.trail[: len(self.trail) - self.max_trail]
        # horizon test
        if self.r <= self.rs:
            self.alive = False

class Mission6FixedTimestepSimple(Mission5UnitsSchwarzschild):
    """
    Mission 6: Rays with fixed timestep and trails, building on Mission 5.
    - Visual time scaling (self.time_scale) slows the simulation for legibility.
    - Fixed integration substeps (self.fixed_step_s) ensure smooth deterministic stepping.
    """
    def get_name(self):
        return "Mission 6: Rays with Trails (Fixed Timestep)"

    def initialize(self):
        # call parent which sets up pixels_per_metre, centre, rs_m, rs_px, world size, etc.
        super().initialize()

        # debug flag for lightweight diagnostics
        self.debug = False

        # Visual time scaling: fraction of real time to simulate per real second.
        # For example, 0.01 means 1% speed (100x slower on screen).
        self.time_scale = 0.00001

        # Fixed integrator timestep (seconds) for stable substepping.
        # Choose small enough to produce smooth trails. 1e-3 is a good starting point.
        self.fixed_step_s = 1e-3

        # Accumulator to handle variable-frame dt using fixed substeps
        self._sim_accum = 0.0

        # Maximum simulated time we'll allow to accumulate per frame (guard against hiccups)
        self._max_sim_step = 0.1  # seconds

        # Prepare ray list (in metres relative to BH centre at (0,0))
        self.rays = []
        margin_m = self.world_height_m / 20.0
        ys_m = np.linspace(
            -self.world_height_m / 2.0 + margin_m,
            self.world_height_m / 2.0 - margin_m,
            20
        )
        # start x to the left of BH (metres)
        x0_m = -self.world_width_m / 2.0 + margin_m
        # rightward velocity of light in m/s (cartesian)
        dir_vec = np.array([self.c, 0.0], dtype=np.float64)
        # trail length cap per ray
        max_trail = 800

        for y_m in ys_m:
            pos_m = np.array([x0_m, y_m], dtype=np.float64)
            self.rays.append(Ray(pos_m, dir_vec, self.rs_m, self.c, max_trail=max_trail))

        # rendering program(s) created once and reused
        self._trail_prog = None
        self._create_render_prog_if_needed()

        if self.debug:
            print("[Mission6] init: rays:", len(self.rays),
                  "rs_m:", self.rs_m, "rs_px:", self.rs_px,
                  "pixels_per_metre:", self.pixels_per_metre,
                  "time_scale:", self.time_scale,
                  "fixed_step_s:", self.fixed_step_s)

    def _create_render_prog_if_needed(self):
        if self._trail_prog is not None:
            return
        # simple shader expecting per-vertex alpha and pixel coords
        self._trail_prog = self.ctx.program(
            vertex_shader='''
                #version 330
                in vec2 in_vert;   // pixel coords
                in float in_alpha; // per-vertex alpha
                out float v_alpha;
                uniform vec2 u_view; // (width, height) in pixels
                void main() {
                    vec2 pixel = in_vert;
                    vec2 ndc = (pixel / u_view) * 2.0 - 1.0;
                    ndc.y = -ndc.y; // flip Y (pixels top-left -> GL bottom-left)
                    gl_Position = vec4(ndc, 0.0, 1.0);
                    gl_PointSize = 4.0; // ensure points are visible on core profiles
                    v_alpha = in_alpha;
                }
            ''',
            fragment_shader='''
                #version 330
                in float v_alpha;
                out vec4 f_color;
                void main() {
                    f_color = vec4(1.0, 1.0, 1.0, v_alpha);
                }
            '''
        )

    def update(self, dt):
        """
        dt: real frame time in seconds.
        We scale it by time_scale to produce a slower visual simulation, then integrate
        using fixed small substeps for determinism and smooth trails.
        """
        if self.debug:
            print("[Mission6] raw dt:", dt)

        # scale real elapsed time into simulation (visual) time
        sim_dt = float(dt) * float(self.time_scale)

        # accumulate and guard against runaway
        self._sim_accum += sim_dt
        if self._sim_accum > self._max_sim_step:
            self._sim_accum = self._max_sim_step

        # step in fixed increments
        while self._sim_accum >= self.fixed_step_s:
            for ray in self.rays:
                if ray.alive:
                    ray.step(self.fixed_step_s)
            self._sim_accum -= self.fixed_step_s

        # optionally do a small partial step for the remaining accumulator to reduce visible stutter
        if self._sim_accum > 0.0:
            partial = self._sim_accum
            for ray in self.rays:
                if ray.alive:
                    ray.step(partial)
            # consume the partial
            self._sim_accum = 0.0

        # If all rays died, reinitialise (spawn fresh rays)
        if not any(ray.alive for ray in self.rays):
            if self.debug:
                print("[Mission6] all rays dead -> reinitializing")
            self.initialize()

    def render(self):
        """
        Render trails (LINE_STRIP) and current ray heads (POINTS), then render the black hole disc.
        All ray positions are converted from metres -> pixels by:
            pixel = self.center + pos_m * self.pixels_per_metre
        """
        # background
        self.ctx.clear(0.08, 0.08, 0.10)

        # enable alpha blending for faded trails
        self.ctx.enable(moderngl.BLEND)

        prog = self._trail_prog

        # Draw trails: LINE_STRIP per ray (alpha fades along the trail)
        for ray in self.rays:
            if len(ray.trail) < 2:
                continue
            N = len(ray.trail)
            # convert trail (metres) -> pixel coords
            verts = np.array([
                [self.center[0] + p[0] * self.pixels_per_metre,
                 self.center[1] + p[1] * self.pixels_per_metre]
                for p in ray.trail
            ], dtype=np.float32)
            # fade from faint to bright
            alphas = np.linspace(0.05, 1.0, N, dtype=np.float32)

            # create buffers (for a production build reuse them to avoid per-frame allocations)
            vbo = self.ctx.buffer(verts.tobytes())
            abo = self.ctx.buffer(alphas.tobytes())
            vao_content = [
                (vbo, '2f', 'in_vert'),
                (abo, '1f', 'in_alpha'),
            ]
            vao = self.ctx.vertex_array(prog, vao_content)
            prog['u_view'].value = (float(self.window_width), float(self.window_height))
            vao.render(moderngl.LINE_STRIP)
            # VBOs/VAO will be garbage-collected; reuse in future if desired for perf

        # Draw current ray heads as points (supply alpha buffer so in_alpha is always present)
        pts = [
            np.array([
                self.center[0] + ray.x * self.pixels_per_metre,
                self.center[1] + ray.y * self.pixels_per_metre
            ], dtype=np.float32)
            for ray in self.rays if ray.alive
        ]
        if pts:
            pts = np.stack(pts)
            vbo = self.ctx.buffer(pts.tobytes())
            alphas = np.ones((len(pts),), dtype=np.float32)
            abo = self.ctx.buffer(alphas.tobytes())
            vao_content = [
                (vbo, '2f', 'in_vert'),
                (abo, '1f', 'in_alpha'),
            ]
            vao = self.ctx.vertex_array(prog, vao_content)
            prog['u_view'].value = (float(self.window_width), float(self.window_height))
            vao.render(moderngl.POINTS)

        # Draw black hole disc (use helper from parent class)
        self._ensure_bh_disc()
        self._bh_disc_prog['u_view'].value = (float(self.window_width), float(self.window_height))
        self._bh_disc_prog['u_center'].value = (float(self.center[0]), float(self.center[1]))
        self._bh_disc_prog['u_radius'].value = float(self.rs_px)
        self._bh_disc_vao.render(moderngl.TRIANGLE_FAN)