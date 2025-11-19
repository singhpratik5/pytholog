"""
Complex backtracking test cases for Pytholog.
These tests verify that the library correctly implements Prolog-style backtracking
for queries with multiple solutions.
"""

import pytholog as pl


def test_simple_choice_point():
    """Test basic backtracking with multiple facts."""
    kb = pl.KnowledgeBase("choice")
    kb([
        "color(red)",
        "color(green)",
        "color(blue)"
    ])
    
    result = kb.query(pl.Expr("color(X)"))
    # Should find all three colors
    assert len(result) == 3
    colors = {r['X'] for r in result if isinstance(r, dict)}
    assert colors == {'red', 'green', 'blue'}


def test_multiple_rules_same_predicate():
    """Test backtracking with multiple rule definitions for same predicate."""
    kb = pl.KnowledgeBase("multi_rule")
    kb([
        "parent(tom, bob)",
        "parent(tom, liz)",
        "parent(bob, ann)",
        "parent(bob, pat)",
        "parent(pat, jim)",
        "ancestor(X, Y) :- parent(X, Y)",
        "ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y)"
    ])
    
    # tom is ancestor of bob, liz, ann, pat, jim
    result = kb.query(pl.Expr("ancestor(tom, X)"))
    descendants = {r['X'] for r in result if isinstance(r, dict)}
    assert 'bob' in descendants
    assert 'liz' in descendants
    assert 'ann' in descendants
    assert 'pat' in descendants
    assert 'jim' in descendants


def test_symmetric_relation():
    """Test backtracking with symmetric relations (like friends)."""
    kb = pl.KnowledgeBase("symmetric")
    kb([
        "friend(alice, bob)",
        "friend(bob, charlie)",
        "friend(charlie, dave)",
        "friends(X, Y) :- friend(X, Y)",
        "friends(X, Y) :- friend(Y, X)"
    ])
    
    # alice is friends with bob (both directions)
    result = kb.query(pl.Expr("friends(alice, X)"))
    friends_of_alice = {r['X'] for r in result if isinstance(r, dict)}
    assert 'bob' in friends_of_alice
    
    # bob is friends with alice and charlie
    result = kb.query(pl.Expr("friends(bob, X)"))
    friends_of_bob = {r['X'] for r in result if isinstance(r, dict)}
    assert 'alice' in friends_of_bob
    assert 'charlie' in friends_of_bob


def test_backtracking_with_failure():
    """Test that backtracking continues after failures."""
    kb = pl.KnowledgeBase("failure")
    kb([
        "number(1)",
        "number(2)",
        "number(3)",
        "number(4)",
        "number(5)",
        "even(X) :- number(X), 0 is X % 2"
    ])
    
    result = kb.query(pl.Expr("even(X)"))
    evens = {r['X'] for r in result if isinstance(r, dict)}
    # Should find 2 and 4 (even numbers)
    assert 2 in evens
    assert 4 in evens
    assert 1 not in evens
    assert 3 not in evens
    assert 5 not in evens


def test_nested_backtracking():
    """Test backtracking with nested goals."""
    kb = pl.KnowledgeBase("nested")
    kb([
        "likes(mary, food)",
        "likes(mary, wine)",
        "likes(john, wine)",
        "likes(john, mary)",
        "likes(bob, mary)",
        "likes(bob, wine)",
        # X and Y like the same thing Z
        "common_interest(X, Y, Z) :- likes(X, Z), likes(Y, Z)"
    ])
    
    # Find all common interests between mary and john
    result = kb.query(pl.Expr("common_interest(mary, john, Z)"))
    common = {r['Z'] for r in result if isinstance(r, dict)}
    assert 'wine' in common


def test_generate_and_test():
    """Test generate-and-test pattern with backtracking."""
    kb = pl.KnowledgeBase("generate_test")
    kb([
        "person(alice)",
        "person(bob)",
        "person(charlie)",
        "age(alice, 25)",
        "age(bob, 30)",
        "age(charlie, 25)",
        # Find people with same age
        "same_age(X, Y) :- person(X), person(Y), age(X, A), age(Y, A), neq(X, Y)"
    ])
    
    result = kb.query(pl.Expr("same_age(alice, Y)"))
    same_age_as_alice = {r['Y'] for r in result if isinstance(r, dict)}
    assert 'charlie' in same_age_as_alice
    assert 'alice' not in same_age_as_alice  # neq should exclude alice


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
