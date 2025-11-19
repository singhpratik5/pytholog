import pytholog as pl

kb = pl.KnowledgeBase('relations')

kb([
    "member(X, [X|_]).",
    "member(X, [_|T]) :- member(X, T).",
    "subset([], _).",
    "subset([H|T], List) :- member(H, List), subset(T, List)."
])

print("--- Testing subset/member Bug ---")

print("\n Query 1: Is [a, c] a subset of [a, b, c]?")
print("Result:", kb.query(pl.Expr("subset([a,c], [a,b,c])")))

print("\n Query 2: Is [a, d] a subset of [a, b, c]?")
print("Result:", kb.query(pl.Expr("subset([a,d], [a,b,c])")))

print("\n Query 3: What are the subsets of [1, 2]?")
print("Result:", kb.query(pl.Expr("subset(X, [1,2])")))
