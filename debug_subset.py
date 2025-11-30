from pytholog import KnowledgeBase, pl_expr
from pytholog import unify as original_unify

kb = KnowledgeBase("subset_test")
kb([
    "member(X, [X|T])",
    "member(X, [H|T]) :- member(X, T)",
    "subset([], L)",
    "subset([H|T], List) :- member(H, List), subset(T, List)"
])

# Patch to add debug logging
def debug_unify(lh, rh, lh_domain, rh_domain):
    import copy
    before_lh = copy.deepcopy(lh_domain)
    before_rh = copy.deepcopy(rh_domain)
    result = original_unify(lh, rh, lh_domain, rh_domain)
    print(f"UNIFY: {lh} [{before_lh}->{lh_domain}] WITH {rh} [{before_rh}->{rh_domain}] = {result}")
    return result

import pytholog.search_util
pytholog.search_util.unify = debug_unify

print("=== Query: subset([a,c],[a,b,c]) ===")
result = kb.query(pl_expr("subset([a,c],[a,b,c])"))
print(f"Result: {result}")
