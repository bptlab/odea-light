from functools import reduce
from . Concept import Concept

# ==========================


def get_min(items: list):
    return float(min(items))


def get_max(items: list):
    return float(max(items))


def avg(items: list):
    return sum(items) / len(items)

# ==========================


def get_prefix(target: Concept, path: list):
    return path[:path.index(target.label) + 1]


def dist(source: Concept, target: Concept, paths: list, agg) -> int:
    dist = []
    for path in paths:
        dist.append(path.index(target.label) -
                    path.index(source.label))

    return agg(dist)


def rdist(source: Concept, target: Concept, paths: list, agg) -> float:

    dists = []

    Gamma = []
    Gamma_p = agg(list(map(lambda p: len(p) - 1, paths)))  # dist_to_top

    for path in paths:
        prefix = get_prefix(target, path)
        if prefix not in Gamma:
            Gamma.append(prefix)

    for path in Gamma:
        l = len(path) - 1
        dists.append(l / Gamma_p)

    return agg(dists)


def granularity(paths_from_concept: list, paths_from_leaves: list, agg):

    Gamma = list(map(lambda path: len(path) - 1, paths_from_concept))
    Gamma_p = list(map(lambda path: len(path) - 1, paths_from_leaves))

    gran = 1 - (agg(Gamma) / (agg(Gamma_p) + 1))

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
