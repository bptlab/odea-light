import os
from dotenv import load_dotenv

from odea.io.sparql import SparQLConnector
from odea.abstraction.concept import Concept
from odea.abstraction.helper import abstraction as abs_helper

load_dotenv()

SPARQL_ENDPOINT = os.getenv('SPARQL_ENDPOINT')
SPARQL_PREFIX = os.getenv('SPARQL_PREFIX')

connector = SparQLConnector(SPARQL_ENDPOINT, SPARQL_PREFIX)


def test_flat_path():
    mock_path_1 = [1, [2, [3]]]
    mock_path_2 = [1, [2, [3, [4]], [5, [6]]]]
    mock_path_3 = [1, [2, [3, [4], [7]], [5, [6]]]]

    assert abs_helper.flat_path(mock_path_1, []) == [[1, 2, 3]]
    assert abs_helper.flat_path(mock_path_2, []) == [
        [1, 2, 3, 4], [1, 2, 5, 6]]
    assert abs_helper.flat_path(mock_path_3, []) == [
        [1, 2, 3, 4], [1, 2, 3, 7], [1, 2, 5, 6]]


def test_select_mapping():

    s = Concept('Book_Expense')
    s.set_supertypes(connector.get_supertypes(s))

    mappings = abs_helper.find_abstraction_candidates([s], connector)

    leaf_paths = abs_helper.get_leaf_paths(connector)

    selected_concept = abs_helper.select_mapping(
        mappings, connector, leaf_paths)

    assert selected_concept[0].target.label == 'Booking'
