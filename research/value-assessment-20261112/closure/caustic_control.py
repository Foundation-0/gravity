#!/usr/bin/env python3
"""A coherent caustic control, not AeST and not a new physical theory.

Run: python3 caustic_control.py
Requires numpy and scipy. All units are dimensionless. No gravity, collisions,
nonlinear wave interaction, thermal bath, forcing or fitted parameters appear.
"""
from pathlib import Path
import json
import math
import platform

import numpy as np
import scipy
from scipy.special import jv, jvp, j0


OUT = Path(__file__).resolve().parent


def grid(n):
    return np.arange(n) * (2 * np.pi / n), np.fft.fftfreq(n, 1/n)


def smooth(a, k, ell):
    return np.fft.ifft(np.fft.fft(a) * np.exp(-0.5 * (ell*k)**2)).real


def wave(eps, t, ell, n=4096):
    x, k = grid(n)
    initial = np.exp(1j*np.cos(x)/eps)
    initial_hat = np.fft.fft(initial)
    evolution = np.exp(-0.5j*eps*k*k*t)
    phat = initial_hat * evolution
    psi = np.fft.ifft(phat)
    px = np.fft.ifft(1j*k*phat)
    pxx = np.fft.ifft(-k*k*phat)
    pt = 0.5j*eps*pxx
    pxt = np.fft.ifft(1j*k*np.fft.fft(pt))
    rho = abs(psi)**2
    j = eps*np.imag(np.conj(psi)*px)
    # Differentiate the represented field before forming products. Applying
    # three derivatives to FFT roundoff in rho needlessly magnifies noise.
    rhoxx = 2*(abs(px)**2 + np.real(np.conj(psi)*pxx))
    flux = eps*eps*(abs(px)**2 - rhoxx/4)
    r = smooth(rho, k, ell)
    jm = smooth(j, k, ell)
    fluxm = smooth(flux, k, ell)
    stress = fluxm - jm*jm/r
    rhot = 2*np.real(np.conj(psi)*pt)
    jt = eps*np.imag(np.conj(pt)*px + np.conj(psi)*pxt)
    dxj = np.fft.ifft(1j*k*np.fft.fft(j)).real
    dxflux = np.fft.ifft(1j*k*np.fft.fft(flux)).real
    reverse = np.fft.ifft(np.fft.fft(np.conj(psi))*evolution)
    norm = np.linalg.norm
    occupancy = abs(phat/n)**2
    checks = {
        'mass_mean': float(rho.mean()),
        'energy_mean': float((eps*eps*abs(px)**2/2).mean()),
        'momentum_mean': float(j.mean()),
        'continuity_relative_residual': float(norm(rhot+dxj)/max(norm(rhot), 1.0)),
        'momentum_relative_residual': float(norm(jt+dxflux)/max(norm(jt), 1.0)),
        'time_reversal_relative_field_error': float(norm(reverse-np.conj(initial))/norm(initial)),
        'modal_occupation_max_change': float(np.max(abs(occupancy-abs(initial_hat/n)**2))),
        'momentum_distribution_second_moment': float(np.sum((eps*k)**2*occupancy)),
        'momentum_distribution_fourth_moment': float(np.sum((eps*k)**4*occupancy)),
        'momentum_distribution_kurtosis': float(np.sum((eps*k)**4*occupancy)/np.sum((eps*k)**2*occupancy)**2),
        'high_k_mass_fraction_abs_k_gt_n_over_4': float(occupancy[abs(k)>n/4].sum()/occupancy.sum()),
    }
    central = {
        'density': float(r[0]),
        'mean_velocity': float(jm[0]/r[0]),
        'stress': float(stress[0]),
        'stress_over_density': float(stress[0]/r[0]),
        'K_5_over_3_proxy': float(stress[0]/r[0]**(5/3)),
    }
    return r, jm, stress, central, checks


def classical(t, ell, n=4096):
    """Exact Fourier moments of x=q-t sin(q), v=-sin(q), uniform q.

    n_m=J_m(mt), j_m=i J_m'(mt), M2_m=-J_m''(mt) for m>0.
    A Gaussian filter makes truncation above |m|=ceil(12/ell) negligible.
    """
    _, k = grid(n)
    rhoh = np.zeros(n, complex)
    jh = np.zeros(n, complex)
    m2h = np.zeros(n, complex)
    rhoh[0] = 1
    m2h[0] = 0.5
    active = (abs(k)>0) & (abs(k)<=math.ceil(12/ell))
    order = abs(k[active]).astype(int)
    arg = order*t
    weight = np.exp(-0.5*(ell*order)**2)
    rhoh[active] = jv(order, arg)*weight
    jh[active] = 1j*np.sign(k[active])*jvp(order, arg, 1)*weight
    m2h[active] = -jvp(order, arg, 2)*weight
    rho, j, m2 = [np.fft.ifft(n*h).real for h in (rhoh, jh, m2h)]
    assert rho.min() > 0
    stress = m2-j*j/rho
    return rho, j, stress


def central_quadrature(t, ell, nq=131072):
    """Independent Lagrangian quadrature, without Eulerian binning."""
    q = 2*np.pi*(np.arange(nq)+0.5)/nq - np.pi
    xx = q-t*np.sin(q)
    v = -np.sin(q)
    weight = sum(np.exp(-0.5*((xx+2*np.pi*m)/ell)**2)
                 for m in range(-2,3))/(math.sqrt(2*np.pi)*ell)
    rho = 2*np.pi*np.mean(weight)
    j = 2*np.pi*np.mean(weight*v)
    flux = 2*np.pi*np.mean(weight*v*v)
    return rho, j, flux-j*j/rho


def run():
    convergence=[]
    checks=[]
    time_rows=[]
    for ell in [0.1,0.2,0.4]:
        rc,jc,pc = classical(1.5, ell)
        qr,qj,qp = central_quadrature(1.5,ell)
        assert np.allclose([rc[0],jc[0],pc[0]],[qr,qj,qp],rtol=2e-11,atol=2e-12)
        for eps in [0.08,0.04,0.02,0.01]:
            r,j,p,c,ch = wave(eps,1.5,ell)
            for key,expected in [('mass_mean',1),('energy_mean',0.25),('momentum_mean',0)]:
                assert abs(ch[key]-expected)<2e-12
            assert ch['time_reversal_relative_field_error']<1e-12
            assert ch['continuity_relative_residual']<1e-9
            assert ch['momentum_relative_residual']<1e-9
            assert ch['high_k_mass_fraction_abs_k_gt_n_over_4']<1e-20
            assert abs(ch['momentum_distribution_second_moment']-0.5)<2e-12
            assert abs(ch['momentum_distribution_fourth_moment']-(0.375+eps*eps/2))<2e-12
            row={'eps':eps,'ell':ell,'t':1.5,'central':c,
                 'density_relative_L2_error_vs_collisionless':float(np.linalg.norm(r-rc)/np.linalg.norm(rc)),
                 'stress_relative_L2_error_vs_collisionless':float(np.linalg.norm(p-pc)/np.linalg.norm(pc)),
                 'classical_central_density':float(rc[0]),'classical_central_stress':float(pc[0])}
            convergence.append(row)
            checks.append({'eps':eps,'ell':ell,**ch})
    for t in [0,0.5,0.9,1.0,1.2,1.5,2,3,6,12]:
        r,j,p,c,ch=wave(0.02,t,0.2)
        time_rows.append({'t':t,**c,'mean_coarse_stress':float(p.mean())})
    # Resolution is varied at fixed physical dispersion and filter.
    r1,j1,p1,_,_=wave(0.01,1.5,0.2,n=2048)
    r2,j2,p2,_,_=wave(0.01,1.5,0.2,n=4096)
    refinement=float(max(np.max(abs(r1-r2[::2])),np.max(abs(j1-j2[::2])),np.max(abs(p1-p2[::2]))))
    assert refinement<1e-10
    # A literal rho-only stress closure fails across controlled infall speeds.
    # Use cold regular initial sheets x_i(q)=q-D_i sin(q), v=-a sin(q).
    # At the SAME t=1, D_i+a*t=1.5 makes rho identical; velocity and
    # stress scale as a and a^2. Symmetry gives local u(0)=0 for each.
    rc,jc,pc=classical(1.5,0.2)
    pair=[{'infall_amplitude':a,'initial_displacement_amplitude':1.5-a,
           'physical_time':1.0,'dimensionless_age':1.5,
           'first_caustic_time':(1-(1.5-a))/a,
           'central_density':float(rc[0]),'central_velocity':float(a*jc[0]/rc[0]),
           'central_stress':float(a*a*pc[0])} for a in [0.75,1,1.5]]
    # In strict planar collapse embedded in 3D, the kinetic stress has rank 1.
    eigenvalues=[float(pc[0]),0.0,0.0]
    # Arcsine distribution arises from the velocity marginal v=-sin(q).
    # Its perturbation response is J0(kt); a Gaussian at variance 1/2 differs.
    response=[{'k_t':z,'arcsine_density_response':float(j0(z)),
               'gaussian_same_variance_density_response':float(np.exp(-z*z/4))}
              for z in [0,1,2,2.404825557695773,3,4,6]]
    # Exact quantum torus recurrence: exp(-i eps k^2 T/2)=1 at T=4pi/eps.
    _,_,_,initial,_=wave(0.02,0,0.2)
    _,_,_,recur,_=wave(0.02,4*np.pi/0.02,0.2)
    assert abs(initial['K_5_over_3_proxy']-recur['K_5_over_3_proxy'])<1e-10
    results={
        'scope':'Exact free Schrodinger and collisionless caustic controls. NOT AeST; no gravity, collisions or interacting-wave thermalization.',
        'equations':{'wave':'i eps psi_t = -eps^2 psi_xx/2',
                     'initial':'psi(x,0)=exp(i cos(x)/eps), x on [0,2pi)',
                     'kinetic':'x(q,t)=q-t sin(q), v=-sin(q), uniform q',
                     'first_classical_caustic_time':1,
                     'wave_momentum_flux':'eps^2 |psi_x|^2 - eps^2 rho_xx/4',
                     'coarse_stress':'GaussianFilter(momentum_flux)-GaussianFilter(j)^2/GaussianFilter(rho)'},
        'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},
        'convergence':convergence,'conservation_and_reversibility':checks,
        'central_time_series_eps_002_ell_02':time_rows,
        'resolution_2048_4096_max_absolute_difference':refinement,
        'matched_density_velocity_different_infall_stress':pair,
        'planar_classical_stress_eigenvalues_at_center':eigenvalues,
        'planar_normalized_anisotropy_frobenius_over_trace':float(math.sqrt(2/3)),
        'generated_velocity_marginal':{'density':'1/(pi sqrt(1-v^2)) on |v|<1',
            'variance':0.5,'fourth_moment':0.375,'kurtosis':1.5,
            'same_variance_gaussian_fourth_moment':0.75,'same_variance_gaussian_kurtosis':3},
        'long_wavelength_response_of_homogenized_kinetic_control':response,
        'torus_recurrence':{'eps':0.02,'time':float(4*np.pi/0.02),'initial_central':initial,'recurrent_central':recur},
        'tests':'All assertions passed. Fourier kinetic moments checked against independent Lagrangian quadrature.'
    }
    (OUT/'results.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({'tests':results['tests'],'refinement':refinement,
        'convergence_ell_02':[x for x in convergence if x['ell']==0.2],
        'time_series':time_rows,'matched_pair':pair},indent=2))


if __name__=='__main__':
    run()
