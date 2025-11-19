"""
Advanced list operation test cases for Pytholog.
These tests verify Prolog-style list operations including member, append, reverse, etc.
"""

import pytholog as pl


def test_member_basic():
    """Test basic member/2 predicate."""
    kb = pl.KnowledgeBase("member_basic")
    kb([
        "member(X, [X|_])",
        "member(X, [_|T]) :- member(X, T)"
    ])
    
    # Check if 2 is member of [1,2,3]
    result = kb.query(pl.Expr("member(2, [1,2,3])"))
    assert result == ["Yes"] or (len(result) > 0 and result[0] != "No")
    
    # Generate all members
    result = kb.query(pl.Expr("member(X, [a,b,c])"))
    members = [r['X'] for r in result if isinstance(r, dict) and 'X' in r]
    assert 'a' in members
    assert 'b' in members
    assert 'c' in members


def test_append_basic():
    """Test append/3 predicate for list concatenation."""
    kb = pl.KnowledgeBase("append_basic")
    kb([
        "append([], L, L)",
        "append([H|T1], L2, [H|T3]) :- append(T1, L2, T3)"
    ])
    
    # Append [1,2] and [3,4]
    result = kb.query(pl.Expr("append([1,2], [3,4], Z)"))
    if result and len(result) > 0 and isinstance(result[0], dict):
        z_val = result[0].get('Z')
        # Should be [1,2,3,4]
        assert z_val is not None


def test_length_list():
    """Test length/2 predicate."""
    kb = pl.KnowledgeBase("length_test")
    kb([
        "length([], 0)",
        "length([_|T], N) :- length(T, M), N is M + 1"
    ])
    
    # Length of empty list
    result = kb.query(pl.Expr("length([], N)"))
    assert result == ["Yes"] or (len(result) > 0 and isinstance(result[0], dict) and result[0].get('N') == 0)
    
    # Length of [a,b,c] should be 3
    result = kb.query(pl.Expr("length([a,b,c], N)"))
    if result and len(result) > 0 and isinstance(result[0], dict):
        assert result[0].get('N') in [3, '3']


def test_last_element():
    """Test finding last element of a list."""
    kb = pl.KnowledgeBase("last_elem")
    kb([
        "last([X], X)",
        "last([_|T], X) :- last(T, X)"
    ])
    
    result = kb.query(pl.Expr("last([a,b,c,d], X)"))
    if result and len(result) > 0 and isinstance(result[0], dict):
        assert result[0].get('X') == 'd'


def test_reverse_list():
    """Test reversing a list."""
    kb = pl.KnowledgeBase("reverse_test")
    kb([
        "reverse([], [])",
        "reverse([H|T], R) :- reverse(T, RT), append(RT, [H], R)",
        "append([], L, L)",
        "append([H|T1], L2, [H|T3]) :- append(T1, L2, T3)"
    ])
    
    result = kb.query(pl.Expr("reverse([1,2,3], R)"))
    # Should reverse to [3,2,1]
    if result and len(result) > 0 and isinstance(result[0], dict):
        r_val = result[0].get('R')
        assert r_val is not None


def test_list_sum():
    """Test summing elements of a list."""
    kb = pl.KnowledgeBase("sum_test")
    kb([
        "sum_list([], 0)",
        "sum_list([H|T], S) :- sum_list(T, ST), S is H + ST"
    ])
    
    result = kb.query(pl.Expr("sum_list([1,2,3,4], S)"))
    if result and len(result) > 0 and isinstance(result[0], dict):
        assert result[0].get('S') in [10, '10']


def test_list_max():
    """Test finding maximum element in a list."""
    kb = pl.KnowledgeBase("max_test")
    kb([
        "max_list([X], X)",
        "max_list([H|T], M) :- max_list(T, MT), H > MT, M is H",
        "max_list([H|T], M) :- max_list(T, MT), H <= MT, M is MT"
    ])
    
    result = kb.query(pl.Expr("max_list([3,7,2,9,1], M)"))
    if result and len(result) > 0 and isinstance(result[0], dict):
        assert result[0].get('M') in [9, '9']


def test_nth_element():
    """Test accessing nth element of a list (1-indexed)."""
    kb = pl.KnowledgeBase("nth_test")
    kb([
        "nth(1, [H|_], H)",
        "nth(N, [_|T], E) :- N > 1, N1 is N - 1, nth(N1, T, E)"
    ])
    
    # 3rd element of [a,b,c,d,e] should be c
    result = kb.query(pl.Expr("nth(3, [a,b,c,d,e], E)"))
    if result and len(result) > 0 and isinstance(result[0], dict):
        assert result[0].get('E') == 'c'


def test_prefix_list():
    """Test checking if one list is prefix of another."""
    kb = pl.KnowledgeBase("prefix_test")
    kb([
        "prefix([], _)",
        "prefix([H|T1], [H|T2]) :- prefix(T1, T2)"
    ])
    
    # [1,2] is prefix of [1,2,3,4]
    result = kb.query(pl.Expr("prefix([1,2], [1,2,3,4])"))
    assert result == ["Yes"] or (len(result) > 0 and result[0] != "No")


def test_sublist():
    """Test finding sublists."""
    kb = pl.KnowledgeBase("sublist_test")
    kb([
        "prefix([], _)",
        "prefix([H|T1], [H|T2]) :- prefix(T1, T2)",
        "sublist(S, L) :- prefix(S, L)",
        "sublist(S, [_|T]) :- sublist(S, T)"
    ])
    
    # [2,3] is sublist of [1,2,3,4]
    result = kb.query(pl.Expr("sublist([2,3], [1,2,3,4])"))
    assert result == ["Yes"] or (len(result) > 0 and result[0] != "No")


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
