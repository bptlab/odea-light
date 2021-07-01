from pm4py.objects.log.importer.xes import importer as xes_importer
from pm4py.objects.log.obj import EventLog

import pandas as pd

from copy import deepcopy

from typing import List

from .. abstraction.concept import Concept
from .. abstraction.mapping import Mapping


def concepts_from_log(log_file: str, mapping_file: str) -> List[Concept]:
    """Extracts and transforms events from an XES event log into corresponding
    concepts of an ontology, based on a given named entity resolution (mapping).

    Args:
        log_file (str): path to XES file
        mapping_file (str): path to CSV file

    Returns:
        List[Concept]: list low-level concepts
    """

    def get_event_classes_with_freq(log: EventLog) -> dict:
        event_classes = {}

        for trace in log:
            for event in trace:
                if event['concept:name'].strip() not in event_classes.keys():
                    event_classes[event['concept:name']] = 1
                else:
                    event_classes[event['concept:name']] += 1

        return event_classes

    log = xes_importer.apply(log_file)
    event_classes = get_event_classes_with_freq(log)
    mapping = import_mapping(mapping_file)

    concepts_col = {}

    for event_class, freq in event_classes.items():

        concept_name = mapping[event_class]

        if concept_name is not None:
            if concept_name in concepts_col.keys():
                concepts_col[concept_name] += freq
            else:
                concepts_col[concept_name] = freq

    concepts = []
    for name, freq in concepts_col.items():
        concepts.append(Concept(name, freq))

    return concepts


def import_mapping(file: str) -> dict:
    """Import CSV file for named entity resolution (mapping).

    Args:
        file (str): path to CSV file

    Returns:
        dict: mapping of event labels to concept names
    """
    data = pd.read_csv(file)
    mapping = {}
    for idx, row in data.iterrows():
        if type(row['Concept']) is float:
            mapping[row['Event']] = None
        else:
            mapping[row['Event']] = row['Concept']

    return mapping


def enhance_event_labels(log: EventLog, label_mapping: dict,
                         abstraction_mapping: List[Mapping]) -> EventLog:
    """Enhance event log by replacing event labels by corresponding concept names.

    Args:
        log (EventLog): event log to enhance
        label_mapping ([dict]): mapping of event names to concept names
        abstraction_mapping (List[Mapping]): mapping of low-level concept names to high-level concept names

    Returns:
        EventLog: enhanced (abstracted) event log
    """

    def concept_to_concept(abstractions):
        mappings = {}
        for mapping in abstractions:
            mappings[mapping.source.label] = mapping.target.label
        return mappings

    enhanced_log = deepcopy(log)

    concept_mapping = concept_to_concept(abstraction_mapping)

    for trace in enhanced_log:
        for event in trace:
            concept_name = label_mapping[event['concept:name']]
            if concept_name in concept_mapping.keys():
                event['concept:name'] = concept_mapping[concept_name]

    return enhanced_log
