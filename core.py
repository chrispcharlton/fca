import dataclasses
import numpy as np

@dataclasses.dataclass()
class Concept():
    extent: set = dataclasses.field(default_factory=set)
    intent: set = dataclasses.field(default_factory=set)

class Context():
    def __init__(self, matrix):
        self.matrix = matrix

    def __getitem__(self, item):
        return self.matrix[item]

    @property
    def objs(self):
        return {obj:set(np.where(self.matrix[obj])[0]) for obj in range(len(self.matrix))}

    @property
    def attrs(self):
        return {attr:set(np.where(self.matrix[:,attr])[0]) for attr in range(len(self.matrix[0]))}

    @classmethod
    def from_attribute_sets(cls, tuples, n_attr=None):
        if n_attr:
            assert n_attr >= max([max(s) for s in tuples])
        else:
            n_attr = max([max(s) for s in tuples])
        matrix = np.zeros(shape=(len(tuples), n_attr+1), dtype=bool)
        for row, tuple in enumerate(tuples):
            matrix[row, list(tuple)] = True
        return Context(matrix)


class BaseAlgorithm(object):
    concepts: iter

    def __iter__(self):
        return (c for c in self.concepts)

    def __getitem__(self, item):
        return self.concepts[item]


tuples = [{0,1,3}, {1,2}, {0,2,3,4}, {1,3}]
c = Context.from_attribute_sets(tuples)
