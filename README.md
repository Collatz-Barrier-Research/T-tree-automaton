# T-tree-automaton
Overview

This repository implements an automaton and symbolic computation framework for exploring T-trees in the context of the Collatz conjecture. It focuses on prefix-residue tracking, generating functions for path merges, residue enhancements, and pruning integration. The goal is to automate verifications of T-tree reconvergence for small parameters (e.g., k=3, m=), potentially advancing toward a full inductive proof. 

Key features:
Symbolic merging of generating functions for T-paths.
Residue looping over odd r mod10^k.
Pruning for non-reconverging or high-degree paths.
Built with SymPy for algebraic manipulation.
This is research code—contributions welcome for expansions like full barrier simulations or larger (k).


Installation 

Clone the repo:

git clone https://github.com/collatz-barrier-research/T-tree-automaton.git
cd T-tree-automaton

Install dependencies (Python 3.8+ required):

pip install sympy

For reproducibility, use a virtual environment: 

python -m venv env
source env/bin/activate
pip install -r requirements.txt  # Create this file with 'sympy'

UsageRun the main script to compute merged generating functions with residues and pruning: python

# In collatz_t_merge.py (edit k_val, depth, prune_bound as needed)
result = residue_merge(k_val=1, depth=3, prune_bound=10)
print(result.expand())

Example output (for k=):
(3n+1)/2^o⋅x^3+((4^k)m−1)/3⋅x^2+n/2⋅x+P⋅10^(d+k)+r
Customization: Adjust k_val for modulus, depth for path length, prune_bound to control reconvergence checks.
Testing Larger k: For k=3, run on a machine with more RAM or cloud (e.g., Google Colab) to handle mod=1000.
Reproducibility Notes: Seed random elements if added (none currently). Results are deterministic symbolic expressions. Tested on Python 3.12; outputs match paper examples (e.g., paths from n=27). 

Mathematical BackgroundThe script models Collatz transitions symbolically:Forward rule: f(n) = \begin{cases} n/2 & n \even \\ (3n+1)/2^o & n \odd \end{cases}
Inverse edges: f1(m)=((4^k)m−1)/3f_1(m) = (4^k m - 1)/3f_1(m) = (4^k m - 1)/3
for m≡1 mod3

Merges use common subexpression elimination (CSE) to factor shared paths, pruning if degree > bound or non-integer coefficients. 

LicenseMIT License. See LICENSE for details.ContributingFork the repo, make changes, and submit a pull request. Issues welcome for bugs or feature requests (e.g., integrate NetworkX for full DAG visualization). 
