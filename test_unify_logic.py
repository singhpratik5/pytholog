from pytholog.util import parse_term, is_var_node

# Manually test the unification logic
pattern = parse_term("[_|_]", side="L")
concrete = parse_term("[a]", side="R")

print(f"Pattern: {pattern}")
print(f"Concrete: {concrete}")

# Simulate what _unify_nodes should do
def test_unify(a, b):
    print(f"\n--- Unifying {a} with {b}")
    
    # Check for list_pat vs list
    if a.get("type") == "list_pat" and b.get("type") == "list":
        print("  -> list_pat vs list detected")
        elems = b.get("elems", [])
        if len(elems) == 0:
            print("  -> Empty list, fail")
            return False
        head = elems[0]
        tail_list = {"type": "list", "elems": elems[1:]}
        print(f"  -> Extracted head: {head}")
        print(f"  -> Extracted tail: {tail_list}")
        a_head = a.get("head")
        a_tail = a.get("tail")
        print(f"  -> Unifying pattern head {a_head} with {head}")
        
        # Check if head is a var (anonymous)
        if is_var_node(a_head):
            print(f"    -> Head is var, should match")
        
        print(f"  -> Unifying pattern tail {a_tail} with {tail_list}")
        
        # Check if tail is a var (anonymous)
        if is_var_node(a_tail):
            print(f"    -> Tail is var, should match")
        
        return True
    
    return False

result = test_unify(pattern, concrete)
print(f"\nResult: {result}")
