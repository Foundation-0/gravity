"""Independent review checks. Never imports the author probes.

Replays their scripts only in temporary copies and tests the central formulas
using separate Bessel expansions, quadrature, and symbolic differentiation.
"""
from pathlib import Path
import hashlib
import json
import math
import shutil
import subprocess
import sys
import tempfile

import numpy as np
from scipy.integrate import quad
from scipy.special import jv, j0
from scipy.stats import norm
import sympy as sp

ROOT=Path(__file__).resolve().parent


def checks_closure():
    eps=.02; ell=.2
    # Jacobi-Anger expansion, independent of the source's initial-data FFT.
    modes=np.arange(-180,181)
    amplitudes=1j**modes*jv(modes,1/eps)
    xx=np.linspace(-math.pi,math.pi,4096,endpoint=False)
    basis=np.exp(1j*np.outer(xx,modes))
    kernel=sum(np.exp(-(xx+2*math.pi*m)**2/(2*ell**2)) for m in range(-2,3))/(math.sqrt(2*math.pi)*ell)
    integrator=lambda a:float(np.sum(a*kernel)*2*math.pi/len(xx))
    rows=[]
    for t in [0,.9,1.5,3,6]:
        c=amplitudes*np.exp(-.5j*eps*modes**2*t)
        psi=basis@c; px=basis@(1j*modes*c); pxx=basis@(-modes**2*c)
        # Equivalent stress written without rho_xx.
        rho=abs(psi)**2
        current=eps*np.imag(psi.conj()*px)
        flux=.5*eps**2*(abs(px)**2-np.real(psi.conj()*pxx))
        r,j,T=map(integrator,[rho,current,flux])
        stress=T-j*j/r
        rows.append({'t':t,'density':r,'current':j,'stress':stress,'K_5_over_3':stress/r**(5/3)})
    saved=json.loads((ROOT/'closure/results.json').read_text())
    maxdiff=0
    for row in rows:
        ref=next(v for v in saved['central_time_series_eps_002_ell_02'] if v['t']==row['t'])
        maxdiff=max(maxdiff,abs(row['density']-ref['density']),abs(row['stress']-ref['stress']),
                    abs(row['K_5_over_3']-ref['K_5_over_3_proxy']))
    assert maxdiff<1e-10
    occupations=abs(amplitudes)**2
    m2=float(np.sum((eps*modes)**2*occupations))
    m4=float(np.sum((eps*modes)**4*occupations))
    assert abs(m2-.5)<1e-12 and abs(m4-(.375+eps**2/2))<1e-12
    # Independent adaptive Lagrangian integral at the caustic center.
    def local_moment(power):
        def f(q):
            x=q-1.5*math.sin(q); v=-math.sin(q)
            w=sum(math.exp(-(x+2*math.pi*m)**2/(2*ell**2)) for m in range(-2,3))/(math.sqrt(2*math.pi)*ell)
            return w*v**power
        return quad(f,-math.pi,math.pi,epsabs=1e-12,epsrel=1e-12)[0]
    cr,cj,cT=[local_moment(p) for p in range(3)]
    cp=cT-cj*cj/cr
    assert abs(cr-4.772108)<1e-6 and abs(cp-2.652046)<1e-6
    # Momentum conservation from real and imaginary parts of Schrodinger.
    a,b,ax,bx,axx,bxx,axxx,bxxx,e=sp.symbols('a b ax bx axx bxx axxx bxxx e',real=True)
    at,bt=-e*bxx/2,e*axx/2
    axt,bxt=-e*bxxx/2,e*axxx/2
    mass_res=sp.expand(2*a*at+2*b*bt+e*(a*bxx-b*axx))
    momentum_res=sp.expand(e*(at*bx+a*bxt-bt*ax-b*axt)
                          +e**2/2*(ax*axx+bx*bxx-a*axxx-b*bxxx))
    assert mass_res==0 and momentum_res==0
    s=2.404825557695773
    # Characteristic function of the sine marginal, no imported response code.
    response=quad(lambda q:math.cos(s*math.sin(q))/(2*math.pi),-math.pi,math.pi,epsabs=1e-13)[0]
    gaussian=math.exp(-s*s/4)
    assert abs(response)<1e-13 and abs(response-j0(s))<1e-13
    return {'Bessel_wave_rows':rows,'max_difference_from_author':maxdiff,
            'modal_second_moment':m2,'modal_fourth_moment':m4,'classical_adaptive_quadrature':{'rho':cr,'j':cj,'stress':cp},
            'matched_state_stress_range_factor':(1.5/.75)**2,
            'mass_conservation_symbolic_residual':str(mass_res),
            'momentum_conservation_symbolic_residual':str(momentum_res),
            'arcsine_response_at_first_J0_zero':response,'Gaussian_same_variance_response':gaussian}


def checks_observations():
    g,a,b=sp.symbols('g a b',positive=True)
    x=sp.sqrt(b*g/a)
    f=b*g/(1-sp.exp(-x))
    t=x/(2*(sp.exp(x)-1))
    assert sp.simplify(a*sp.diff(f,a)/f-t)==0
    assert sp.simplify(b*sp.diff(f,b)/f-(1-t))==0
    rng=np.random.default_rng(853943)
    z=np.r_[0,rng.uniform(0,3,400)]
    g=np.exp(rng.uniform(-13,6,len(z)))
    E=np.sqrt(.315*(1+z)**3+.685)
    def prediction(A,B,C,q,s,u):
        aa=A*E**q; bg=B*E**s*g
        return C*E**u*bg/(-np.expm1(-np.sqrt(bg/aa)))
    p=prediction(1.2,.7,1.1,.9,-.3,.2)
    pp=prediction(1.2,.7,1.1,.9+.8,-.3+.8,.2-.8)
    pa=prediction(1.2*2.7,.7*2.7,1.1/2.7,.9,-.3,.2)
    h=prediction(1,1,1,1,0,0); c=prediction(1,1,1,0,-1,1)
    errs={'exponent_symmetry':float(np.max(abs(pp/p-1))),
          'amplitude_symmetry':float(np.max(abs(pa/p-1))),
          'q1_vs_q0_counterexample':float(np.max(abs(c/h-1)))}
    assert max(errs.values())<1e-13
    xx=np.sqrt(.7*E**(-.3)*g/(1.2*E**.9))
    tt=np.zeros_like(xx)
    small=xx<700
    tt[small]=xx[small]/(2*np.expm1(xx[small]))
    logE=np.log(E)
    J=np.column_stack([tt,1-tt,tt*logE,(1-tt)*logE,np.ones_like(z),logE])
    null0=np.array([1,1,0,0,-1,0]);null1=np.array([0,0,1,1,0,-1])
    assert np.max(abs(J@null0))<1e-14 and np.max(abs(J@null1))<1e-14
    assert np.linalg.matrix_rank(J,tol=1e-10)==4
    deep=.5*(np.log(1.2*.7*g)+(.9-.3)*logE)+math.log(1.1)+.2*logE
    apparent_q=np.polyfit(logE,2*deep-np.log(g),1)[0]
    assert abs(apparent_q-(.9-.3+2*.2))<1e-12
    thresholds=[]
    for zlo,zhi in [(0,1),(.33,1.44)]:
        Efun=lambda z:math.sqrt(.315*(1+z)**3+.685)
        L=math.log10(Efun(zhi)/Efun(zlo))
        sigma_b=L/norm.ppf(.975); sigma_v=sigma_b/4
        thresholds.append({'redshifts':[zlo,zhi],'lever_dex':L,'sigma_b_only_dex':sigma_b,
                           'sigma_velocity_only_dex':sigma_v,'approx_velocity_fraction':math.log(10)*sigma_v})
    # Explicit covariance matrix, then generalized least squares mean variance.
    cov=.05**2*np.eye(8)+.10**2*np.ones((8,8))
    honest=float(1/math.sqrt(np.ones(8)@np.linalg.solve(cov,np.ones(8))))
    naive=float(math.sqrt(np.diag(cov)[0]/8))
    saved=json.loads((ROOT/'observations/results.json').read_text())
    selection=saved['selection_control']
    alphas=np.array(selection['cut_in_noise_sigma'])
    # Numerically integrate the truncated density rather than use Mills formula.
    means=np.array([.1*quad(lambda x:x*norm.pdf(x),lo,np.inf,epsabs=1e-12)[0]
                    /quad(lambda x:norm.pdf(x),lo,np.inf,epsabs=1e-12)[0] for lo in alphas])
    maxsel=float(np.max(abs(means-np.array(selection['retained_mean_residual_dex']))))
    assert maxsel<1e-12
    return {'homogeneity_relative_errors':errs,'full_parameter_rank':int(np.linalg.matrix_rank(J,tol=1e-10)),
            'amplitude_null_vector':null0.tolist(),'exponent_null_vector':null1.tolist(),
            'deep_apparent_q':float(apparent_q),'expected_q_plus_s_plus_2u':1.0,
            'precision_thresholds':thresholds,'covariance_GLS_sigma_dex':honest,
            'covariance_naive_sigma_dex':naive,'underestimate_factor':honest/naive,
            'selection_integral_max_difference_dex':maxsel}


def replay():
    rows=[]
    with tempfile.TemporaryDirectory(prefix='second-review-') as td:
        tmp=Path(td)
        for folder,script in [('closure','caustic_control.py'),('observations','probe.py')]:
            runpath=tmp/folder; runpath.mkdir()
            shutil.copy2(ROOT/folder/script,runpath/script)
            run=subprocess.run([sys.executable,'-B',script],cwd=runpath,capture_output=True,text=True)
            assert run.returncode==0,run.stderr
            actual=json.loads((runpath/'results.json').read_text())
            saved=json.loads((ROOT/folder/'results.json').read_text())
            assert actual==saved
            rows.append({'probe':folder+'/'+script,'exit_code':run.returncode,
                         'all_saved_JSON_values_match_replay':True})
    return rows


def main():
    files=['closure/research.md','closure/caustic_control.py','closure/results.json','closure/sources.json',
           'observations/research.md','observations/probe.py','observations/results.json','observations/sources.json']
    hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files}
    results={'artifact_sha256':hashes,'closure_independent_checks':checks_closure(),
             'observations_independent_checks':checks_observations(),'temporary_author_replays':replay()}
    assert hashes=={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files}
    results['author_artifacts_unchanged']=True
    (ROOT/'second-review-checks.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))


if __name__=='__main__':main()
