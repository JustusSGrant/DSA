from Node import TreeNode

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