"""
This script showcases the computation of the two support metrics for mapping
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
from odea.io import event_log_helper as helper

# set up
load_dotenv()

SPARQL_ENDPOINT = os.getenv('SPARQL_ENDPOINT')
SPARQL_PREFIX = os.getenv('SPARQL_PREFIX')

connector = SparQLConnector(SPARQL_ENDPOINT, SPARQL_PREFIX)

# Import event data ...
log_file = 'data/Claim_handeling_v2_filtered.xes'
mapping_file = 'data/claim_event_mapping.csv'

event_to_con_mapping = helper.import_mapping(mapping_file)

# ... prepare low-level concepts ...
ll_concepts: List[Concept]
ll_concepts = helper.concepts_from_log(log_file, mapping_file)

c: Concept

for c in ll_concepts:
    c.set_supertypes(connector.get_supertypes(c))
    c.set_subtypes(connector.get_subtypes(c))
    c.set_parents(connector.get_parents(c))
    c.set_children(connector.get_children(c))

# ... and find abstraction candidates.
mappings: List[Mapping] = abs_helper.find_abstraction_candidates(
    ll_concepts, connector)


# explore mappings
agg = m_helper.avg  # select aggregation function

seen_flag = []

print('{:32s} | {:^13s} | {:^10s}'.format('Concept', 'Support', 'SFC'))
print('---------------------------------|---------------|----------')

for ma in mappings:
    ma.target.supp = m.support(ma.target, mappings)
    ma.target.supp_freq = m.supp_by_freq(ma.target, mappings)
    if ma.target.label not in seen_flag:
        print('{:32s} | {:^13.0f} | {:^10.3f}'.format(
            ma.target.label, ma.target.supp, ma.target.supp_freq))
        seen_flag.append(ma.target.label)
