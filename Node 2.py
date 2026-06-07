class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_node(self, node):
        self.children.append(node)