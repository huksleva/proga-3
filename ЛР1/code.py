def sum(nums, target):
    for i in range(len(nums)-1):
        for g in range(i+1, len(nums)):
            if nums[i] + nums[g] == target:
                print(i, g)
