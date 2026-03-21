"""Load and cache OWL ontologies."""
from pathlib import Path
from typing import Optional

from rdflib import Graph

from human_services.utils.config import get_ontology_path

_ontology_cache: Optional[Graph] = None


def load_ontology(base_path: Optional[Path] = None) -> Graph:
    """
    Load human services ontology (core + extensions).

    Returns:
        Combined RDF graph with all ontology content.
    """
    global _ontology_cache
    if _ontology_cache is not None:
        return _ontology_cache

    path = base_path or get_ontology_path()
    graph = Graph()

    ontology_files = [
        "human_services.ttl",
        "eligibility_shapes.ttl",
        "snap_program.ttl",
        "medicaid_program.ttl",
        "life_events.ttl",
    ]

    for filename in ontology_files:
        filepath = path / filename
        if filepath.exists():
            graph.parse(str(filepath), format="turtle")

    _ontology_cache = graph
    return graph


def clear_cache() -> None:
    """Clear ontology cache (for testing)."""
    global _ontology_cache
    _ontology_cache = None
