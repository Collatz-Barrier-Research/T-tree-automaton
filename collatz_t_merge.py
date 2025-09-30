import sympy as sp

# Symbols for general use
n, x, o, r, k, P, d = sp.symbols('n x o r k P d')

# Grammar rules (even/odd from symbolic collapse)
even_rule = n / 2
odd_rule = (3 * n + 1) / 2**o

# Inverse edges f1/f2
m = sp.symbols('m')
f1 = (4**k * m - 1) / 3  # m ≡1 mod 3
f2 = 2 * (4**k - 1)/3 * m - 1  # m ≡2 mod 3

# GF for forward path with grammar
def grammar_gf(start, depth=3):
    expr = start
    for i in range(depth):
        # Apply rules symbolically
        expr = sp.Piecewise((even_rule.subs(n, expr), sp.Mod(expr, 2)==0),
                            (odd_rule.subs(n, expr), True)) * x**i
    return expr + start  # Sum path

# Merge using CSE (common subexpressions)
def merge_gfs(gf1, gf2):
    commons, simplified = sp.cse([gf1, gf2])
    return sp.simplify(sum(simplified) + sum(c * x**i for i, c in enumerate(commons)))

# Inverse path GF using f1/f2
def inverse_gf(root, depth=2):
    expr = root
    for _ in range(depth):
        expr = sp.Piecewise((f1.subs(m, expr), sp.Mod(expr, 3)==1),
                            (f2.subs(m, expr), True))
    return expr * x**depth + root

# Pruning: Drop if degree > bound or non-integer (symbolic check)
def prune_gf(gf, max_degree=10):
    if gf.as_poly(x).degree() > max_degree:
        return None  # Pruned: Too long (non-reconverging)
    coeffs = gf.as_poly(x).all_coeffs()
    if all(c.is_integer for c in coeffs if c != 0):
        return gf
    return None  # Pruned: Non-integer coeffs

# Enhance for Residues: Loop over odd r mod 10^k
def residue_merge(k_val=3, depth=3, prune_bound=10):
    mod = 10 ** k_val
    merged_all = 0
    for res in range(1, mod, 2):  # Odd residues
        # Barrier n (simplified: ignore M, focus P=1, d=0 for demo)
        start = P * 10**(d + k) + res  # Symbolic barrier
        gf_fwd = grammar_gf(start.subs({P:1, d:0, k:k_val}), depth)
        gf_inv = inverse_gf(res, depth)  # Inverse from residue
        
        merged = merge_gfs(gf_fwd, gf_inv)
        pruned = prune_gf(merged, prune_bound)
        
        if pruned is not None:
            merged_all += pruned  # Accumulate valid merged paths
    
    return merged_all.simplify()

# Run for small k=1 (for test; scale to 3 on cloud)
result = residue_merge(k_val=1)
print("Merged GF with residues and pruning:")
print(result.expand())
