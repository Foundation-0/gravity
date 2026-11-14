"""Independent analytic controls for corrected conditional benchmarks."""
import math
import unittest
import wave11_machian_pairing_unification as w11
import wave12_cosmic_dawn_quasar_collapse as w12

class Controls(unittest.TestCase):
    def test_newton(self):
        mass, radius = 5e10*w12.M_SUN, 30*w12.KPC
        exact = math.pi/(2*math.sqrt(2))*math.sqrt(radius**3/(w12.G*mass))
        self.assertLess(abs(w12.radial_point_mass_fall_time(mass,radius)/exact-1),1e-12)

    def test_deep_mond(self):
        mass, radius = 5e10*w12.M_SUN, 30*w12.KPC
        a0 = w12.G*mass/radius**2*1e8
        speed = (w12.G*mass*a0)**0.25
        exact = math.sqrt(math.pi/2)*radius/speed
        numeric = w12.radial_point_mass_fall_time(mass,radius,a0,intervals=512)
        self.assertLess(abs(numeric/exact-1),5e-4)
        shortcut = math.pi/(2*math.sqrt(2))*radius/speed
        self.assertAlmostEqual(shortcut/exact,math.sqrt(math.pi)/2,places=14)

    def test_convergence(self):
        times = [w12.radial_point_mass_fall_time(5e10*w12.M_SUN,30*w12.KPC,w12.A0_EMP,intervals=n)/w12.MYR for n in (64,128,256)]
        self.assertLess(max(times)-min(times),1e-6)
        self.assertAlmostEqual(times[-1],200.075137583,places=6)

    def test_mass_flow(self):
        efolds=math.log(1.5e9/100)
        tedd=w12.SIGMA_T*w12.C_SI/(4*math.pi*w12.G*w12.M_P)/w12.MYR
        for mdot in (.1,1,2,3,5):
            lam,time=w12.slim_disk_growth_time_myr(efolds,mdot)
            self.assertGreater(mdot-.1*lam,0)
            self.assertAlmostEqual(efolds*.1*tedd/time+.1*lam,mdot,places=13)
            if mdot<=2:
                self.assertAlmostEqual(time,efolds*(.1/.9)*tedd/mdot,places=10)
        with self.assertRaises(ValueError): w12.slim_disk_growth_time_myr(efolds,0)

    def test_growth_counterexamples(self):
        s=w12.audit_c31_salpeter_seed_and_clustering_wall()['seed_duty_cycle_audit_for_J1602A_1p5e9_Msun']
        self.assertLess(s['popIII_100Msun_duty_primordial_H_He_eps0p10'],1)
        self.assertAlmostEqual(s['popIII_100Msun_req_time_primordial_H_He_Schwarzschild_Myr']/s['popIII_100Msun_req_time_pure_H_Schwarzschild_Myr'],1-.245/2,places=5)
        self.assertAlmostEqual(s['fixed_Schwarzschild_efficiency'],1-math.sqrt(8/9),places=14)

    def test_curvature_closure(self):
        for ok in (-.01,-.004,-.001,0,.01): self.assertAlmostEqual(w11.closed_cpl_hubble_squared(1,ok),1,places=14)

    def test_kinetic_curvature(self):
        h=1e-4
        p=lambda u:(u*u-1)**2
        self.assertAlmostEqual((p(h)-2*p(0)+p(-h))/h**2,-4,places=6)
        self.assertEqual(4*0*(0**2-1),0)

if __name__=='__main__': unittest.main()
