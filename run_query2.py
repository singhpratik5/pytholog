from pytholog import KnowledgeBase
from pytholog.expr import Expr

kb = KnowledgeBase('relations')
kb(["member(X, [X|_]).","member(X, [_|T]) :- member(X, T).","subset([], _).","subset([H|T], List) :- member(H, List), subset(T, List)."])
print('Query subset([a,c],[a,b,c]) ->', kb.query(Expr('subset([a,c], [a,b,c])')))
print('Query subset([a,d],[a,b,c]) ->', kb.query(Expr('subset([a,d], [a,b,c])')))
print('Query subset(X,[1,2]) ->', kb.query(Expr('subset(X, [1,2])')))
