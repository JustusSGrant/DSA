# Kadane's Algorithm finds the max subarray by keeping a local and global max, and constantly compating adjacent arr elements to update them.
def maxSubArray(arr):
    globalMax = arr[0]
    localMax = arr[0]
    for num in arr[1:]:
        localMax = max(num, localMax + num)
        globalMax = max(globalMax, localMax)      
    return globalMax

def maxSubSequence(arr):
    positiveSum = sum(x for x in arr if x > 0)
    if positiveSum > 0:
        maxSubSequenceSum = positiveSum 
        maxSubSequenceArr = [x for x in arr if x > 0]
    else:
        maxSubSequenceSum = max(arr)
        maxSubSequenceArr = [max(arr)]
    return (maxSubSequenceSum, maxSubSequenceArr)
    