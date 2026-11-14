#!/usr/bin/env python3
"""Frozen-protocol slow-mode ensemble and hidden fast-mode leakage.

Dimensionless Q0=1. No fitting and no change to the audited action/background.
"""
import json,math,hashlib
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import linear_sum_assignment

HERE=Path(__file__).resolve().parent
QI=.01;DELTA=1e-5

def bg(a):
    q=QI/a**3;Q=1+q;Kp=4*q;R=4*q+2*q*q;W=Q*Kp;H=math.sqrt(R/3)
    return Q,Kp,R,W,H


def rhs(a,x,closure=None):
    Q,Kp,R,W,H=bg(a);r=KVAL*KVAL/a**2;ca=Kp/(4*Q);w=2*(Q-1)**2/R
    delta,theta=x[:2]
    Phi=-(R*delta+3*H*W*theta)/(2*r)
    if closure is None:
        chi,Z=x[2:];gamma=(R*delta+r*Z)/(4*Q);pressure=Kp*gamma
    else:pressure=0. if closure=='zero' else ca*R*delta
    Phidot=-H*Phi+W*theta/2
    dd=3*H*(w*delta-pressure/R)+3*W/R*Phidot-r*W/R*theta
    td=3*H*ca*theta+pressure/W+Phi
    if closure is not None:return np.array([dd,td])
    Qdot=-3*H*Kp/4
    chd=gamma+Q*Z+(Qdot/Q-Q)*chi-Qdot*theta
    Zd=(-H+Q)*Z+(Kp-3*Q)*chi
    return np.array([dd,td,chd,Zd])


def matrix(a,closure=None):
    dim=4 if closure is None else 2
    return np.column_stack([rhs(a,np.eye(dim)[:,j],closure) for j in range(dim)])


def modes():
    aa=np.linspace(1,2,201);eigrows=[];vecrows=[];prev=None
    for a in aa:
        eig,V=np.linalg.eig(matrix(a))
        if prev is None:
            positive=np.flatnonzero(eig.imag>1e-8)
            assert len(positive)==2
            fastp=int(max(positive,key=lambda j:eig[j].imag));fastm=int(np.argmin(abs(eig-eig[fastp].conjugate())))
            slow=[i for i in range(4) if i not in (fastp,fastm)]
            slow=sorted(slow,key=lambda i:eig[i].imag,reverse=True)
            order=slow+[fastp,fastm]
        else:
            ii,jj=linear_sum_assignment(abs(prev[:,None]-eig[None,:]));order=jj[np.argsort(ii)]
        eig=eig[order];V=V[:,order].astype(complex)
        assert max(abs(eig[:2].imag))<.1*abs(eig[2].imag) and eig[2].imag>0 and eig[3].imag<0
        V/=np.linalg.norm(V,axis=0)
        if vecrows:
            overlap=np.sum(vecrows[-1].conj()*V,axis=0)
            V*=np.exp(-1j*np.angle(overlap))[None,:]
        eigrows.append(eig);vecrows.append(V);prev=eig
    ee=np.array(eigrows);VV=np.array(vecrows);dVda=np.gradient(VV,aa,axis=0,edge_order=2)
    omega=ee[:,2].imag;domega=np.gradient(omega,aa,edge_order=2)
    gaps=[];rates=[];adiabatic=[];mix=[];mix_fs=[];mix_sf=[];conds=[]
    for i,a in enumerate(aa):
        H=bg(a)[-1];gap=min(abs(ee[i,s]-ee[i,f]) for s in (0,1) for f in (2,3))
        mixing=np.linalg.solve(VV[i],dVda[i]*(a*H))
        gaps.append(gap/H);rates.append(max(abs(ee[i,:2]))/omega[i])
        adiabatic.append(abs(a*H*domega[i])/omega[i]**2)
        mix.append(max(abs(mixing[s,f])/abs(ee[i,s]-ee[i,f]) for s,f in [(0,2),(0,3),(1,2),(1,3),(2,0),(2,1),(3,0),(3,1)]))
        mix_fs.append(max(abs(mixing[f,s])/abs(ee[i,f]-ee[i,s]) for f in (2,3) for s in (0,1)))
        mix_sf.append(max(abs(mixing[s,f])/abs(ee[i,s]-ee[i,f]) for s in (0,1) for f in (2,3)))
        conds.append(np.linalg.cond(VV[i]))
    e0,V0=ee[0],VV[0]
    S=np.column_stack([V0[:,0].real,V0[:,0].imag])
    assert np.linalg.cond(S[:2])<1e8,'Slow subspace cannot uniquely match retained data'
    slow_state=S@np.linalg.solve(S[:2],np.array([1.,-bg(1.)[-1]/KVAL**2]))
    f=V0[:,2]/V0[0,2]
    contaminants=[]
    for phase in (0.,math.pi/2,math.pi,3*math.pi/2):
        g=(np.exp(1j*phase)*f).real
        w=g-S@np.linalg.solve(S[:2],g[:2])
        assert np.linalg.norm(w[:2])<1e-10
        contaminants.append((phase,w))
    info={'initial_eigenvalues':[[float(e.real),float(e.imag)] for e in e0],
          'final_eigenvalues':[[float(e.real),float(e.imag)] for e in ee[-1]],
          'min_fast_slow_gap_over_H':float(min(gaps)),
          'max_slow_rate_over_fast_frequency':float(max(rates)),
          'max_frequency_adiabatic_ratio':float(max(adiabatic)),
          'max_fast_slow_eigenvector_mixing_over_gap':float(max(mix)),
          'max_fast_from_slow_mixing_over_gap':float(max(mix_fs)),
          'max_slow_from_fast_mixing_over_gap':float(max(mix_sf)),
          'max_eigenvector_condition_number':float(max(conds)),
          'initial_retained_slow_basis_condition_number':float(np.linalg.cond(S[:2])),
          'initial_fast_spectral_coordinate_norm':float(np.linalg.norm(np.linalg.solve(V0,slow_state)[2:])),
          'slow_initial_state_per_unit_delta':slow_state.tolist(),
          'compensated_leakage_vectors':[{'phase':phase,'state':w.tolist()} for phase,w in contaminants]}
    return slow_state,contaminants,info


def fundamental(grid,closure=None,tol=1e-11):
    n=4 if closure is None else 2
    def derivative(a,flat):
        return (matrix(a,closure)@flat.reshape(n,n)/(a*bg(a)[-1])).ravel()
    sol=solve_ivp(derivative,(1,2),np.eye(n).ravel(),t_eval=grid,method='DOP853',rtol=tol,atol=tol*1e-4)
    assert sol.success and sol.y.shape[1]==len(grid)
    return sol.y.T.reshape(len(grid),n,n)


def observables(grid,state):
    Q,Kp,R,W,H=np.array([bg(a) for a in grid]).T
    delta=state[:,0];theta=state[:,1];r=KVAL*KVAL/grid**2
    lens=-(R*delta+3*H*W*theta)/r
    return np.array([delta,lens])


def run_one(k,refined=False):
    global KVAL;KVAL=k
    slow_state,contaminants,info=modes()
    grid=np.linspace(1,2,4001 if refined else 2001);tol=1e-12 if refined else 1e-10
    fund=fundamental(grid,tol=tol)
    closures={c:fundamental(grid,c,tol) for c in ('zero','adiabatic')}
    initial=DELTA*slow_state
    reference={c:observables(grid,np.einsum('tij,j->ti',F,initial[:2])) for c,F in closures.items()}
    scales=np.max(abs(reference['zero']),axis=1)
    prepared=[(0.,0.,initial)]
    for eta in (.001,.01,.1):
        prepared.extend((eta,phase,initial+DELTA*eta*w) for phase,w in contaminants)
    rows=[]
    for eta,phase,x0 in prepared:
        assert np.max(abs(x0[:2]-initial[:2]))<1e-15
        states=np.einsum('tij,j->ti',fund,x0);obs=observables(grid,states)
        Q,Kp,R,W,H=np.array([bg(a) for a in grid]).T;r=k*k/grid**2
        Phi=obs[1]/2;vn=Q*states[:,1];al=(states[:,2]-vn)/Q
        gamma=(R*states[:,0]+r*states[:,3])/(4*Q)
        amplitudes={'density_contrast':float(np.max(abs(obs[0]))),'lensing_sum':float(np.max(abs(obs[1]))),
                    'aether_spatial':float(np.max(abs(k*al/grid))),'delta_Q_over_Q':float(np.max(abs(gamma/Q))),
                    'chi':float(np.max(abs(states[:,2])))}
        for c,pred in reference.items():
            errors=np.max(abs(obs-pred),axis=1)/scales
            rows.append({'k':k,'eta':eta,'phase':phase,'closure':c,'density_error':float(errors[0]),
                         'lensing_error':float(errors[1]),'passes_1_percent':bool(max(errors)<.01),
                         'max_amplitudes':amplitudes})
    # Direct integration is separate from the fundamental-matrix solution.
    direct=solve_ivp(lambda a,x:rhs(a,x)/(a*bg(a)[-1]),(1,2),initial,t_eval=grid,
                     method='DOP853',rtol=1e-12,atol=1e-20)
    baseline=np.einsum('tij,j->ti',fund,initial)
    direct_error=float(np.max(abs(direct.y.T-baseline))/DELTA)
    assert direct.success and direct_error<1e-7
    return {'k':k,'mode_diagnostics':info,'direct_vs_fundamental_error_per_delta_i':direct_error,
            'reference_scales':scales.tolist(),'rows':rows}


def main():
    results={'protocol_sha256':hashlib.sha256((HERE/'PROTOCOL.md').read_bytes()).hexdigest(),
             'scope':'Same-action instantaneous slow-subspace initialization, plus compensated fast contamination. No invariant-manifold or observational claim.',
             'points':[run_one(k) for k in (6.,9.,12.,18.,24.)]}
    refinement=run_one(12.,True)
    base=results['points'][2]
    err=max(abs(a[field]-b[field]) for a,b in zip(base['rows'],refinement['rows']) for field in ('density_error','lensing_error'))
    assert err<1e-5
    results['refinement']={'k':12.,'grid_points':4001,'rtol':1e-12,'max_error_fraction_change':err,
                           'direct_vs_fundamental_error_per_delta_i':refinement['direct_vs_fundamental_error_per_delta_i']}
    (HERE/'evidence.json').write_text(json.dumps(results,indent=2)+'\n')
    for point in results['points']:
        print('k',point['k'],'diagnostics',point['mode_diagnostics'])
        for eta in (0.,.001,.01,.1):
            for c in ('zero','adiabatic'):
                rr=[r for r in point['rows'] if r['eta']==eta and r['closure']==c]
                print(eta,c,'max error',max(max(r['density_error'],r['lensing_error']) for r in rr),'passes',sum(r['passes_1_percent'] for r in rr),'/',len(rr))
    print('refinement',results['refinement'])

if __name__=='__main__':main()
