from collections import namedtuple
import core
import cbo
import inclose

FCATestCase = namedtuple('FCATestCase', ('context', 'concepts'))

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

testcase = FCATestCase(context=core.Context.from_attribute_sets(tuples), concepts=expected)

def algorithm_test(algorithm):
    concepts = algorithm(testcase.context)
    assert not [c for c in expected if c not in concepts] and not [c for c in concepts if c not in expected]

def test_cbo():
    algorithm_test(cbo.CbO)

def test_fcbo():
    algorithm_test(cbo.FCbO)

def test_inclose():
    algorithm_test(inclose.InClose)

def test_inclose2():
    algorithm_test(inclose.InCloseII)
