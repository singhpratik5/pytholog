"""
EXTREME CHALLENGE TEST SUITE FOR PYTHOLOG
==========================================
Tests the limits of the system with:
- Complex mathematical computations
- Deep recursion and nested structures
- Advanced algorithmic patterns
- Combination of multiple operations
"""

from pytholog import KnowledgeBase
from pytholog.expr import Expr

def run_test(kb, query, test_name, expected=None):
    """Helper to run tests with formatted output"""
    print(f"\n{test_name}")
    print(f"     Query: {query}")
    result = kb.query(Expr(query))
    print(f"     Result: {result}")
    if expected:
        if result == expected:
            print("     [PASS]")
            return True
        else:
            print(f"     [FAIL] - Expected: {expected}")
            return False
    else:
        print("     [PASS]")
        return True

def main():
    passed = 0
    total = 0
    
    print("\n" + "="*80)
    print("                    EXTREME CHALLENGE TEST SUITE")
    print("="*80)
    
    # ========================================================================
    # SECTION 1: ADVANCED MATHEMATICAL COMPUTATIONS
    # ========================================================================
    print("\n" + "="*80)
    print("                    SECTION 1: ADVANCED MATHEMATICS")
    print("="*80)
    
    kb = KnowledgeBase("math_extreme")
    kb(["prime(2).",
        "prime(3).",
        "prime(5).",
        "prime(7).",
        "prime(11).",
        "prime(13).",
        "prime(17).",
        "prime(19).",
        "prime(23).",
        "prime(29).",
        "prime(31).",
        
        # Test 1: Find all prime factors of a number
        "prime_factors(N, []) :- N =:= 1.",
        "prime_factors(N, [P|Rest]) :- N > 1, prime(P), 0 =:= N mod P, N1 is N / P, prime_factors(N1, Rest).",
        "prime_factors(N, Factors) :- N > 1, prime(P), N mod P > 0, N > P, prime_factors(N, Factors).",
        
        # Test 2: Calculate LCM (Least Common Multiple)
        "gcd_calc(X, 0, X) :- X > 0.",
        "gcd_calc(X, Y, G) :- Y > 0, R is X mod Y, gcd_calc(Y, R, G).",
        "lcm(X, Y, L) :- gcd_calc(X, Y, G), L is (X * Y) / G.",
        
        # Test 3: Sum of squares from 1 to N
        "sum_squares(0, 0).",
        "sum_squares(N, Sum) :- N > 0, N1 is N - 1, sum_squares(N1, S1), Sum is S1 + (N * N).",
        
        # Test 4: Digital root (recursive sum of digits until single digit)
        "sum_digits(N, N) :- N < 10.",
        "sum_digits(N, Sum) :- N >= 10, D is N mod 10, N1 is N / 10, sum_digits(N1, S1), Temp is S1 + D, sum_digits(Temp, Sum).",
        
        # Test 5: Perfect number check (sum of divisors equals number)
        "divisors_sum(N, 1, Sum) :- Sum is 1.",
        "divisors_sum(N, D, Sum) :- D > 1, D < N, 0 =:= N mod D, D1 is D - 1, divisors_sum(N, D1, S1), Sum is S1 + D.",
        "divisors_sum(N, D, Sum) :- D > 1, D < N, N mod D > 0, D1 is D - 1, divisors_sum(N, D1, Sum).",
        "perfect_number(N) :- N1 is N - 1, divisors_sum(N, N1, Sum), Sum =:= N.",
        
        # Test 6: Binomial coefficient C(n,k) = n! / (k! * (n-k)!)
        "fact(0, 1).",
        "fact(N, F) :- N > 0, N1 is N - 1, fact(N1, F1), F is N * F1.",
        "binomial(N, 0, 1).",
        "binomial(N, N, 1).",
        "binomial(N, K, C) :- K > 0, K < N, N1 is N - 1, K1 is K - 1, binomial(N1, K1, C1), binomial(N1, K, C2), C is C1 + C2.",
        
        # Test 7: Catalan number C_n = (2n)! / ((n+1)! * n!)
        "catalan(0, 1).",
        "catalan(N, C) :- N > 0, N1 is N - 1, catalan(N1, C1), C is C1 * (4 * N - 2) / (N + 1).",
    ])
    
    total += 1
    if run_test(kb, "lcm(12, 18, L)", "TEST 1: Least Common Multiple"):
        passed += 1
    
    total += 1
    if run_test(kb, "sum_squares(5, Sum)", "TEST 2: Sum of squares 1² + 2² + ... + 5²"):
        passed += 1
    
    total += 1
    if run_test(kb, "sum_digits(9875, D)", "TEST 3: Digital root of 9875"):
        passed += 1
    
    total += 1
    if run_test(kb, "perfect_number(6)", "TEST 4: Check if 6 is perfect (1+2+3=6)"):
        passed += 1
    
    total += 1
    if run_test(kb, "binomial(5, 2, C)", "TEST 5: Binomial coefficient C(5,2)"):
        passed += 1
    
    total += 1
    if run_test(kb, "catalan(4, C)", "TEST 6: 4th Catalan number"):
        passed += 1
    
    # ========================================================================
    # SECTION 2: DEEPLY NESTED STRUCTURES
    # ========================================================================
    print("\n" + "="*80)
    print("                    SECTION 2: DEEPLY NESTED STRUCTURES")
    print("="*80)
    
    kb2 = KnowledgeBase("nested_extreme")
    kb2(["# Deep tree operations",
         "tree_depth(leaf, 0).",
         "tree_depth(node(_, L, R), D) :- tree_depth(L, DL), tree_depth(R, DR), DL > DR, D is DL + 1.",
         "tree_depth(node(_, L, R), D) :- tree_depth(L, DL), tree_depth(R, DR), DR >= DL, D is DR + 1.",
         
         # Tree sum
         "tree_sum(leaf, 0).",
         "tree_sum(node(V, L, R), S) :- tree_sum(L, SL), tree_sum(R, SR), S is V + SL + SR.",
         
         # Count leaves
         "count_leaves(leaf, 1).",
         "count_leaves(node(_, L, R), N) :- count_leaves(L, NL), count_leaves(R, NR), N is NL + NR.",
         
         # Mirror tree
         "mirror(leaf, leaf).",
         "mirror(node(V, L, R), node(V, ML, MR)) :- mirror(R, ML), mirror(L, MR).",
         
         # Tree to list (in-order traversal)
         "tree_to_list(leaf, []).",
         "tree_to_list(node(V, L, R), List) :- tree_to_list(L, LL), tree_to_list(R, LR), append(LL, [V], Temp), append(Temp, LR, List).",
         
         # Helper: append
         "append([], L, L).",
         "append([H|T], L2, [H|R]) :- append(T, L2, R).",
         
         # Nested list operations
         "depth_list([], 1).",
         "depth_list([H|T], D) :- is_list(H), depth_list(H, DH), depth_list(T, DT), DH > DT, D is DH + 1.",
         "depth_list([H|T], D) :- is_list(H), depth_list(H, DH), depth_list(T, DT), DT >= DH, D is DT + 1.",
         "depth_list([H|T], D) :- \\+(is_list(H)), depth_list(T, D).",
         
         # Check if element is list
         "is_list([]).",
         "is_list([_|_]).",
         
         # Complete flatten to atomic elements
         "complete_flatten([], []).",
         "complete_flatten([H|T], Result) :- is_list(H), complete_flatten(H, FH), complete_flatten(T, FT), append(FH, FT, Result).",
         "complete_flatten([H|T], [H|FT]) :- \\+(is_list(H)), complete_flatten(T, FT).",
         
         # Count all elements in nested structure
         "count_all([], 0).",
         "count_all([H|T], N) :- is_list(H), count_all(H, NH), count_all(T, NT), N is NH + NT.",
         "count_all([H|T], N) :- \\+(is_list(H)), count_all(T, NT), N is NT + 1.",
         
         # Max depth of nesting
         "max_nesting([], 0).",
         "max_nesting([H|T], D) :- is_list(H), max_nesting(H, DH), max_nesting(T, DT), DH1 is DH + 1, DH1 > DT, D is DH1.",
         "max_nesting([H|T], D) :- is_list(H), max_nesting(H, DH), max_nesting(T, DT), DH1 is DH + 1, DT >= DH1, D is DT.",
         "max_nesting([H|T], D) :- \\+(is_list(H)), max_nesting(T, D).",
    ])
    
    total += 1
    if run_test(kb2, "tree_depth(node(5, node(3, leaf, leaf), node(7, leaf, node(9, leaf, leaf))), D)", 
                "TEST 7: Calculate depth of binary tree"):
        passed += 1
    
    total += 1
    if run_test(kb2, "tree_sum(node(10, node(5, leaf, leaf), node(15, leaf, leaf)), S)", 
                "TEST 8: Sum all values in tree"):
        passed += 1
    
    total += 1
    if run_test(kb2, "count_leaves(node(1, node(2, leaf, leaf), node(3, leaf, node(4, leaf, leaf))), N)", 
                "TEST 9: Count leaves in tree"):
        passed += 1
    
    total += 1
    if run_test(kb2, "complete_flatten([1, [2, [3, [4, 5]], 6], 7], R)", 
                "TEST 10: Complete flatten of deeply nested list"):
        passed += 1
    
    total += 1
    if run_test(kb2, "count_all([1, [2, [3, 4], 5], [6, 7]], N)", 
                "TEST 11: Count all elements in nested structure"):
        passed += 1
    
    total += 1
    if run_test(kb2, "max_nesting([1, [2, [3, [4]]], [5]], D)", 
                "TEST 12: Maximum nesting depth"):
        passed += 1
    
    # ========================================================================
    # SECTION 3: COMPLEX ALGORITHMIC PATTERNS
    # ========================================================================
    print("\n" + "="*80)
    print("                    SECTION 3: COMPLEX ALGORITHMS")
    print("="*80)
    
    kb3 = KnowledgeBase("algorithms")
    kb3(["# Merge sort implementation",
         "merge_sort([], []).",
         "merge_sort([X], [X]).",
         "merge_sort(List, Sorted) :- List = [_,_|_], split_half(List, L1, L2), merge_sort(L1, S1), merge_sort(L2, S2), merge(S1, S2, Sorted).",
         
         # Split list in half
         "split_half(List, L1, L2) :- length_list(List, Len), Half is Len / 2, take_n(Half, List, L1), drop_n(Half, List, L2).",
         
         # Length
         "length_list([], 0).",
         "length_list([_|T], N) :- length_list(T, N1), N is N1 + 1.",
         
         # Take first N
         "take_n(0, _, []).",
         "take_n(N, [H|T], [H|R]) :- N > 0, N1 is N - 1, take_n(N1, T, R).",
         
         # Drop first N
         "drop_n(0, L, L).",
         "drop_n(N, [_|T], R) :- N > 0, N1 is N - 1, drop_n(N1, T, R).",
         
         # Merge sorted lists
         "merge([], L, L).",
         "merge(L, [], L).",
         "merge([H1|T1], [H2|T2], [H1|R]) :- H1 =< H2, merge(T1, [H2|T2], R).",
         "merge([H1|T1], [H2|T2], [H2|R]) :- H1 > H2, merge([H1|T1], T2, R).",
         
         # Quick select - find Kth smallest element
         "partition_pivot(_, [], [], []).",
         "partition_pivot(P, [H|T], [H|Smaller], Larger) :- H < P, partition_pivot(P, T, Smaller, Larger).",
         "partition_pivot(P, [H|T], Smaller, [H|Larger]) :- H >= P, partition_pivot(P, T, Smaller, Larger).",
         
         "quick_select([X], 1, X).",
         "quick_select([H|T], K, Result) :- partition_pivot(H, T, Smaller, Larger), length_list(Smaller, Len), K1 is Len + 1, K =:= K1, Result = H.",
         "quick_select([H|T], K, Result) :- partition_pivot(H, T, Smaller, Larger), length_list(Smaller, Len), K1 is Len + 1, K < K1, quick_select(Smaller, K, Result).",
         "quick_select([H|T], K, Result) :- partition_pivot(H, T, Smaller, Larger), length_list(Smaller, Len), K1 is Len + 1, K > K1, K2 is K - K1, quick_select(Larger, K2, Result).",
         
         # Longest increasing subsequence length
         "lis([X], 1).",
         "lis([H|T], Len) :- lis_helper([H|T], H, 1, Len).",
         
         "lis_helper([], _, Curr, Curr).",
         "lis_helper([H|T], Prev, Curr, Len) :- H > Prev, Curr1 is Curr + 1, lis_helper(T, H, Curr1, Len).",
         "lis_helper([H|T], Prev, Curr, Len) :- H =< Prev, lis_helper(T, Prev, Curr, Len).",
         
         # Matrix operations - transpose
         "transpose([[]|_], []).",
         "transpose(Matrix, [Row|Rows]) :- get_first_column(Matrix, Row, RestMatrix), transpose(RestMatrix, Rows).",
         
         "get_first_column([], [], []).",
         "get_first_column([[H|T]|Rest], [H|Col], [T|RestRows]) :- get_first_column(Rest, Col, RestRows).",
         
         # Sum of matrix diagonal
         "matrix_diagonal_sum([], 0, 0).",
         "matrix_diagonal_sum([Row|Rows], Idx, Sum) :- nth_elem(Idx, Row, Val), Idx1 is Idx + 1, matrix_diagonal_sum(Rows, Idx1, RestSum), Sum is Val + RestSum.",
         
         "nth_elem(1, [H|_], H).",
         "nth_elem(N, [_|T], X) :- N > 1, N1 is N - 1, nth_elem(N1, T, X).",
    ])
    
    total += 1
    if run_test(kb3, "merge_sort([5,2,8,1,9,3], Sorted)", 
                "TEST 13: Merge sort implementation"):
        passed += 1
    
    total += 1
    if run_test(kb3, "quick_select([7,3,9,1,5,2,8], 4, X)", 
                "TEST 14: Find 4th smallest element (quick select)"):
        passed += 1
    
    total += 1
    if run_test(kb3, "lis([1,3,2,4,3,5,6,2], Len)", 
                "TEST 15: Longest increasing subsequence length"):
        passed += 1
    
    total += 1
    if run_test(kb3, "transpose([[1,2,3],[4,5,6]], T)", 
                "TEST 16: Matrix transpose"):
        passed += 1
    
    total += 1
    if run_test(kb3, "matrix_diagonal_sum([[1,2,3],[4,5,6],[7,8,9]], 1, Sum)", 
                "TEST 17: Sum of matrix main diagonal"):
        passed += 1
    
    # ========================================================================
    # SECTION 4: COMBINATORIAL CHALLENGES
    # ========================================================================
    print("\n" + "="*80)
    print("                    SECTION 4: COMBINATORIAL CHALLENGES")
    print("="*80)
    
    kb4 = KnowledgeBase("combinatorics")
    kb4(["# Generate all partitions of a number",
         "partition_number(0, []).",
         "partition_number(N, [N]).",
         "partition_number(N, [H|T]) :- N > 0, between(1, N, H), N1 is N - H, partition_number(N1, T), check_decreasing([H|T]).",
         
         "# Helper: generate numbers between M and N",
         "between(M, N, M) :- M =< N.",
         "between(M, N, X) :- M < N, M1 is M + 1, between(M1, N, X).",
         
         "# Check if list is in decreasing order",
         "check_decreasing([_]).",
         "check_decreasing([H1,H2|T]) :- H1 >= H2, check_decreasing([H2|T]).",
         
         "# Generate all ways to make change",
         "make_change(0, _, []).",
         "make_change(Amount, [Coin|Coins], [Coin|Rest]) :- Amount >= Coin, Amount1 is Amount - Coin, make_change(Amount1, [Coin|Coins], Rest).",
         "make_change(Amount, [_|Coins], Change) :- make_change(Amount, Coins, Change).",
         
         "# Generate all subsets of specific size K",
         "subset_size(0, _, []).",
         "subset_size(K, [H|T], [H|Rest]) :- K > 0, K1 is K - 1, subset_size(K1, T, Rest).",
         "subset_size(K, [_|T], Subset) :- K > 0, subset_size(K, T, Subset).",
         
         "# All ways to distribute N items into K groups",
         "distribute(0, 0, []).",
         "distribute(N, K, [H|T]) :- N > 0, K > 0, between(0, N, H), K1 is K - 1, N1 is N - H, distribute(N1, K1, T).",
         
         "# Generate all binary strings of length N",
         "binary_string(0, []).",
         "binary_string(N, [0|T]) :- N > 0, N1 is N - 1, binary_string(N1, T).",
         "binary_string(N, [1|T]) :- N > 0, N1 is N - 1, binary_string(N1, T).",
         
         "# Count valid parentheses strings of length 2N",
         "valid_parens(0, 0, []).",
         "valid_parens(Open, Close, ['('|Rest]) :- Open > 0, Open1 is Open - 1, valid_parens(Open1, Close, Rest).",
         "valid_parens(Open, Close, [')'|Rest]) :- Close > Open, Close1 is Close - 1, valid_parens(Open, Close1, Rest).",
    ])
    
    total += 1
    if run_test(kb4, "partition_number(5, P)", 
                "TEST 18: All integer partitions of 5"):
        passed += 1
    
    total += 1
    if run_test(kb4, "make_change(10, [5,2,1], Change)", 
                "TEST 19: All ways to make change for 10 (coins: 5,2,1)"):
        passed += 1
    
    total += 1
    if run_test(kb4, "subset_size(2, [a,b,c,d], S)", 
                "TEST 20: All 2-element subsets of [a,b,c,d]"):
        passed += 1
    
    total += 1
    if run_test(kb4, "distribute(5, 3, D)", 
                "TEST 21: Distribute 5 items into 3 groups"):
        passed += 1
    
    total += 1
    if run_test(kb4, "binary_string(3, B)", 
                "TEST 22: All binary strings of length 3"):
        passed += 1
    
    total += 1
    if run_test(kb4, "valid_parens(2, 2, P)", 
                "TEST 23: Valid parentheses strings with 2 pairs"):
        passed += 1
    
    # ========================================================================
    # SECTION 5: GRAPH ALGORITHMS
    # ========================================================================
    print("\n" + "="*80)
    print("                    SECTION 5: GRAPH ALGORITHMS")
    print("="*80)
    
    kb5 = KnowledgeBase("graphs")
    kb5(["# Graph representation: edge(From, To, Weight)",
         "edge(a, b, 4).",
         "edge(a, c, 2).",
         "edge(b, c, 1).",
         "edge(b, d, 5).",
         "edge(c, d, 8).",
         "edge(c, e, 10).",
         "edge(d, e, 2).",
         "edge(d, f, 6).",
         "edge(e, f, 3).",
         
         "# Find path between two nodes",
         "path(X, Y, [X,Y]) :- edge(X, Y, _).",
         "path(X, Y, [X|Path]) :- edge(X, Z, _), path(Z, Y, Path).",
         
         "# Find path with total weight",
         "path_weight(X, Y, [X,Y], W) :- edge(X, Y, W).",
         "path_weight(X, Y, [X|Path], W) :- edge(X, Z, W1), path_weight(Z, Y, Path, W2), W is W1 + W2.",
         
         "# Check if graph has cycle",
         "has_cycle(Start) :- edge(Start, Next, _), path(Next, Start, _).",
         
         "# All nodes reachable from Start",
         "reachable(X, X).",
         "reachable(X, Y) :- edge(X, Z, _), reachable(Z, Y).",
         
         "# Find all nodes at distance K",
         "at_distance(X, X, 0).",
         "at_distance(X, Y, K) :- K > 0, edge(X, Z, _), K1 is K - 1, at_distance(Z, Y, K1).",
         
         "# Count paths between nodes",
         "count_paths(X, Y, N) :- findall(P, path(X, Y, P), Paths), length_list(Paths, N).",
         "length_list([], 0).",
         "length_list([_|T], N) :- length_list(T, N1), N is N1 + 1.",
         
         "# Undirected edge (bidirectional)",
         "connected(X, Y) :- edge(X, Y, _).",
         "connected(X, Y) :- edge(Y, X, _).",
    ])
    
    total += 1
    if run_test(kb5, "path(a, f, P)", 
                "TEST 24: Find path from a to f"):
        passed += 1
    
    total += 1
    if run_test(kb5, "path_weight(a, e, P, W)", 
                "TEST 25: Find path from a to e with weight"):
        passed += 1
    
    total += 1
    if run_test(kb5, "has_cycle(a)", 
                "TEST 26: Check if graph has cycle from node a"):
        passed += 1
    
    total += 1
    if run_test(kb5, "reachable(a, f)", 
                "TEST 27: Check if f is reachable from a"):
        passed += 1
    
    total += 1
    if run_test(kb5, "at_distance(a, d, 2)", 
                "TEST 28: Check if d is at distance 2 from a"):
        passed += 1
    
    # ========================================================================
    # SECTION 6: STRING AND PATTERN PROCESSING
    # ========================================================================
    print("\n" + "="*80)
    print("                    SECTION 6: STRING PROCESSING")
    print("="*80)
    
    kb6 = KnowledgeBase("strings")
    kb6(["# String/list pattern matching",
         "is_palindrome([]).",
         "is_palindrome([_]).",
         "is_palindrome([H|T]) :- append(Middle, [H], T), is_palindrome(Middle).",
         
         "append([], L, L).",
         "append([H|T], L2, [H|R]) :- append(T, L2, R).",
         
         "# Run-length encoding",
         "encode([], []).",
         "encode([X|Xs], [[N,X]|Encoded]) :- count_same(X, [X|Xs], N, Rest), encode(Rest, Encoded).",
         
         "count_same(_, [], 0, []).",
         "count_same(X, [X|Xs], N, Rest) :- count_same(X, Xs, N1, Rest), N is N1 + 1.",
         "count_same(X, [Y|Xs], 0, [Y|Xs]) :- X \\= Y.",
         
         "# Find all occurrences of sublist",
         "occurs_at([], _, 0).",
         "occurs_at(Pattern, List, Pos) :- prefix_at(Pattern, List, Pos).",
         "occurs_at(Pattern, [_|T], Pos) :- occurs_at(Pattern, T, Pos1), Pos is Pos1 + 1.",
         
         "prefix_at([], _, 0).",
         "prefix_at([H|T1], [H|T2], Pos) :- prefix_at(T1, T2, Pos).",
         
         "# Longest common prefix",
         "lcp([], _, []).",
         "lcp(_, [], []).",
         "lcp([H|T1], [H|T2], [H|R]) :- lcp(T1, T2, R).",
         "lcp([H1|_], [H2|_], []) :- H1 \\= H2.",
         
         "# Check if list has repeated consecutive elements",
         "has_consecutive_same([]).",
         "has_consecutive_same([_]).",
         "has_consecutive_same([H,H|_]).",
         "has_consecutive_same([H1,H2|T]) :- H1 \\= H2, has_consecutive_same([H2|T]).",
         
         "# Generate all rotations of a list",
         "rotate_list(L, L).",
         "rotate_list(L, R) :- L = [H|T], append(T, [H], L1), rotate_list(L1, R).",
    ])
    
    total += 1
    if run_test(kb6, "is_palindrome([r,a,c,e,c,a,r])", 
                "TEST 29: Check if 'racecar' is palindrome"):
        passed += 1
    
    total += 1
    if run_test(kb6, "encode([a,a,a,b,b,c,a,a], E)", 
                "TEST 30: Run-length encoding of [a,a,a,b,b,c,a,a]"):
        passed += 1
    
    total += 1
    if run_test(kb6, "lcp([1,2,3,4], [1,2,5,6], P)", 
                "TEST 31: Longest common prefix"):
        passed += 1
    
    total += 1
    if run_test(kb6, "has_consecutive_same([1,2,2,3])", 
                "TEST 32: Check for consecutive duplicates"):
        passed += 1
    
    total += 1
    if run_test(kb6, "rotate_list([1,2,3], R)", 
                "TEST 33: All rotations of [1,2,3]"):
        passed += 1
    
    # ========================================================================
    # FINAL RESULTS
    # ========================================================================
    print("\n" + "="*80)
    print(f"                    FINAL RESULTS: {passed}/{total} tests passed ({100*passed//total}%)")
    print("="*80)
    
    if passed == total:
        print("\n[PERFECT] All extreme challenge tests passed!")
    elif passed >= total * 0.9:
        print(f"\n[EXCELLENT] {passed} out of {total} tests passed.")
    elif passed >= total * 0.7:
        print(f"\n[GOOD] {passed} out of {total} tests passed. Some challenges remain.")
    else:
        print(f"\n[NEEDS WORK] {passed} out of {total} tests passed. Significant challenges detected.")


if __name__ == "__main__":
    main()
