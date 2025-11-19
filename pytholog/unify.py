from .util import parse_term, term_to_string, is_var_node, unifiable_check


def unify(lh, rh, lh_domain=None, rh_domain=None):
    if rh_domain is None:
        rh_domain = {}
    if lh_domain is None:
        lh_domain = {}

    nterms = len(rh.terms)
    if unifiable_check(nterms, rh, lh) == False:
        return False

    # substitution map: keys are tuples ('L', name) or ('R', name), values are nodes or other var-keys
    subs = {}

    # initialize subs with pre-bound domain values
    for k, v in (lh_domain or {}).items():
        subs[('L', k)] = parse_term(v, side='L')
    for k, v in (rh_domain or {}).items():
        subs[('R', k)] = parse_term(v, side='R')

    def _key_for_var(node):
        return (node['side'], node['name'])

    def _deref(node):
        # dereference var nodes recursively via subs, protect against cycles
        visited = set()
        def _deref_inner(n):
            if is_var_node(n):
                key = _key_for_var(n)
                if key in visited:
                    return n
                visited.add(key)
                val = subs.get(key)
                if val is None:
                    return n
                if isinstance(val, dict):
                    return _deref_inner(val)
                else:
                    return val
            else:
                return n

        return _deref_inner(node)

    def _bind_var(var_node, value_node):
        key = _key_for_var(var_node)
        # avoid trivial self-binding
        # occurs-check: do not bind var to a value that contains the same var
        def _occurs(var_key, node, seen_nodes=None):
            if seen_nodes is None:
                seen_nodes = set()
            # avoid infinite recursion over the same node id
            nid = id(node)
            if nid in seen_nodes:
                return False
            seen_nodes.add(nid)
            node = _deref(node)
            if is_var_node(node):
                return _key_for_var(node) == var_key
            t = node.get('type')
            if t == 'list':
                for e in node.get('elems', []):
                    if _occurs(var_key, e, seen_nodes):
                        return True
                return False
            if t == 'list_pat':
                return _occurs(var_key, node.get('head'), seen_nodes) or _occurs(var_key, node.get('tail'), seen_nodes)
            return False

        if _occurs(key, value_node):
            return False
        subs[key] = value_node
        return True

    def _unify_nodes(a, b, depth=0):
        if depth > 50:
            return False
        
        a = _deref(a)
        b = _deref(b)
        # if both are the same var node
        if is_var_node(a) and is_var_node(b) and _key_for_var(a) == _key_for_var(b):
            return True

        # var on a
        if is_var_node(a):
            ok = _bind_var(a, b)
            return bool(ok)
        if is_var_node(b):
            ok = _bind_var(b, a)
            return bool(ok)

        # both const
        if a['type'] == 'const' and b['type'] == 'const':
            return a['value'] == b['value']

        # list pattern vs concrete list
        if a['type'] == 'list_pat' and b['type'] == 'list':
            elems = b['elems']
            if len(elems) == 0:
                return False
            head = elems[0]
            tail_list = {'type': 'list', 'elems': elems[1:]}
            return _unify_nodes(a['head'], head, depth+1) and _unify_nodes(a['tail'], tail_list, depth+1)
        if b['type'] == 'list_pat' and a['type'] == 'list':
            elems = a['elems']
            if len(elems) == 0:
                return False
            head = elems[0]
            tail_list = {'type': 'list', 'elems': elems[1:]}
            return _unify_nodes(b['head'], head, depth+1) and _unify_nodes(b['tail'], tail_list, depth+1)

        # both lists
        if a['type'] == 'list' and b['type'] == 'list':
            if len(a['elems']) != len(b['elems']):
                return False
            for ea, eb in zip(a['elems'], b['elems']):
                if not _unify_nodes(ea, eb):
                    return False
            return True

        # types mismatch
        return False

    # unify term by term
    for i in range(nterms):
        rh_arg = rh.terms[i]
        lh_arg = lh.terms[i]
        # wildcard
        if lh_arg == '_':
            continue
        
        a_node = parse_term(lh_arg, side='L')
        b_node = parse_term(rh_arg, side='R')
        ok = _unify_nodes(a_node, b_node)
        if not ok:
            return False

    # propagation: translate subs entries back to lh_domain and rh_domain when possible
    def _resolve_to_value(node):
        node = _deref(node)
        if is_var_node(node):
            return None
        # convert node to string-ish or python structures
        if node['type'] == 'const':
            return node['value']
        # for lists and list patterns, return canonical string representation
        return term_to_string(node)

    # update lh_domain and rh_domain with resolved values
    # for every subs key
    for (side, name), val in list(subs.items()):
        node = val
        resolved = _resolve_to_value(node)
        if resolved is not None:
            if side == 'L':
                lh_domain[name] = resolved
            else:
                rh_domain[name] = resolved

    return True

