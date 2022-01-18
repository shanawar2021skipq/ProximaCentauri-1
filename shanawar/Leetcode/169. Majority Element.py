class Solution(object):
    def majorityElement(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        num_len = len(nums)
        num_hash = {}
        for num in nums:
            num_hash[num] = num_hash.get(num, 0) + 1
            if num_hash[num] > num_len/2:
                return num

        