from pytholog import KnowledgeBase
from pytholog.expr import Expr
kb = KnowledgeBase('relations')
kb(["member(X, [X|_]).","member(X, [_|T]) :- member(X, T).","subset([], _).","subset([H|T], List) :- member(H, List), subset(T, List)."])
print('Querying subset([a,c],[a,b,c])')
print(kb.query(Expr('subset([a,c], [a,b,c])')))
