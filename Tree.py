from Node import TreeNode
from collections import deque

def bst_min(root):
    curr = root
    while curr and curr.left:
        bst_min(curr)
    return curr

# Time Complexity: Worst case: O(logn)    
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
            
            
# DFS Algorithms
# Time Complexity: O(n)             
def inorder_dfs(root, target):
    if not root:
        return
    result = []
    inorder_dfs(root.left, target)
    print(root.val)
    if (root.val == target):
        return root
    inorder_dfs(root.right, target)
    
def revorder_dfs(root, target):
    if not root:
        return
    result = []
    revorder_dfs(root.right, target)
    print(root.val)
    if root.val == target:
        return root
    revorder_dfs(root.left, target)
    
def bst_preorder(root):
    if not root:
        return
    result = []
    print(root.val)
    bst_preorder(root.left)
    bst_preorder(root.right)
    
def bst_postorder(root):
    if not root:
        return
    result = []
    bst_postorder(root.left)
    bst_postorder(root.right)
    print(root.val)
    
# BFS Algorithms
def tree_bfs(root, target):
    nodeQueue = deque()
    
    if root:
        nodeQueue.append(root)
    level = 0
    while len(nodeQueue) > 0:
        print("level: ", level)
        for i in range(len(nodeQueue)):
            curr = nodeQueue.popleft()
            print(curr.val)
            if (curr.val == target):
                return curr
            if curr.left:
                nodeQueue.append(curr.left, target)
            if curr.right:
                nodeQueue.append(curr.right, target)
        level += 1
    