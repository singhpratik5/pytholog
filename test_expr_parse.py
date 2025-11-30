from pytholog.expr import Expr

expr1 = Expr("nonempty([_|_])")
expr2 = Expr("nonempty([a])")

print(f"expr1 predicate: {expr1.predicate}")
print(f"expr1 terms: {expr1.terms}")
print(f"expr1 terms[0]: {repr(expr1.terms[0])}")

print(f"\nexpr2 predicate: {expr2.predicate}")
print(f"expr2 terms: {expr2.terms}")
print(f"expr2 terms[0]: {repr(expr2.terms[0])}")

expr3 = Expr("test([a,b,c])")
print(f"\nexpr3 predicate: {expr3.predicate}")
print(f"expr3 terms: {expr3.terms}")
print(f"expr3 terms[0]: {repr(expr3.terms[0])}")
