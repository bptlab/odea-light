"""
This script showcases the computation of the granularity of concepts.
"""

from odea.abstraction.concept import Concept
from odea.abstraction import metrics as m
from odea.abstraction.helper import metrics as m_helper
from odea.abstraction.helper import abstraction as abs_helper

from odea.io.sparql import SparQLConnector

from typing import List
import os
from dotenv import load_dotenv

# set up
load_dotenv()

SPARQL_ENDPOINT = os.getenv('SPARQL_ENDPOINT')
SPARQL_PREFIX = os.getenv('SPARQL_PREFIX')

connector = SparQLConnector(SPARQL_ENDPOINT, SPARQL_PREFIX)


# define a set of concepts
TOP_CONCEPT = Concept('Task')

concepts = [
    Concept('Copy'),
    Concept('External_Review'),
    Concept('Extended_Review'),
    Concept('Processing_Task'),
    Concept('Communication_Task'),
    Concept('Document_Management'),
    Concept('Task')
]


agg = m_helper.get_max  # select aggregation function

# get paths from any leaf to top
leaf_paths = abs_helper.get_leaf_paths(connector)


print('{:20s} | {:13s}'.format('Concept', 'Granularity'))
print('---------------------|------------')
for c in concepts:
    paths = abs_helper.find_path_to(c, TOP_CONCEPT, connector)
    c.granularity = m.granularity(paths, leaf_paths, agg)
    print('{:20s} | {:^13.3f}'.format(c.label, c.granularity))
