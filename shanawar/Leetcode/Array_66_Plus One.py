class Solution(object):
    def plusOne(self, digits):
        """
        :type digits: List[int]
        :rtype: List[int]
        """
        for i in reversed(range(len(digits))):
            if (digits[i]!=9):
                digits[i]+=1
                break
            else:
                digits[i]=0
        if (digits[0]==0):
            digits.insert(0,1)
        return digits
            
