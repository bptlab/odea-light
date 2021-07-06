"""
This script showcases the computation of the expressiveness of concepts.
"""

from odea.abstraction.concept import Concept
from odea.abstraction import metrics as m

from odea.io.sparql import SparQLConnector

import os
from dotenv import load_dotenv

# set up
load_dotenv()

SPARQL_ENDPOINT = os.getenv('SPARQL_ENDPOINT')
SPARQL_PREFIX = os.getenv('SPARQL_PREFIX')

connector = SparQLConnector(SPARQL_ENDPOINT, SPARQL_PREFIX)


# define a set of concepts
concepts = [
    Concept('Copy'),
    Concept('External_Review'),
    Concept('Extended_Review'),
    Concept('Processing_Task'),
    Concept('Communication_Task'),
    Concept('Document_Management'),
    Concept('Task')
]
c: Concept


print('{:20s} | {:16s}'.format('Concept', 'Expressiveness'))
print('---------------------|---------------')
for c in concepts:
    c.set_subtypes(connector.get_subtypes(c))
    print('{:20s} | {:>14.3f}'.format(c.label, m.expr(c)))
