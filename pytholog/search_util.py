from .unify import unify
from .goal import Goal
from .util import prob_parser, substitute_vars
from .fact import Fact
       
def parent_inherits(rl, rulef, currentgoal, Q):
    for f in range(len(rulef)): ## loop over corresponding rules
        ## take only the ones with the same predicate and same number of terms
        if len(rl.terms) != len(rulef[f].lh.terms): continue
        ## a father goal is the rule we need to search inheriting the domain of the grandfather    
        father = Goal(rulef[f], currentgoal)
        ## unify current rule fact lh with father rhs to get grandfather domain inherited
        uni = unify(rulef[f].lh, rl,
            father.domain, ## saving in father domain
            currentgoal.domain) ## using current goal domain (query input)
        if uni:
            Q.push(father) ## if unify succeeds add father to queue to be searched
        
def child_assigned(rl, rulef, currentgoal, Q):   
    if len(currentgoal.domain) == 0 or all(i not in currentgoal.domain for i in rl.terms):
        for f in range(len(rulef)): ## loop over corresponding facts
            ## take only the ones with the same predicate and same number of terms
            if len(rl.terms) != len(rulef[f].lh.terms): continue
            ## a child goal from the current fact with current goal as parent    
            child = Goal(rulef[f], currentgoal)
            ### if there is nothing to unify then push to the queue directly
            Q.push(child)
            
    else:
        # Use a full scan over candidate facts when we have domain info.
        # Binary-search optimization is fragile when facts contain variables or list-structures,
        # and can miss valid candidates. A full scan is correct and simpler.
        first, last = (0, len(rulef))
        for f in range(first, last): ## loop over only corresponding facts
            ## take only the ones with the same predicate and same number of terms
            if len(rl.terms) != len(rulef[f].lh.terms): continue
            ## a child goal from the current fact with current goal as parent    
            child = Goal(rulef[f], currentgoal)
            
            ## unify current rule fact lh with current goal rhs to get child domain
            uni = unify(rulef[f].lh, rl,
                        child.domain, ## saving in child domain
                        currentgoal.domain) ## using current goal domain
            
            if uni:
                Q.push(child) ## if unify succeeds add child to queue to be searched
                
            
def child_to_parent(child, Q): # which is the current goal
    parent = child.parent.__copy__() #to ensure that parent's domain is different without affecting children's
    
    # Get the parent's current goal and the child's proven fact
    parent_goal = parent.fact.rhs[parent.ind]
    child_lh = child.fact.lh
    
    # Substitute child's variables using child's domain to get the "ground" fact it proved
    from .expr import Expr
    child_lh_subst_terms = [substitute_vars(t, child.domain) for t in child_lh.terms]
    # Convert all terms to strings to avoid type errors
    child_lh_subst_terms_str = [str(term) for term in child_lh_subst_terms]
    child_lh_subst = Expr(child_lh.predicate + "(" + ",".join(child_lh_subst_terms_str) + ")")
    
    # Now unify the parent's goal (with parent's domain) with the child's substituted fact (with empty domain)
    # This will bind any remaining variables in the parent's goal to match the child's proven fact
    uni = unify(parent_goal, child_lh_subst, parent.domain, {})
    
    if uni:
        parent.ind += 1
        Q.push(parent)


def prob_calc(currentgoal, rl, Q):
    ## Probabilities and numeric evaluation
    key, value = prob_parser(currentgoal.domain, rl.to_string(), rl.terms)
    ## eval the mathematic operation
    value = eval(value)
    if value == True: 
        value = currentgoal.domain.get(key)
        ## it is true but there is no key in the domain (helpful for ML rules in future)
        if value is None:
            value = "Yes"
    elif value == False:
        value = "No"
    currentgoal.domain[key] = value ## assign a new key in the domain with the evaluated value
    prob_child = Goal(Fact(rl.to_string()),
                      parent = currentgoal,
                      domain = currentgoal.domain)
    Q.push(prob_child)


def fact_binary_search(facts, key):
    # search for the indices of the key in the facts heap
    # start to get last occurrence index at the right side
    right = 0
    length = len(facts)
    while right < length:
        middle = (right + length) // 2
        f = facts[middle]
        if key < f.lh.terms[f.lh.index]:
            length = middle
        else: 
            right = middle + 1
    # now first occurence at the left side
    left = 0
    length = right - 1
    while left < length:
        middle = (left + length) // 2
        f = facts[middle]
        if key > f.lh.terms[f.lh.index]: 
            left = middle + 1
        else: 
            length = middle
    
    if left == right == 0: # if facts aren't sorted with index 0
        left, right = (0, len(facts))
            
    return left, right #- 1
    
def filter_eq(rule, currentgoal, Q):
    # apply inequality check
    currentgoal.domain = {k:v for k,v in currentgoal.domain.items() if currentgoal.domain[rule.terms[0]] != currentgoal.domain[rule.terms[1]]}

    prob_child = Goal(Fact(rule.to_string()),
                      parent = currentgoal,
                      domain = currentgoal.domain)
    Q.push(prob_child)