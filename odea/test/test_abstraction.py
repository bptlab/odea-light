from odea.io.sparql import SparQLConnector

connector = SparQLConnector('', '')


def test_flat_path():
    mock_path_1 = [1, [2, [3]]]
    mock_path_2 = [1, [2, [3, [4]], [5, [6]]]]
    mock_path_3 = [1, [2, [3, [4], [7]], [5, [6]]]]

    assert connector.flat_path(mock_path_1, []) == [[1, 2, 3]]
    assert connector.flat_path(mock_path_2, []) == [[1, 2, 3, 4], [1, 2, 5, 6]]
    assert connector.flat_path(mock_path_3, []) == [
        [1, 2, 3, 4], [1, 2, 3, 7], [1, 2, 5, 6]]
