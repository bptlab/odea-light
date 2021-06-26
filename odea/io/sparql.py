from SPARQLWrapper import SPARQLWrapper, JSON
from .. abstraction import Concept

from typing import List


class SparQLConnector():

    def __init__(self, url, prefix):

        self.endpoint = SPARQLWrapper(url)
        self.prefix = prefix

        self.ROOT = 'Things'

    def get_supertypes(self, c: Concept) -> List[str]:
        #sparql = SPARQLWrapper("http://localhost:3030/ds/query")
        query = """
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        prefix ic: <{:s}>
        
        SELECT DISTINCT ?class
        WHERE {{
            ic:{:s} rdfs:subClassOf* ?class .
        }}
        """.format(self.prefix, c.label)

        results = self.query(query)

        concepts = []

        for result in results["results"]["bindings"]:
            concepts.append(result["class"]["value"][len(self.prefix):])

        return concepts

    def get_subtypes(self, c: Concept) -> List[str]:
        query = """
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        prefix ic: <{:s}>
        
        SELECT DISTINCT ?class
        WHERE {{
            ?class rdfs:subClassOf* ic:{:s}.
        }}
        """.format(self.prefix, c.label)

        results = self.query(query)

        concepts = []

        for result in results["results"]["bindings"]:
            concepts.append(result["class"]["value"][len(self.prefix):])

        return concepts

    def get_parents(self, c: Concept):
        query = """
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        prefix ic: <{:s}>
        
        SELECT DISTINCT ?class
        WHERE {{
            ic:{:s} rdfs:subClassOf ?class .
        }}
        """.format(self.prefix, c.label)

        results = self.query(query)
        concepts = []

        for result in results["results"]["bindings"]:
            concepts.append(result["class"]["value"][len(self.prefix):])

        return concepts

    def get_children(self, c: Concept):
        query = """
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        prefix ic: <{:s}>
        
        SELECT DISTINCT ?class
        WHERE {{
            ?class rdfs:subClassOf ic:{:s} .
        }}
        """.format(self.prefix, c.label)

        results = self.query(query)
        concepts = []

        for result in results["results"]["bindings"]:
            concepts.append(result["class"]["value"][len(self.prefix):])

        return concepts

    def get_leaves(self):
        query = """
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        prefix ic: <{:s}>

        SELECT DISTINCT ?leaf
        WHERE {{
            ?leaf rdfs:subClassOf* ic:{:s} .
            FILTER NOT EXISTS {{ ?child rdfs:subClassOf ?leaf . }}
        }}
        """.format(self.prefix, 'Task')

        results = self.query(query)
        concepts = []

        for result in results["results"]["bindings"]:
            concepts.append(result["leaf"]["value"][len(self.prefix):])

        return concepts
# =============

    def query(self, query):
        self.endpoint.setQuery(query)
        self.endpoint.setReturnFormat(JSON)
        return self.endpoint.query().convert()

    def find_all_paths(self, source: Concept, path: list) -> list:

        if source.parents != []:
            parents = source.parents
        else:
            source.set_parents(self.get_parents(source))
            parents = source.parents

        if len(parents) > 0:
            for parent in parents:
                path.append([parent.label])
                self.find_all_paths(parent, path[-1])
        else:
            pass

        return path

    def find_path_to(self, source: Concept, target: Concept):
        path = []
        paths = self.find_all_paths(source, path)
        paths = self.flat_path(paths, [])

        p2 = []
        for p in paths:
            p2.append([source.label] + p)

        paths = p2

        paths = list(filter(lambda path: target.label in path, paths))

        return paths

    def flat_path(self, path: list, new_path: list) -> list:

        pre = []
        nested = False
        for e in path:
            if isinstance(e, list):
                nested = True
                ee = pre + e
                new_path = self.flat_path(ee, new_path)
            else:
                pre.append(e)

        if not nested:
            new_path.append(pre)
        return new_path
