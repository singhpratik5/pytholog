from .util import rule_terms
import re
from .expr import Expr
import uuid

class Fact:
    def __init__ (self, fact):
        self._parse_fact(fact)
        
    def _parse_fact(self, fact):
        fact = fact.replace(" ", "")
        # normalize by removing trailing periods from fact strings
        fact = re.sub(r"\.+$", "", fact)
        self.terms = rule_terms(fact)
        if ":-" in fact:
            if_ind = fact.index(":-")
            self.lh = Expr(fact[:if_ind])
            replacements = {"),": ")AND", ");": ")OR"}  ## AND OR conditions placeholders
            replacements = dict((re.escape(k), v) for k, v in replacements.items()) 
            pattern = re.compile("|".join(replacements.keys()))
            rh = pattern.sub(lambda x: replacements[re.escape(x.group(0))], fact[if_ind + 2:])
            rh = re.split("AND|OR", rh)
            self.rhs = [Expr(g) for g in rh] 
            rs = [i.to_string() for i in self.rhs]
            self.fact = (self.lh.to_string() + ":-" + ",".join(rs))
        else:   ## to store normal expr as facts as well in the database
            self.lh = Expr(fact)
            self.rhs = []
            self.fact = self.lh.to_string()
    
    ## returning string value of the fact
    def to_string(self):
        return self.fact

    def __repr__ (self) :
        return self.fact
        
    def __lt__(self, other):
        return self.lh.terms[self.lh.index] < other.lh.terms[other.lh.index]

    def fresh(self, uid=None):
        """Return a fresh copy of this Fact with all variables renamed by appending a unique suffix.
        Variables are tokens starting with an uppercase letter or underscore. The rename is applied
        to the textual representation of the fact before parsing a new Fact object.
        """
        if uid is None:
            uid = uuid.uuid4().hex[:8]
        s = self.fact
        # Replace variable-like tokens (starting with uppercase or underscore) with token_uid
        s2 = re.sub(r"\b([A-Z_][A-Za-z0-9_]*)\b", lambda m: f"{m.group(1)}_{uid}", s)
        return Fact(s2)
        