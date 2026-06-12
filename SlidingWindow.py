from typing import List


def variableLenSlidingWindow(self, arr):
    # find len of longest valid subset of unique chars
    left = 0
    longest = 0
    resultSet = set()
    n = len(arr)
    
    for right in range(n):
        # while invalid
        while arr[right] in resultSet:
            resultSet.remove(arr[left])
            left += 1
        windowLen = (right - left) + 1
        longest = max(longest, windowLen)
        resultSet.add(right)
    return longest
        
def fixedLenSlidingWindow(self, nums: List[int], k: int):
    # find max average of elements within contiguous subset of length = len
    aryLen = len(nums)
    curr_sum = 0
    # Build initial window and calculate avg
    for i in range (k):
        curr_sum += nums[i]
    max_avg = curr_sum / k
    
    # begin sliding window and recalculating
    for i in range (k, aryLen):
        curr_sum += nums[i] # shift right pointer forward and add the new value included in our window
        curr_sum -= nums[i - k] # shift left pointer forward and remove old val that has fallen outside of window
        max_avg = max(max_avg, curr_sum/k) # reset max avg is needed
    return max_avg