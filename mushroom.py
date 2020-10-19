import core
import inclose

with open('mushroom.txt', 'r') as m:
    lines = m.readlines()

attr_sets = [set(map(int, l.strip('\n').split())) for l in lines]

context = core.Context.from_attribute_sets(attr_sets)

concepts = inclose.InCloseII(context)
n = 238710
assert len(concepts.concepts) == n