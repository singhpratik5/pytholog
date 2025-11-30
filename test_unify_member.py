from pytholog.fact import Fact
from pytholog.expr import Expr
from pytholog.unify import unify

lh = Fact('member(X,[X|_])').lh
rh = Expr('member(a,[a,b,c])')
ld = {}
rd = {}
print('lh:', lh.to_string(), 'lh.terms=', lh.terms)
print('rh:', rh.to_string(), 'rh.terms=', rh.terms)
print('unify result =', unify(lh, rh, ld, rd))
print('ld after unify =', ld)
print('rd after unify =', rd)
