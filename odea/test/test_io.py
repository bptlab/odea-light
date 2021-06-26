import pandas as pd
from pm4py.objects.log.importer.xes import importer as xes_importer

from odea.io.event_log_helper import (
    get_event_classes_with_freq,
    import_mapping
)

log = xes_importer.apply('/data/test_event_log.xes')
mapping_data = '/data/test_mapping.csv'


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


def test_get_event_classes_with_freq():
    event_classes = {'a': 4, 'b': 2, 'c': 2, 'd': 3, 'g': 1, 'h': 1, 'l': 1}
    assert get_event_classes_with_freq(log) == event_classes
