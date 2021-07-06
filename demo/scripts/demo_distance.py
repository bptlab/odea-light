"""
This script showcases the computation of the two distance metrics for mapping
of low-level and high-level concepts.
"""

from odea.abstraction import mapping
from odea.abstraction.mapping import Mapping
from typing import List
import os
from dotenv import load_dotenv

from odea.abstraction import metrics as m
from odea.abstraction.concept import Concept
from odea.abstraction.helper import metrics as m_helper
from odea.abstraction.helper import abstraction as abs_helper

from odea.io.sparql import SparQLConnector

# set up
load_dotenv()

SPARQL_ENDPOINT = os.getenv('SPARQL_ENDPOINT')
SPARQL_PREFIX = os.getenv('SPARQL_PREFIX')

connector = SparQLConnector(SPARQL_ENDPOINT, SPARQL_PREFIX)


# define a set of low-level and high-level concepts
ll_concepts = [
    Concept('Copy'),
    Concept('External_Review')
]

hl_concepts = [
    Concept('Extended_Review'),
    Concept('Processing_Task'),
    Concept('Communication_Task'),
    Concept('Document_Management')
]


# prepare low-level concepts and find abstraction candidates
mappings: List[Mapping] = []  # abstraction candidates

c: Concept

for c in ll_concepts:
    c.set_supertypes(connector.get_supertypes(c))
    c.set_subtypes(connector.get_subtypes(c))
    c.set_parents(connector.get_parents(c))
    c.set_children(connector.get_children(c))

    for hl_c in hl_concepts:
        if c.has_supertype(hl_c):
            paths = abs_helper.find_path_to(c, hl_c, connector)
            mappings.append(Mapping(c, hl_c, paths))


# explore mappings

agg = m_helper.avg  # select aggregation function

for ma in mappings:
    ma.evaluation['dist'] = m.dist(ma, agg)
    ma.evaluation['rdist'] = m.rdist(ma, agg)
    print(ma)
