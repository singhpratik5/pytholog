from pytholog import KnowledgeBase, Expr

# Test the most basic case
kb = KnowledgeBase("test")
kb(["empty([])"])

result = kb.query(Expr("empty([])"))
print(f"empty([]) → {result}")

kb2 = KnowledgeBase("test2") 
kb2(["nonempty([_|_])"])

result = kb2.query(Expr("nonempty([a])"))
print(f"nonempty([a]) → {result}")

result = kb2.query(Expr("nonempty([])"))
print(f"nonempty([]) → {result}")
