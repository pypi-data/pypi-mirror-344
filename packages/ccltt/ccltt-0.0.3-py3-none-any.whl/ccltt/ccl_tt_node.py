
import copy


class CclTtNode:
    def __init__(self, tree, node_id: int, name: str = None):
        self.tree = tree
        self.node_id = node_id
        self.name = name

    def __str__(self):
        return f"CclTtNode (id={self.node_id} name={self.name})"
    
    def value(self):
        return self.tree.db.get_node_value(self.tree.name, self.node_id)
    
    def type(self):
        return self.tree.db.get_node_type(self.tree.name, self.node_id)

    def __repr__(self):
        return self.__str__()
    
    def add(self, path: str):
        """自己添加一个子节点"""
        return self.tree.add_path(self.node_id, path)
    def get(self, path: str):
        return self.tree.find_by_path_with_wildcard(self.node_id, path)
        

class CclTtNodes:
    def __init__(self, nodes):
        self.nodes= nodes
    

    def __str__(self):
        return f"CclTtNodes (nodes: {self.nodes})"

    def __repr__(self):
        return self.__str__()

    def value(self):
        if len(self.nodes) != 1:
            return None
        return self.nodes[0].value()
    
    def type(self):
        if len(self.nodes) != 1:
            return None
        return self.nodes[0].type()

    def add(self, path, val = None):
        """自己添加一个子节点"""
        if not isinstance(path, str) and not isinstance(path, CclTtNodes):
            if self.add_link(val, path):
                return True
            return False
        elif val is not None:
            if self.add_val(path, val):
                return True
            return False
        elif isinstance(path, str):
            if self.add_dir(path):
                return True
            return False
        elif isinstance(path, CclTtNodes):
            if self.add_tree(path):
                return True
            return False
        
    
    def add_dir(self, path: str):
        """自己添加一个子节点"""
        for node in self.nodes:
            if not node.tree.add_path(node.node_id, path):
                return False
        return True
    
    def add_tree(self, nodes):
        if len(self.nodes) != 1:
            return False
        root_node = self.nodes[0]
        for node in nodes.nodes:
            if node.tree.name != root_node.tree.name:
                if( not root_node.tree.deep_copy(root_node.node_id, node.node_id, source_tree = node.tree.name)):
                    return False
            else:
                if( not root_node.tree.deep_copy(root_node.node_id, node.node_id)):
                    return False
        return True
    
    def add_val(self, path ,val):
        
        if isinstance(val, bool):
            for node in self.nodes:
                if not node.tree.add_val(node.node_id, path,"bool",val):
                    return False
            return True
        elif isinstance(val, str):
            for node in self.nodes:
                if not node.tree.add_val(node.node_id, path,"str",val):
                    return False
            return True
        elif isinstance(val, int):
            for node in self.nodes:
                if not node.tree.add_val(node.node_id, path,"int",val):
                    return False
            return True
        elif isinstance(val, float):
            for node in self.nodes:
                if not node.tree.add_val(node.node_id, path,"real",val):
                    return False
            return True

    def add_link(self, node, alias: str | None):
        if len(self.nodes) != 1:
            return False
        if len(node.nodes) != 1:
            return False
        root_node = self.nodes[0]
        add_node = node.nodes[0]
        if( not root_node.tree.add_link(root_node.node_id, add_node.node_id, alias)):
            return False
        return True
    
    def get(self, path: str):
        ans = []
        for node in self.nodes:
            ans.extend(node.tree.find_by_path_with_wildcard(node.node_id, path))
        if len(ans) == 0:
            return None
        return CclTtNodes(ans)
    
    def name(self):
        if len(self.nodes) == 1:
            return self.nodes[0].name
        return None
    
    def copy(self):
        return CclTtNodes(copy.copy(self.nodes))
    
    def delete(self, path = None):
        """删除节点"""
        if path is  None:
            for node in self.nodes:
                node.tree.delete_node_and_children(node.node_id)
            del self
            return
        node = self.get(path)
        if node is None:
            return
        node.delete()
        return 
    
    def rename(self, name1: str ,name2 :str = None):
        if name2 is None:
            if len(self.nodes) == 1:
                self.nodes[0].name = name1
                return True
            else:
                return False
        else:
            chul_node =  self.get(name1)
            if chul_node is None:
                return False
            chul_node.rename(name2)
            return True

        

def merge(a:CclTtNodes, b:CclTtNodes, c = None):
    """两个节点的并集"""
    if a is None:
        return b
    if b is None:
        return a
    return CclTtNodes(a.nodes + b.nodes)

def remove(a:CclTtNodes, b:CclTtNodes):
    a_copy = a.copy()
    for node in a_copy.nodes:
        for node2 in b.nodes:
            if node.node_id == node2.node_id and node.tree.name == node2.tree.name:
                a_copy.nodes.remove(node)
    return a_copy