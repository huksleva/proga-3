def TwoSum(nums, target):
    res = []
    for i in range(len(nums)-1):
        for g in range(i+1, len(nums)):
            if nums[i] + nums[g] == target:
                res.append([i, g])
    return res