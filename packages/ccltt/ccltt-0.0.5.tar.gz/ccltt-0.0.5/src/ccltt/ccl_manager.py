import json
import re
from .ccl_tt_tree import CclTtTree
from .data_base import MyDatabase
from .ccl_tt_node import CclTtNode, CclTtNodes
from collections import OrderedDict


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
        elif ty == "int list":
            father.add(name, [int(val) for val in value])
        elif ty == "real list":
            father.add(name, [float(val) for val in value])
    else:
        father.add(name)
    node = father.get(name)
    for child_data in data.get('children', []):
        build_tree(node,child_data)


def parse_config_to_dict(config_text):
    #先创建一个根节点
    root = {
        "name": "root",
        "children": []
    }
    current_node = root
    stack = [current_node]
    lines = config_text.splitlines()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("//"):
            continue
        #如果这一行是一个名字，并且接下来一行是一个{
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', line):
            new_node = {
                "name": line,
                "children": []
            }
            current_node["children"].append(new_node)
            stack.append(current_node)
        elif line == "{":
            current_node = new_node
        elif line == "}":
            if stack:
                stack.pop()
                if stack:
                    current_node = stack[-1]
                else:
                    current_node = root
        elif re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*.*$', line):
            #如果这一行是一个名字=值
            name, value = line.split("=", 1)
            name = name.strip()
            value = value.strip()
            name = name.strip('"')
            value = value.strip('"')
            type = "str"
            if value.lower() == "true":
                value = True
                type = "bool"
            elif value.lower() == "false":
                value = False
                type = "bool"
            elif re.match(r'^\d+$', value):
                value = int(value)
                type = "int"
            elif re.match(r'^\d+\.\d+$', value):
                value = float(value)
                type = "real"
            #1.0e-5
            elif re.match(r'^\d+\.?\d*[eE][+-]?\d+$', value):
                value = float(value)
                type = "real"
            #0.0,0.0,1.0
            elif re.match(r'^\d+(,\d+)*$', value):
                value = [int(val) for val in value.split(",")]
                type = "int list"
            elif re.match(r'^\d+(\.\d+)?(,\d+(\.\d+)?)*$', value):
                value = [float(v) for v in value.split(",")]
                type = "real list"
            #velocity[0]=0.0;velocity[1]=0.0;velocity[2]=0.0;
            elif re.match(r'(\w+\[?\d*\]?)=("[^"]*"|[^;]+)', value):
                pattern = r'(\w+\[?\d*\]?)=("[^"]*"|[^;]+)'
                value_node = {
                    "name": name,
                    "children": []
                }
                for key, v in re.findall(pattern, value):
                    key = key.strip()
                    v = v.strip()
                    type = "str"
                    if v.startswith('"') and v.endswith('"'):
                        v = v[1:-1]
                        type = "str"
                    if re.match(r'^\d+$', v):
                        v = int(v)
                        type = "int"
                    elif re.match(r'^\d+\.\d+$', v):
                        v = float(v)
                        type = "real"
                    elif re.match(r'^\d+\.?\d*[eE][+-]?\d+$', v):
                        v = float(v)
                        type = "real"
                    elif re.match(r'^\d+(,\d+)*$', v):
                        v = [int(val) for val in v.split(",")]
                        type = "int list"
                    elif re.match(r'^\d+(\.\d+)?(,\d+(\.\d+)?)*$', v):
                        v = [float(val) for val in v.split(",")]
                        type = "real list"
                    value_node["children"].append({"name": key, "value": v, "type": type})
                current_node["children"].append(value_node)
                continue

            value_node = {
                "name": name,
                "value": value,
                "type": type,
            }
            current_node["children"].append(value_node)
        else:
            print(f"无法解析的行: {line}")
            return None
    return root
        


def build_tree_from_json(path: str):
    with open(path, "r", encoding="utf-8") as f:
        config_text = f.read()
    root =  parse_config_to_dict(config_text)
    # with open('output.json', 'w', encoding='utf-8') as f:
    #     json.dump(root, f, ensure_ascii=False, indent=4)
    #得到json数据格式
    json_str = json.dumps(root, indent=4, ensure_ascii=False)
    data = json.loads(json_str, object_pairs_hook=OrderedDict)
    manager = CclManager()
    tree = manager.trees["source"]
    root = tree.ROOT()
    for child_data in data.get('children', []):
        build_tree(root,child_data)
    return manager
