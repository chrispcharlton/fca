import numpy as np
import core
import cbo

import queue


tuplesmin = [{1, 3}, {1, 2}, {0, 2, 4}, {1, 3}]
tuplesmax = [{0, 1, 3}, {1, 2}, {0, 2, 3, 4}, {1, 3}]

mincontext = core.Context.from_attribute_sets(tuplesmin)
maxcontext = core.Context.from_attribute_sets(tuplesmax)

def doublepass():
    minconcepts = list(cbo.FCbO(mincontext).concepts)
    maxconcepts = cbo.FCbO(maxcontext).concepts
    plausible = [c for c in maxconcepts if c not in minconcepts]
    return minconcepts, plausible

class FCbO(core.BaseAlgorithm):
    def __init__(self, context, mincontext):
        self.max_context = context
        self.min_context = mincontext
        self.certain_concepts = []
        self.plausible_concepts = []
        self._fast_generate_from(core.Concept(extent=set(self.max_context.objs)), 0, {i:set() for i in self.max_context.attrs})

    def _is_cannonical_extent(self, extent, intent):
        for col in reversed(range(max(intent))):
            if col in intent:
                continue
            else:
                if all(self.min_context.matrix[list(extent), col]):
                    return False
        return True

    def _is_cannonical_intent(self, extent, intent):
        if set(np.where(self.min_context.matrix[:,list(intent)].all(axis=1))[0]).difference(extent):
            return False
        else:
            return True

    def _fast_generate_from(self, concept, y, N):
        # Sort whether a concept is certain or plausible based on minimal context
        if concept not in self.certain_concepts:
            if (not concept.intent) or (not concept.extent):
                self.certain_concepts.append(concept)
            elif self.min_context.matrix[list(concept.extent), list(concept.intent)].all():
                self.certain_concepts.append(concept)
            else:
                self.plausible_concepts.append(concept)
                # if not certain, find certain subconcept
                extent = set(np.array(list(concept.extent))[self.min_context.matrix[np.ix_(list(concept.extent),list(concept.intent))].all(axis=1)])
                intent = set(np.array(list(concept.intent))[self.min_context.matrix[np.ix_(list(concept.extent),list(concept.intent))].all(axis=0)])
                if extent:
                    if self._is_cannonical_extent(extent, concept.intent):
                        self.certain_concepts.append(core.Concept(extent=extent, intent=concept.intent))
                if intent:
                    if self._is_cannonical_intent(concept.extent, intent):
                        self.certain_concepts.append(core.Concept(extent=concept.extent, intent=intent))

        q = queue.Queue()
        if concept.intent == set(self.max_context.attrs) or y > max(self.max_context.attrs):
            return
        for j in range(y, len(self.max_context.attrs)):
            Yj = set(a for a in self.max_context.attrs if a < j)
            if not j in concept.intent and (N[j].intersection(Yj)).issubset(concept.intent.intersection(Yj)):
                C = concept.extent.intersection(self.max_context.attr_closure(j))
                D = self.max_context.obj_closure(C)
                new_concept = core.Concept(extent=C, intent=D)
                if concept.intent.intersection(Yj) == new_concept.intent.intersection(Yj):
                    q.put((new_concept, j))
                else:
                    N[j] = D
        while not q.empty():
            next_input = q.get()
            self._fast_generate_from(next_input[0], next_input[1] + 1, N)

x = FCbO(maxcontext, mincontext)

def assert_success():
    x =  FCbO(maxcontext, mincontext)
    certain, plausible = doublepass()
    assert not [c for c in x.certain_concepts if c not in certain] and not [c for c in certain if c not in x.certain_concepts]
    assert not [c for c in plausible if c not in x.plausible_concepts] and not [c for c in x.plausible_concepts if c not in plausible]

assert_success()

import timeit

timeit.timeit(doublepass, number=10)

def test():
    FCbO(maxcontext, mincontext)

timeit.timeit(test, number=10)
