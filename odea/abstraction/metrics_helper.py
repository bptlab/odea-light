from typing import List
from . Concept import Concept
from . Mapping import Mapping


def get_abstraction_goals(mappings: List[Mapping]) -> List[str]:
    """Returns the set of high-level concept names that are chosen as the result
    of the abstraction. This set corresponds to C_A in the paper.

    Args:
        mappings (list): abstraction candidates

    Returns:
        List(str): concept names
    """
    ca = []
    for mapping in mappings:
        ca.append(mapping.target.label)

    ca = list(set(ca))

    return ca


def get_abstractable_concepts(mappings: List[Mapping]) -> List[str]:
    """Returns the set of low-level concept names that can be abstracted to any
    high-level concepts, based on the provided mapping. This set corresponds to
    C_L'_A in the paper.

    Args:
        mappings (list): abstraction candidates

    Returns:
        List[str]: concept names
    """
    alc = []  # abstractable low-level concepts
    for mapping in mappings:
        alc.append(mapping.source.label)

    alc = list(set(alc))

    return alc


def get_low_level_concepts(ll_concepts: List[Concept]) -> List[str]:
    """Returns the set of low-level concept names. This set corresponds to C_L'
    in the paper.

    Args:
        ll_concepts (list): list of low-level concepts

    Returns:
        List[str]: concept names
    """
    cl = []
    for con in ll_concepts:
        cl.append(con.label)

    cl = list(set(cl))

    return cl


def get_not_abstractable_concepts(ll_concepts: List[Concept], mappings: List[Mapping]) -> List[str]:
    """Returns the set of low-level concept names that can not be abstracted to any
    high-level concept. This set corresponds to C_L' - C_L'_A in the paper.

    Args:
        ll_concepts (List[Concept]): set of low-level concepts
        mappings (List[Mapping]): abstraction candidates

    Returns:
        List[str]: concept names
    """
    alc = get_abstractable_concepts(mappings)
    ll_concepts = get_low_level_concepts(ll_concepts)

    nalc = list(set(ll_concepts) - set(alc))

    return nalc
