"""
Comprehensive test suite for pytholog inference engine.
Tests basic facts, rules, list operations, recursion, backtracking, and edge cases.
"""
import pytholog as pl
from pytholog import KnowledgeBase, Expr


def test_simple_facts():
    """Test basic fact storage and retrieval."""
    kb = KnowledgeBase("test_facts")
    kb([
        "parent(tom, bob)",
        "parent(tom, liz)",
        "parent(bob, ann)",
        "parent(bob, pat)",
        "parent(pat, jim)"
    ])
    
    # Ground queries
    assert kb.query(Expr("parent(tom, bob)")) == ["Yes"]
    assert kb.query(Expr("parent(tom, liz)")) == ["Yes"]
    assert kb.query(Expr("parent(tom, ann)")) == ["No"]
    
    # Variable queries
    result = kb.query(Expr("parent(tom, X)"))
    assert len(result) == 2
    assert {"X": "bob"} in result
    assert {"X": "liz"} in result


def test_simple_rules():
    """Test basic rule inference."""
    kb = KnowledgeBase("test_rules")
    kb([
        "parent(tom, bob)",
        "parent(bob, ann)",
        "grandparent(X, Z) :- parent(X, Y), parent(Y, Z)"
    ])
    
    assert kb.query(Expr("grandparent(tom, ann)")) == ["Yes"]
    assert kb.query(Expr("grandparent(bob, ann)")) == ["No"]
    
    result = kb.query(Expr("grandparent(tom, X)"))
    assert len(result) >= 1
    assert {"X": "ann"} in result


def test_list_membership():
    """Test member/2 predicate."""
    kb = KnowledgeBase("test_member")
    kb([
        "member(X, [X|_])",
        "member(X, [_|T]) :- member(X, T)"
    ])
    
    # Ground queries
    assert kb.query(Expr("member(a, [a,b,c])")) == ["Yes"]
    assert kb.query(Expr("member(b, [a,b,c])")) == ["Yes"]
    assert kb.query(Expr("member(c, [a,b,c])")) == ["Yes"]
    assert kb.query(Expr("member(d, [a,b,c])")) == ["No"]
    assert kb.query(Expr("member(a, [])")) == ["No"]
    
    # Variable in list
    result = kb.query(Expr("member(X, [1,2,3])"))
    assert len(result) >= 1
    # Should find at least the first element
    assert any(r.get("X") in ["1", "2", "3"] for r in result if isinstance(r, dict))


def test_list_append():
    """Test append/3 predicate."""
    kb = KnowledgeBase("test_append")
    kb([
        "append([], L, L)",
        "append([H|T], L2, [H|L3]) :- append(T, L2, L3)"
    ])
    
    # Ground queries
    assert kb.query(Expr("append([], [1,2], [1,2])")) == ["Yes"]
    assert kb.query(Expr("append([a], [b,c], [a,b,c])")) == ["Yes"]
    assert kb.query(Expr("append([a,b], [c], [a,b,c])")) == ["Yes"]
    assert kb.query(Expr("append([a], [b], [c])")) == ["No"]


def test_list_length():
    """Test length/2 predicate."""
    kb = KnowledgeBase("test_length")
    kb([
        "length([], 0)",
        "length([_|T], N) :- length(T, M), N is M + 1"
    ])
    
    # Ground queries
    assert kb.query(Expr("length([], 0)")) == ["Yes"]
    assert kb.query(Expr("length([a], 1)")) == ["Yes"]
    assert kb.query(Expr("length([a,b], 2)")) == ["Yes"]
    assert kb.query(Expr("length([a,b,c], 3)")) == ["Yes"]
    assert kb.query(Expr("length([a,b], 3)")) == ["No"]


def test_subset_basic():
    """Test subset/2 predicate with ground queries."""
    kb = KnowledgeBase("test_subset")
    kb([
        "member(X, [X|_])",
        "member(X, [_|T]) :- member(X, T)",
        "subset([], _)",
        "subset([H|T], List) :- member(H, List), subset(T, List)"
    ])
    
    # Empty set is subset of any list
    assert kb.query(Expr("subset([], [])")) == ["Yes"]
    assert kb.query(Expr("subset([], [a,b,c])")) == ["Yes"]
    
    # Ground queries
    assert kb.query(Expr("subset([a], [a,b,c])")) == ["Yes"]
    assert kb.query(Expr("subset([a,c], [a,b,c])")) == ["Yes"]
    assert kb.query(Expr("subset([a,b,c], [a,b,c])")) == ["Yes"]
    
    # Negative cases
    assert kb.query(Expr("subset([d], [a,b,c])")) == ["No"]
    assert kb.query(Expr("subset([a,d], [a,b,c])")) == ["No"]
    assert kb.query(Expr("subset([a,b,c,d], [a,b,c])")) == ["No"]


def test_recursion_depth():
    """Test deep recursion."""
    kb = KnowledgeBase("test_recursion")
    kb([
        "ancestor(X, Y) :- parent(X, Y)",
        "ancestor(X, Z) :- parent(X, Y), ancestor(Y, Z)",
        "parent(a, b)",
        "parent(b, c)",
        "parent(c, d)",
        "parent(d, e)",
        "parent(e, f)"
    ])
    
    assert kb.query(Expr("ancestor(a, b)")) == ["Yes"]
    assert kb.query(Expr("ancestor(a, c)")) == ["Yes"]
    assert kb.query(Expr("ancestor(a, f)")) == ["Yes"]
    assert kb.query(Expr("ancestor(c, f)")) == ["Yes"]
    assert kb.query(Expr("ancestor(f, a)")) == ["No"]


def test_multiple_rules_same_predicate():
    """Test predicates with multiple rule definitions."""
    kb = KnowledgeBase("test_multi_rules")
    kb([
        "likes(alice, pizza)",
        "likes(bob, burger)",
        "likes(X, food) :- hungry(X)",
        "hungry(charlie)",
        "hungry(dave)"
    ])
    
    assert kb.query(Expr("likes(alice, pizza)")) == ["Yes"]
    assert kb.query(Expr("likes(bob, burger)")) == ["Yes"]
    assert kb.query(Expr("likes(charlie, food)")) == ["Yes"]
    assert kb.query(Expr("likes(dave, food)")) == ["Yes"]
    assert kb.query(Expr("likes(alice, burger)")) == ["No"]


def test_negation_as_failure():
    """Test negation (if supported)."""
    kb = KnowledgeBase("test_negation")
    kb([
        "mortal(X) :- human(X)",
        "human(socrates)",
        "human(plato)",
        "god(zeus)"
    ])
    
    assert kb.query(Expr("mortal(socrates)")) == ["Yes"]
    assert kb.query(Expr("mortal(plato)")) == ["Yes"]
    # Note: negation may not be supported, so we test what we can
    assert kb.query(Expr("mortal(zeus)")) == ["No"]


def test_arithmetic():
    """Test arithmetic operations."""
    kb = KnowledgeBase("test_arithmetic")
    kb([
        "sum(X, Y, Z) :- Z is X + Y",
        "double(X, Y) :- Y is X * 2"
    ])
    
    result = kb.query(Expr("sum(2, 3, Z)"))
    assert len(result) >= 1
    assert any(r.get("Z") == "5" or r.get("Z") == 5 for r in result if isinstance(r, dict))
    
    result = kb.query(Expr("double(5, Y)"))
    assert len(result) >= 1
    assert any(r.get("Y") == "10" or r.get("Y") == 10 for r in result if isinstance(r, dict))


def test_unification_patterns():
    """Test complex unification patterns."""
    kb = KnowledgeBase("test_unify")
    kb([
        "same(X, X)",
        "first([H|_], H)",
        "second([_,X|_], X)",
        "pair(X, Y, [X,Y])"
    ])
    
    assert kb.query(Expr("same(a, a)")) == ["Yes"]
    assert kb.query(Expr("same(a, b)")) == ["No"]
    
    result = kb.query(Expr("same(X, hello)"))
    assert len(result) >= 1
    assert {"X": "hello"} in result
    
    result = kb.query(Expr("first([a,b,c], X)"))
    assert len(result) >= 1
    assert {"X": "a"} in result
    
    result = kb.query(Expr("second([a,b,c], X)"))
    assert len(result) >= 1
    assert {"X": "b"} in result


def test_empty_list_handling():
    """Test edge cases with empty lists."""
    kb = KnowledgeBase("test_empty")
    kb([
        "empty([])",
        "nonempty([_|_])"
    ])
    
    assert kb.query(Expr("empty([])")) == ["Yes"]
    assert kb.query(Expr("empty([a])")) == ["No"]
    assert kb.query(Expr("nonempty([a])")) == ["Yes"]
    assert kb.query(Expr("nonempty([a,b])")) == ["Yes"]
    assert kb.query(Expr("nonempty([])")) == ["No"]


def test_anonymous_variables():
    """Test anonymous variable _ handling."""
    kb = KnowledgeBase("test_anon")
    kb([
        "ignore_second([X,_], X)",
        "has_two([_,_])"
    ])
    
    result = kb.query(Expr("ignore_second([a,b], X)"))
    assert len(result) >= 1
    assert {"X": "a"} in result
    
    assert kb.query(Expr("has_two([a,b])")) == ["Yes"]
    assert kb.query(Expr("has_two([a,b,c])")) == ["No"]


def test_variable_scope():
    """Test that variables in different rules don't interfere."""
    kb = KnowledgeBase("test_scope")
    kb([
        "rule1(X) :- helper(X, Y), value(Y, 1)",
        "rule2(X) :- helper(X, Y), value(Y, 2)",
        "helper(a, foo)",
        "helper(b, bar)",
        "value(foo, 1)",
        "value(bar, 2)"
    ])
    
    assert kb.query(Expr("rule1(a)")) == ["Yes"]
    assert kb.query(Expr("rule2(b)")) == ["Yes"]
    assert kb.query(Expr("rule1(b)")) == ["No"]
    assert kb.query(Expr("rule2(a)")) == ["No"]


def test_transitive_closure():
    """Test transitive closure (path finding)."""
    kb = KnowledgeBase("test_path")
    kb([
        "edge(a, b)",
        "edge(b, c)",
        "edge(c, d)",
        "edge(b, e)",
        "path(X, Y) :- edge(X, Y)",
        "path(X, Z) :- edge(X, Y), path(Y, Z)"
    ])
    
    assert kb.query(Expr("path(a, b)")) == ["Yes"]
    assert kb.query(Expr("path(a, c)")) == ["Yes"]
    assert kb.query(Expr("path(a, d)")) == ["Yes"]
    assert kb.query(Expr("path(a, e)")) == ["Yes"]
    assert kb.query(Expr("path(c, a)")) == ["No"]


if __name__ == "__main__":
    import pytest
    import sys
    
    # Run tests with verbose output
    sys.exit(pytest.main([__file__, "-v", "-x"]))
