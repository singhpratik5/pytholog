from pytholog import KnowledgeBase
from pytholog.expr import Expr

kb = KnowledgeBase('relations')
kb(["member(X, [X|_]).","member(X, [_|T]) :- member(X, T)."])
print('member(a,[a,b,c]) ->', kb.query(Expr('member(a, [a,b,c])')))
print('member(c,[a,b,c]) ->', kb.query(Expr('member(c, [a,b,c])')))
print('member(d,[a,b,c]) ->', kb.query(Expr('member(d, [a,b,c])')))
print('member(X,[1,2]) ->', kb.query(Expr('member(X, [1,2])')))
