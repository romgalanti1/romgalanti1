class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        n=len(nums)
        d=dict()
        for i in range(n):
            complement=target-nums[i]
            if complement in d:
                return i,d[complement]
            else:
                d[nums[i]]=i


            