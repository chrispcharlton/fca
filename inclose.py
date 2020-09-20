import numpy as np

def IsCannonical(r, y, rnew):
    global concepts
    for col in reversed(range(y)):
        if col in concepts[r]['in']:
            continue
        else:
            if not concepts[rnew]['ex'].difference(set(np.where(context[:,col])[0])):
                return False
    return True

def InClose(r, y):
    global rnew, concepts
    rnew = rnew + 1
    concepts[rnew] = {'ex':set(), 'in':set()}
    for j in range(y, len(context[0])):
        concepts[rnew]['ex'] = set()
        for i in concepts[r]['ex']:
            if context[i,j]:
                concepts[rnew]['ex'].add(i)
        # if len(concepts[rnew]['ex']) > 0:
        if concepts[rnew]['ex'] == concepts[r]['ex']:
            concepts[r]['in'].add(j)
        else:
            if IsCannonical(r, j, rnew):
                concepts[rnew]['in'] = concepts[r]['in'].union({j})
                InClose(rnew, j+1)

def do_InClose(context):
    global rnew, concepts
    rnew = 0
    concepts = {0: {'ex': set([x for x in range(len(context))]), 'in': set()}}
    InClose(0, 0)
    del concepts[max(concepts.keys())]
    return list(concepts.values())

if __name__ == '__main__':

    x = set(range(4))
    y = set(range(5))
    i = {(0,0), (2,0),
         (0,1), (1,1), (3,1),
         (1,2), (2,2),
         (0,3), (2,3), (3,3),
         (2,4),}

    expected = [
        {'ex':x, 'in':set()},
        {'ex':{0,2,3}, 'in': {3}},
        {'ex':{1,2}, 'in': {2}},
        {'ex':{0,1,3}, 'in': {1}},
        {'ex': {0,3}, 'in': {1,3}},
        {'ex':{1}, 'in': {1,2}},
        {'ex':{0,2}, 'in': {0,3}},
        {'ex':{2}, 'in': {0,2,3,4}},
        {'ex':{0}, 'in': {0,1,3}},
        {'ex':set(), 'in': {0,1,2,3,4}}
    ]

    context = np.zeros((len(x), len(y)), dtype=bool)
    for rel in i:
        context[rel[0], rel[1]] = True

    concepts = do_InClose(context)
    assert not [c for c in expected if c not in concepts] and not [c for c in concepts if c not in expected]
