from pytholog import KnowledgeBase, Expr

kb = KnowledgeBase("test_arithmetic")
kb([
    "sum(X, Y, Z) :- Z is X + Y",
    "double(X, Y) :- Y is X * 2"
])

result = kb.query(Expr("sum(2, 3, Z)"))
print(f"sum(2, 3, Z) result: {result}")
print(f"Result type: {type(result)}")
if result and isinstance(result[0], dict):
    print(f"Z value: {result[0].get('Z')}, type: {type(result[0].get('Z'))}")

result2 = kb.query(Expr("double(5, Y)"))
print(f"\ndouble(5, Y) result: {result2}")
