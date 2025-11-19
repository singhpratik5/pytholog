from pytholog.unify import unify
from pytholog.fact import Fact
from pytholog.expr import Expr

f1 = Fact('subset([], _).')
f2 = Fact('subset([H|T], List) :- member(H, List), subset(T, List).')
q = Expr('subset([a,c], [a,b,c])')
print('f1.lh.terms=', f1.lh.terms)
print('f2.lh.terms=', f2.lh.terms)
print('q.terms=', q.terms)
print('unify f1 with q ->', unify(f1.lh, q, {}, {}))
print('unify f2 with q ->', unify(f2.lh, q, {}, {}))
