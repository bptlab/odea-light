from odea.io.sparql import SparQLConnector
from odea.abstraction.Concept import Concept
from odea.abstraction import abstraction_helper as abshelper

endpoint = 'http://localhost:3030/ds/query'
prefix = 'http://www.semanticweb.org/bpt/ontologies/2021/5/insurance-company#'

connector = SparQLConnector(endpoint, prefix)


def test_flat_path():
    mock_path_1 = [1, [2, [3]]]
    mock_path_2 = [1, [2, [3, [4]], [5, [6]]]]
    mock_path_3 = [1, [2, [3, [4], [7]], [5, [6]]]]

    assert connector.flat_path(mock_path_1, []) == [[1, 2, 3]]
    assert connector.flat_path(mock_path_2, []) == [[1, 2, 3, 4], [1, 2, 5, 6]]
    assert connector.flat_path(mock_path_3, []) == [
        [1, 2, 3, 4], [1, 2, 3, 7], [1, 2, 5, 6]]


def test_select_mapping():

    s = Concept('Book_Expense')
    s.set_supertypes(connector.get_supertypes(s))
    mappings = abshelper.find_abstraction_candidates([s], connector, {})

    leaf_paths = abshelper.get_leaf_paths(connector)

    selected_concept = abshelper.select_mapping(
        mappings, connector, leaf_paths)

    assert selected_concept[0].target.label == 'Booking'
