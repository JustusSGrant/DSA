from collections import deque

from Node import TreeNode

def bst_min(root):
    curr = root
    while curr and curr.left:
        curr = curr.left
    return curr
  
def bst_insert_node(root, val):
    if not root:
        return TreeNode(val)
    
    if val > root.val:
        root.right = bst_insert_node(root.right, val)
    elif val < root.val:
        root.left = bst_insert_node(root.left, val)
    return root

def bst_remove_node(root, val):
    if not root:
        return None
    
    if val > root.val:
        root.right = bst_remove_node(root.right, val)
    elif val < root.val:
        root.left = bst_remove_node(root.left, val)
    else:
        if not root.left:
            return root.right
        elif not root.right:
            return root.left
        else:
            minNode = bst_min(root.right)
            root.val = minNode.val
            root.right = bst_remove_node(root.right, minNode.val)
            return root
            
# Left -> Root -> Right
def in_order_traversal(root):
    result = []
    def depth_first_search(node):
        if not node:
            return
        depth_first_search(node.left)
        result.append(node.val)
        depth_first_search(node.right)
    depth_first_search(root)
    return result

# Root -> Left -> Right
def pre_order_traversal(root):
    result = []
    def depth_first_search(node):
        if not node:
            return
        result.append(node.val)
        depth_first_search(node.left)
        depth_first_search(node.right)
    depth_first_search(root)
    return result
    
# Left -> Right -> Root
def post_order_traversal(root):
    result = []
    def depth_first_search(node):
        if not node:
            return
        depth_first_search(node.left)
        depth_first_search(node.right)
        result.append(node.val)
    depth_first_search(root)
    return result

def level_order(root): # BFS
    if not root:
        return[]
    result = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                    queue.append(node.right)
        result.append(level)
    return result