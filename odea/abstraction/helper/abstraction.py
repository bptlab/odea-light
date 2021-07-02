from odea.io.sparql import SparQLConnector

from .. concept import Concept
from .. mapping import Mapping
from .. import metrics as m
from . import metrics as m_helper

from typing import List


def find_abstraction_candidates(concepts: List[Concept],
                                connector: SparQLConnector) -> List[Mapping]:
    """Find abstraction candidates (mappings) for all concepts.

    Args:
        concepts (List[Concept]): list of low-level concepts
        connector (SparQLConnector): SparQLConnector
        metrics (dict): set of metrics and their configurations to evaluate each mapping

    Returns:
        List[Mapping]: abstraction candidates (mappings)
    """
    mappings = []

    for ll_con in concepts:
        for hl_con in ll_con.supertypes:
            paths = find_path_to(ll_con, hl_con, connector)
            mapping = Mapping(ll_con, hl_con, paths)
            mappings.append(mapping)

    return mappings


def get_leaf_paths(connector: SparQLConnector, top=Concept('Task')) -> List[list]:
    """Retruns all paths from all leaves to the top of the ontology.

    Args:
        connector (SparQLConnector): SparQLConnector
        top ([type], optional): top-level concept. Defaults to Concept('Task').

    Returns:
        List[list]: list of paths
    """
    leaves = connector.get_leaves()
    leaf_paths = []
    for leaf in leaves:
        leaf_paths += (find_path_to(Concept(leaf), top, connector))

    return leaf_paths


def select_mapping(mappings: List[Mapping],
                   connector: SparQLConnector, leaf_paths: list,
                   top=Concept('Task'), gran=0, agg=m_helper.avg) -> Mapping:
    """Select mapping from abstraction candidates with the lowest granularity of
    the target/high-level concept.

    Args:
        source (Concept): low-level concept
        mappings (List[Mapping]): abstraction candidates
        connector (SparQLConnector): SparQLConnector
        leaf_paths (list): all paths from all leaves to top
        top (Concept, optional): Top-level concept of the ontology. Defaults to Concept('Task').
        gran (int, optional): Maximum granularity of the selected high-level concept. Defaults to 1.
        agg (fun): aggregation function

    Returns:
        select_mapping [Mapping]: selected abstraction mapping for source
    """
    def select(source: Concept, mappings: List[Mapping],
               connector: SparQLConnector, leaf_paths: list, gran: int,
               top=Concept('Task'), agg=m_helper.avg) -> Mapping:

        selected_mapping: Mapping = None

        candidates = list(
            filter(lambda mapping: source.label ==
                   mapping.source.label, mappings)
        )

        for candidate in candidates:
            paths = find_path_to(candidate.target, top, connector)
            candidate.target.granularity = m.granularity(
                paths, leaf_paths, agg)

            if candidate.target.granularity >= gran:
                gran = candidate.target.granularity
                selected_mapping = candidate

        return selected_mapping

    selected_mappings = []
    source_concepts = []
    seen = []
    for mapping in mappings:
        if mapping.source.label not in seen:
            source_concepts.append(mapping.source)
            seen.append(mapping.source.label)

    for concept in source_concepts:
        selected_abs = select(concept, mappings, connector, leaf_paths, gran)
        selected_mappings.append(selected_abs)

    return selected_mappings


def filter_abstraction_candidates(mappings: List[Mapping],
                                  dist: int,
                                  supp: int) -> List[Mapping]:
    """Filter abstraction candidates based on given constraints (dist and supp).

    Args:
        mappings (List[Mapping]): abstraction candidates
        dist (int): upper-bound for distance
        supp (int): lower-bound for support

    Returns:
        List[Mapping]: filtered abstraction candidates
    """

    # 1, 2
    f1 = list(filter(lambda m: m.evaluation['dist'] <= dist, mappings))
    # f1 = list(filter(lambda m: m.evaluation['rdist'] <= dist, mappings)) # 3

    f2 = list(filter(lambda m: m.target.supp > supp, f1))  # 1
    # f2 = list(filter(lambda m: m.target.supp_freq > supp, f1))  # 2

    return f2


def find_path_to(source: Concept, target: Concept, connector: SparQLConnector):
    path = []
    paths = find_all_paths(source, connector, path)
    paths = flat_path(paths, [])

    p2 = []
    for p in paths:
        p2.append([source.label] + p)

    paths = p2

    paths = list(filter(lambda path: target.label in path, paths))

    return paths


def find_all_paths(source: Concept, connector: SparQLConnector, path: list) -> list:

    if source.parents != []:
        parents = source.parents
    else:
        source.set_parents(connector.get_parents(source))
        parents = source.parents

    if len(parents) > 0:
        for parent in parents:
            path.append([parent.label])
            find_all_paths(parent, connector, path[-1])
    else:
        pass

    return path


def flat_path(path: list, new_path: list) -> list:

    pre = []
    nested = False
    for e in path:
        if isinstance(e, list):
            nested = True
            ee = pre + e
            new_path = flat_path(ee, new_path)
        else:
            pre.append(e)

    if not nested:
        new_path.append(pre)
    return new_path
