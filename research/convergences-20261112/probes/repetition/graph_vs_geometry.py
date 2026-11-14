#!/usr/bin/env python3
"""A fixed interaction graph during the cab-to-fcc geometric fold.

Python standard library only. Does not modify or import the source repository.
The curve is taken from aska-digital/incentre-lattice,
results/fold-continuous-fcc/PROOF.md (commit recorded in results.json).
This probe counts contacts, samples the density and verifies exactly that
the interior contact graph equals the bar graph. It extends the source's
Bernstein certificate to strict nonbar distances using integer arithmetic.
Its infinite-image exclusion uses the analytic bound from that source.
"""
import hashlib
import itertools
import json
import math
from pathlib import Path

P = tuple(tuple(sign * (i == axis) for i in range(3))
          for axis in range(3) for sign in (1, -1))
C = ((0, -1, -1), (1, 0, -1), (1, -1, 0))
SHIFTS = tuple(n for n in itertools.product(range(-3, 4), repeat=3)
               if sum(x*x for x in n) <= 11)
ZERO = (0, 0, 0)


def lattice(s):
    t = 2*s/(1+s*s)
    a = math.sqrt(2)*(1-s*s)/(1+s*s)
    return tuple(tuple((2+a)*(i == j) + t*C[i][j] for j in range(3))
                 for i in range(3))


def distance2(p, q, n, L):
    return sum((q[i]-p[i] + sum(n[j]*L[j][i] for j in range(3)))**2
               for i in range(3))


def bar(p, q, n):
    """Directed edge from motif p in cell 0 to motif q in cell n."""
    a = next(i for i, x in enumerate(p) if x)
    b = next(i for i, x in enumerate(q) if x)
    if n == ZERO:
        return a != b
    return (a == b and q[a] == -p[a]
            and n == tuple(p[a]*(i == a) for i in range(3)))


def edges_for(p, L, contact=False, tol=1e-10):
    return [(q, n) for q in P for n in SHIFTS
            if not (p == q and n == ZERO)
            and (abs(distance2(p, q, n, L)-2) < tol if contact else bar(p, q, n))]


def triangles_per_vertex(p, L, contact=False):
    neighbors = edges_for(p, L, contact)
    count = 0
    for (q, n), (r, m) in itertools.combinations(neighbors, 2):
        delta = tuple(y-x for x, y in zip(n, m))
        count += (abs(distance2(q, r, delta, L)-2) < 1e-10 if contact
                  else bar(q, r, delta))
    return count


def determinant(L):
    a, b, c = L
    return (a[0]*(b[1]*c[2]-b[2]*c[1])
            - a[1]*(b[0]*c[2]-b[2]*c[0])
            + a[2]*(b[0]*c[1]-b[1]*c[0]))


def graph_digest(L):
    edges = [(i, P.index(q), n) for i, p in enumerate(P)
             for q, n in edges_for(p, L)]
    return hashlib.sha256(json.dumps(edges).encode()).hexdigest()


def qadd(x, y):
    return (x[0]+y[0], x[1]+y[1])


def qscale(x, n):
    return (x[0]*n, x[1]*n)


def qdot(x, y):
    # Exact coefficients of 1 and sqrt(2), all integers.
    return (sum(a*c+2*b*d for (a, b), (c, d) in zip(x, y)),
            sum(a*d+b*c for (a, b), (c, d) in zip(x, y)))


def qsign(x):
    a, b = x
    if not b:
        return (a > 0)-(a < 0)
    if not a:
        return (b > 0)-(b < 0)
    if (a > 0) == (b > 0):
        return (a > 0)-(a < 0)
    return ((a*a > 2*b*b)-(a*a < 2*b*b))*((a > 0)-(a < 0))


def exact_interior_contacts(matrix=C):
    """Every nonbar distance is strictly >sqrt(2) for 0<s<1.

    Integer arithmetic with pairs a+b*sqrt(2). Twelve times every degree-four
    Bernstein coefficient is integral. Every Bernstein basis function is
    positive in the open interval: one positive coefficient suffices.
    The infinite-image exclusion is the analytic bound stated in the source.
    """
    identities = strict = 0
    for p in P:
        for q in P:
            for n in SHIFTS:
                if p == q and n == ZERO:
                    continue
                v = tuple(y-x for x, y in zip(p, q))
                A = [(2*x+y, x) for x, y in zip(n, v)]
                B = [(2*sum(n[j]*matrix[j][i] for j in range(3)), 0) for i in range(3)]
                D = [(2*x+y, -x) for x, y in zip(n, v)]
                coeff = [qadd(qdot(A, A), (-2, 0)), qscale(qdot(A, B), 2),
                         qadd(qadd(qdot(B, B), qscale(qdot(A, D), 2)), (-4, 0)),
                         qscale(qdot(B, D), 2), qadd(qdot(D, D), (-2, 0))]
                b12 = []
                for k in range(5):
                    value = (0, 0)
                    for j in range(k+1):
                        numerator = 12*math.comb(k, j)
                        denominator = math.comb(4, j)
                        assert numerator % denominator == 0
                        value = qadd(value, qscale(coeff[j], numerator//denominator))
                    b12.append(value)
                assert all(qsign(x) >= 0 for x in b12)
                identical = all(x == (0, 0) for x in b12)
                assert identical == bar(p, q, n)
                identities += identical
                strict += not identical
    return {"directed_bar_identities": identities,
            "directed_nonbar_strict_distance_polynomials": strict,
            "arithmetic": "exact integer pairs a+b*sqrt(2)",
            "interior_contact_graph_equals_prescribed_bar_graph": True,
            "scope": "0<s<1; distant images excluded by analytic singular-value bound"}


def main():
    assert qsign((665857, -470832)) == 1  # near-cancelling Pell pair, norm +1
    assert qsign((-665857, 470832)) == -1
    interior_certificate = exact_interior_contacts()
    bad_matrix = ((1, -1, -1), C[1], C[2])  # changes one bridge's length
    rejected_bad_curve = False
    try:
        exact_interior_contacts(bad_matrix)
    except AssertionError:
        rejected_bad_curve = True
    assert rejected_bad_curve
    states = []
    for s in (0.0, 0.25, 0.5, 0.75, 0.9, 0.99, 1.0):
        L = lattice(s)
        nonbar = [distance2(p, q, n, L) for p in P for q in P for n in SHIFTS
                  if not (p == q and n == ZERO) and not bar(p, q, n)]
        bar_errors = [abs(distance2(p, q, n, L)-2) for p in P
                      for q, n in edges_for(p, L)]
        states.append({
            "s": s,
            "density": 2*math.sqrt(2)*math.pi/determinant(L),
            "bar_degree_each_vertex": [len(edges_for(p, L)) for p in P],
            "contact_degree_each_vertex": [len(edges_for(p, L, True)) for p in P],
            "bar_graph_sha256": graph_digest(L),
            "max_bar_squared_length_error": max(bar_errors),
            "smallest_nonbar_gap_over_contact_distance": math.sqrt(min(nonbar)/2)-1,
        })
    assert all(x["bar_degree_each_vertex"] == [5]*6 for x in states)
    assert len({x["bar_graph_sha256"] for x in states}) == 1
    assert states[0]["contact_degree_each_vertex"] == [5]*6
    assert states[-1]["contact_degree_each_vertex"] == [12]*6
    assert max(x["max_bar_squared_length_error"] for x in states) < 1e-12
    # At s=1 every coordinate is integral: count all contacts with exact integers.
    L1 = tuple(tuple(2*(i == j)+C[i][j] for j in range(3)) for i in range(3))
    exact_contacts = [sum(distance2(p, q, n, L1) == 2
                          for q in P for n in SHIFTS) for p in P]
    assert exact_contacts == [12]*6
    bar_triangles = [triangles_per_vertex(p, L1) for p in P]
    contact_triangles = [triangles_per_vertex(p, L1, True) for p in P]
    assert bar_triangles == [4]*6
    assert contact_triangles == [24]*6
    # Expansion for an infinite simple graph (no small-torus identifications):
    # log Z/N = log 2 + (z/4) K^2 + (triangles/N) K^3 + O(K^4).
    # K = J/(k_B T). Follows from the even-subgraph high-temperature expansion.
    output = {
        "status": "reproducible model calculation; no material prediction",
        "source_repository": "https://github.com/aska-digital/incentre-lattice",
        "source_commit": "db3b51d0f31e04ea3c0ffafb553f70fcdfc617ec",
        "source_path": "results/fold-continuous-fcc/PROOF.md",
        "assumption": "Fixed scalar Ising J on prescribed bars; no interactions on other contacts",
        "image_bound": "sigma_min(L)>=1 and |p-q|<=2 exclude |n|^2>=12 from contact; written source proof",
        "states": states,
        "exact_endpoint_contacts": exact_contacts,
        "exact_interior_certificate": interior_certificate,
        "negative_controls": {"near_cancellation_signs": "passed", "changed_bridge_curve_rejected": rejected_bad_curve},
        "bar_graph": {"edges_per_cell": 15, "triangles_per_cell": 8,
                      "ground_energy_per_site_over_J": -2.5,
                      "logZ_per_site_K2_coefficient": 1.25,
                      "logZ_per_site_K3_coefficient": 4/3,
                      "reduced_susceptibility_K_coefficient": 5},
        "full_fcc_contact_graph": {"edges_per_cell": 36, "triangles_per_cell": 48,
                      "ground_energy_per_site_over_J": -6,
                      "logZ_per_site_K2_coefficient": 3,
                      "logZ_per_site_K3_coefficient": 8,
                      "reduced_susceptibility_K_coefficient": 12},
        "limitation": "Exact interior contact result uses the source curve and analytic distant-image bound. Fixed-bar partition-function invariance is algebraic by definition. No Tc or percolation threshold estimated."
    }
    destination = Path(__file__).with_name("graph-results.json")
    destination.write_text(json.dumps(output, indent=2)+"\n")
    print(json.dumps({"states": len(states), "bar_degree": 5,
                      "endpoint_contact_degree": 12,
                      "density_ratio": states[-1]["density"]/states[0]["density"],
                      "output": str(destination)}, indent=2))


if __name__ == "__main__":
    main()
