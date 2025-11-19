from pytholog.util import parse_term
from pytholog.unify import unify
from pytholog.expr import Expr

# Parse the pattern and the concrete list
pattern_expr = Expr("[_|_]")
concrete_expr = Expr("[a]")

print(f"Pattern terms: {pattern_expr.terms}")
print(f"Concrete terms: {concrete_expr.terms}")

# Try to unify them
domain = {}
result = unify(pattern_expr, concrete_expr, domain, {})
print(f"\nUnify result: {result}")
print(f"Domain after: {domain}")

# Also test with the full predicate
fact_expr = Expr("nonempty([_|_])")
query_expr = Expr("nonempty([a])")

print(f"\nFact predicate: {fact_expr.predicate}, terms: {fact_expr.terms}")
print(f"Query predicate: {query_expr.predicate}, terms: {query_expr.terms}")

domain2 = {}
result2 = unify(fact_expr, query_expr, domain2, {})
print(f"\nUnify result: {result2}")
print(f"Domain after: {domain2}")
