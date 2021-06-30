from SPARQLWrapper import SPARQLWrapper, JSON
from .. abstraction import Concept

from typing import List


class SparQLConnector():

    def __init__(self, url, prefix):

        self.endpoint = SPARQLWrapper(url)
        self.prefix = prefix

        self.ROOT = 'Things'

    def get_supertypes(self, c: Concept) -> List[str]:
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

    def get_parents(self, c: Concept) -> List[str]:
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

    def get_children(self, c: Concept) -> List[str]:
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

    def get_leaves(self) -> List[str]:
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

    def query(self, query):
        self.endpoint.setQuery(query)
        self.endpoint.setReturnFormat(JSON)
        return self.endpoint.query().convert()
