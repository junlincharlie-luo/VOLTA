"""
Knowledge Graph module for POPPER.

This module provides data structures and utilities for managing a unified knowledge graph
that combines:
- Literature citations (papers, abstracts, findings)
- Domain ontology (e.g., Gene -> Protein -> Pathway relationships)
- Support/contradiction relationships to hypotheses
"""

from typing import Dict, List, Optional, Set, Tuple, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import json
import os
from collections import defaultdict


class NodeType(Enum):
    """Types of nodes in the knowledge graph."""
    # Literature nodes
    PAPER = "paper"
    AUTHOR = "author"
    FINDING = "finding"

    # Domain ontology nodes (biology-focused)
    GENE = "gene"
    PROTEIN = "protein"
    PATHWAY = "pathway"
    DISEASE = "disease"
    DRUG = "drug"
    CELL_TYPE = "cell_type"
    TISSUE = "tissue"
    ORGANISM = "organism"

    # Generic nodes
    CONCEPT = "concept"
    HYPOTHESIS = "hypothesis"
    EVIDENCE = "evidence"


class EdgeType(Enum):
    """Types of edges/relationships in the knowledge graph."""
    # Literature relationships
    CITES = "cites"
    AUTHORED_BY = "authored_by"
    REPORTS = "reports"

    # Support/contradiction relationships
    SUPPORTS = "supports"
    CONTRADICTS = "contradicts"
    INCONCLUSIVE = "inconclusive"

    # Domain ontology relationships
    ENCODES = "encodes"  # Gene -> Protein
    PARTICIPATES_IN = "participates_in"  # Protein -> Pathway
    REGULATES = "regulates"
    INHIBITS = "inhibits"
    ACTIVATES = "activates"
    ASSOCIATED_WITH = "associated_with"
    EXPRESSED_IN = "expressed_in"
    INTERACTS_WITH = "interacts_with"
    CAUSES = "causes"
    TREATS = "treats"

    # Generic relationships
    RELATED_TO = "related_to"
    PART_OF = "part_of"
    IS_A = "is_a"


@dataclass
class KGNode:
    """Represents a node in the knowledge graph."""
    id: str
    node_type: NodeType
    name: str
    properties: Dict[str, Any] = field(default_factory=dict)

    # Literature-specific fields
    abstract: Optional[str] = None
    year: Optional[int] = None
    journal: Optional[str] = None
    doi: Optional[str] = None

    # Domain-specific fields
    aliases: List[str] = field(default_factory=list)
    external_ids: Dict[str, str] = field(default_factory=dict)  # e.g., {"NCBI": "1234", "UniProt": "P12345"}

    def to_dict(self) -> Dict[str, Any]:
        """Convert node to dictionary for serialization."""
        return {
            "id": self.id,
            "node_type": self.node_type.value,
            "name": self.name,
            "properties": self.properties,
            "abstract": self.abstract,
            "year": self.year,
            "journal": self.journal,
            "doi": self.doi,
            "aliases": self.aliases,
            "external_ids": self.external_ids
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "KGNode":
        """Create node from dictionary."""
        return cls(
            id=data["id"],
            node_type=NodeType(data["node_type"]),
            name=data["name"],
            properties=data.get("properties", {}),
            abstract=data.get("abstract"),
            year=data.get("year"),
            journal=data.get("journal"),
            doi=data.get("doi"),
            aliases=data.get("aliases", []),
            external_ids=data.get("external_ids", {})
        )


@dataclass
class KGEdge:
    """Represents an edge/relationship in the knowledge graph."""
    source_id: str
    target_id: str
    edge_type: EdgeType
    properties: Dict[str, Any] = field(default_factory=dict)

    # Evidence/confidence fields
    confidence: float = 1.0  # 0.0 to 1.0
    evidence_count: int = 1
    source_papers: List[str] = field(default_factory=list)  # Paper IDs supporting this edge

    def to_dict(self) -> Dict[str, Any]:
        """Convert edge to dictionary for serialization."""
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "edge_type": self.edge_type.value,
            "properties": self.properties,
            "confidence": self.confidence,
            "evidence_count": self.evidence_count,
            "source_papers": self.source_papers
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "KGEdge":
        """Create edge from dictionary."""
        return cls(
            source_id=data["source_id"],
            target_id=data["target_id"],
            edge_type=EdgeType(data["edge_type"]),
            properties=data.get("properties", {}),
            confidence=data.get("confidence", 1.0),
            evidence_count=data.get("evidence_count", 1),
            source_papers=data.get("source_papers", [])
        )


@dataclass
class PriorKnowledge:
    """Structured representation of prior knowledge relevant to a hypothesis."""
    hypothesis: str
    supporting_evidence: List[Dict[str, Any]] = field(default_factory=list)
    contradicting_evidence: List[Dict[str, Any]] = field(default_factory=list)
    related_concepts: List[Dict[str, Any]] = field(default_factory=list)
    suggested_tests: List[str] = field(default_factory=list)
    confidence_assessment: Optional[str] = None

    def to_summary(self) -> str:
        """Generate a text summary for the Reference Agent to use."""
        summary_parts = []

        summary_parts.append(f"## Prior Knowledge Summary for Hypothesis:\n\"{self.hypothesis}\"\n")

        if self.supporting_evidence:
            summary_parts.append("### Supporting Evidence:")
            for i, evidence in enumerate(self.supporting_evidence, 1):
                summary_parts.append(f"{i}. {evidence.get('summary', 'N/A')}")
                if evidence.get('source'):
                    summary_parts.append(f"   Source: {evidence['source']}")
                if evidence.get('confidence'):
                    summary_parts.append(f"   Confidence: {evidence['confidence']}")
            summary_parts.append("")

        if self.contradicting_evidence:
            summary_parts.append("### Contradicting Evidence:")
            for i, evidence in enumerate(self.contradicting_evidence, 1):
                summary_parts.append(f"{i}. {evidence.get('summary', 'N/A')}")
                if evidence.get('source'):
                    summary_parts.append(f"   Source: {evidence['source']}")
            summary_parts.append("")

        if self.related_concepts:
            summary_parts.append("### Related Concepts:")
            for concept in self.related_concepts:
                summary_parts.append(f"- {concept.get('name', 'N/A')}: {concept.get('relationship', 'related')}")
            summary_parts.append("")

        if self.suggested_tests:
            summary_parts.append("### Suggested Falsification Tests Based on Prior Knowledge:")
            for i, test in enumerate(self.suggested_tests, 1):
                summary_parts.append(f"{i}. {test}")
            summary_parts.append("")

        if self.confidence_assessment:
            summary_parts.append(f"### Overall Assessment:\n{self.confidence_assessment}")

        return "\n".join(summary_parts)


class KnowledgeGraph:
    """
    Main knowledge graph class that manages nodes, edges, and provides query capabilities.
    """

    def __init__(self):
        self.nodes: Dict[str, KGNode] = {}
        self.edges: List[KGEdge] = []

        # Indexes for efficient querying
        self._edges_by_source: Dict[str, List[KGEdge]] = defaultdict(list)
        self._edges_by_target: Dict[str, List[KGEdge]] = defaultdict(list)
        self._edges_by_type: Dict[EdgeType, List[KGEdge]] = defaultdict(list)
        self._nodes_by_type: Dict[NodeType, List[str]] = defaultdict(list)
        self._nodes_by_name: Dict[str, List[str]] = defaultdict(list)  # name -> [node_ids]

    def add_node(self, node: KGNode) -> None:
        """Add a node to the knowledge graph."""
        self.nodes[node.id] = node
        self._nodes_by_type[node.node_type].append(node.id)
        self._nodes_by_name[node.name.lower()].append(node.id)

        # Index aliases too
        for alias in node.aliases:
            self._nodes_by_name[alias.lower()].append(node.id)

    def add_edge(self, edge: KGEdge) -> None:
        """Add an edge to the knowledge graph."""
        self.edges.append(edge)
        self._edges_by_source[edge.source_id].append(edge)
        self._edges_by_target[edge.target_id].append(edge)
        self._edges_by_type[edge.edge_type].append(edge)

    def get_node(self, node_id: str) -> Optional[KGNode]:
        """Get a node by its ID."""
        return self.nodes.get(node_id)

    def find_nodes_by_name(self, name: str, exact: bool = False) -> List[KGNode]:
        """Find nodes by name (case-insensitive)."""
        name_lower = name.lower()
        if exact:
            node_ids = self._nodes_by_name.get(name_lower, [])
        else:
            node_ids = []
            for key, ids in self._nodes_by_name.items():
                if name_lower in key:
                    node_ids.extend(ids)

        return [self.nodes[nid] for nid in set(node_ids) if nid in self.nodes]

    def find_nodes_by_type(self, node_type: NodeType) -> List[KGNode]:
        """Find all nodes of a specific type."""
        node_ids = self._nodes_by_type.get(node_type, [])
        return [self.nodes[nid] for nid in node_ids if nid in self.nodes]

    def get_neighbors(self, node_id: str, edge_types: Optional[List[EdgeType]] = None) -> List[Tuple[KGNode, KGEdge]]:
        """Get all neighboring nodes connected to the given node."""
        neighbors = []

        # Outgoing edges
        for edge in self._edges_by_source.get(node_id, []):
            if edge_types is None or edge.edge_type in edge_types:
                if edge.target_id in self.nodes:
                    neighbors.append((self.nodes[edge.target_id], edge))

        # Incoming edges
        for edge in self._edges_by_target.get(node_id, []):
            if edge_types is None or edge.edge_type in edge_types:
                if edge.source_id in self.nodes:
                    neighbors.append((self.nodes[edge.source_id], edge))

        return neighbors

    def find_supporting_evidence(self, concept_name: str) -> List[Tuple[KGNode, KGEdge]]:
        """Find evidence that supports a concept/hypothesis."""
        results = []
        nodes = self.find_nodes_by_name(concept_name)

        for node in nodes:
            for neighbor, edge in self.get_neighbors(node.id, [EdgeType.SUPPORTS]):
                results.append((neighbor, edge))

        return results

    def find_contradicting_evidence(self, concept_name: str) -> List[Tuple[KGNode, KGEdge]]:
        """Find evidence that contradicts a concept/hypothesis."""
        results = []
        nodes = self.find_nodes_by_name(concept_name)

        for node in nodes:
            for neighbor, edge in self.get_neighbors(node.id, [EdgeType.CONTRADICTS]):
                results.append((neighbor, edge))

        return results

    def get_pathway_for_gene(self, gene_name: str) -> List[Dict[str, Any]]:
        """Get the pathway information for a gene (Gene -> Protein -> Pathway)."""
        pathway_info = []
        genes = self.find_nodes_by_name(gene_name)

        for gene in genes:
            if gene.node_type != NodeType.GENE:
                continue

            gene_info = {"gene": gene.name, "proteins": [], "pathways": []}

            # Find proteins encoded by this gene
            for neighbor, edge in self.get_neighbors(gene.id, [EdgeType.ENCODES]):
                if neighbor.node_type == NodeType.PROTEIN:
                    gene_info["proteins"].append(neighbor.name)

                    # Find pathways this protein participates in
                    for pathway_neighbor, pathway_edge in self.get_neighbors(
                        neighbor.id, [EdgeType.PARTICIPATES_IN]
                    ):
                        if pathway_neighbor.node_type == NodeType.PATHWAY:
                            gene_info["pathways"].append(pathway_neighbor.name)

            pathway_info.append(gene_info)

        return pathway_info

    def query_hypothesis(self, hypothesis: str, domain: str = "biology") -> PriorKnowledge:
        """
        Query the knowledge graph for information relevant to a hypothesis.

        This is the main method used by the Reference Agent.
        """
        prior_knowledge = PriorKnowledge(hypothesis=hypothesis)

        # Extract key terms from hypothesis (simple keyword extraction)
        keywords = self._extract_keywords(hypothesis)

        for keyword in keywords:
            # Find related nodes
            nodes = self.find_nodes_by_name(keyword)

            for node in nodes:
                # Add as related concept
                prior_knowledge.related_concepts.append({
                    "name": node.name,
                    "type": node.node_type.value,
                    "relationship": "mentioned_in_hypothesis"
                })

                # Find supporting evidence
                for neighbor, edge in self.get_neighbors(node.id, [EdgeType.SUPPORTS]):
                    if neighbor.node_type == NodeType.PAPER:
                        prior_knowledge.supporting_evidence.append({
                            "summary": f"{neighbor.name}" + (f": {neighbor.abstract[:200]}..." if neighbor.abstract else ""),
                            "source": neighbor.doi or neighbor.name,
                            "confidence": edge.confidence,
                            "year": neighbor.year
                        })
                    elif neighbor.node_type == NodeType.FINDING:
                        prior_knowledge.supporting_evidence.append({
                            "summary": neighbor.name,
                            "source": ", ".join(edge.source_papers) if edge.source_papers else "Unknown",
                            "confidence": edge.confidence
                        })

                # Find contradicting evidence
                for neighbor, edge in self.get_neighbors(node.id, [EdgeType.CONTRADICTS]):
                    if neighbor.node_type in [NodeType.PAPER, NodeType.FINDING]:
                        prior_knowledge.contradicting_evidence.append({
                            "summary": neighbor.name + (f": {neighbor.abstract[:200]}..." if neighbor.abstract else ""),
                            "source": neighbor.doi if hasattr(neighbor, 'doi') and neighbor.doi else "Unknown"
                        })

                # Get pathway information for biology domain
                if domain.lower() in ["biology", "genetics", "molecular biology"]:
                    pathway_info = self.get_pathway_for_gene(node.name)
                    for info in pathway_info:
                        if info["pathways"]:
                            prior_knowledge.suggested_tests.append(
                                f"Test {node.name} relationship with pathway(s): {', '.join(info['pathways'])}"
                            )

        # Generate confidence assessment
        n_support = len(prior_knowledge.supporting_evidence)
        n_contradict = len(prior_knowledge.contradicting_evidence)

        if n_support == 0 and n_contradict == 0:
            prior_knowledge.confidence_assessment = (
                "No prior evidence found in the knowledge graph. "
                "This hypothesis appears to be novel or uses terminology not in our database."
            )
        elif n_support > n_contradict * 2:
            prior_knowledge.confidence_assessment = (
                f"Strong prior support found ({n_support} supporting vs {n_contradict} contradicting). "
                "Consider focusing falsification tests on edge cases or unexplored conditions."
            )
        elif n_contradict > n_support * 2:
            prior_knowledge.confidence_assessment = (
                f"Significant contradicting evidence found ({n_contradict} contradicting vs {n_support} supporting). "
                "This hypothesis may face challenges. Consider reviewing the contradicting studies."
            )
        else:
            prior_knowledge.confidence_assessment = (
                f"Mixed evidence found ({n_support} supporting, {n_contradict} contradicting). "
                "This is an active area of research with ongoing debate."
            )

        return prior_knowledge

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text for querying (simple implementation)."""
        # Remove common words and split
        stop_words = {
            "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
            "have", "has", "had", "do", "does", "did", "will", "would", "could",
            "should", "may", "might", "must", "shall", "can", "need", "dare",
            "to", "of", "in", "for", "on", "with", "at", "by", "from", "as",
            "into", "through", "during", "before", "after", "above", "below",
            "between", "under", "again", "further", "then", "once", "here",
            "there", "when", "where", "why", "how", "all", "each", "few",
            "more", "most", "other", "some", "such", "no", "nor", "not",
            "only", "own", "same", "so", "than", "too", "very", "just",
            "and", "but", "if", "or", "because", "until", "while", "that",
            "which", "who", "whom", "this", "these", "those", "that", "hypothesis"
        }

        # Simple tokenization
        words = text.lower().replace(",", " ").replace(".", " ").replace("(", " ").replace(")", " ").split()
        keywords = [w for w in words if w not in stop_words and len(w) > 2]

        return list(set(keywords))

    def save(self, filepath: str) -> None:
        """Save knowledge graph to JSON file."""
        data = {
            "nodes": [node.to_dict() for node in self.nodes.values()],
            "edges": [edge.to_dict() for edge in self.edges]
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    @classmethod
    def load(cls, filepath: str) -> "KnowledgeGraph":
        """Load knowledge graph from JSON file."""
        kg = cls()
        with open(filepath, 'r') as f:
            data = json.load(f)

        for node_data in data.get("nodes", []):
            kg.add_node(KGNode.from_dict(node_data))

        for edge_data in data.get("edges", []):
            kg.add_edge(KGEdge.from_dict(edge_data))

        return kg

    def __len__(self) -> int:
        """Return number of nodes in the graph."""
        return len(self.nodes)

    def stats(self) -> Dict[str, Any]:
        """Return statistics about the knowledge graph."""
        return {
            "num_nodes": len(self.nodes),
            "num_edges": len(self.edges),
            "node_types": {nt.value: len(ids) for nt, ids in self._nodes_by_type.items()},
            "edge_types": {et.value: len(edges) for et, edges in self._edges_by_type.items()}
        }


def create_sample_biology_kg() -> KnowledgeGraph:
    """
    Create a sample knowledge graph with biology domain data for demonstration.
    """
    kg = KnowledgeGraph()

    # Add some sample genes
    gene_vav1 = KGNode(
        id="gene_vav1",
        node_type=NodeType.GENE,
        name="VAV1",
        properties={"description": "Vav guanine nucleotide exchange factor 1"},
        aliases=["VAV", "VAV1"],
        external_ids={"NCBI": "7409", "HGNC": "12657"}
    )
    kg.add_node(gene_vav1)

    gene_il2 = KGNode(
        id="gene_il2",
        node_type=NodeType.GENE,
        name="IL2",
        properties={"description": "Interleukin 2"},
        aliases=["IL-2", "Interleukin-2", "T-cell growth factor"],
        external_ids={"NCBI": "3558", "HGNC": "6001"}
    )
    kg.add_node(gene_il2)

    # Add proteins
    protein_vav1 = KGNode(
        id="protein_vav1",
        node_type=NodeType.PROTEIN,
        name="VAV1 protein",
        properties={"function": "Guanine nucleotide exchange factor"},
        external_ids={"UniProt": "P15498"}
    )
    kg.add_node(protein_vav1)

    protein_il2 = KGNode(
        id="protein_il2",
        node_type=NodeType.PROTEIN,
        name="IL-2 protein",
        properties={"function": "Cytokine, T-cell growth factor"},
        external_ids={"UniProt": "P60568"}
    )
    kg.add_node(protein_il2)

    # Add pathways
    pathway_tcell = KGNode(
        id="pathway_tcell_activation",
        node_type=NodeType.PATHWAY,
        name="T-cell receptor signaling pathway",
        properties={"description": "Signal transduction pathway in T lymphocytes"}
    )
    kg.add_node(pathway_tcell)

    pathway_cytokine = KGNode(
        id="pathway_cytokine",
        node_type=NodeType.PATHWAY,
        name="Cytokine-cytokine receptor interaction",
        properties={"description": "Cytokine signaling network"}
    )
    kg.add_node(pathway_cytokine)

    # Add a sample paper
    paper1 = KGNode(
        id="paper_vav1_il2_2020",
        node_type=NodeType.PAPER,
        name="VAV1 regulates IL-2 production in T cells",
        abstract="This study demonstrates that VAV1 is a critical regulator of IL-2 production through the T-cell receptor signaling pathway...",
        year=2020,
        journal="Journal of Immunology",
        doi="10.1000/example.doi.1"
    )
    kg.add_node(paper1)

    # Add findings
    finding1 = KGNode(
        id="finding_vav1_il2",
        node_type=NodeType.FINDING,
        name="VAV1 knockdown reduces IL-2 production by 70% in activated T cells",
        properties={"method": "siRNA knockdown", "cell_type": "primary human T cells"}
    )
    kg.add_node(finding1)

    # Add edges (relationships)
    # Gene encodes protein
    kg.add_edge(KGEdge(
        source_id="gene_vav1",
        target_id="protein_vav1",
        edge_type=EdgeType.ENCODES
    ))

    kg.add_edge(KGEdge(
        source_id="gene_il2",
        target_id="protein_il2",
        edge_type=EdgeType.ENCODES
    ))

    # Proteins participate in pathways
    kg.add_edge(KGEdge(
        source_id="protein_vav1",
        target_id="pathway_tcell_activation",
        edge_type=EdgeType.PARTICIPATES_IN,
        confidence=0.95
    ))

    kg.add_edge(KGEdge(
        source_id="protein_il2",
        target_id="pathway_cytokine",
        edge_type=EdgeType.PARTICIPATES_IN,
        confidence=0.99
    ))

    # VAV1 regulates IL2
    kg.add_edge(KGEdge(
        source_id="gene_vav1",
        target_id="gene_il2",
        edge_type=EdgeType.REGULATES,
        confidence=0.85,
        evidence_count=5,
        source_papers=["paper_vav1_il2_2020"]
    ))

    # Paper supports the finding
    kg.add_edge(KGEdge(
        source_id="paper_vav1_il2_2020",
        target_id="finding_vav1_il2",
        edge_type=EdgeType.REPORTS
    ))

    # Finding supports the relationship
    kg.add_edge(KGEdge(
        source_id="finding_vav1_il2",
        target_id="gene_vav1",
        edge_type=EdgeType.SUPPORTS,
        confidence=0.85
    ))

    return kg


# Utility functions for loading/creating KG

def load_kg_from_file(filepath: str) -> Optional[KnowledgeGraph]:
    """Load a knowledge graph from a JSON file if it exists."""
    if os.path.exists(filepath):
        return KnowledgeGraph.load(filepath)
    return None


def get_or_create_kg(filepath: str, create_sample: bool = True) -> KnowledgeGraph:
    """Get existing KG or create a new one with sample data."""
    kg = load_kg_from_file(filepath)
    if kg is None:
        if create_sample:
            kg = create_sample_biology_kg()
            kg.save(filepath)
        else:
            kg = KnowledgeGraph()
    return kg
