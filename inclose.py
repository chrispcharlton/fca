"""
Implementation of In-Close algorithm for computing formal concepts. This algorithm was initially described in the 2009 paper
"In-Close, a Fast Algorithm for Computing Formal Concepts" by Simon Andrews (http://ceur-ws.org/Vol-483/paper1.pdf).
"""

import numpy as np
from core import Concept, Context


class InClose(object):
    def _is_cannonical(self, r, y):
        for col in reversed(range(y)):
            if col in self.concepts[r].intent:
                continue
            else:
                if not self.concepts[self.rnew].extent.difference(context.attrs[col]):
                    return False
        return True

    def _in_close(self, r, y, min_extent=-1):
        self.rnew += 1
        self.concepts[self.rnew] = Concept()
        for j in range(y, len(self.context.attrs)):
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
        self.concepts = {0: Concept(extent=set(self.context.objs))}
        self._in_close(0, 0)
        del self.concepts[max(self.concepts.keys())]
        return list(self.concepts.values())


class InCloseII(object):
    def _is_cannonical(self, r, y):
        for col in reversed(range(y)):
            if col in self.concepts[r].intent:
                continue
            else:
                if not self.concepts[self.rnew].extent.difference(context.attrs[col]):
                    return False
        return True

    def _in_close(self, r, y):
        jchildren = list()
        rchildren = list()
        for j in range(y, len(self.context.attrs)):
            if not j in self.concepts[r].intent:
                self.concepts[self.rnew].extent = set()
                for i in self.concepts[r].extent:
                    if self.context[i,j]:
                        self.concepts[self.rnew].extent = self.concepts[self.rnew].extent.union({i})
                if self.concepts[self.rnew].extent == self.concepts[r].extent:
                    self.concepts[r].intent = self.concepts[r].intent.union({j})
                else:
                    if self._is_cannonical(r, j):
                        jchildren.append(j)
                        rchildren.append(int(self.rnew))
                        self.concepts[self.rnew].intent = self.concepts[r].intent.union({j})
                        self.rnew += 1
                        self.concepts[self.rnew] = Concept()
        for k in range(len(jchildren)):
            self._in_close(rchildren[k], jchildren[k] + 1)

    def run(self, context):
        self.rnew = 1
        self.context = context
        self.concepts = {0: Concept(extent=set(self.context.objs))}
        self.concepts[self.rnew] = Concept()
        self._in_close(0, 0)
        del self.concepts[max(self.concepts.keys())]
        return list(self.concepts.values())


if __name__ == '__main__':

    tuples = [{0, 1, 3}, {1, 2}, {0, 2, 3, 4}, {1, 3}]

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

    context = Context.from_attribute_sets(tuples)

    concepts = InClose().run(context)
    assert not [c for c in expected if c not in concepts] and not [c for c in concepts if c not in expected]
    concepts = InCloseII().run(context)
    assert not [c for c in expected if c not in concepts] and not [c for c in concepts if c not in expected]
