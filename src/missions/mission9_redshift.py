# src/missions/mission9_redshift.py
# Mission 9: Gravitational redshift & frequency-shift visualisation
#
# - Inherits Mission8Validation so it keeps Schwarzschild geodesics, validation helpers,
#   time-scaling and fixed-substep stepping.
# - Colours ray trails and heads according to a gravitational redshift mapping.
# - Two colouring modes are provided:
#     * 'local'  : colour by local frequency factor relative to infinity,
#                  g_local = sqrt(1 - r_s / r). (low g -> red; high g -> blue)
#     * 'infty'  : colour by the asymptotic factor for a photon emitted at the ray's initial radius,
#                  g_emit = sqrt(1 - r_s / r_emit) (constant per ray).
#
# Guidance for participants (solution notes)
# - Photons conserve the affine energy E; static observers measure frequency proportional to E / sqrt(f(r)).
#   The code uses the simpler and pedagogical quantity g(r) = sqrt(f(r)) to colour rays.
# - Colour mapping is deliberately simple (linear blend between "red" and "cool white/blue")
#   to make trends visually obvious. Participants may replace the mapping with any better
#   physically motivated colour map (e.g., Planck-weighted colours or hue shifts).
#
# Implementation notes
# - Uses per-vertex RGBA in the trail/point shader. The parent class rendering is overridden
#   to supply colour buffers per vertex. Buffer reuse is not implemented here for clarity;
#   participants should reuse VBOs for performance in production.
#
import numpy as np
import moderngl
from .mission8_validation import Mission8Validation, ValidatingRay

class Mission9Redshift(Mission8Validation):
    """
    Mission 9: Visualise gravitational redshift by colouring photons.

    Inherits:
      - Mission8Validation: provides Schwarzschild rays, validation logic and stepping.
    Key additions:
      - colour_mode: 'local' or 'infty'
      - mapping of g-factor -> RGB colour per vertex
      - modified render() to supply per-vertex colour and alpha attributes to the GPU
    """
    def get_name(self):
        return "Mission 9: Gravitational Redshift Visualisation"

    def initialize(self):
        # Use parent initialiser to set up BH, world and validation ray layout.
        # Mission8.initialize constructs ValidatingRay instances; we call it to keep measurement logic.
        super().initialize()

        # Colouring config:
        # 'local'  : colour varies along the ray with current radius r -> g(r) = sqrt(1 - r_s/r)
        # 'infty'  : colour is constant per ray based on the initial emission radius (r_emit)
        self.colour_mode = 'local'   # 'local' or 'infty'

        # scale for visual brightness if you want to exaggerate effect (1.0 = no exaggeration)
        self.brightness_scale = 1.0

        # Ensure the rendering program that accepts per-vertex colour exists
        self._create_colour_render_prog()

        if getattr(self, 'debug', False):
            print("[Mission9] redshift visualisation initialised; colour_mode=", self.colour_mode)

    def _create_colour_render_prog(self):
        """
        Create a shader program that accepts per-vertex colour (vec3) and alpha (float).
        We reuse u_view to map pixels -> NDC as in earlier missions.
        """
        if hasattr(self, '_col_prog') and self._col_prog is not None:
            return
        self._col_prog = self.ctx.program(
            vertex_shader='''
                #version 330
                in vec2 in_vert;
                in vec3 in_col;
                in float in_alpha;
                out vec3 v_col;
                out float v_alpha;
                uniform vec2 u_view;
                void main() {
                    vec2 pixel = in_vert;
                    vec2 ndc = (pixel / u_view) * 2.0 - 1.0;
                    ndc.y = -ndc.y; // flip y for top-left pixel coords
                    gl_Position = vec4(ndc, 0.0, 1.0);
                    gl_PointSize = 4.0;
                    v_col = in_col;
                    v_alpha = in_alpha;
                }
            ''',
            fragment_shader='''
                #version 330
                in vec3 v_col;
                in float v_alpha;
                out vec4 f_color;
                void main() {
                    f_color = vec4(v_col, v_alpha);
                }
            '''
        )

    def _g_factor(self, r_m):
        """
        Compute g(r) = sqrt(1 - r_s / r) safely (clamp negative).
        r_m: radius in metres
        """
        rs = float(self.rs_m)
        # avoid division by zero and clamp to [0,1]
        if r_m <= rs:
            return 0.0
        val = 1.0 - rs / r_m
        if val <= 0.0:
            return 0.0
        return float(np.sqrt(val))

    def _colour_from_g(self, g):
        """
        Map g in [0,1] -> RGB colour.
        - g near 0 (strong redshift) -> warm red
        - g near 1 (far field)        -> cool pale-blue/white
        Returns a tuple (r,g,b).
        """
        g = float(np.clip(g, 0.0, 1.0))
        # simple linear blend: red (1,0.2,0.0) -> cool white/blue (0.7,0.85,1.0)
        warm = np.array([1.0, 0.2, 0.0], dtype=np.float32)
        cool = np.array([0.7, 0.85, 1.0], dtype=np.float32)
        col = (1.0 - g) * warm + g * cool
        # apply brightness scale
        col *= float(self.brightness_scale)
        # clamp
        col = np.clip(col, 0.0, 1.0)
        return col.astype(np.float32)

    def render(self):
        """
        Override render to provide per-vertex colour for trails and points.
        The rest of the scene (background and BH disc) is drawn as usual.
        """
        # background
        self.ctx.clear(0.08, 0.08, 0.10)
        self.ctx.enable(moderngl.BLEND)

        prog = self._col_prog

        # Draw trails with colour per vertex
        for ray in self.rays:
            if len(ray.trail) < 2:
                continue
            N = len(ray.trail)
            # trail vertices: convert trail (metres) -> pixel coords
            verts = np.array([
                [self.center[0] + p[0] * self.pixels_per_metre,
                 self.center[1] + p[1] * self.pixels_per_metre]
                for p in ray.trail
            ], dtype=np.float32)

            # compute per-vertex colours depending on selected mode
            cols = np.zeros((N, 3), dtype=np.float32)
            for i, p in enumerate(ray.trail):
                # p is (x,y) in metres; compute r
                r_m = float(np.hypot(p[0], p[1]))
                if self.colour_mode == 'local':
                    g = self._g_factor(r_m)
                else:  # 'infty' : colour constant for this ray using the initial emission radius
                    # initial radius approximated by ray.impact_b and initial x; more robustly
                    # use the first trail entry (start location)
                    r_emit = float(np.hypot(ray.trail[0][0], ray.trail[0][1]))
                    g = self._g_factor(r_emit)
                cols[i] = self._colour_from_g(g)

            # alpha fades along trail for visual clarity
            alphas = np.linspace(0.05, 1.0, N, dtype=np.float32)

            # create buffers and VAO
            vbo = self.ctx.buffer(verts.tobytes())
            cbo = self.ctx.buffer(cols.tobytes())
            abo = self.ctx.buffer(alphas.tobytes())
            vao_content = [
                (vbo, '2f', 'in_vert'),
                (cbo, '3f', 'in_col'),
                (abo, '1f', 'in_alpha'),
            ]
            vao = self.ctx.vertex_array(prog, vao_content)
            prog['u_view'].value = (float(self.window_width), float(self.window_height))
            vao.render(moderngl.LINE_STRIP)

        # Draw ray heads as coloured points (use same per-ray colour as last trail sample)
        pts = []
        cols_pts = []
        alphas_pts = []
        for ray in self.rays:
            if not ray.alive and len(ray.trail) == 0:
                continue
            # get current position (x,y) in metres
            x = ray.trail[-1][0] if len(ray.trail) else ray.x
            y = ray.trail[-1][1] if len(ray.trail) else ray.y
            px = float(self.center[0] + x * self.pixels_per_metre)
            py = float(self.center[1] + y * self.pixels_per_metre)
            pts.append([px, py])
            # compute colour as above (use current r)
            r_m = float(np.hypot(x, y))
            if self.colour_mode == 'local':
                g = self._g_factor(r_m)
            else:
                r_emit = float(np.hypot(ray.trail[0][0], ray.trail[0][1]))
                g = self._g_factor(r_emit)
            cols_pts.append(self._colour_from_g(g))
            alphas_pts.append(1.0 if ray.alive else 0.4)

        if pts:
            pts = np.array(pts, dtype=np.float32)
            cols_pts = np.array(cols_pts, dtype=np.float32)
            alphas_pts = np.array(alphas_pts, dtype=np.float32)

            vbo = self.ctx.buffer(pts.tobytes())
            cbo = self.ctx.buffer(cols_pts.tobytes())
            abo = self.ctx.buffer(alphas_pts.tobytes())
            vao_content = [
                (vbo, '2f', 'in_vert'),
                (cbo, '3f', 'in_col'),
                (abo, '1f', 'in_alpha'),
            ]
            vao = self.ctx.vertex_array(prog, vao_content)
            prog['u_view'].value = (float(self.window_width), float(self.window_height))
            vao.render(moderngl.POINTS)

        # Draw the black hole disc via parent's helper
        self._ensure_bh_disc()
        self._bh_disc_prog['u_view'].value = (float(self.window_width), float(self.window_height))
        self._bh_disc_prog['u_center'].value = (float(self.center[0]), float(self.center[1]))
        self._bh_disc_prog['u_radius'].value = float(self.rs_px)
        self._bh_disc_vao.render(moderngl.TRIANGLE_FAN)

    # Optional helper: toggle colour mode at runtime (participants may wire to UI/keys)
    def toggle_colour_mode(self):
        if self.colour_mode == 'local':
            self.colour_mode = 'infty'
        else:
            self.colour_mode = 'local'
        if getattr(self, 'debug', False):
            print("[Mission9] colour_mode set to", self.colour_mode)