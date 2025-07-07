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
    
