import json
from .ccl_tt_tree import CclTtTree
from .data_base import MyDatabase
from .ccl_tt_node import CclTtNode, CclTtNodes


class CclManager:
    def __init__(self):
        self.db = MyDatabase()
        self.trees = {}
        self.init_tree("source")
    
    def init_tree(self, name: str):
        if name in self.trees:
            return False
        tree = CclTtTree(name, self.db)
        self.trees[name] = tree
        return tree

def build_tree(father:CclTtNodes,data):
    name = data["name"]
    ty = data.get("type", None)
    value = data.get("value", None)
    if ty is not None and value is not None:
        if ty == "int":
            father.add(name, int(value))
        elif ty == "bool":
            father.add(name, bool(value))
        elif ty == "str":
            father.add(name, str(value))
        elif ty == "real":
            father.add(name, float(value))
    else:
        father.add(name)
    node = father.get(name)
    for child_data in data.get('children', []):
        build_tree(node,child_data)

def build_tree_from_json(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    manager = CclManager()
    tree = manager.trees["source"]
    root = tree.ROOT()
    build_tree(root,data)
    return manager

        