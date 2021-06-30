import os
from dotenv import load_dotenv

from ..io.sparql import SparQLConnector
from ..abstraction.Concept import Concept

load_dotenv()

SPARQL_ENDPOINT = os.getenv('SPARQL_ENDPOINT')
SPARQL_PREFIX = os.getenv('SPARQL_PREFIX')

con = SparQLConnector(SPARQL_ENDPOINT, SPARQL_PREFIX)


def test_get_supertypes():
    c1 = Concept('Copy')
    supertypes1 = ['Copy', 'Archive', 'Document_Management',
                   'Administrative_Task', 'Task']

    c2 = Concept('Task')
    assert con.get_supertypes(c1).sort() == supertypes1.sort()
    assert con.get_supertypes(c2) == ['Task']


def test_get_subtypes():
    c1 = Concept('Accounting_Task')
    supertypes1 = ['Accounting_Task', 'Account_Verification',
                   'Booking', 'Grant_Transaction', 'Book_Expense', 'Book_Income']

    c2 = Concept('Copy')
    assert con.get_subtypes(c1).sort() == supertypes1.sort()
    assert con.get_subtypes(c2) == ['Copy']


def test_get_parents():
    c1 = Concept('Copy')
    supertypes1 = ['Archive', 'Document_Management']

    c2 = Concept('Task')
    assert con.get_parents(c1).sort() == supertypes1.sort()
    assert con.get_parents(c2) == []


def test_get_children():
    c1 = Concept('Accounting_Task')
    supertypes1 = ['Account_Verification',
                   'Booking', 'Grant_Transaction']

    c2 = Concept('Copy')
    assert con.get_children(c1).sort() == supertypes1.sort()
    assert con.get_children(c2) == []
