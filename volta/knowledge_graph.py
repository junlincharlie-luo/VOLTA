"""
Knowledge Graph module for VOLTA.

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

    # Battery/Raman domain nodes
    MATERIAL = "material"  # LiCoO2, NCM811, NCA, etc.
    RAMAN_PEAK = "raman_peak"  # Eg mode, A1g mode, D-band, G-band (features embedded as properties)
    ELECTROCHEMICAL_PARAM = "electrochemical_param"  # Voltage, SOC
    STRUCTURAL_PROPERTY = "structural_property"  # M-O bond, cation ordering

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

    # Battery/Raman relationships
    SHIFTS_WITH = "shifts_with"  # Peak -> electrochemical param (position change)
    CORRELATES_WITH = "correlates_with"  # Feature -> parameter
    OBSERVED_IN = "observed_in"  # Peak -> material
    HAS_PEAK_AT = "has_peak_at"  # Material -> peak
    INDICATES = "indicates"  # Feature -> property
    INCREASES_WITH = "increases_with"  # Feature increases with parameter
    DECREASES_WITH = "decreases_with"  # Feature decreases with parameter

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


def create_raman_battery_kg() -> KnowledgeGraph:
    """
    Create knowledge graph for Raman battery analysis from literature.

    This KG captures relationships between:
    - Raman peak features (position, width, intensity for Eg, A1g, D-band, G-band)
    - Electrochemical parameters (voltage, SOC)
    - Structural properties (M-O bond, cation ordering, oxygen redox)

    Each Raman peak has 3 separate feature nodes (position, width, intensity).
    All relationships cite their source literature.
    """
    kg = KnowledgeGraph()

    # =========================================================================
    # RAMAN PEAK FEATURE NODES (12 nodes: 4 peaks × 3 features)
    # =========================================================================

    # Eg mode features
    kg.add_node(KGNode(
        id="eg_position",
        node_type=NodeType.RAMAN_PEAK,
        name="Eg position",
        properties={
            "peak": "Eg",
            "feature_type": "position",
            "wavenumber_range": [475, 488],
            "unit": "cm⁻¹",
            "description": "Eg peak center wavenumber, sensitive to M-O bond angle"
        },
        aliases=["Eg peak position", "Eg center"]
    ))

    kg.add_node(KGNode(
        id="eg_width",
        node_type=NodeType.RAMAN_PEAK,
        name="Eg width",
        properties={
            "peak": "Eg",
            "feature_type": "width",
            "unit": "cm⁻¹",
            "description": "Eg FWHM, indicates structural disorder"
        },
        aliases=["Eg FWHM", "Eg sigma"]
    ))

    kg.add_node(KGNode(
        id="eg_intensity",
        node_type=NodeType.RAMAN_PEAK,
        name="Eg intensity",
        properties={
            "peak": "Eg",
            "feature_type": "intensity",
            "unit": "a.u.",
            "description": "Eg amplitude, reflects M-O bond population"
        },
        aliases=["Eg amplitude", "Eg area"]
    ))

    # A1g mode features
    kg.add_node(KGNode(
        id="a1g_position",
        node_type=NodeType.RAMAN_PEAK,
        name="A1g position",
        properties={
            "peak": "A1g",
            "feature_type": "position",
            "wavenumber_range": [545, 610],
            "unit": "cm⁻¹",
            "description": "A1g peak center wavenumber, sensitive to M-O bond length"
        },
        aliases=["A1g peak position", "A1g center"]
    ))

    kg.add_node(KGNode(
        id="a1g_width",
        node_type=NodeType.RAMAN_PEAK,
        name="A1g width",
        properties={
            "peak": "A1g",
            "feature_type": "width",
            "unit": "cm⁻¹",
            "description": "A1g FWHM, indicates cation ordering/disorder"
        },
        aliases=["A1g FWHM", "A1g sigma"]
    ))

    kg.add_node(KGNode(
        id="a1g_intensity",
        node_type=NodeType.RAMAN_PEAK,
        name="A1g intensity",
        properties={
            "peak": "A1g",
            "feature_type": "intensity",
            "unit": "a.u.",
            "description": "A1g amplitude, reflects oxygen participation in bonding"
        },
        aliases=["A1g amplitude", "A1g area"]
    ))

    # D-band features
    kg.add_node(KGNode(
        id="dband_position",
        node_type=NodeType.RAMAN_PEAK,
        name="D-band position",
        properties={
            "peak": "D-band",
            "feature_type": "position",
            "wavenumber_range": [1340, 1360],
            "unit": "cm⁻¹",
            "description": "D-band peak center (~1350 cm⁻¹)"
        },
        aliases=["D peak position", "D center"]
    ))

    kg.add_node(KGNode(
        id="dband_width",
        node_type=NodeType.RAMAN_PEAK,
        name="D-band width",
        properties={
            "peak": "D-band",
            "feature_type": "width",
            "unit": "cm⁻¹",
            "description": "D-band FWHM, indicates defect distribution"
        },
        aliases=["D FWHM", "D sigma"]
    ))

    kg.add_node(KGNode(
        id="dband_intensity",
        node_type=NodeType.RAMAN_PEAK,
        name="D-band intensity",
        properties={
            "peak": "D-band",
            "feature_type": "intensity",
            "unit": "a.u.",
            "description": "ID, used in ID/IG ratio for disorder quantification"
        },
        aliases=["ID", "D amplitude"]
    ))

    # G-band features
    kg.add_node(KGNode(
        id="gband_position",
        node_type=NodeType.RAMAN_PEAK,
        name="G-band position",
        properties={
            "peak": "G-band",
            "feature_type": "position",
            "wavenumber_range": [1580, 1600],
            "unit": "cm⁻¹",
            "description": "G-band peak center (~1585 cm⁻¹), shifts with charge transfer"
        },
        aliases=["G peak position", "G center"]
    ))

    kg.add_node(KGNode(
        id="gband_width",
        node_type=NodeType.RAMAN_PEAK,
        name="G-band width",
        properties={
            "peak": "G-band",
            "feature_type": "width",
            "unit": "cm⁻¹",
            "description": "G-band FWHM, indicates graphitic order"
        },
        aliases=["G FWHM", "G sigma"]
    ))

    kg.add_node(KGNode(
        id="gband_intensity",
        node_type=NodeType.RAMAN_PEAK,
        name="G-band intensity",
        properties={
            "peak": "G-band",
            "feature_type": "intensity",
            "unit": "a.u.",
            "description": "IG, reference for ID/IG ratio"
        },
        aliases=["IG", "G amplitude"]
    ))

    # =========================================================================
    # ELECTROCHEMICAL PARAMETER NODES
    # =========================================================================
    kg.add_node(KGNode(
        id="param_voltage",
        node_type=NodeType.ELECTROCHEMICAL_PARAM,
        name="Voltage",
        properties={
            "unit": "V",
            "typical_range": [2.5, 4.5],
            "description": "Cell potential vs Li/Li+"
        },
        aliases=["potential", "cell voltage", "V"]
    ))

    kg.add_node(KGNode(
        id="param_soc",
        node_type=NodeType.ELECTROCHEMICAL_PARAM,
        name="SOC",
        properties={
            "unit": "%",
            "range": [0, 100],
            "description": "State of charge - fraction of Li remaining in cathode"
        },
        aliases=["state of charge", "lithiation state", "x in LixMO2"]
    ))

    # =========================================================================
    # STRUCTURAL PROPERTY NODES
    # =========================================================================
    kg.add_node(KGNode(
        id="prop_mo_bond",
        node_type=NodeType.STRUCTURAL_PROPERTY,
        name="M-O bond length",
        properties={
            "unit": "Å",
            "description": "Metal-oxygen bond distance in MO6 octahedra"
        },
        aliases=["metal-oxygen bond", "M-O distance"]
    ))

    kg.add_node(KGNode(
        id="prop_cation_order",
        node_type=NodeType.STRUCTURAL_PROPERTY,
        name="Cation ordering",
        properties={
            "description": "Li/vacancy ordering in the lithium layer"
        },
        aliases=["Li ordering", "vacancy ordering", "cation arrangement"]
    ))

    kg.add_node(KGNode(
        id="prop_ox_redox",
        node_type=NodeType.STRUCTURAL_PROPERTY,
        name="Oxygen redox",
        properties={
            "description": "Lattice oxygen participation in charge compensation"
        },
        aliases=["anionic redox", "O2-/O- redox", "lattice oxygen oxidation"]
    ))

    # =========================================================================
    # EDGES: Peak Features -> Electrochemical Parameters
    # =========================================================================

    # A1g position -> Voltage (redshift during charge)
    kg.add_edge(KGEdge(
        source_id="a1g_position",
        target_id="param_voltage",
        edge_type=EdgeType.SHIFTS_WITH,
        properties={
            "direction": "redshift",
            "magnitude": "~22 cm⁻¹ during charge",
            "details": "A1g position redshifts during delithiation"
        },
        confidence=0.92,
        source_papers=["Cation Ordering and Redox Chemistry of Layered Ni-Rich LixNi1−2yCoyMnyO2..."]
    ))

    # A1g position -> SOC (strong negative correlation)
    kg.add_edge(KGEdge(
        source_id="a1g_position",
        target_id="param_soc",
        edge_type=EdgeType.CORRELATES_WITH,
        properties={
            "correlation": "r ≈ -0.88",
            "details": "Strong negative correlation between A1g position and SOC"
        },
        confidence=0.90,
        source_papers=["In situ and Operando Raman Spectroscopy of Layered Transition Metal Oxides..."]
    ))

    # A1g width -> Voltage (decreases during charge)
    kg.add_edge(KGEdge(
        source_id="a1g_width",
        target_id="param_voltage",
        edge_type=EdgeType.DECREASES_WITH,
        properties={
            "magnitude": "-33% during charge",
            "details": "A1g FWHM decreases as voltage increases (better ordering)"
        },
        confidence=0.85,
        source_papers=["Cation Ordering and Redox Chemistry of Layered Ni-Rich LixNi1−2yCoyMnyO2..."]
    ))

    # A1g intensity -> Voltage (increases during charge)
    kg.add_edge(KGEdge(
        source_id="a1g_intensity",
        target_id="param_voltage",
        edge_type=EdgeType.INCREASES_WITH,
        properties={
            "magnitude": "+30% during charge",
            "details": "A1g intensity increases during charge"
        },
        confidence=0.82,
        source_papers=["Advanced Raman spectroscopy for battery applications..."]
    ))

    # Eg position -> SOC (blueshift with decreasing SOC)
    kg.add_edge(KGEdge(
        source_id="eg_position",
        target_id="param_soc",
        edge_type=EdgeType.SHIFTS_WITH,
        properties={
            "direction": "blueshift",
            "details": "Eg position shifts to higher wavenumber with decreasing SOC"
        },
        confidence=0.80,
        source_papers=["In situ and Operando Raman Spectroscopy of Layered Transition Metal Oxides..."]
    ))

    # Eg intensity -> Voltage (increases during charge)
    kg.add_edge(KGEdge(
        source_id="eg_intensity",
        target_id="param_voltage",
        edge_type=EdgeType.INCREASES_WITH,
        properties={
            "magnitude": "+28% during charge",
            "details": "Eg intensity increases during delithiation"
        },
        confidence=0.85,
        source_papers=["Cation Ordering and Redox Chemistry of Layered Ni-Rich LixNi1−2yCoyMnyO2..."]
    ))

    # G-band position -> Voltage (redshift)
    kg.add_edge(KGEdge(
        source_id="gband_position",
        target_id="param_voltage",
        edge_type=EdgeType.SHIFTS_WITH,
        properties={
            "direction": "redshift",
            "magnitude": "~3.5 cm⁻¹/V",
            "details": "G-band position redshifts with voltage (charge transfer)"
        },
        confidence=0.78,
        source_papers=["In-operando Raman study of lithium plating on graphite electrodes..."]
    ))

    # =========================================================================
    # EDGES: Peak Features -> Structural Properties
    # =========================================================================

    # A1g position -> M-O bond length
    kg.add_edge(KGEdge(
        source_id="a1g_position",
        target_id="prop_mo_bond",
        edge_type=EdgeType.INDICATES,
        properties={
            "details": "A1g position reflects M-O bond length - redshift indicates weakening"
        },
        confidence=0.90,
        source_papers=["In situ and Operando Raman Spectroscopy of Layered Transition Metal Oxides..."]
    ))

    # A1g width -> Cation ordering
    kg.add_edge(KGEdge(
        source_id="a1g_width",
        target_id="prop_cation_order",
        edge_type=EdgeType.INDICATES,
        properties={
            "details": "A1g FWHM sensitive to Li/vacancy ordering in Li layer"
        },
        confidence=0.88,
        source_papers=["Cation Ordering and Redox Chemistry of Layered Ni-Rich LixNi1−2yCoyMnyO2..."]
    ))

    # A1g intensity -> Oxygen redox
    kg.add_edge(KGEdge(
        source_id="a1g_intensity",
        target_id="prop_ox_redox",
        edge_type=EdgeType.INDICATES,
        properties={
            "details": "A1g intensity changes indicate oxygen participation in redox"
        },
        confidence=0.85,
        source_papers=["Capacity Decay Mechanism for Lithium-rich Layered Oxides..."]
    ))

    # Eg position -> M-O bond (angle)
    kg.add_edge(KGEdge(
        source_id="eg_position",
        target_id="prop_mo_bond",
        edge_type=EdgeType.INDICATES,
        properties={
            "details": "Eg position sensitive to O-M-O bond angle"
        },
        confidence=0.85,
        source_papers=["Advanced Raman spectroscopy for battery applications..."]
    ))

    # D-band intensity -> Carbon disorder (ID/IG)
    kg.add_edge(KGEdge(
        source_id="dband_intensity",
        target_id="prop_cation_order",
        edge_type=EdgeType.INDICATES,
        properties={
            "details": "D-band intensity (ID/IG ratio) indicates carbon disorder/defects"
        },
        confidence=0.80,
        source_papers=["In-operando Raman study of lithium plating on graphite electrodes..."]
    ))

    # =========================================================================
    # EDGES: Structural Property -> Electrochemical Parameter
    # =========================================================================
    kg.add_edge(KGEdge(
        source_id="prop_mo_bond",
        target_id="param_voltage",
        edge_type=EdgeType.CORRELATES_WITH,
        properties={
            "details": "M-O bond length changes with oxidation state during charge/discharge"
        },
        confidence=0.90,
        source_papers=["In situ and Operando Raman Spectroscopy of Layered Transition Metal Oxides..."]
    ))

    # =========================================================================
    # EDGES: Inter-Peak Feature Relationships
    # =========================================================================

    # ID/IG ratio: D-band and G-band intensities are used together
    kg.add_edge(KGEdge(
        source_id="dband_intensity",
        target_id="gband_intensity",
        edge_type=EdgeType.RELATED_TO,
        properties={
            "relationship": "ID/IG ratio",
            "details": "D-band and G-band intensities form ID/IG ratio for carbon disorder"
        },
        confidence=0.95,
        source_papers=["In-operando Raman study of lithium plating on graphite electrodes..."]
    ))

    # Eg and A1g positions are correlated (same structure)
    kg.add_edge(KGEdge(
        source_id="eg_position",
        target_id="a1g_position",
        edge_type=EdgeType.CORRELATES_WITH,
        properties={
            "details": "Eg and A1g modes from same R-3m structure, positions shift together"
        },
        confidence=0.85,
        source_papers=["In situ and Operando Raman Spectroscopy of Layered Transition Metal Oxides..."]
    ))

    # Eg and A1g intensities have inverse relationship during charge
    kg.add_edge(KGEdge(
        source_id="eg_intensity",
        target_id="a1g_intensity",
        edge_type=EdgeType.CORRELATES_WITH,
        properties={
            "details": "Eg/A1g intensity ratio changes with Li content, both increase during charge"
        },
        confidence=0.80,
        source_papers=["Cation Ordering and Redox Chemistry of Layered Ni-Rich LixNi1−2yCoyMnyO2..."]
    ))

    # A1g position and width are anti-correlated
    kg.add_edge(KGEdge(
        source_id="a1g_position",
        target_id="a1g_width",
        edge_type=EdgeType.CORRELATES_WITH,
        properties={
            "correlation": "negative",
            "details": "A1g redshift often accompanied by narrowing (improved ordering)"
        },
        confidence=0.82,
        source_papers=["Cation Ordering and Redox Chemistry of Layered Ni-Rich LixNi1−2yCoyMnyO2..."]
    ))

    # G-band position and D-band intensity relationship
    kg.add_edge(KGEdge(
        source_id="gband_position",
        target_id="dband_intensity",
        edge_type=EdgeType.CORRELATES_WITH,
        properties={
            "details": "G-band shift and D-band growth indicate carbon structural changes"
        },
        confidence=0.75,
        source_papers=["In-operando Raman study of lithium plating on graphite electrodes..."]
    ))

    return kg


def create_raman_battery_kg_v2() -> KnowledgeGraph:
    """
    Create v2 knowledge graph for Raman battery analysis from literature.

    Changes vs v1:
    - Adds explicit carbon disorder structural property.
    - Reroutes D-band intensity to carbon disorder (not cation ordering).
    - Keeps existing edges and nodes otherwise unchanged.
    """
    base_kg = create_raman_battery_kg()

    kg = KnowledgeGraph()
    for node in base_kg.nodes.values():
        kg.add_node(KGNode.from_dict(node.to_dict()))

    # Add explicit carbon disorder node
    kg.add_node(KGNode(
        id="prop_carbon_disorder",
        node_type=NodeType.STRUCTURAL_PROPERTY,
        name="Carbon disorder",
        properties={
            "description": "Graphitic disorder quantified by ID/IG from D/G bands"
        },
        aliases=["graphite disorder", "carbon defects", "ID/IG"]
    ))

    for edge in base_kg.edges:
        if (
            edge.source_id == "dband_intensity"
            and edge.target_id == "prop_cation_order"
            and edge.edge_type == EdgeType.INDICATES
        ):
            continue
        kg.add_edge(KGEdge.from_dict(edge.to_dict()))

    kg.add_edge(KGEdge(
        source_id="dband_intensity",
        target_id="prop_carbon_disorder",
        edge_type=EdgeType.INDICATES,
        properties={
            "details": "D-band intensity (ID/IG ratio) indicates carbon disorder/defects"
        },
        confidence=0.80,
        source_papers=["In-operando Raman study of lithium plating on graphite electrodes..."]
    ))

    return kg
