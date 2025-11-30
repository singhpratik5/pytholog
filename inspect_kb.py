from pytholog import KnowledgeBase
kb = KnowledgeBase('relations')
kb(["member(X, [X|_]).","member(X, [_|T]) :- member(X, T).","subset([], _).","subset([H|T], List) :- member(H, List), subset(T, List)."])
print('subset facts:')
for f in kb.db['subset']['facts']._container:
    print('  fact:', f.to_string())
    print('   lh.terms:', f.lh.terms)
print('member facts:')
for f in kb.db['member']['facts']._container:
    print('  fact:', f.to_string())
    print('   lh.terms:', f.lh.terms)
print('DB keys:', list(kb.db.keys()))
