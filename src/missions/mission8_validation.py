# src/missions/mission8_validation.py
# Mission 8: Validate light bending vs weak-field analytic formula
#
# - Inherits the time-scaling, fixed-substep stepping and rendering pipeline from Mission7.
# - Replaces the ray instances with validating rays that measure asymptotic deflection
#   and compare to the weak-field analytic approximation:
#   $$
#   \Delta\phi_{\mathrm{analytic}} \approx \frac{2 r_s}{b}
#   $$
#   where b is the impact parameter (initial transverse offset, metres).
#
# Guidance for participants (solution notes)
# - The numeric deflection is measured from the initial heading angle (atan2(vy, vx))
#   and the asymptotic outgoing heading approximated by the vector between the last two
#   trail points once the ray is sufficiently far to the right of the BH.
# - Use the printed comparisons to validate integrator step size and confirm weak-field
#   agreement for large impact parameters.
#
# Implementation details
# - We consider a ray to be "measurable" once it has moved to x > measure_x_m (far right)
#   and its radius is large (> measure_r_m). These thresholds are chosen from the world size.
# - We compute an outgoing direction from the last two trail points to approximate the
#   asymptotic propagation direction. For better precision one may fit a line to many
#   far-field points or integrate further out.
#
# - Participants should tune self.measure_factor and integration step sizes to validate
#   different regimes (weak-field agreement, near-photon-sphere behaviour).
#
import numpy as np
from .mission7_light_bending import Mission7LightBending, SchwarzschildRay

class ValidatingRay(SchwarzschildRay):
    """
    Extends SchwarzschildRay with initial heading and measurement storage.
    - initial_heading: atan2(vy, vx) (radians)
    - impact_param_b: |initial y| (metres) as approximate impact parameter (sufficient for rays starting far away)
    - measured: True if deflection was measured
    - deflection: measured deflection in radians (theta_final - initial_heading)
    - analytic_deflection: 2*r_s/b
    """
    def __init__(self, pos_m, vel_m_s, rs_m, c_m_s, max_trail=2000):
        # call parent initialiser (computes dt_dlambda, E, L etc.)
        super().__init__(pos_m, vel_m_s, rs_m, c_m_s, max_trail=max_trail)
        # store initial cartesian heading angle (radians)
        vx = float(vel_m_s[0]); vy = float(vel_m_s[1])
        self.initial_heading = float(np.arctan2(vy, vx))
        # approximate impact parameter b (metres) -- for rays started far left this is |y|
        self.impact_b = float(abs(pos_m[1]))
        # measurement fields
        self.measured = False
        self.deflection = None
        self.analytic_deflection = (2.0 * float(rs_m) / self.impact_b) if self.impact_b != 0.0 else np.inf

    def try_measure_deflection(self, measure_x_m, measure_r_m):
        """
        Attempt to measure outgoing asymptotic direction when the ray is sufficiently far from BH.
        Criteria:
          - ray is alive or dead but has a trail
          - current x > measure_x_m (right-hand far field)
          - current r > measure_r_m (far radius)
          - not already measured
        Measurement:
          - approximate outgoing direction using last two trail points:
            theta_out = atan2(y_n - y_{n-1}, x_n - x_{n-1})
          - deflection = wrap(theta_out - initial_heading) into [-pi, pi]
        """
        if self.measured:
            return False
        if len(self.trail) < 2:
            return False
        if not (self.x > measure_x_m and self.r > measure_r_m):
            return False

        # approximate outgoing direction from last two trail points
        p_last = self.trail[-1]
        p_prev = self.trail[-2]
        dx = float(p_last[0]) - float(p_prev[0])
        dy = float(p_last[1]) - float(p_prev[1])
        if dx == 0.0 and dy == 0.0:
            return False
        theta_out = float(np.arctan2(dy, dx))

        # compute deflection and normalise to [-pi, pi]
        dtheta = theta_out - self.initial_heading
        # bring into [-pi, pi]
        dtheta = (dtheta + np.pi) % (2.0 * np.pi) - np.pi

        self.deflection = float(dtheta)
        self.measured = True
        return True


class Mission8Validation(Mission7LightBending):
    """
    Mission 8: Numeric validation of light bending against the weak-field analytic formula.

    - Inherits from Mission7LightBending but constructs ValidatingRay instances instead of
      bare SchwarzschildRay objects.
    - On each simulation update it attempts to measure the outgoing deflection for rays
      that have moved sufficiently far to the right of the black hole.
    - When a measurement is made it prints a concise numeric comparison and stores the value
      in the ray for later inspection.
    """
    def get_name(self):
        return "Mission 8: Light Bending Validation"

    def initialize(self):
        """
        Initialise the world (via the fixed-timestep mission) and create validating rays.
        We call the Mission6 initializer to set up the BH constants and rendering plumbing,
        then create our own ValidatingRay instances placed similarly to Mission7.
        """
        # Call Mission6 initializer to set up environment and variables (pixels_per_metre, rs_m, etc.)
        # We avoid calling Mission7.initialize directly because it creates SchwarzschildRay;
        # we want ValidatingRay instead.
        from .mission6_fixed_timestep_simple import Mission6FixedTimestepSimple
        Mission6FixedTimestepSimple.initialize(self)

        # Keep debug flag and time scaling values from parent (they were set in Mission6.initialize)
        if not hasattr(self, 'debug'):
            self.debug = False

        # Create validating rays analogous to Mission7 layout
        self.rays = []
        margin_m = self.world_height_m / 20.0
        ys_m = np.linspace(
            -self.world_height_m / 2.0 + margin_m,
            self.world_height_m / 2.0 - margin_m,
            20
        )
        x0_m = -self.world_width_m / 2.0 + margin_m
        dir_vec = np.array([self.c, 0.0], dtype=np.float64)  # initial coordinate velocity (m/s) rightward
        max_trail = 2000

        for y_m in ys_m:
            pos_m = np.array([x0_m, y_m], dtype=np.float64)
            vray = ValidatingRay(pos_m, dir_vec, self.rs_m, self.c, max_trail=max_trail)
            self.rays.append(vray)

        # measurement thresholds (metres)
        # measure_x_m: we measure once the ray has moved to the right-hand far field
        self.measure_x_m = self.world_width_m * 0.4  # 40% of half-world to the right
        # measure_r_m: ensure the radial position is large enough (far-field)
        self.measure_r_m = max(self.world_width_m, self.world_height_m) * 0.45

        # counters for reporting
        self._measure_count = 0
        self._report_interval = 5  # print summary every N measurements

        if self.debug:
            print("[Mission8] created", len(self.rays), "validating rays")
            print("[Mission8] measure_x_m:", self.measure_x_m, "measure_r_m:", self.measure_r_m)

        # Ensure render program of parent is created
        self._create_render_prog_if_needed()

    def update(self, dt):
        """
        Integrate as in Mission7 but attempt to measure deflection for each ray after stepping.
        Uses the same fixed-substep simulation pattern (time_scale, fixed_step_s) as before.
        """
        # scale real time -> simulation time using parent's time_scale
        sim_dt = float(dt) * float(self.time_scale)
        self._sim_accum += sim_dt
        if self._sim_accum > self._max_sim_step:
            self._sim_accum = self._max_sim_step

        # step rays in fixed increments; convert sim seconds -> d_lambda per ray
        while self._sim_accum >= self.fixed_step_s:
            # step all rays by fixed_step_s
            for ray in self.rays:
                if ray.alive:
                    d_lambda = ray.affine_step_for_sim_dt(self.fixed_step_s)
                    if not np.isfinite(d_lambda) or d_lambda <= 0.0:
                        continue
                    ray.step_rk4(d_lambda)
            self._sim_accum -= self.fixed_step_s

            # After each full fixed step, attempt to measure deflection where possible
            self._attempt_measurements()

        # small partial step to reduce stutter
        if self._sim_accum > 0.0:
            partial = self._sim_accum
            for ray in self.rays:
                if ray.alive:
                    d_lambda = ray.affine_step_for_sim_dt(partial)
                    if not np.isfinite(d_lambda) or d_lambda <= 0.0:
                        continue
                    ray.step_rk4(d_lambda)
            # attempt measurement after partial step
            self._attempt_measurements()
            self._sim_accum = 0.0

        # If all rays are dead (captured) or measured we can reinitialise to run another batch
        if not any(ray.alive for ray in self.rays) or all(ray.measured for ray in self.rays):
            if getattr(self, 'debug', False):
                print("[Mission8] all rays processed; reinitialising")
            # Pause briefly or reinitialise fresh rays so user can observe results
            self.initialize()

    def _attempt_measurements(self):
        """
        Check each ray to see if it meets the far-field criteria. If measurement occurs,
        print a concise comparison (measured vs analytic) and increment the counter.
        """
        for ray in self.rays:
            if ray.measured:
                continue
            measured_now = ray.try_measure_deflection(self.measure_x_m, self.measure_r_m)
            if measured_now:
                self._measure_count += 1
                # measured deflection in radians -> degrees
                measured_deg = np.degrees(ray.deflection)
                analytic_deg = np.degrees(ray.analytic_deflection) if np.isfinite(ray.analytic_deflection) else np.inf
                # print a short summary line
                print(f"[Mission8] ray b={ray.impact_b:.3e} m: measured Δφ={measured_deg:.4f}° ; "
                      f"analytic ≈ {analytic_deg:.4f}° ; ratio (meas/analytic) = "
                      f"{(ray.deflection / ray.analytic_deflection) if np.isfinite(ray.analytic_deflection) else np.nan:.4f}")
                # periodic summary
                if self._measure_count % self._report_interval == 0:
                    self._print_summary()

    def _print_summary(self):
        """
        Print a short aggregated summary of all measured rays so far.
        """
        measured = [r for r in self.rays if r.measured]
        if not measured:
            return
        lines = []
        for r in measured:
            md = np.degrees(r.deflection)
            ad = np.degrees(r.analytic_deflection) if np.isfinite(r.analytic_deflection) else np.inf
            lines.append(f"b={r.impact_b:.3e} m: meas={md:.3f}°, anal={ad:.3f}°")
        print("[Mission8] summary of measured rays:")
        for L in lines:
            print("  ", L)

    # Rendering: inherit parent render which converts ray.trail (metres) -> pixels
    # Optionally one could add an overlay that draws the analytic circles (r_s and photon sphere)
    # in a contrasting colour; the parent already draws the black hole disc. Participants can
    # extend render() to draw the photon sphere at r = 1.5 * r_s using a line loop if desired.