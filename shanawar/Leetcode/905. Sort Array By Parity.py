class Solution(object):
    def sortArrayByParity(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        """
        o=[]
        e=[]
        for i in nums:
            if(i%2==0):
                o.append(i)
            else:
                e.append(i)
        return o+e
