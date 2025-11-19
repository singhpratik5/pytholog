from pytholog.expr import Expr

# Test parsing of "is" expressions
e1 = Expr("Z is X + Y")
print(f"Expr: 'Z is X + Y'")
print(f"  predicate: '{e1.predicate}'")
print(f"  terms: {e1.terms}")
print()

e2 = Expr("sum(X, Y, Z)")
print(f"Expr: 'sum(X, Y, Z)'")
print(f"  predicate: '{e2.predicate}'")
print(f"  terms: {e2.terms}")
