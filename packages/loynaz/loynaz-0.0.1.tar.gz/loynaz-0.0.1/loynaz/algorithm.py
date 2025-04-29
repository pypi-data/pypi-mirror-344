# Created on 02/05/2025
# Author: Frank Vega

import itertools
from . import utils

import networkx as nx
import baldor.algorithm as alg

def find_edge_dominating(graph):
    """
    Compute an approximate minimum edge dominating set set for an undirected graph by transforming it into a chordal graph.

    Args:
        graph (nx.Graph): A NetworkX Graph object representing the input graph.

    Returns:
        set: A set of vertex indices representing the minimum edge dominating set set.
             Returns an empty set if the graph is empty or has no edges.
    """
    # Check if the input graph is a valid undirected NetworkX Graph; raises an error if not.
    if not isinstance(graph, nx.Graph):
        raise ValueError("Input must be an undirected NetworkX Graph.")

    # Handle edge cases: return an empty set if the graph has no nodes or no edges, as no edge dominating set is needed.
    if graph.number_of_nodes() == 0 or graph.number_of_edges() == 0:
        return set()

    # Remove all self-loop edges since they cannot be part of an edge dominating set.
    graph.remove_edges_from(list(nx.selfloop_edges(graph)))
    # Remove isolated nodes from the graph to process the remaining components, as they do not contribute to an edge dominating set.
    graph.remove_nodes_from(list(nx.isolates(graph)))

    # After removing isolated nodes, if the graph is empty, return an empty set (no edge dominating set needed).
    if graph.number_of_nodes() == 0:
        return set()

    # Initialize an empty set to store the approximate edge dominating set.
    approximate_edge_dominating = set()

    # Iterate over each connected component of the graph to compute the edge dominating set independently.
    for component in nx.connected_components(graph):
        # Extract the subgraph corresponding to the current connected component.
        subgraph = graph.subgraph(component)

        # Handle small components: if the subgraph has 2 or fewer edges, select one edge to dominate all edges in the component.
        if subgraph.number_of_edges() <= 2:
            # Add the first edge from the subgraph to the edge dominating set and move to the next component.
            approximate_edge_dominating.add(next(iter(set(subgraph.edges()))))
            continue    

        # Transform the subgraph into a line graph, where nodes represent edges of the subgraph, and edges represent adjacency between edges.
        line_graph = nx.line_graph(subgraph)    

        # Use Baldor's 2-approximation algorithm to find a dominating set in the line graph.
        # This dominating set corresponds to an edge dominating set in the original graph via the transformation.
        edge_dominating = alg.find_dominating_set(line_graph)

        # Add the edges from the dominating set (representing edges in the original subgraph) to the approximate edge dominating set.
        approximate_edge_dominating.update(edge_dominating)

    # Return the computed approximate edge dominating set set.
    return approximate_edge_dominating


def find_edge_dominating_brute_force(graph):
    """
    Computes an exact minimum edge dominating set in exponential time.

    Args:
        graph: A NetworkX Graph.

    Returns:
        A set of vertex indices representing the exact edge dominating set, or None if the graph is empty.
    """

    if graph.number_of_nodes() == 0 or graph.number_of_edges() == 0:
        return None

    # Remove all self-loop edges
    graph.remove_edges_from(list(nx.selfloop_edges(graph)))
    # Remove isolated nodes from the graph to process the remaining components
    graph.remove_nodes_from(list(nx.isolates(graph)))

    n_edges = len(graph.edges())

    for k in range(1, n_edges + 1): # Iterate through all possible sizes
        for candidate in itertools.combinations(graph.edges(), k):
            edge_candidate = set(candidate)
            if utils.is_edge_dominating_set(graph, edge_candidate):
                return edge_candidate
                
    return None



def find_edge_dominating_approximation(graph):
    """
    Computes an approximate edge dominating set in polynomial time with an approximation ratio of at most 2 for undirected graphs.

    Args:
        graph: A NetworkX Graph.

    Returns:
        A set of vertex indices representing the approximate edge dominating set, or None if the graph is empty.
    """

    if graph.number_of_nodes() == 0 or graph.number_of_edges() == 0:
        return None

    #networkx doesn't have a guaranteed minimum edge dominating set function, so we use approximation
    edge_dominating = nx.approximation.dominating_set.min_edge_dominating_set(graph)
    return edge_dominating