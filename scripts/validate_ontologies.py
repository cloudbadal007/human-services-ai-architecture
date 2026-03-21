"""Validate all OWL/SHACL files."""
from pathlib import Path

from rdflib import Graph


def main():
    base = Path("ontologies")
    files = list(base.glob("*.ttl"))
    print(f"Validating {len(files)} ontology files...")
    for f in files:
        try:
            g = Graph()
            g.parse(str(f), format="turtle")
            print(f"  ✓ {f.name}")
        except Exception as e:
            print(f"  ✗ {f.name}: {e}")
    print("Done.")


if __name__ == "__main__":
    main()
