import re

class Expr:
    def __init__ (self, fact):
        self._parse_expr(fact)
            
    def _parse_expr(self, fact):
        fact = fact.replace(" ", "")
        self.f = fact
        splitting = r"is|\*|\+|\-|\/|>=|<=|>|<|and|or|in|not"
        if "(" not in fact: 
            fact = "(" + fact + ")"
        pred_ind = fact.index("(")
        self.predicate = fact[:pred_ind]
        self.terms = fact[pred_ind:]
        to_remove = str.maketrans("", "", "() ")
        self.terms = self.terms.translate(to_remove)
        if self.predicate == "": 
            self.terms = re.split(splitting, self.terms)
        else: 
            # Safe term splitting: only split on commas at top level (not inside brackets/parens)
            self.terms = self._split_terms(self.terms)
        self.string = self.f
        self.index = 0
    
    def _split_terms(self, terms_str):
        """Split terms on commas, but only at top level (not inside brackets or parentheses)."""
        if not terms_str:
            return []
        
        terms = []
        current = []
        depth = 0
        
        for char in terms_str:
            if char in '([':
                depth += 1
                current.append(char)
            elif char in ')]':
                depth = max(0, depth - 1)
                current.append(char)
            elif char == ',' and depth == 0:
                if current:
                    terms.append(''.join(current))
                    current = []
            else:
                current.append(char)
        
        if current:
            terms.append(''.join(current))
        
        return terms
    
    ## return string value of the expr in case we need it elsewhere with different type
    def to_string(self):
        return self.string

    def __repr__ (self) :
        return self.string
        
    def __lt__(self, other):
        return self.terms[self.index] < other.terms[other.index]
        

#pl_expr deprecated
class DeprecationHelper(object):
    def __init__(self, new_target):
        self.new_target = new_target

    def _warn(self):
        from warnings import warn
        warn("pl_expr class has been renamed to Expr!")

    def __call__(self, *args, **kwargs):
        self._warn()
        return self.new_target(*args, **kwargs)

    def __getattr__(self, attr):
        self._warn()
        return getattr(self.new_target, attr)

pl_expr = DeprecationHelper(Expr)       