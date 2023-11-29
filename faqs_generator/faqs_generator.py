import pydot # mostly for types
from typing import List, Dict
import re
from pprint import pformat
from .grammars import town_weap_grammar, weap_dun_grammar, dun_boss_weap_grammar, dun_boss_arm_grammar, town_arm_grammar, arm_dun_grammar, boss_key_grammar, key_town_grammar
import tracery
from copy import deepcopy

class FaqsGenerator():
    """ Class to handle state while going through the generative process-- also contains some helper
        methods for pulling useful generative information out of nodes of a graph.
    Attributes:
        characters (List[Dict]): list of character information for this FAQ.
        seen (List[Dict]): some scratch space for being able to hold onto context from nodes that were seen a long time ago
        type_name_elem_rgx (Pattern): a regex to pull out salient information from a node name
        type_name_rgx (Pattern): a regex to pull out salient information from a node name
    """
    characters: List[Dict]
    seen:List[Dict] # some scratch space for contexts for generation

    # these regexes suck, but whatever. try to match the first one, if no match, fallback to the second
    type_name_elem_rgx = re.compile(r"^(?P<type>\w+?)_(?P<name>\w+)_(?P<elem>\w+)$")
    type_name_rgx = re.compile(r"^(?P<type>\w+?)_(?P<name>\w+)")
    
    def __init__(self):
        """ Constructor
        """
        self.characters = []
        self.seen = []
        

    def generate_text(self, source:pydot.Node, dest:pydot.Node) -> None:
        """ Given an edge (as described by it's source and destination nodes), find the
            relevant grammar and generate text!
        Args:
            source (Node): the source node for our directed edge
            dest (Node): the destination node for our directed edge
        """
         # should really be classes but _here we are_
        src_dict = self._extract_node(source.get_name())
        dest_dict = self._extract_node(dest.get_name())
        
        # ok, given src_dict, dest_dict and the seen list, we should be able to pick & augment a grammar
        if src_dict["type"] == "Town" and dest_dict["type"] == "Weap":
            edge_grammar = deepcopy(town_weap_grammar)
            # need to add the town name and the weapon name
            edge_grammar["town"].append(src_dict["name"])
            edge_grammar["weap"].append(dest_dict["name"])

            grammar = tracery.Grammar(edge_grammar)
            text = grammar.flatten("#origin#")
            print(text + "\n\n")
        elif src_dict["type"] == "Town" and dest_dict["type"] == "Arm":
            edge_grammar = deepcopy(town_arm_grammar)
            # need to add the town name and the armor name
            edge_grammar["town"].append(src_dict["name"])
            edge_grammar["arm"].append(dest_dict["name"])

            grammar = tracery.Grammar(edge_grammar)
            text = grammar.flatten("#origin#")
            print(text + "\n\n")
        elif src_dict["type"] == "Weap" and dest_dict["type"] == "Dun":
            edge_grammar = deepcopy(weap_dun_grammar)
            
            # augment with weap, dun and town
            edge_grammar["town"].append(self.seen[0]["name"]) #awful, just drek
            edge_grammar["weap"].append(src_dict["name"])
            edge_grammar["dun"].append(dest_dict["name"])

            grammar = tracery.Grammar(edge_grammar)
            text = grammar.flatten("#origin#")
            print(text + "\n\n")
        elif src_dict["type"] == "Arm" and dest_dict["type"] == "Dun":
            edge_grammar = deepcopy(arm_dun_grammar)
            
            # augment with weap, dun and town
            edge_grammar["town"].append(self.seen[0]["name"]) #awful, just drek
            edge_grammar["arm"].append(src_dict["name"])
            edge_grammar["dun"].append(dest_dict["name"])

            grammar = tracery.Grammar(edge_grammar)
            text = grammar.flatten("#origin#")
            print(text + "\n\n")
        elif src_dict["type"] == "Dun" and dest_dict["type"] == "Boss":
            seen_equip = [ctx_elem for ctx_elem in self.seen if ctx_elem["type"] == "Weap" or ctx_elem["type"] == "Arm"][0]
            if seen_equip["type"] == "Weap":
                edge_grammar = deepcopy(dun_boss_weap_grammar)
                # augment with dun, weap, boss, elem
                edge_grammar["dun"].append(src_dict["name"])
                edge_grammar["weap"].append(seen_equip["name"])
                edge_grammar["boss"].append(dest_dict["name"])
                edge_grammar["elem"].append(seen_equip["elem"])
            elif seen_equip["type"] == "Arm":
                edge_grammar = deepcopy(dun_boss_arm_grammar)
                # augment with dun, weap, boss, elem
                edge_grammar["dun"].append(src_dict["name"])
                edge_grammar["arm"].append(seen_equip["name"])
                edge_grammar["boss"].append(dest_dict["name"])
                edge_grammar["elem"].append(seen_equip["elem"])

            grammar = tracery.Grammar(edge_grammar) #type:ignore I mean the complaint here is true
            text = grammar.flatten("#origin#")
            print(text + "\n\n")

        elif src_dict["type"] == "Boss" and dest_dict["type"] == "Key":
            edge_grammar = deepcopy(boss_key_grammar)

            edge_grammar["key"].append(dest_dict["name"])
            grammar = tracery.Grammar(edge_grammar)
            text = grammar.flatten("#origin#")
            print(text + "\n\n")

        elif src_dict["type"] == "Key" and dest_dict["type"] == "Town":
            edge_grammar = deepcopy(key_town_grammar)

            edge_grammar["key"].append(src_dict["name"])
            edge_grammar["town"].append(dest_dict["name"])

            grammar = tracery.Grammar(edge_grammar)
            text = grammar.flatten("#origin#")
            print(text + "\n\n")
        elif src_dict["type"] == "Start":
            print("NEED TO WRITE A GRAMMAR FOR THE START TO FIRST CHARACTER EDGE\n\n")
        elif dest_dict["type"] == "End":
            print("NEED TO WRITE A GRAMMAR FOR THE LAST KEY ITEM TO THE END NODE EDGE\n\n")
        elif src_dict["type"] == "Char" or dest_dict["type"] == "Char":
            print("NEED TO WRITE GRAMMARS FOR ANY CHARACTER RELATED EDGES\n\n")
        else:
            raise RuntimeError(f"No grammar found for {src_dict['type']} --> {dest_dict['type']}")

        # and then set the context for the _next_ round of generation
        self.extract_context(source, dest)
    def extract_context(self, start_node:pydot.Node, end_node:pydot.Node) -> None:
        """ given an edge (as the start/dest node), figure out what kind of edge it is and pull out the nodes we need for context
            This is forward-looking, adding context for the _next_ edge we'd encounter.
            This makes it spectacularly bad for anything but toy contexts
        Args:
            start_node (Node): the source node for our directed edge
            end_node (Node): the destination node for our directed edge
        """
        # should really be classes but _here we are_
        src_dict = self._extract_node(start_node.get_name())
        dest_dict = self._extract_node(end_node.get_name())

        # certain edges need to add context for the _next_ generation step
        if src_dict["type"] == "Town" and dest_dict["type"] == "Weap" or \
            src_dict["type"] == "Town" and dest_dict["type"] == "Arm":
            # add the town to the seen list
            self.seen.append(src_dict)
        elif src_dict["type"] == "Weap" and dest_dict["type"] == "Dun" or \
            src_dict["type"] == "Arm" and dest_dict["type"] == "Dun":
            self.seen = [] # reset seen
            self.seen.append(src_dict) # add the armor / weapon to the context
        elif src_dict["type"] == "Dun" and dest_dict["type"] == "Boss":
            # we need to get one node of context before dun
            self.seen.append(src_dict) # add the dungeon to the context
        elif src_dict["type"] == "Boss" and dest_dict["type"] == "Key":
            # clear the context
            self.seen = []
        elif dest_dict["type"] == "Char":
            self.characters.append(dest_dict)

    @classmethod
    def _extract_node(cls, node_name:str) -> Dict:
        """ Helper method to extract out semantic information from a node name, which has
            certain packed semantics
        Args:
            node_name (str): the name of a node. These are more or less in code, usually something like
                                [node type]_[node name]_[node attrs]
        Returns:
            dict: an unpacked, usable version of the semantic info in the node name
        """
        triple_match = cls.type_name_elem_rgx.match(node_name)
        if triple_match:
            return {
                "type": triple_match.group("type"),
                "name": triple_match.group("name"),
                "elem": triple_match.group("elem")
            }
        double_match = cls.type_name_rgx.match(node_name)
        if double_match:
            return {
                "type": double_match.group("type"),
                "name": double_match.group("name")
            }

        if node_name == "Start":
            return {
                "type": "Start",
                "name": node_name
            }
        
        if node_name == "End":
            return {
                "type": "End",
                "name": node_name
            }
        raise RuntimeError(f"Couldn't get information from {node_name}")