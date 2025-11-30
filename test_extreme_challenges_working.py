"""
WORKING EXTREME CHALLENGE TEST SUITE FOR PYTHOLOG
==================================================
Adapted to work within current Pytholog capabilities.
Tests that push the system while respecting current limitations.
"""

from pytholog import KnowledgeBase
from pytholog.expr import Expr

def run_test(kb, query, test_name, check_func=None):
    """Helper to run tests with formatted output"""
    print(f"\n{test_name}")
    print(f"     Query: {query}")
    try:
        result = kb.query(Expr(query))
        print(f"     Result: {result}")
        
        if check_func:
            if check_func(result):
                print("     [PASS]")
                return True
            else:
                print(f"     [FAIL]")
                return False
        else:
            # Just check it didn't return "No"
            if result != ["No"] and len(result) > 0:
                print("     [PASS]")
                return True
            else:
                print("     [FAIL] - Got No")
                return False
    except Exception as e:
        print(f"     [ERROR] {str(e)[:100]}")
        return False

def main():
    passed = 0
    total = 0
    
    print("\n" + "="*80)
    print("           WORKING EXTREME CHALLENGE TEST SUITE FOR PYTHOLOG")
    print("="*80)
    
    # ========================================================================
    # SECTION 1: MATHEMATICAL COMPUTATIONS
    # ========================================================================
    print("\n" + "="*80)
    print("                    SECTION 1: MATHEMATICS")
    print("="*80)
    
    kb = KnowledgeBase("math")
    kb([
        # Factorial
        "fact(0, 1)",
        "fact(N, F) :- N > 0, N1 is N - 1, fact(N1, F1), F is N * F1",
        
        # Fibonacci
        "fib(0, 0)",
        "fib(1, 1)",
        "fib(N, F) :- N > 1, N1 is N - 1, fib(N1, F1), N2 is N - 2, fib(N2, F2), F is F1 + F2",
        
        # Sum from 1 to N
        "sum_to(0, 0)",
        "sum_to(N, Sum) :- N > 0, N1 is N - 1, sum_to(N1, S1), Sum is S1 + N",
        
        # Power
        "power(_, 0, 1)",
        "power(X, N, P) :- N > 0, N1 is N - 1, power(X, N1, P1), P is X * P1",
        
        # Double factorial (product of even or odd numbers)
        "double_all(0, 0)",
        "double_all(N, D) :- N > 0, N1 is N - 1, double_all(N1, D1), D is N * 2",
        
        # Is even
        "is_even(0)",
        "is_even(N) :- N > 0, N1 is N - 2, is_even(N1)"
    ])
    
    total += 1
    if run_test(kb, "fact(5, F)", "TEST 1: Factorial of 5",
                lambda r: len(r) > 0 and isinstance(r[0], dict) and r[0].get('F') == 120):
        passed += 1
    
    total += 1
    if run_test(kb, "fib(6, F)", "TEST 2: 6th Fibonacci number",
                lambda r: len(r) > 0 and isinstance(r[0], dict) and r[0].get('F') == 8):
        passed += 1
    
    total += 1
    if run_test(kb, "sum_to(10, S)", "TEST 3: Sum 1+2+...+10",
                lambda r: len(r) > 0 and isinstance(r[0], dict) and r[0].get('S') == 55):
        passed += 1
    
    total += 1
    if run_test(kb, "power(2, 10, P)", "TEST 4: 2^10",
                lambda r: len(r) > 0 and isinstance(r[0], dict) and r[0].get('P') == 1024):
        passed += 1
    
    total += 1
    if run_test(kb, "is_even(8)", "TEST 5: Check if 8 is even"):
        passed += 1
    
    # ========================================================================
    # SECTION 2: LIST OPERATIONS
    # ========================================================================
    print("\n" + "="*80)
    print("                    SECTION 2: LIST OPERATIONS")
    print("="*80)
    
    kb2 = KnowledgeBase("lists")
    kb2([
        # Length
        "length([], 0)",
        "length([_|T], N) :- length(T, N1), N is N1 + 1",
        
        # Append
        "append([], L, L)",
        "append([H|T1], L2, [H|T3]) :- append(T1, L2, T3)",
        
        # Reverse with accumulator
        "reverse(L, R) :- rev_acc(L, [], R)",
        "rev_acc([], Acc, Acc)",
        "rev_acc([H|T], Acc, R) :- rev_acc(T, [H|Acc], R)",
        
        # Member
        "member(X, [X|_])",
        "member(X, [_|T]) :- member(X, T)",
        
        # Last element
        "last([X], X)",
        "last([_|T], X) :- last(T, X)",
        
        # Nth element (1-indexed)
        "nth(1, [H|_], H)",
        "nth(N, [_|T], E) :- N > 1, N1 is N - 1, nth(N1, T, E)",
        
        # Take first N elements
        "take(0, _, [])",
        "take(N, [H|T], [H|R]) :- N > 0, N1 is N - 1, take(N1, T, R)",
        
        # Sum of list elements
        "sum_list([], 0)",
        "sum_list([H|T], S) :- sum_list(T, S1), S is H + S1"
    ])
    
    total += 1
    if run_test(kb2, "length([a,b,c,d,e], N)", "TEST 6: Length of 5-element list",
                lambda r: len(r) > 0 and isinstance(r[0], dict) and r[0].get('N') == 5):
        passed += 1
    
    total += 1
    if run_test(kb2, "append([1,2], [3,4], L)", "TEST 7: Append two lists"):
        passed += 1
    
    total += 1
    if run_test(kb2, "reverse([1,2,3,4], R)", "TEST 8: Reverse a list"):
        passed += 1
    
    total += 1
    if run_test(kb2, "member(3, [1,2,3,4])", "TEST 9: Check membership"):
        passed += 1
    
    total += 1
    if run_test(kb2, "last([a,b,c,d], X)", "TEST 10: Find last element",
                lambda r: len(r) > 0 and isinstance(r[0], dict) and r[0].get('X') == 'd'):
        passed += 1
    
    total += 1
    if run_test(kb2, "nth(3, [a,b,c,d,e], E)", "TEST 11: Get 3rd element",
                lambda r: len(r) > 0 and isinstance(r[0], dict) and r[0].get('E') == 'c'):
        passed += 1
    
    total += 1
    if run_test(kb2, "take(3, [1,2,3,4,5], L)", "TEST 12: Take first 3 elements"):
        passed += 1
    
    total += 1
    if run_test(kb2, "sum_list([1,2,3,4,5], S)", "TEST 13: Sum list elements",
                lambda r: len(r) > 0 and isinstance(r[0], dict) and r[0].get('S') == 15):
        passed += 1
    
    # ========================================================================
    # SECTION 3: GRAPH ALGORITHMS  
    # ========================================================================
    print("\n" + "="*80)
    print("                    SECTION 3: GRAPH ALGORITHMS")
    print("="*80)
    
    kb3 = KnowledgeBase("graphs")
    kb3([
        # Graph edges
        "edge(a, b)",
        "edge(b, c)",
        "edge(c, d)",
        "edge(a, e)",
        "edge(e, f)",
        "edge(b, f)",
        
        # Path finding
        "path(X, Y) :- edge(X, Y)",
        "path(X, Y) :- edge(X, Z), path(Z, Y)",
        
        # Reachable
        "reachable(X, X)",
        "reachable(X, Y) :- edge(X, Z), reachable(Z, Y)"
    ])
    
    total += 1
    if run_test(kb3, "path(a, d)", "TEST 14: Find if path exists from a to d"):
        passed += 1
    
    total += 1
    if run_test(kb3, "reachable(a, f)", "TEST 15: Check if f reachable from a"):
        passed += 1
    
    # ========================================================================
    # SECTION 4: BACKTRACKING & SEARCH
    # ========================================================================
    print("\n" + "="*80)
    print("                    SECTION 4: BACKTRACKING & SEARCH")
    print("="*80)
    
    kb4 = KnowledgeBase("backtrack")
    kb4([
        # All solutions
        "color(red)",
        "color(green)",
        "color(blue)",
        
        # Generate pairs
        "pair(X, Y) :- color(X), color(Y)",
        
        # Family relations
        "parent(tom, bob)",
        "parent(tom, liz)",
        "parent(bob, ann)",
        "parent(bob, pat)",
        "parent(pat, jim)",
        
        # Ancestor
        "ancestor(X, Y) :- parent(X, Y)",
        "ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y)"
    ])
    
    total += 1
    if run_test(kb4, "color(X)", "TEST 16: Generate all colors",
                lambda r: len(r) == 3):
        passed += 1
    
    total += 1
    if run_test(kb4, "ancestor(tom, X)", "TEST 17: Find all descendants of tom",
                lambda r: len(r) >= 4):  # bob, liz, ann, pat, jim
        passed += 1
    
    # ========================================================================
    # SECTION 5: RECURSION DEPTH
    # ========================================================================
    print("\n" + "="*80)
    print("                    SECTION 5: DEEP RECURSION")
    print("="*80)
    
    kb5 = KnowledgeBase("deep")
    kb5([
        # Count down
        "countdown(0, [0])",
        "countdown(N, [N|Rest]) :- N > 0, N1 is N - 1, countdown(N1, Rest)",
        
        # Repeat element N times
        "repeat(_, 0, [])",
        "repeat(X, N, [X|Rest]) :- N > 0, N1 is N - 1, repeat(X, N1, Rest)"
    ])
    
    total += 1
    if run_test(kb5, "countdown(10, L)", "TEST 18: Generate list [10,9,...,0]"):
        passed += 1
    
    total += 1
    if run_test(kb5, "repeat(a, 5, L)", "TEST 19: Repeat element 5 times"):
        passed += 1
    
    # ========================================================================
    # SECTION 6: SORTING & ORDERING
    # ========================================================================
    print("\n" + "="*80)
    print("                    SECTION 6: SORTING & ORDERING")
    print("="*80)
    
    kb6 = KnowledgeBase("sort")
    kb6([
        # Min of two numbers
        "min(X, Y, X) :- X < Y",
        "min(X, Y, Y) :- X >= Y",
        
        # Max of two numbers
        "max(X, Y, X) :- X > Y",
        "max(X, Y, Y) :- X <= Y",
        
        # Partition list around pivot
        "partition([], _, [], [])",
        "partition([H|T], P, [H|Less], Greater) :- H < P, partition(T, P, Less, Greater)",
        "partition([H|T], P, Less, [H|Greater]) :- H >= P, partition(T, P, Less, Greater)"
    ])
    
    total += 1
    if run_test(kb6, "min(5, 3, M)", "TEST 20: Minimum of 5 and 3",
                lambda r: len(r) > 0 and isinstance(r[0], dict) and r[0].get('M') == 3):
        passed += 1
    
    total += 1
    if run_test(kb6, "max(5, 3, M)", "TEST 21: Maximum of 5 and 3",
                lambda r: len(r) > 0 and isinstance(r[0], dict) and r[0].get('M') == 5):
        passed += 1
    
    total += 1
    if run_test(kb6, "partition([3,1,4,2,5], 3, Less, Greater)", "TEST 22: Partition around pivot 3"):
        passed += 1
    
    # ========================================================================
    # FINAL RESULTS
    # ========================================================================
    print("\n" + "="*80)
    print(f"                FINAL RESULTS: {passed}/{total} tests passed ({100*passed//total}%)")
    print("="*80)
    
    if passed == total:
        print("\n[PERFECT] All tests passed!")
    elif passed >= total * 0.9:
        print(f"\n[EXCELLENT] {passed} out of {total} tests passed.")
    elif passed >= total * 0.7:
        print(f"\n[GOOD] {passed} out of {total} tests passed.")
    else:
        print(f"\n[NEEDS WORK] {passed} out of {total} tests passed.")
    
    return passed, total

if __name__ == "__main__":
    main()
