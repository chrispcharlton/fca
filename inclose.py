import numpy as np
import dataclasses

@dataclasses.dataclass()
class Concept():
    extent: set = dataclasses.field(default_factory=set)
    intent: set = dataclasses.field(default_factory=set)

class InClose(object):
    def __init__(self):
        self.rnew = 0
        self.concepts = list()

    def _is_cannonical(self, r, y):
        for col in reversed(range(y)):
            if col in self.concepts[r].intent:
                continue
            else:
                if not self.concepts[self.rnew].extent.difference(set(np.where(self.context[:,col])[0])):
                    return False
        return True

    def _in_close(self, r, y, min_extent=-1):
        self.rnew += 1
        self.concepts[self.rnew] = Concept()
        for j in range(y, len(self.context[0])):
            self.concepts[self.rnew].extent = set()
            for i in self.concepts[r].extent:
                if self.context[i,j]:
                    self.concepts[self.rnew].extent.add(i)
            # Only include concepts with extent larger than min_extent (default include all concepts)
            if len(self.concepts[self.rnew].extent) > min_extent:
                if self.concepts[self.rnew].extent == self.concepts[r].extent:
                    self.concepts[r].intent.add(j)
                else:
                    if self._is_cannonical(r, j):
                        self.concepts[self.rnew].intent = self.concepts[r].intent.union({j})
                        self._in_close(self.rnew, j + 1)

    def run(self, context):
        self.rnew = 0
        self.context = context
        self.concepts = {0: Concept(extent=set([c for c in range(len(context))]))}
        self._in_close(0, 0)
        del self.concepts[max(self.concepts.keys())]
        return list(self.concepts.values())

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

    concepts = InClose().run(context)
    assert not [c for c in expected if c not in concepts] and not [c for c in concepts if c not in expected]
