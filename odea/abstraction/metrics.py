from functools import reduce

from odea.io.sparql import SparQLConnector
from . concept import Concept
from . mapping import Mapping
from . helper import metrics as m_helper


def dist(mapping: Mapping, agg) -> int:
    dist = []
    for path in mapping.paths:
        dist.append(path.index(mapping.target.label) -
                    path.index(mapping.source.label))

    return agg(dist)


def rdist(mapping: Mapping, agg):

    Gamma = []

    for path in mapping.paths:
        prefix = m_helper.get_prefix(mapping.target, path)
        if prefix not in Gamma:
            Gamma.append(len(prefix) - 1)

    Gamma_p = agg(list(map(lambda p: len(p) - 1, mapping.paths)))

    l = agg(Gamma)

    return l / (Gamma_p + 1)


def granularity(paths_from_concept: list, paths_from_leaves: list, agg):
    """

    A number close to 1 indicates a fine granularity, while a number close to 0
    referres to a coarse granularity of the concept.

    Args:
        paths_from_concept (list): [description]
        paths_from_leaves (list): [description]
        agg ([type]): [description]

    Returns:
        [type]: [description]
    """

    Gamma = list(map(lambda path: len(path) - 1, paths_from_concept))
    Gamma_p = list(map(lambda path: len(path) - 1, paths_from_leaves))

    gran = (agg(Gamma) / (agg(Gamma_p) + 1))

    return round(gran, 3)


def support(concept: Concept, mappings: list) -> float:
    counter = 0
    for mapping in mappings:
        if concept.label == mapping.target.label:
            counter += 1

    return counter


def rel_support(concept: Concept, mappings: list) -> float:
    counter = 0
    ll_concepts = []
    for mapping in mappings:
        if concept.label == mapping.target.label:
            counter += 1
        ll_concepts.append(mapping.source.label)

    return counter / len(set(ll_concepts))


def supp_by_freq(concept: Concept, mappings: list) -> float:
    counter = 0
    total = {}
    for m in mappings:
        if m.target.label is concept.label:
            counter += m.source.freq
        if m.source.label not in total.keys():
            total[m.source.label] = m.source.freq

    return round(counter/sum(total.values()), 3)


def expr(concept: Concept):
    return len(concept.subtypes)


def complexity_reduction(selected_hl_concepts: list, ll_concepts: list):
    return round(len(selected_hl_concepts) / (len(ll_concepts) + 1), 3)


def complexity_reduction_total(selected_hl_concepts: list, not_abstractable: list, ll_concepts: list):

    denom = set(selected_hl_concepts + not_abstractable)
    total = set(ll_concepts)

    return round(1 - len(denom) / len(total), 3)
