from typing import List


class Concept():

    def __init__(self, label=None, freq=1):
        self.label = label
        self.freq = freq
        self.supp = None
        self.supp_freq = None
        self.gran = None
        self.expr = None

        self.supertypes = []
        self.subtypes = []

        self.parents = []
        self.children = []

    def set_subtypes(self, subtypes: List[str]):
        subtypes = list(filter(lambda x: x != self.label, subtypes))
        self.subtypes = [Concept(subtype) for subtype in subtypes]

    def set_supertypes(self, supertypes: List[str]):
        supertypes = list(filter(lambda x: x != self.label, supertypes))
        self.supertypes = [Concept(supertype) for supertype in supertypes]

    def set_parents(self, parents: List[str]):
        parents = list(filter(lambda x: x != self.label, parents))
        self.parents = [Concept(parent) for parent in parents]

    def set_children(self, children: List[str]):
        children = list(filter(lambda x: x != self.label, children))
        self.children = [Concept(child) for child in children]

    def has_supertype(self, concept: 'Concept'):
        for c in self.supertypes:
            if c.label == concept.label:
                return True
        return False
