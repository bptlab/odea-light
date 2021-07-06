import pandas as pd
from pm4py.objects.log.importer.xes import importer as xes_importer

from odea.io.event_log_helper import (
    import_mapping
)
mapping_data = 'data/test_mapping.csv'


def test_import_mapping():

    mapping = {
        'a1': 'A',
        'a2': 'A',
        'a3': 'A',
        'b1': 'B',
        'b2': 'B',
        'c': 'C',
        'd': None,
        'e1': 'E',
        'e2': 'E'
    }

    assert import_mapping(mapping_data) == mapping
