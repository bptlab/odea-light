from . concept import Concept


class Mapping():

    def __init__(self, source: Concept, target: Concept, paths: list):
        self.source = source
        self.target = target
        self.paths = paths
        self.evaluation = {}

    def __str__(self):
        label = '{:s} -> {:s}'.format(self.source.label,
                                      self.target.label)

        details = [label]

        for k, v in self.evaluation.items():
            details.append('\t- {:<15s}: {:n}'.format(k, v))

        return '\n'.join(details)
