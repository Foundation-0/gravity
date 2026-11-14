#!/usr/bin/env python3
"""Independent spatially-flat-gauge ADM reduction and integration.

The evolution is derived here from a lapse/shift-retaining action. The submitted
module is imported only after this derivation, to compare its Newtonian solution.
"""
from pathlib import Path
import hashlib,importlib.util,json,math
import numpy as np
import sympy as S
from scipy.integrate import solve_ivp

HERE=Path(__file__).resolve().parent
SUBMITTED=HERE.parent/'public-checkpoint'
if not SUBMITTED.is_dir():SUBMITTED=HERE.parent
expected={'response.py':'e28c8f4ada1e41924e6317f8932de4d065307516cd57c5ff83a0cf23b72397ef',
          'derivation.md':'5700296d3d35b09b6101f8695dd57abfc86863a3287f9f050beb2828513a93fe'}
for name,sha in expected.items():assert hashlib.sha256((SUBMITTED/name).read_bytes()).hexdigest()==sha

a,H,Q,Kp,k=S.symbols('a H Q Kp k',nonzero=True,real=True)
v,al,vd,ad,n,beta=S.symbols('v al vd ad lapse shift',real=True)
Kpp=S.Integer(4);KB=S.Integer(1);b=S.Integer(1);lam=S.Integer(1)
chi=v+Q*al;gamma=vd-Q*n;E=ad+n
# ADM h_ij=a² delta_ij, N=1+n, N_i=partial_i beta. Spatial integration
# removes (partial_i partial_j beta)^2-(Delta beta)^2 for a scalar Fourier mode.
Lg=-6*a**3*H**2*n**2+4*a*k**2*H*n*beta
La=a**3*Kpp*gamma**2+a*k**2*(KB*E**2+2*b*E*chi-b*(1+lam)*chi**2+
                                      Kp*(2*al*v+Q*al**2)-2*Kp*beta*v)
L=Lg+La
constraint=S.factor(S.diff(L,beta)/(2*a*k**2))
assert constraint==2*H*n-Kp*v
nsol=Kp*v/(2*H)
Lr=S.expand(L.subs(n,nsol))
assert S.diff(Lr,beta)==0
coords=S.Matrix([v,al]);vel=S.Matrix([vd,ad])
momentum=S.Matrix([S.diff(Lr,z) for z in vel])
kinetic=momentum.jacobian(vel)
assert kinetic==S.diag(8*a**3,2*a*k**2)
back=S.Matrix([a,H,Q,Kp]);backdot=S.Matrix([a*H,-Q*Kp/2,-3*H*Kp/4,-3*H*Kp])
force=S.Matrix([S.diff(Lr,z) for z in coords])-momentum.jacobian(coords)*vel-momentum.jacobian(back)*backdot
acc=S.simplify(kinetic.inv()*force)
accfun=S.lambdify((a,H,Q,Kp,k,v,al,vd,ad),acc,'numpy')

# Direct Newtonian-gauge extrinsic-curvature expansion. This independently
# checks the disputed H Phi dotPhi convention without importing its action.
eps,Ph,Psi,Phd=S.symbols('eps Phi Psi Phidot',real=True)
kin_exact=-6*a**3*(1-2*eps*Ph)**S.Rational(3,2)/S.sqrt(1+2*eps*Psi)*(H-eps*Phd/(1-2*eps*Ph))**2
quadratic=S.expand(S.diff(kin_exact,eps,2).subs(eps,0)/2)
quoted=a**3*(-6*Phd**2-12*H*(Ph+Psi)*Phd-9*H**2*(Ph+Psi)**2)
assert S.simplify(quadratic-quoted)==0

spec=importlib.util.spec_from_file_location('submitted',SUBMITTED/'response.py')
submitted=importlib.util.module_from_spec(spec);spec.loader.exec_module(submitted)
rows=[]
for kval in (6.,12.,24.):
    qi=.01;amplitude=1e-6
    def background(scale):
        q=qi/scale**3
        return 1+q,4*q,math.sqrt((4*q+2*q*q)/3)
    Q0,Kp0,H0=background(1.)
    end=2*(8-1)/(3*H0+math.sqrt(9*H0*H0+12*qi*(8-1)))
    times=np.linspace(0,end,1001)
    # Compensated velocity preparation has zero metric, coordinates and metric
    # velocity initially, so the two gauges have identical initial field data.
    initial=np.array([1.,0.,0.,amplitude,4*Q0*amplitude/kval**2])
    def rhs(t,y):
        scale,vf,af,vdf,adf=y
        qq,kp,hh=background(scale)
        accelerations=np.asarray(accfun(scale,hh,qq,kp,kval,vf,af,vdf,adf)).ravel()
        return np.r_[scale*hh,vdf,adf,accelerations]
    sol=solve_ivp(rhs,(0,end),initial,t_eval=times,method='DOP853',rtol=3e-12,atol=1e-20)
    assert sol.success
    scale,vf,af,vdf,adf=sol.y
    q=qi/scale**3;qq=1+q;kp=4*q;hh=np.sqrt((4*q+2*q*q)/3);r=kval*kval/scale**2
    lapse=kp*vf/(2*hh);Ef=adf+lapse;chif=vf+qq*af;Z=Ef+chif;gf=vdf-qq*lapse
    # Reconstruct Newtonian Phi by the Hamiltonian constraint after gauge
    # transformation. The Qdot terms cancel against the momentum contribution.
    Phi=-(qq*4*gf-r*Z+3*hh*kp*vf)/(2*r)
    vn=vf-qq*Phi/hh;an=af+Phi/hh
    gn=gf+3*kp*Phi/4
    D=qq*4*gn-r*Z;m=kp*vn;pressure=kp*gn
    independent=np.array([D,m,chif,Z,Phi,pressure,vn,an])
    # Only this comparator uses the submitted right-hand side.
    y0=np.array([1.,0.,0.,4*Q0*amplitude/kval**2,0.,amplitude])
    ref=solve_ivp(lambda t,y:submitted.rhs_fields(t,y,kval,qi),(0,end),y0,t_eval=times,
                  method='DOP853',rtol=3e-12,atol=1e-20)
    aa,vn2,an2,En2,Phi2,gn2=ref.y
    q2=qi/aa**3;qq2=1+q2;kp2=4*q2;chi2=vn2+qq2*an2;Z2=En2+chi2
    reference=np.array([qq2*4*gn2-kval*kval/aa**2*Z2,kp2*vn2,chi2,Z2,Phi2,kp2*gn2,vn2,an2])
    absolute=np.max(np.abs(independent-reference),axis=1)
    errors=absolute/np.maximum(amplitude,np.max(np.abs(reference),axis=1))
    assert max(errors)<1e-7
    rows.append({'k':kval,'max_normalized_discrepancy':float(max(errors)),
                 'by_variable':dict(zip(['D','m','chi','Z','Phi','pressure','v_Newtonian','alpha_Newtonian'],errors.tolist()))})

output={'checked_source_sha256':expected,'action_source':'https://arxiv.org/html/2307.15126v3',
        'method':'Independent scalar ADM expansion in spatially flat gauge, retaining shift; eliminate constraints; derive Euler-Lagrange equations; integrate and reconstruct Newtonian observables.',
        'shift_constraint':str(constraint),'kinetic_hessian':str(kinetic),
        'newtonian_extrinsic_curvature_check':'symbolically exact',
        'comparisons':rows,'review_scope':'Linear scalar action, two physical scalar modes, constraints and observable map. No global or nonlinear stability proof.'}
(HERE/'adm-evidence.json').write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps(output,indent=2))
