# src/missions/mission7_light_bending.py
# Mission 7: Light bending (Schwarzschild null geodesics, equatorial plane)
#
# - Inherits Mission6FixedTimestepSimple for rendering, time-scaling and UI plumbing.
# - Replaces straight-line rays with Schwarzschild null geodesics integrated in the
#   equatorial plane (theta = pi/2) using an RK4 integrator in affine parameter lambda.
# - Rays are initialised in SI units (metres, seconds). Rendering converts metres -> pixels
#   using self.pixels_per_metre and offsets by self.center as in previous missions.
#
# Guidance for participants (solution branch notes)
# - This mission demonstrates genuine light bending: some geodesics are deflected,
#   some are captured by the horizon (r <= r_s), and near the photon sphere (r = 1.5 r_s)
#   unstable whirls can occur.
# - Key equations used:
#   Schwarzschild factor:
#   $$
#   f(r) = 1 - \frac{r_s}{r}
#   $$
#   Effective potential for null geodesics (equatorial plane):
#   $$
#   V_{\mathrm{eff}}(r) = f(r)\,\frac{L^2}{r^2}
#   $$
#   The reduced first-order ODE system (state = [r, p_r, \phi], with p_r = dr/d\lambda):
#   $$
#   \frac{dr}{d\lambda} = p_r, \qquad
#   \frac{d\phi}{d\lambda} = \frac{L}{r^2}, \qquad
#   \frac{dp_r}{d\lambda} = -\frac{1}{2}\frac{dV_{\mathrm{eff}}}{dr}.
#   $$
#   Useful derivative:
#   $$
#   \frac{dV_{\mathrm{eff}}}{dr} = L^2\!\left(-\frac{2}{r^3} + \frac{3 r_s}{r^4}\right).
#   $$
#
# Implementation notes
# - We compute initial affine scale dt/dlambda from the null condition given an initial
#   Cartesian coordinate velocity (vx, vy). That gives initial p_r and dphi/dlambda, and
#   constants E and L which remain fixed during integration.
# - The visual time scaling and fixed-step substepping come from the parent class and are
#   preserved: sim_dt -> d_lambda conversion is performed per-ray using stored dt_dlambda.
#
# Participants: read the methods and comments below to understand how to compute E, L,
# p_r initial value and how the RK4 step is organised.

import numpy as np
from .mission6_fixed_timestep_simple import Mission6FixedTimestepSimple

class SchwarzschildRay:
    """
    A single null geodesic in the Schwarzschild metric, restricted to the equatorial plane.
    State variables and units:
      - positions (x,y) in metres (Cartesian, relative to BH centre at 0,0)
      - internal state integrated in affine parameter lambda: (r, p_r, phi)
      - conserved quantities: E, L (set at init)
      - dt_dlambda (dt/dlambda) computed at init used to convert sim time -> d_lambda
    """
    def __init__(self, pos_m, vel_m_s, rs_m, c_m_s, max_trail=2000):
        # Physical constants and storage
        self.rs = float(rs_m)   # Schwarzschild radius (m)
        self.c = float(c_m_s)   # speed of light (m/s)

        # Cartesian positions in metres (relative to BH centre)
        self.x = float(pos_m[0])
        self.y = float(pos_m[1])

        # polar coordinates
        self.r = float(np.hypot(self.x, self.y))
        self.phi = float(np.arctan2(self.y, self.x))

        # initial Cartesian velocity components (m/s)
        vx = float(vel_m_s[0])
        vy = float(vel_m_s[1])

        # decompose into radial and angular components in coordinate time t
        cosp = np.cos(self.phi)
        sinp = np.sin(self.phi)
        # radial coordinate speed dr/dt
        self.vr = vx * cosp + vy * sinp
        # dphi/dt (omega)
        self.omega = (-vx * sinp + vy * cosp) / (self.r if self.r != 0.0 else 1e-12)

        # Schwarzschild metric factor f(r)
        f = 1.0 - (self.rs / self.r) if self.r != 0.0 else 1.0

        # Solve null condition for dt/dlambda:
        # (dr/dlambda)^2 + V_eff = E^2 with dr/dlambda = (dr/dt) * (dt/dlambda)
        # Rearranged to obtain dt/dlambda from initial coordinate velocities:
        self.dt_dlambda = np.sqrt((self.vr ** 2) / (f ** 2) + (self.r ** 2 * self.omega ** 2) / f)

        # initial affine derivatives
        self.pr = self.vr * self.dt_dlambda                 # dr/dlambda
        self.dphi_dlambda = self.omega * self.dt_dlambda
        self.L = (self.r ** 2) * self.dphi_dlambda          # conserved angular momentum
        self.E = f * self.dt_dlambda                        # conserved energy

        # state variables for integration
        self.r_state = float(self.r)
        self.pr_state = float(self.pr)
        self.phi_state = float(self.phi)

        # trail for rendering (Cartesian, metres)
        self.trail = [np.array([self.x, self.y], dtype=np.float32)]
        self.alive = True
        self.max_trail = int(max_trail)

    def _dVeff_dr(self, r):
        # dV_eff/dr = L^2 * (-2/r^3 + 3 rs / r^4)
        # small-r guard is handled at caller level (we avoid starting at r==0)
        return (self.L ** 2) * (-2.0 / (r ** 3) + 3.0 * self.rs / (r ** 4))

    def derivatives(self, r, pr, phi):
        """
        Return the derivatives (dr/dlambda, dpr/dlambda, dphi/dlambda).
        Using conservation of L for dphi/dlambda, and V_eff for dpr/dlambda.
        """
        dr_dlam = pr
        dphi_dlam = self.L / (r ** 2)
        dpr_dlam = -0.5 * self._dVeff_dr(r)
        return dr_dlam, dpr_dlam, dphi_dlam

    def step_rk4(self, d_lambda):
        """
        Advance the ray by an affine parameter step d_lambda using RK4.
        Update Cartesian x,y from the new (r,phi) and append to trail.
        Mark ray dead if r <= r_s (captured by the horizon).
        """
        if not self.alive:
            return

        r0, pr0, phi0 = self.r_state, self.pr_state, self.phi_state

        # RK4 stages
        k1 = self.derivatives(r0, pr0, phi0)
        k2 = self.derivatives(r0 + 0.5 * d_lambda * k1[0],
                              pr0 + 0.5 * d_lambda * k1[1],
                              phi0 + 0.5 * d_lambda * k1[2])
        k3 = self.derivatives(r0 + 0.5 * d_lambda * k2[0],
                              pr0 + 0.5 * d_lambda * k2[1],
                              phi0 + 0.5 * d_lambda * k2[2])
        k4 = self.derivatives(r0 + d_lambda * k3[0],
                              pr0 + d_lambda * k3[1],
                              phi0 + d_lambda * k3[2])

        self.r_state = r0 + (d_lambda / 6.0) * (k1[0] + 2.0 * k2[0] + 2.0 * k3[0] + k4[0])
        self.pr_state = pr0 + (d_lambda / 6.0) * (k1[1] + 2.0 * k2[1] + 2.0 * k3[1] + k4[1])
        self.phi_state = phi0 + (d_lambda / 6.0) * (k1[2] + 2.0 * k2[2] + 2.0 * k3[2] + k4[2])

        # update Cartesian coords for rendering
        r = self.r_state
        phi = self.phi_state
        self.x = r * np.cos(phi)
        self.y = r * np.sin(phi)

        # append to trail and clamp
        self.trail.append(np.array([self.x, self.y], dtype=np.float32))
        if len(self.trail) > self.max_trail:
            del self.trail[: len(self.trail) - self.max_trail]

        # horizon test
        if self.r_state <= self.rs:
            self.alive = False

    def affine_step_for_sim_dt(self, sim_dt_s):
        """
        Convert a simulation time increment (seconds) into an affine parameter increment
        for this ray. This allows you to keep the visual time scaling approach:
            d_lambda = sim_dt / (dt/dlambda)
        """
        return float(sim_dt_s) / float(self.dt_dlambda)


class Mission7LightBending(Mission6FixedTimestepSimple):
    """
    Mission 7: Light bending in Schwarzschild spacetime (equatorial null geodesics)

    - Inherits from Mission6FixedTimestepSimple (so it keeps the visual time scaling,
      fixed-substep pattern and rendering code for trails / points).
    - Overrides initialisation to create SchwarzschildRay instances and overrides update()
      to integrate them in affine parameter lambda via RK4.
    - Rendering is delegated to the parent class (which converts ray.trail from metres -> pixels).
    """
    def get_name(self):
        return "Mission 7: Light Bending (Schwarzschild Null Geodesics)"

    def initialize(self):
        # Call parent initialize to set up BH params, pixels_per_metre, time_scale,
        # fixed_step_s, rendering program etc. We will replace the ray list afterwards.
        super().initialize()

        # Replace rays with Schwarzschild-integrated rays.
        # Use the same spatial layout as Mission6 for familiarity.
        self.rays = []
        margin_m = self.world_height_m / 20.0
        ys_m = np.linspace(
            -self.world_height_m / 2.0 + margin_m,
            self.world_height_m / 2.0 - margin_m,
            20
        )
        x0_m = -self.world_width_m / 2.0 + margin_m
        # initial coordinate velocity (m/s) — rightward at c to start
        dir_vec = np.array([self.c, 0.0], dtype=np.float64)
        max_trail = 2000

        for y_m in ys_m:
            pos_m = np.array([x0_m, y_m], dtype=np.float64)
            ray = SchwarzschildRay(pos_m, dir_vec, self.rs_m, self.c, max_trail=max_trail)
            self.rays.append(ray)

        # Keep existing render program created by parent; no change needed.
        if getattr(self, 'debug', False):
            print("[Mission7] created", len(self.rays), "Schwarzschild rays")

    def update(self, dt):
        """
        Override update to integrate null geodesics:
        - Use the parent's time scaling (self.time_scale) and fixed substep pattern
          (self.fixed_step_s) to get sim_dt per substep (seconds).
        - Convert sim_dt -> d_lambda using each ray's dt_dlambda and step in affine parameter.
        """
        # same scaling / accumulation pattern as Mission6
        sim_dt = float(dt) * float(self.time_scale)
        # guard and accumulate using parent's fields set in initialize
        self._sim_accum += sim_dt
        if self._sim_accum > self._max_sim_step:
            self._sim_accum = self._max_sim_step

        # step in fixed increments (convert each fixed_step_s to d_lambda per-ray)
        while self._sim_accum >= self.fixed_step_s:
            for ray in self.rays:
                if ray.alive:
                    d_lambda = ray.affine_step_for_sim_dt(self.fixed_step_s)
                    # if d_lambda is extremely small or nan, skip; this should not normally happen
                    if not np.isfinite(d_lambda) or d_lambda <= 0.0:
                        continue
                    ray.step_rk4(d_lambda)
            self._sim_accum -= self.fixed_step_s

        # small partial step to reduce stutter
        if self._sim_accum > 0.0:
            partial = self._sim_accum
            for ray in self.rays:
                if ray.alive:
                    d_lambda = ray.affine_step_for_sim_dt(partial)
                    if not np.isfinite(d_lambda) or d_lambda <= 0.0:
                        continue
                    ray.step_rk4(d_lambda)
            self._sim_accum = 0.0

        # Re-spawn if all rays have been captured
        if not any(ray.alive for ray in self.rays):
            if getattr(self, 'debug', False):
                print("[Mission7] all rays captured; reinitialising")
            self.initialize()