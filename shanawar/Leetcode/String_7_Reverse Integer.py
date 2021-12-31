class Solution(object):
    def reverse(self, x):
        """
        :type x: int
        :rtype: int
        """
        s=str(x)
        x=s.replace('-','')
        x=abs(int((x[::-1])))
        if s[0]=='-':
            x= -1*x 
        if 2**31-1 > x > -2**31:
            return x
        return 0
