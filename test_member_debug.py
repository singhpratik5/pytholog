from pytholog import KnowledgeBase, Expr

kb = KnowledgeBase("test_member")
kb([
    "member(X, [X|_])",
    "member(X, [_|T]) :- member(X, T)"
])

# Test a simple case
print("Test: member(a, [a,b,c])")
result = kb.query(Expr("member(a, [a,b,c])"))
print(f"Result: {result}")
print(f"Expected: ['Yes']")
print()

print("Test: member(b, [a,b,c])")
result = kb.query(Expr("member(b, [a,b,c])"))
print(f"Result: {result}")
print(f"Expected: ['Yes']")
