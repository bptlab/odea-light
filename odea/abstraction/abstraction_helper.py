from ..io.sparql import SparQLConnector

from . Concept import Concept
from . Mapping import Mapping
from . import metrics as m

from typing import List


def find_abstraction_candidates(concepts: List[Concept],
                                connector: SparQLConnector,
                                metrics: dict) -> List[Mapping]:
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
            paths = connector.find_path_to(ll_con, hl_con)
            mapping = Mapping(ll_con, hl_con, paths)
            [mapping.evaluate(metric['key'], metric['fun'], **metric['param'])
                for metric in metrics]
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
        leaf_paths += (connector.find_path_to(Concept(leaf), top))

    return leaf_paths


def select_mapping(mappings: List[Mapping],
                   connector: SparQLConnector, leaf_paths: list,
                   top=Concept('Task'), gran=0, agg=m.avg) -> Mapping:
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
               top=Concept('Task'), agg=m.avg) -> Mapping:

        selected_mapping: Mapping = None

        candidates = list(
            filter(lambda mapping: source.label ==
                   mapping.source.label, mappings)
        )

        for candidate in candidates:
            paths = connector.find_path_to(candidate.target, top)
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

    f1 = list(
        filter(lambda m: m.evaluation['abs. distance'] <= dist, mappings)
    )

    f2 = list(filter(lambda m: m.target.supp > supp, f1))

    return f2
