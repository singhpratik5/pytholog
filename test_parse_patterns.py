from pytholog.util import parse_term

# Test parsing of various list patterns
patterns = [
    "[H|T]",
    "[H|_]",
    "[_|T]",
    "[_,X|_]",
    "[_,X|T]",
    "[a,b,c]",
]

for p in patterns:
    node = parse_term(p)
    print(f"Pattern: {p:15} → {node}")
