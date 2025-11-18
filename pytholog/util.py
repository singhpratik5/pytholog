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


def parse_term(token, side=None):
    # similar to the previous _parse_term in unify.py
    if isinstance(token, dict):
        return token
    if token is None:
        return {'type': 'const', 'value': None}
    t = str(token)
    if is_variable(t):
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
    indx = [x for x,y in enumerate(terms) if y <= "Z"]
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
    if is_variable(rh_arg):
        rh_val = rh_domain.get(rh_arg)
    else: rh_val = rh_arg
    
    return rh_val
    
def unifiable_check(nterms, rh, lh):
    if nterms != len(lh.terms): 
        return False
    if rh.predicate != lh.predicate: 
        return False
    
def lh_eval(rh_val, lh_arg, lh_domain):
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
            return answer_handler([])
            
    return answer