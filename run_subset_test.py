import pytholog as pl
from pytholog import Expr

# Create a new knowledge base
kb = pl.KnowledgeBase('relations')

# Define the standard rules for member and subset
kb([
    "member(X, [X|_]).",
    "member(X, [_|T]) :- member(X, T).",
    "subset([], _).",
    "subset([H|T], List) :- member(H, List), subset(T, List)."
])

# Add a concrete fact to test simple fact lookup
kb(["member(a, [a,b,c])."]) 

print("--- Testing subset/member Bug ---")

# Test 1: A query that should succeed
print("\nQuery 1: Is [a, c] a subset of [a, b, c]?")
print("Result:", kb.query(Expr("subset([a,c], [a,b,c])")))

# Test 2: A query that should fail
print("\nQuery 2: Is [a, d] a subset of [a, b, c]?")
print("Result:", kb.query(Expr("subset([a,d], [a,b,c])")))

# Test 3: A generative query that should find all subsets
print("\nQuery 3: What are the subsets of [1, 2]?")
print("Result:", kb.query(Expr("subset(X, [1,2])")))

print("\nQuick checks for member predicate:")
print("member(a, [a,b,c]):", kb.query(Expr("member(a, [a,b,c])")))
print("member(X, [a,b,c]):", kb.query(Expr("member(X, [a,b,c])")))
