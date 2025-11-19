from pytholog import KnowledgeBase
from pytholog.fact import Fact

kb = KnowledgeBase('relations')
kb(["member(X, [X|_]).","member(X, [_|T]) :- member(X, T).","subset([], _).","subset([H|T], List) :- member(H, List), subset(T, List)."])

print('Original facts in KB:')
for f in kb.db['member']['facts'] if 'member' in kb.db else []:
    print('  ', f.fact)

# pick the subset fact
subset_facts = kb.db.get('subset', {}).get('facts', [])
for i,f in enumerate(subset_facts):
    print(f'FACT #{i}: {f.fact}')
    print('  type:', type(f), 'dir contains fresh?:', hasattr(f, 'fresh'))
    if hasattr(f, 'fresh'):
        fresh = f.fresh('dbg')
        print('  fresh:', fresh.fact)
    print('---')
