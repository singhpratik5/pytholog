from pytholog.util import parse_term

pattern = "[_|_]"
concrete = "[a]"

pattern_node = parse_term(pattern, side="L")
concrete_node = parse_term(concrete, side="R")

print(f"Pattern node: {pattern_node}")
print(f"Concrete node: {concrete_node}")
