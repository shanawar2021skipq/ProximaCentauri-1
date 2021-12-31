class Solution(object):
    def containsDuplicate(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """
        if (max(Counter(nums).values())>1):
            return True
        else:
            return False