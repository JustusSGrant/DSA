from collections import deque

# Can only be run on a pre-sorted array
# Time efficiency: O(logn)
def binary_search(self, nums: List[int], target: int) -> int:
        if not nums:
            return -1
        i = len(nums) // 2
        if nums[i] == target:
            return i
        elif nums[i] > target:
            return self.search(nums[:i], target)
        else:
            res = self.search(nums[i+1:], target)
            return i + 1 + res if res != -1 else -1
        
# Time Complexity when the tree is not balanced (worst case) O(n), best case logn
def binary_search_tree(self, root, target):
    if not root:
        return False
    
    if target > root.val:
        return self.binary_search_tree(root.right, target)
    elif target < root.val:
        return self.binary_search_tree(root.left, target)
    else:
        return True
    
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
    