from pytholog import KnowledgeBase, Expr

kb = KnowledgeBase("test_unify")
kb([
    "same(X, X)",
    "first([H|_], H)",
    "second([_,X|_], X)",
    "pair(X, Y, [X,Y])"
])

print("Test: same(a, a)")
print(f"Result: {kb.query(Expr('same(a, a)'))}\n")

print("Test: same(X, hello)")
print(f"Result: {kb.query(Expr('same(X, hello)'))}\n")

print("Test: first([a,b,c], X)")
print(f"Result: {kb.query(Expr('first([a,b,c], X)'))}\n")

print("Test: second([a,b,c], X)")
print(f"Result: {kb.query(Expr('second([a,b,c], X)'))}\n")

print("Test: pair(1, 2, X)")
print(f"Result: {kb.query(Expr('pair(1, 2, X)'))}\n")

# Debug: check how the fact is stored
print("Facts in DB:")
for pred in kb.db:
    print(f"  {pred}: {kb.db[pred]['facts']}")
