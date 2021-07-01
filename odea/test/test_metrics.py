import os
from dotenv import load_dotenv


from odea.abstraction import metrics
from odea.abstraction.helper import metrics as m_helper

from odea.abstraction.helper import abstraction as abs_helper

from odea.abstraction.concept import Concept
from odea.abstraction.mapping import Mapping

from odea.io.sparql import SparQLConnector


load_dotenv()

SPARQL_ENDPOINT = os.getenv('SPARQL_ENDPOINT')
SPARQL_PREFIX = os.getenv('SPARQL_PREFIX')

connector = SparQLConnector(SPARQL_ENDPOINT, SPARQL_PREFIX)


def test_get_min():
    l = [1, 1, 2, 3, 4]

    assert m_helper.get_min(l) == 1.0


def test_get_max():
    l = [1, 2, 3, 4, 4]

    assert m_helper.get_max(l) == 4.0


def test_avg():
    l = [1, 2, 3, 4]

    assert m_helper.avg(l) == 2.5


def test_dist():
    start = Concept('S')
    target = Concept('T')

    paths = [
        ['S', 'A', 'B', 'C', 'T'],
        ['S', 'A', 'B', 'C', 'D', 'T'],
        ['S', 'A', 'B', 'T']
    ]

    mapping = Mapping(start, target, paths)

    assert metrics.dist(mapping, m_helper.get_min) == 3
    assert metrics.dist(mapping, m_helper.get_max) == 5
    assert metrics.dist(mapping, m_helper.avg) == 4


def test_get_prefix():
    target = Concept('T')

    paths = [
        ['S', 'A', 'B', 'C', 'T', 'G'],
        ['S', 'A', 'B', 'C', 'D', 'T', 'X', 'Y', 'G'],
        ['S', 'A', 'B', 'C', 'T', 'X', 'Y', 'G']
    ]

    assert m_helper.get_prefix(target, paths[0]) == ['S', 'A', 'B', 'C', 'T']
    assert m_helper.get_prefix(target, paths[1]) == [
        'S', 'A', 'B', 'C', 'D', 'T']
    assert m_helper.get_prefix(target, paths[2]) == ['S', 'A', 'B', 'C', 'T']


def test_rel_dist():

    start = Concept('S')
    target = Concept('T')

    paths = [
        ['S', 'A', 'B', 'C', 'T', 'G'],  # 5, 4
        ['S', 'A', 'B', 'C', 'D', 'T', 'X', 'Y', 'G'],  # 8, 5
        ['S', 'A', 'B', 'C', 'T', 'X', 'Y', 'G']  # 7, 4
    ]

    mapping = Mapping(start, target, paths)

    assert metrics.rdist(mapping, m_helper.get_min) == 2/3
    assert metrics.rdist(mapping, m_helper.get_max) == 5/9
    assert metrics.rdist(mapping, m_helper.avg) == (13/3) / (23/3)


def test_granularity():

    concept_top = [
        ['S', 'A', 'B', 'C', 'T', 'G'],  # 5
        ['S', 'A', 'B', 'C', 'D', 'T', 'X', 'Y', 'G'],  # 8
        ['S', 'A', 'B', 'C', 'T', 'X', 'Y', 'G']  # 7
    ]

    leaves_top = [
        ['L1', 'A', 'B', 'C', 'X', 'Y', 'T', 'G'],  # 7
        ['L2', 'A', 'B', 'C', 'T', 'X', 'G'],  # 6
        ['L3', 'A', 'B', 'C', 'D', 'E', 'F', 'H', 'I', 'J', 'G']  # 10
    ]

    assert metrics.granularity(
        concept_top, leaves_top, m_helper.get_min) == round(5/7, 3)
    assert metrics.granularity(
        concept_top, leaves_top, m_helper.get_max) == round(8/11, 3)
    assert metrics.granularity(
        concept_top, leaves_top, m_helper.avg) == round(10/13, 3)


def test_support():
    target = Concept('S')
    mappings = [
        Mapping(Concept('A'), target, []),
        Mapping(Concept('B'), target, []),
        Mapping(Concept('C'), target, []),
        Mapping(Concept('D'), Concept('X'), []),
        Mapping(Concept('E'), Concept('Y'), [])
    ]

    assert metrics.support(target, mappings) == 3


def test_rel_support():
    target = Concept('S')
    mappings = [
        Mapping(Concept('A'), target, []),
        Mapping(Concept('B'), target, []),
        Mapping(Concept('C'), target, []),
        Mapping(Concept('D'), Concept('X'), []),
        Mapping(Concept('E'), Concept('Y'), [])
    ]

    assert metrics.rel_support(target, mappings) == 3/5


def test_support_by_freq():
    target1 = Concept('C')
    target2 = Concept('F')

    mappings = [
        Mapping(Concept('G', 5), target1, []),
        Mapping(Concept('A', 15), target1, []),
        Mapping(Concept('D', 30), target1, []),
        Mapping(Concept('D', 30), target2, []),
        Mapping(Concept('Y', 50), target2, []),
        Mapping(Concept('H', 60), target2, [])
    ]

    assert metrics.supp_by_freq(target1, mappings) == round(50/160, 3)
    assert metrics.supp_by_freq(target2, mappings) == round(140/160, 3)


def test_expr():
    concept = Concept('Decision_Task')
    concept.set_subtypes(connector.get_subtypes(concept))

    assert metrics.expr(concept) == 9


def test_complexity_reduction():

    selected_hl_concepts = ['A', 'B', 'C']

    ll_concepts = ['U', 'V', 'w', 'X', 'Y', 'Z']

    assert metrics.complexity_reduction(
        selected_hl_concepts, ll_concepts) == 0.5


def test_complexity_reduction():

    selected_hl_concepts = ['A', 'B', 'C']

    ll_concepts = ['U', 'V', 'w', 'X', 'Y', 'Z', 'M', 'N', 'O']

    not_abstractable_concepts = ['M', 'N', 'O']

    assert metrics.complexity_reduction_total(
        selected_hl_concepts, not_abstractable_concepts, ll_concepts) == round(1 - 6/9, 3)
