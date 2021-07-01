import os
from dotenv import load_dotenv

from ..io.sparql import SparQLConnector
from ..abstraction.concept import Concept

load_dotenv()

SPARQL_ENDPOINT = os.getenv('SPARQL_ENDPOINT')
SPARQL_PREFIX = os.getenv('SPARQL_PREFIX')

con = SparQLConnector(SPARQL_ENDPOINT, SPARQL_PREFIX)


def test_get_supertypes():
    c1 = Concept('Copy')
    supertypes1 = ['Copy', 'Archive', 'Document_Management',
                   'Administrative_Task', 'Task']

    c2 = Concept('Task')
    assert sorted(con.get_supertypes(c1)) == sorted(supertypes1)
    assert con.get_supertypes(c2) == ['Task']


def test_get_subtypes():
    c1 = Concept('Accounting_Task')
    subtypes1 = ['Accounting_Task', 'Account_Verification',
                 'Booking', 'Grant_Transaction', 'Book_Expense', 'Book_Income']

    c2 = Concept('Copy')
    assert sorted(con.get_subtypes(c1)) == sorted(subtypes1)
    assert con.get_subtypes(c2) == ['Copy']


def test_get_parents():
    c1 = Concept('Copy')
    parents = ['Archive', 'Document_Management']

    c2 = Concept('Task')
    assert sorted(con.get_parents(c1)) == sorted(parents)
    assert con.get_parents(c2) == []


def test_get_children():
    c1 = Concept('Accounting_Task')
    children = ['Account_Verification',
                'Booking', 'Grant_Transaction']

    c2 = Concept('Copy')
    assert sorted(con.get_children(c1)) == sorted(children)
    assert con.get_children(c2) == []
