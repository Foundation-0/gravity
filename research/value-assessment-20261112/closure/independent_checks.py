"""Independent review calculations. Does not import or edit author probes."""
from pathlib import Path
import hashlib
import itertools
import json
import math

import numpy as np
from scipy.integrate import quad
from scipy.linalg import qr
from scipy.special import exp1
import sympy as sp

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent


def astrophysics():
    G=6.67430e-11; c=299792458.; mp=1.67262192369e-27
    sigmaT=6.6524587321e-29; Msun=1.98847e30; Mpc=3.085677581491367e22
    Myr=1e6*365.25*86400.; h=.6736; H0=100*h*1000/Mpc
    om=(.02237+.1200+.00064)/h**2; ob=.02237/h**2; oc=.1200/h**2
    rad=9.236e-5; lam=1-om-rad; z=6.0783
    E=lambda a:math.sqrt(rad/a**4+om/a**3+lam)
    window=quad(lambda a:1/(a*E(a)),1/21,1/(1+z),epsabs=1e-13)[0]/H0/Myr
    tE=sigmaT*c/(4*math.pi*G*mp)/Myr
    growth=[]
    for eps,opacity in [(.1,1),(.1,1-.245/2),(1-math.sqrt(8/9),1)]:
        t=tE*opacity*eps/(1-eps)*math.log(1.5e9/100)
        growth.append({'efficiency':eps,'opacity_factor':opacity,'time_Myr':t,'duty':t/window})
    mass=83913.9617*Msun
    Hz=H0*E(1/(1+z)); rhoCrit=3*Hz**2/(8*math.pi*G)
    rvir=(3*mass/(4*math.pi*200*rhoCrit))**(1/3)
    halo={'radius_pc':rvir/(Mpc/1e6),'compactness':2*G*mass/(rvir*c*c),
          'baryon_budget_Msun':mass/Msun*ob/om,'temperature_K':1.22*mp*G*mass/(2*rvir*1.380649e-23)}
    r0=30*Mpc/1000; mb=5e10*Msun; g0=G*mb/r0**2
    timeunit=math.sqrt(r0/g0)/Myr
    ftrap=1-(.969924/(250/math.sqrt(2)))**2
    times=[]
    # Independent energy integral using an analytic antiderivative of the
    # source's RAR force, rather than solving the author's radial ODE.
    for name,a0,extra in [('Newton',None,0),('MOND_const',1.2e-10,0),
                         ('MOND_H',c*Hz/(2*math.pi),0),('two_branch',1.2e-10,oc/ob*ftrap)]:
        b=math.sqrt(g0/a0) if a0 else None
        def energy(y):
            newton=(1+extra)*(1/y-1)
            if b is None:return newton
            return newton+(math.log(-math.expm1(-b/y))-math.log(-math.expm1(-b)))/b
        def f(u):
            if u==0:
                outer=(1+extra) if b is None else (1+extra)+1/math.expm1(b)
                return math.sqrt(2/outer)
            if u==1:return 0
            return 2*u/math.sqrt(2*energy(1-u*u))
        value,error=quad(f,0,1,epsabs=1e-11,epsrel=1e-11)
        times.append({'case':name,'time_Myr':value*timeunit,'quadrature_error_Myr':error*timeunit})
    integral=1.1-.85*math.e*float(exp1(1))
    rhoinf=math.exp(-3*integral)
    # w+1>0, so rho_DE(a)>=rhoinf for a>=1. The matter term is positive,
    # and curvature -0.004/a^2 >= -0.004. This is an all-future bound.
    future={'integral_1_to_infinity':integral,'rho_DE_limit':rhoinf,
            'strict_H2_lower_bound_all_a_ge_1':(1-om)*rhoinf-.004,
            'renormalized_curvature_H2_lower_bound':(1-om+.004)*rhoinf-.004}
    return {'age_window_Myr':window,'growth':growth,'halo':halo,'infall':times,'future':future,
            'chirp':{'lower':19*647**5,'incorrect':15**3*4**2*10**10,
                     'correct':15**3*4**3*10**10,'upper':19*648**5}}


def mechanical_symbolic():
    a,t,x=sp.symbols('a t x',real=True)
    eye=sp.eye(3); C=sp.Matrix([[0,-1,-1],[1,0,-1],[1,-1,0]])
    points=[sign*eye[:,axis] for axis in range(3) for sign in (1,-1)]
    edges=[(i,j) for i in range(6) for j in range(i+1,6) if i//2!=j//2]
    R=sp.zeros(15,18)
    L=(a+2)*eye+t*C; D=a*eye+t*C
    for n,(i,j) in enumerate(edges+[(0,1),(2,3),(4,5)]):
        v=points[j]-points[i]
        if n>=12:v+=L[n-12,:].T
        for k in range(3):R[n,3*i+k]=-v[k];R[n,3*j+k]=v[k]
    unknown=sp.symbols('w:12')
    w=sp.Matrix([*unknown,1,-1,-1])
    solution=sp.solve(list(R.T*w),unknown,dict=True)
    assert len(solution)==1
    w=w.subs(solution[0])
    assert R.T*w==sp.zeros(18,1)
    N=sp.expand((w.T*w)[0])
    assert sp.simplify(N-(11*a*a+12*t*t+12)/4)==0
    T=sp.diag(1,-1,-1)
    M=D.T*T*L/sp.sqrt(2)
    assert sp.simplify(M-M.T)==sp.zeros(3)
    det=sp.factor((x*eye+t*C).det())
    assert sp.expand(det-(x+t)*(x*x-x*t+2*t*t))==0
    rotation=sp.Matrix([[0,1,-1],[-1,0,-1],[1,1,0]])
    torque=sp.Matrix([[0,2,-2],[0,0,-1],[-1,1,-1]])
    assert rotation.rank()==2 and torque.det()==2
    return {'derived_internal_tensions':[str(y) for y in w[:12]],'norm_squared':str(N),
            'determinant':str(det),'bridge_rotation_rank':rotation.rank(),
            'added_rotation_minor_determinant':int(torque.det())}


def mechanical_numeric():
    p=np.vstack([sign*np.eye(3)[i] for i in range(3) for sign in (1,-1)])
    C=np.array([[0,-1,-1],[1,0,-1],[1,-1,0]])
    def cell(s):return (2+math.sqrt(2)*(1-s*s)/(1+s*s))*np.eye(3)+2*s/(1+s*s)*C
    base=[(i,j,(0,0,0)) for i in range(6) for j in range(i+1,6) if i//2!=j//2]
    base += [(2*i,2*i+1,tuple(np.eye(3,dtype=int)[i])) for i in range(3)]
    canon=lambda edge:min(edge,(edge[1],edge[0],tuple(-x for x in edge[2])))
    contacts=set()
    for i,j,n in itertools.product(range(6),range(6),itertools.product(range(-3,4),repeat=3)):
        v=p[j]-p[i]+np.array(n)@cell(1)
        if v@v==2:contacts.add(canon((i,j,n)))
    extra=sorted(contacts-{canon(b) for b in base})
    assert len(extra)==21
    basis=[np.diag(np.eye(3)[i]) for i in range(3)]
    for i,j in [(1,2),(0,2),(0,1)]:
        E=np.zeros((3,3));E[i,j]=E[j,i]=1/math.sqrt(2);basis.append(E)
    def elasticity(s,eta):
        R=[];B=[]
        for k,(i,j,n) in enumerate(base+extra):
            v=p[j]-p[i]+np.array(n)@cell(s);d=v/np.linalg.norm(v)
            r=np.zeros(18);r[3*i:3*i+3]=-d;r[3*j:3*j+3]+=d
            weight=1 if k<15 else math.sqrt(eta)
            R.append(r[:15]*weight) # Fix vertex 5 translation gauge.
            B.append([d@E@v*weight for E in basis])
        Q,_=qr(np.array(R),mode='full')
        projected=Q[:,15:].T@np.array(B)
        return projected.T@projected/np.linalg.det(cell(s))
    L0=2+math.sqrt(2);Kopen=np.zeros((6,6));Kopen[:3,:3]=(3*np.eye(3)+np.ones((3,3)))/(9*L0)
    v=np.array([1,-1,-1,0,0,0]);Kfold=2*np.outer(v,v)/(17*L0)
    rows=[]
    for s,eta in [(0,1e-6),(.01,1e-8),(.01,1e-6),(.01,1e-4),(1,1e-6),(1e-4,1e-4),(1e-4,1e-16)]:
        K=elasticity(s,eta)
        rows.append({'s':s,'eta':eta,'eigenvalues':np.linalg.eigvalsh(K).tolist(),
                     'distance_to_open':float(np.linalg.norm(K-Kopen)),
                     'distance_to_fold':float(np.linalg.norm(K-Kfold))})
    return {'endpoint_contact_count':len(contacts),'added_count':len(extra),
            'method':'Independent enlarged contact search, translation gauge, full QR energy projection',
            'limit_distance':float(np.linalg.norm(Kopen-Kfold)),'rows':rows}


def photons():
    u,v,b=sp.symbols('u v b',real=True)
    # Average over the relative azimuth analytically before integration.
    kernel=(1+u*u*v*v+(1-u*u)*(1-v*v)/2)*(u-v)**2
    den=sp.integrate(kernel,(v,-1,1),(u,b,1))
    num=sp.integrate(kernel,(v,-1,b),(u,b,1))
    alpha=sp.factor(num/den)
    rows=[]
    for f in [sp.Rational(1,4),sp.Rational(1,2),sp.Rational(99,100),sp.Integer(1)]:
        low=1-2*f
        rows.append({'sky_fraction':float(f),'alpha':float(alpha.subs(b,low)),
                     'decoherence_rate_relative':float((den/den.subs(b,-1)).subs(b,low))})
    return {'alpha_aligned_cap_exact_polynomial_ratio':str(alpha),'rows':rows}


def main():
    files=['wave12/research.md','wave12/probe.py','wave12/evidence.json','wave12/sources.json',
           'convergences/research.md','convergences/derivation.md','convergences/probe.py',
           'convergences/evidence.json','convergences/sources.json']
    result={'artifact_sha256':{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files},
            'astrophysics':astrophysics(),'symbolic_mechanics':mechanical_symbolic(),
            'independent_QR_mechanics':mechanical_numeric(),'symbolic_photon_caps':photons()}
    (OUT/'independent-checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
