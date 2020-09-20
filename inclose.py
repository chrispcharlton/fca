import numpy as np
import dataclasses

@dataclasses.dataclass()
class Concept():
    extent: set = dataclasses.field(default_factory=set)
    intent: set = dataclasses.field(default_factory=set)


def IsCannonical(r, y, rnew):
    global concepts
    for col in reversed(range(y)):
        if col in concepts[r].intent:
            continue
        else:
            if not concepts[rnew].extent.difference(set(np.where(context[:,col])[0])):
                return False
    return True

def InClose(r, y, min_extent=-1):
    global rnew, concepts
    rnew = rnew + 1
    concepts[rnew] = Concept()
    for j in range(y, len(context[0])):
        concepts[rnew].extent = set()
        for i in concepts[r].extent:
            if context[i,j]:
                concepts[rnew].extent.add(i)
        # Only include concepts with extent larger than min_extent (default include all concepts)
        if len(concepts[rnew].extent) > min_extent:
            if concepts[rnew].extent == concepts[r].extent:
                concepts[r].intent.add(j)
            else:
                if IsCannonical(r, j, rnew):
                    concepts[rnew].intent = concepts[r].intent.union({j})
                    InClose(rnew, j+1)

def do_InClose(context):
    global rnew, concepts
    rnew = 0
    concepts = {0: Concept(extent=set([c for c in range(len(context))]))}
    InClose(0, 0)
    # TODO: review deletion rule as it might result in actual concepts being deleted?
    # delete last concept as it will be unfinished
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
        Concept(extent={0, 1, 2, 3}, intent=set()),
        Concept(extent={0, 2, 3}, intent={3}),
        Concept(extent={1, 2}, intent={2}),
        Concept(extent={0, 1, 3}, intent={1}),
        Concept(extent={0, 3}, intent={1, 3}),
        Concept(extent={1}, intent={1, 2}),
        Concept(extent={0, 2}, intent={0, 3}),
        Concept(extent={2}, intent={0, 2, 3, 4}),
        Concept(extent={0}, intent={0, 1, 3}),
        Concept(extent=set(), intent={0, 1, 2, 3, 4})
    ]

    context = np.zeros((len(x), len(y)), dtype=bool)
    for rel in i:
        context[rel[0], rel[1]] = True

    concepts = do_InClose(context)
    assert not [c for c in expected if c not in concepts] and not [c for c in concepts if c not in expected]
