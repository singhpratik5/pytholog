import re
from itertools import chain
from more_itertools import unique_everseen

__all__ = ["is_number", "is_variable", "rh_val_get", "unifiable_check", "lh_eval"] #used in unify module

def parse_list_literal(s):
    """Parse a simple list literal like "[a,b,c]" into a list of element strings.
    Handles nested brackets by splitting on top-level commas.
    Returns None if input is not a list literal.
    """
    if not isinstance(s, str):
        return None
    s = s.strip()
    if not (s.startswith('[') and s.endswith(']')):
        return None
    inner = s[1:-1].strip()
    if inner == '':
        return []
    parts = []
    buf = ''
    depth = 0
    for ch in inner:
        if ch in '[(':
            depth += 1
            buf += ch
        elif ch in '])':
            depth -= 1
            buf += ch
        elif ch == ',' and depth == 0:
            parts.append(buf.strip())
            buf = ''
        else:
            buf += ch
    if buf != '':
        parts.append(buf.strip())
    return parts


def _split_top_level(s, sep=','):
    parts = []
    buf = ''
    depth = 0
    for ch in s:
        if ch in '[(':
            depth += 1
            buf += ch
        elif ch in '])':
            depth -= 1
            buf += ch
        elif ch == sep and depth == 0:
            parts.append(buf)
            buf = ''
        else:
            buf += ch
    if buf != '':
        parts.append(buf)
    return parts


_anon_var_counter = 0

def parse_term(token, side=None):
    global _anon_var_counter
    # similar to the previous _parse_term in unify.py
    if isinstance(token, dict):
        return token
    if token is None:
        return {'type': 'const', 'value': None}
    
    # Preserve numeric types - don't convert to string
    if isinstance(token, (int, float)):
        return {'type': 'const', 'value': token}
    
    # Preserve boolean types
    if isinstance(token, bool):
        return {'type': 'const', 'value': token}
    
    t = str(token)
    if is_variable(t):
        # Handle anonymous variable - each occurrence gets a unique name
        if t == '_':
            _anon_var_counter += 1
            return {'type': 'var', 'side': side, 'name': f'_G{_anon_var_counter}'}
        return {'type': 'var', 'side': side, 'name': t}
    if t.startswith('[') and t.endswith(']'):
        inner = t[1:-1]
        # find top-level pipe
        pipe_index = -1
        buf = ''
        depth = 0
        for idx,ch in enumerate(inner):
            if ch in '[(':
                depth += 1
            elif ch in '])':
                depth -= 1
            elif ch == '|' and depth == 0:
                pipe_index = idx
                break
        if pipe_index >= 0:
            head_tok = inner[:pipe_index]
            tail_tok = inner[pipe_index+1:]
            
            # Check if head has multiple comma-separated elements
            head_elems = _split_top_level(head_tok, ',')
            if len(head_elems) > 1:
                # Multi-element head like [a,b|T] → convert to nested pattern [a|[b|T]]
                # Build from right to left
                result = parse_term(tail_tok, side)
                for elem in reversed(head_elems):
                    result = {'type': 'list_pat', 
                             'head': parse_term(elem.strip(), side), 
                             'tail': result}
                return result
            else:
                # Single element head like [H|T]
                head_node = parse_term(head_tok, side)
                tail_node = parse_term(tail_tok, side)
                return {'type': 'list_pat', 'head': head_node, 'tail': tail_node}
        if inner.strip() == '':
            return {'type': 'list', 'elems': []}
        elems = _split_top_level(inner, ',')
        nodes = [parse_term(e, side) for e in elems]
        return {'type': 'list', 'elems': nodes}
    return {'type': 'const', 'value': t}


def term_to_string(node):
    t = node['type']
    if t == 'const':
        return node['value']
    if t == 'var':
        return node['name']
    if t == 'list':
        return '[' + ','.join(term_to_string(e) for e in node['elems']) + ']'
    if t == 'list_pat':
        return '[' + term_to_string(node['head']) + '|' + term_to_string(node['tail']) + ']'
    return str(node)


def is_var_node(node):
    return isinstance(node, dict) and node.get('type') == 'var'

## a variable is anything that starts with an uppercase letter or is an _
def is_variable(term):
    if is_number(term):
        return False
    elif term <= "Z" or term == "_":
        return True
    else:
        return False
    
## check whether there is a number in terms or not        
def is_number(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False        
        
## it parses the operations and returns the keys and the values to be evaluated        
def prob_parser(domain, rule_string, rule_terms):
    if "is" in rule_string:
        s = rule_string.split("is")
        key = s[0]
        value = s[1]
    else:
        key = list(domain.keys())[0]
        value = rule_string
    for i in rule_terms:
        if i in domain.keys():
            value = re.sub(i, str(domain[i]), value)
    value = re.sub(r"(and|or|in|not)", r" \g<0> ", value) ## add spaces after and before the keywords so that eval() can see them
    return key, value
    
def rule_terms(rule_string):  ## getting list of unique terms
    s = re.sub(" ", "", rule_string)
    # find contents inside parentheses
    groups = re.findall(r"\((.*?)\)", s)
    terms = []
    for g in groups:
        # split on top-level commas (ignore commas inside brackets or nested parentheses)
        buf = ""
        depth = 0
        for ch in g:
            if ch in "[(":
                depth += 1
                buf += ch
            elif ch in ")]":
                depth -= 1
                buf += ch
            elif ch == ',' and depth == 0:
                terms.append(buf)
                buf = ""
            else:
                buf += ch
        if buf != "":
            terms.append(buf)
    return list(unique_everseen(terms))
    
## the function that takes care of equalizing all uppercased variables
def term_checker(expr):
    #if not isinstance(expr, Expr):
    #    expr = Expr(expr)
    terms = expr.terms[:]
    indx = [x for x,y in enumerate(terms) if is_variable(y)]
    for i in indx:
        ## give the same value for any uppercased variable in the same index
        terms[i] = "Var" + str(i)
    #return expr, "%s(%s)" % (expr.predicate, ",".join(terms))
    return indx, "%s(%s)" % (expr.predicate, ",".join(terms))
    
def get_path(db, expr, path):
    terms = db[expr.predicate]["facts"][0].lh.terms
    path = [{k: i[k] for k in i.keys() if k not in terms} for i in path]
    pathe = [] 
    for i in path:
        for k,v in i.items():
            pathe.append(v)
    return set(pathe)

def pl_read(kb, file):
    file = open(file, "r")
    lines = file.readlines()
    facts = []
    for i in lines:
        i = i.strip()
        i = re.sub(r'\.+$', "", i)
        facts.append(i)
    kb(facts)
    print(f"facts and rules have been added to {kb.name}.db")


def rh_val_get(rh_arg, lh_arg, rh_domain):
    # If rh_arg is a variable, return its binding from rh_domain (if any)
    if is_variable(rh_arg):
        return rh_domain.get(rh_arg)

    # Otherwise, treat rh_arg as a concrete term and return it unchanged.
    # Avoid performing recursive substitutions or list expansions here — those
    # proved to cause unbounded growth and non-termination. Left-hand-side
    # evaluation (`lh_eval`) handles pattern matching (including `[H|T]`).
    return rh_arg


def substitute_vars(term, domain, _depth=0):
    """Substitute all variables in a term using the given domain."""
    # Safety check to prevent infinite recursion
    if _depth > 100:
        raise RecursionError(f"substitute_vars: max depth exceeded for term {term[:50]}")
    
    if not isinstance(term, str):
        return term
    
    # If it's a simple variable, look it up
    if is_variable(term):
        result = domain.get(term, term)
        # If the result is also a variable, try to resolve it
        if is_variable(result) and result != term:
            return substitute_vars(result, domain, _depth + 1)
        return result
    
    # If it's a list pattern like [H|T], substitute the variables inside
    if term.startswith("[") and "|" in term:
        inner = term[1:-1]
        if "|" in inner:
            head, tail = inner.split("|", 1)
            head = head.strip()
            tail = tail.strip()
            head_val = substitute_vars(head, domain, _depth + 1)
            tail_val = substitute_vars(tail, domain, _depth + 1)
            # Reconstruct: if tail is a list, merge; otherwise keep as pattern
            if tail_val.startswith("[") and tail_val.endswith("]"):
                # tail is a list [x,y,...] so we can merge: [head,x,y,...]
                tail_content = tail_val[1:-1]
                if tail_content:
                    return f"[{head_val},{tail_content}]"
                else:
                    return f"[{head_val}]"
            else:
                # tail is not a proper list or is a variable, keep pattern form
                return f"[{head_val}|{tail_val}]"
    
    # Otherwise return as-is
    return term
    
def unifiable_check(nterms, rh, lh):
    if nterms != len(lh.terms): 
        return False
    if rh.predicate != lh.predicate: 
        return False
    
def lh_eval(rh_val, lh_arg, lh_domain):
    # handle list-patterns like [H|T] on the left-hand side
    if isinstance(lh_arg, str) and lh_arg.startswith("[") and "|" in lh_arg:
        # extract head and tail variable names: [Head|Tail]
        inner = lh_arg[1:-1]
        
        if "|" not in inner:
            return False
        head, tail = inner.split("|", 1)
        head = head.strip()
        tail = tail.strip()
        # rh_val should be a concrete list like [a,b] or []
        if not isinstance(rh_val, str) or not rh_val.startswith("["):
            return False
        # parse elements of rh_val at top-level commas
        elems = []
        content = rh_val[1:-1].strip()

        # if rh_val itself is a pattern (contains a '|' inside), do not treat it as a concrete list
        if '|' in content:
            return False

        if content == "":
            elems = []
        else:
            buf = ''
            depth = 0
            for ch in content:
                if ch in '([':
                    depth += 1
                    buf += ch
                elif ch in ')]':
                    depth = max(depth - 1, 0)
                    buf += ch
                elif ch == ',' and depth == 0:
                    elems.append(buf.strip())
                    buf = ''
                else:
                    buf += ch
            if buf != '':
                elems.append(buf.strip())

        # empty list cannot match [H|T]
        if len(elems) == 0:
            return False
        # bind head to first element, tail to remaining list expressed as string
        lh_domain[head] = elems[0]
        tail_list = '[' + ','.join(elems[1:]) + ']'
        lh_domain[tail] = tail_list
        return None

    if is_variable(lh_arg):  #variable in destination
        lh_val = lh_domain.get(lh_arg)
        if not lh_val:
            lh_domain[lh_arg] = rh_val
            #return lh_domain
        elif lh_val != rh_val:
            return False
    elif lh_arg != rh_val:
        return False

def answer_handler(answer):
    if len(answer) == 0: 
        answer.append("No")  ## if no answers at all return "No" 
        return answer
    
    elif len(answer) > 1:
        if any(ans != "Yes" for ans in answer):
            answer = [i for i in answer if i != "Yes"]
        elif all(ans == "Yes" for ans in answer):
            # multiple duplicate 'Yes' answers -> return a single 'Yes'
            return ["Yes"]
            
    return answer