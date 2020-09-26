import core
import queue


class CbO(core.BaseAlgorithm):
    def __init__(self, context):
        self.context = context
        self.concepts = []
        self._generate_from(core.Concept(extent=set(self.context.objs)), 0)

    def _generate_from(self, concept, y):
        if concept not in self.concepts:
            self.concepts.append(concept)
        q = queue.Queue()
        if concept.intent == set(self.context.attrs) or y > max(self.context.attrs):
            return
        for j in range(y, len(self.context.attrs)):
            Yj = set(a for a in self.context.attrs if a < j)
            C = concept.extent.intersection(self.context.attr_closure(j))
            D = self.context.obj_closure(C)
            new_concept = core.Concept(extent=C, intent=D)
            if concept.intent.intersection(Yj) == new_concept.intent.intersection(Yj):
                q.put((new_concept, j))
        while not q.empty():
            next_input = q.get()
            self._generate_from(next_input[0], next_input[1] + 1)


class FCbO(core.BaseAlgorithm):
    def __init__(self, context):
        self.context = context
        self.concepts = []
        self._generate_from(core.Concept(extent=set(self.context.objs)), 0, {i:set() for i in self.context.attrs})

    def _generate_from(self, concept, y, N):
        if concept not in self.concepts:
            self.concepts.append(concept)
        q = queue.Queue()
        if concept.intent == set(self.context.attrs) or y > max(self.context.attrs):
            return
        for j in range(y, len(self.context.attrs)):
            M = N[j]
            Yj = set(a for a in self.context.attrs if a < j)
            if not j in concept.intent and (M.intersection(Yj)).issubset(concept.intent.intersection(Yj)):
                C = concept.extent.intersection(self.context.attr_closure(j))
                D = self.context.obj_closure(C)
                new_concept = core.Concept(extent=C, intent=D)
                if concept.intent.intersection(Yj) == new_concept.intent.intersection(Yj):
                    q.put((new_concept, j))
                else:
                    M = D
        while not q.empty():
            next_input = q.get()
            self._generate_from(next_input[0], next_input[1] + 1, N)


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

    concepts = CbO(context)
    assert not [c for c in expected if c not in concepts] and not [c for c in concepts if c not in expected]
    concepts = FCbO(context)
    assert not [c for c in expected if c not in concepts] and not [c for c in concepts if c not in expected]


    x = []
    for c in concepts:
        if c in x:
            print(c)
        else:
            x.append(c)

