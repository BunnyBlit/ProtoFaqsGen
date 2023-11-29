""" CLI to Do The Thing: takes in a built graph (in the DOT language) and runs through it,
    emitting generated text as it goes.
    Takes in a single argument, which is a DOT file of the graph. The graph itself must have
    certain semantics, see the readme
"""
import pydot
from typing import List, Callable
from pathlib import Path
from argparse import ArgumentParser

from faqs_generator.faqs_generator import FaqsGenerator


def _dfs_walk(cur_node:pydot.Node, graph:pydot.Dot, callback:Callable) -> None:
    """ Walk an acyclic graph (tree?) depth-first. This may need to account for cycles at some point.
        Fire callback at each edge, which is how we generate text!
    Args:
        cur_node (Node): the node we're currently at
        graph (Dot): the directed graph we're walking
        callback (Callable): a callback function to fire on every edge to generate text
                            needs to take in two nodes to represent an edge
    """
    edges = graph.get_edge_list()
    for edge in edges:
        if edge.get_source() == cur_node.get_name():
            next = graph.get_node(edge.get_destination())[0] # this sucks, but should always work
            # we want to trigger some event here
            callback(cur_node, next) # I _happen_ to know this signature, but I should annotate it
            # recurse using the destination
            _dfs_walk(next, graph, callback)

def generate_faq(args):
    """Do the thing! Generate a FAQ from the CLI arguments. Read in a file, find the start node
        walk the graph, generating text at every edge
    Args:
        args (Namespace): the parsed CLI arguments
    """
    input_file:Path = args.file
    graphs:List[pydot.Dot] | None = pydot.graph_from_dot_file(input_file)
    generator = FaqsGenerator()
    if graphs: #someday python'll have a null-coalesing operator
        for graph in graphs:
            # walk the graph, which is gonna be a little annoying
            # even though its just a single sequence of events
            # pydot's API is _awful_ so we're doing it this way
            start_node:pydot.Node = graph.get_node("Start")[0] #it's invalid to have more than one start, although that can be handled better
            _dfs_walk(start_node, graph, generator.generate_text)


def build_parser() -> ArgumentParser:
    """Utility function to build out the parser we use to parse CLI arguments
    """
    parser = ArgumentParser(description="A tool to parse an annotated graph and emit the information we'd pass to a grammar")
    parser.add_argument("-f", "--file", type=Path, help="Path to an input graph file")
    parser.set_defaults(func=generate_faq)
    return parser

if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
