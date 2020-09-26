"""
Implementation of In-Close algorithm for computing formal concepts. This algorithm was initially described in the 2009 paper
"In-Close, a Fast Algorithm for Computing Formal core.Concepts" by Simon Andrews (http://ceur-ws.org/Vol-483/paper1.pdf).
"""

import numpy as np
import core


class InClose(core.BaseAlgorithm):
    rnew = 0
    initial_state = [core.Concept()]

    def __init__(self, context):
        self.context = context
        self.concepts = self.initial_state.copy()
        self.concepts[0].extent = self.context.objs.keys()
        self._in_close(0, 0)
        if not self._is_closed(self.concepts[-1]):
            del self.concepts[-1]

    def _is_closed(self, concept):
        for con2 in self.concepts:
            if not concept.intent.difference(con2.intent):
                if not concept.extent.difference(con2.extent):
                    return False
        return True

    def _is_cannonical(self, r, y):
        for col in reversed(range(y)):
            if col in self.concepts[r].intent:
                continue
            else:
                if not self.concepts[self.rnew].extent.difference(context.attrs[col]):
                    return False
        return True

    def _in_close(self, r, y):
        self.rnew += 1
        self.concepts.append(core.Concept())
        for j in range(y, len(self.context.attrs)):
            self.concepts[self.rnew].extent = set()
            for i in self.concepts[r].extent:
                if self.context[i,j]:
                    self.concepts[self.rnew].extent.add(i)
            if self.concepts[self.rnew].extent == self.concepts[r].extent:
                self.concepts[r].intent.add(j)
            else:
                if self._is_cannonical(r, j):
                    self.concepts[self.rnew].intent = self.concepts[r].intent.union({j})
                    self._in_close(self.rnew, j + 1)


class InCloseII(InClose):
    rnew = 1
    initial_state = [core.Concept(), core.Concept()]

    def __init__(self, context):
        super().__init__(context)

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
                        self.concepts.append(core.Concept())
        for k in range(len(jchildren)):
            self._in_close(rchildren[k], jchildren[k] + 1)


if __name__ == '__main__':

    tuples = [{0, 1, 3}, {1, 2}, {0, 2, 3, 4}, {1, 3}]

    expected = [
        core.Concept(extent={0, 1, 2, 3}, intent=set()),
        core.Concept(extent={0, 2, 3}, intent={3}),
        core.Concept(extent={1, 2}, intent={2}),
        core.Concept(extent={0, 1, 3}, intent={1}),
        core.Concept(extent={0, 3}, intent={1, 3}),
        core.Concept(extent={1}, intent={1, 2}),
        core.Concept(extent={0, 2}, intent={0, 3}),
        core.Concept(extent={2}, intent={0, 2, 3, 4}),
        core.Concept(extent={0}, intent={0, 1, 3}),
        core.Concept(extent=set(), intent={0, 1, 2, 3, 4})
    ]

    context = core.Context.from_attribute_sets(tuples)

    concepts = InClose(context)
    assert not [c for c in expected if c not in concepts] and not [c for c in concepts if c not in expected]
    concepts = InCloseII(context)
    assert not [c for c in expected if c not in concepts] and not [c for c in concepts if c not in expected]
