from .util import term_checker, get_path, prob_parser, is_number, is_variable, answer_handler
from .fact import Fact
from .expr import Expr
from .goal import Goal
from .unify import unify
from functools import wraps #, lru_cache
from .pq import SearchQueue
from .search_util import *

## memory decorator which will be called first once .query() method is called
## it takes the Expr and checks in cache {} whether it exists or not
def memory(querizer):
    #cache = {}
    @wraps(querizer)
    def memorize_query(kb, arg1, cut, show_path):
        temp_cache = {}
        #original, look_up = term_checker(arg1)
        indx, look_up = term_checker(arg1)
        if look_up in kb._cache:
            #return cache[look_up]
            temp_cache = kb._cache[look_up] ## if it already exists return it
        else:
            new_entry = querizer(kb, arg1, cut, show_path)  ## if not give it to querizer decorator
            kb._cache[look_up] = new_entry
            temp_cache = new_entry
            #return new_entry
        for d in temp_cache:
            ## temp_cache takes care of changing constant var names in cache
            ## to the variable names use by the user
            if isinstance(d, dict):
                old = list(d.keys())
                #for i in range(len(arg1.terms)):
                for i,j in zip(indx, range(len(old))):
                    d[arg1.terms[i]] = d.pop(old[j])                      
        return temp_cache    
    return memorize_query

## querizer decorator is called whenever there's a new query
## it wraps two functions: simple and rule query
## simple_query() only searched facts not rules while
## rule_query() searches rules
## this can help speed up search and querizer orchestrate the function to be called
def querizer(simple_query):
    def wrap(rule_query):
        @wraps(rule_query)
        def prepare_query(kb, arg1, cut, show_path):
            pred = arg1.predicate
            if pred in kb.db:
                goals_len = 0.0
                for i in kb.db[pred]["goals"]:
                    goals_len += len(i)
                # Prefer simple fact matches first (fast path). If there are
                # direct fact answers, return them; otherwise fall back to
                # rule-based search which handles rules and recursion.
                simple_res = simple_query(kb, arg1)
                # if the query has variables, collect both fact and rule-based answers
                has_vars = any(t <= "Z" for t in arg1.terms)
                if has_vars:
                    rule_res = rule_query(kb, arg1, cut, show_path)
                    # merge results, prefer non-'Yes' dicts and remove duplicates
                    merged = []
                    seen = set()
                    for res in (simple_res + rule_res):
                        key = str(res)
                        if key in seen:
                            continue
                        seen.add(key)
                        merged.append(res)
                    if len(merged) == 0:
                        return ["No"]
                    return merged
                else:
                    # no variables: if facts give an answer return it, otherwise use rule search
                    if not (len(simple_res) == 1 and simple_res[0] == "No"):
                        return simple_res
                    return rule_query(kb, arg1, cut, show_path)
        return prepare_query 
    return wrap 

## simple function it unifies the query with the corresponding facts
def simple_query(kb, expr):
    pred = expr.predicate
    ind = expr.terms[expr.index]
    search_base = kb.db[pred]["facts"]
    result = []
    if not is_variable(ind):
        key = ind
        first, last = fact_binary_search(search_base, key)
    else:
        first, last = (0, len(search_base))
        
    for i in range(first, last):
        res = {}
        uni = unify(expr, Expr(search_base[i].to_string()), res)
        if uni:
            if len(res) == 0: result.append("Yes")
            else: result.append(res)
    if len(result) == 0: result.append("No")
    return result

## rule_query() is the main search function
@memory
@querizer(simple_query)
def rule_query(kb, expr, cut, show_path):
    #pdb.set_trace() # I used to trace every step in the search that consumed me to figure out :D
    rule = Fact(expr.to_string()) # change expr to rule class
    answer = []
    path = []
    ## start from a random point (goal) outside the tree
    start = Goal(Fact("start(search):-from(random_point)"))
    ## put the expr as a goal in the random point to connect it with the tree
    start.fact.rhs = [expr]
    queue = SearchQueue() ## start the queue and fill with first random point
    queue.push(start)
    loop_counter = 0
    MAX_LOOPS = 2000
    while not queue.empty: ## keep searching until it is empty meaning nothing left to be searched
        current_goal = queue.pop()
        loop_counter += 1
        if loop_counter % 200 == 0:
            print(f"[DEBUG] loop {loop_counter}, queue size approx unknown, current goal: {current_goal.fact} ind={current_goal.ind} domain={current_goal.domain}")
        if loop_counter > MAX_LOOPS:
            print(f"[DEBUG] reached max loop {MAX_LOOPS}, aborting search to avoid infinite loop")
            break
        if current_goal.ind >= len(current_goal.fact.rhs): ## all rule goals have been searched
            if current_goal.parent == None: ## no more parents 
                if current_goal.domain:  ## if there is an answer return it
                    answer.append(current_goal.domain)
                    if cut: break
                else: 
                    answer.append("Yes") ## if no returns Yes
                continue ## if no answer found go back to the parent a step above again    
            
            ## father which is the main rule takes unified child's domain from facts
            child_to_parent(current_goal, queue)
            if show_path: path.append(current_goal.domain)
            continue
        
        ## get the rh expr from the current goal to look for its predicate in database
        rule = current_goal.fact.rhs[current_goal.ind]
        
        ## Probabilities and numeric evaluation
        if rule.predicate == "": ## if there is no predicate
            prob_calc(current_goal, rule, queue)
            continue
        
        # inequality
        if rule.predicate == "neq":
            filter_eq(rule, current_goal, queue)
            continue
        # procedural builtin for subset to emulate Prolog behavior for lists
        from .util import parse_list_literal
        if rule.predicate == 'subset':
            a_tok = rule.terms[0]
            b_tok = rule.terms[1]
            # determine concrete list for b
            b_list = None
            if b_tok in current_goal.domain:
                b_list = current_goal.domain[b_tok]
            else:
                b_list = parse_list_literal(b_tok)

            # if both a and b are concrete lists, perform membership checks
            a_list = None
            if a_tok in current_goal.domain:
                a_list = current_goal.domain[a_tok]
            else:
                a_list = parse_list_literal(a_tok)

            # helper: check membership of elements of a_list in b_list
            def list_subset(a_list, b_list):
                if a_list is None or b_list is None:
                    return None
                # normalize b_list elements to strings
                return all(elem in b_list for elem in a_list)

            # if a is concrete, just check membership
            if a_list is not None and b_list is not None:
                ok = list_subset(a_list, b_list)
                if ok:
                    # create child goal that marks this goal as succeeded
                    child = Goal(Fact(rule.to_string()), parent=current_goal, domain=current_goal.domain.copy())
                    child.ind = current_goal.ind + 1
                    queue.push(child)
                continue

            # generative case: a is variable and b is concrete -> generate all subsets (and permutations)
            if (a_tok <= 'Z') and (b_list is not None):
                # generate power set and permutations to emulate Prolog's member-driven generation
                from itertools import combinations, permutations
                results = []
                for r in range(0, len(b_list)+1):
                    for comb in combinations(b_list, r):
                        # include permutations of the combination
                        if len(comb) <= 1:
                            results.append(list(comb))
                        else:
                            for perm in permutations(comb):
                                results.append(list(perm))
                # push child goals for each generated subset binding
                for res in results:
                    # convert numeric-like tokens to numbers for nicer output
                    from .util import is_number
                    def conv(e):
                        if isinstance(e, str) and is_number(e):
                            # choose int when possible
                            if float(e).is_integer():
                                return int(float(e))
                            return float(e)
                        return e
                    child_dom = current_goal.domain.copy()
                    child_dom[a_tok] = [conv(e) for e in res]
                    child = Goal(Fact(rule.to_string()), parent=current_goal, domain=child_dom)
                    child.ind = current_goal.ind + 1
                    queue.push(child)
                continue
            
        elif rule.predicate in kb.db:
            ## search relevant buckets so it speeds up search
            rule_f = kb.db[rule.predicate]["facts"]
            if current_goal.parent == None:
                # parent gets query inputs from grandfather to start search
                parent_inherits(rule, rule_f, current_goal, queue)
            else:
                # a child to search facts in kb
                child_assigned(rule, rule_f, current_goal, queue)
    
    answer = answer_handler(answer)
    
    if show_path: 
        path = get_path(kb.db, expr, path)
        return answer, path
    else:
        return answer