class Solution(object):
    def reversePrefix(self, word, ch):
        """
        :type word: str
        :type ch: str
        :rtype: str
        """
        a=word.find(ch)
        b=(word[:a+1])
        return( b[::-1]+word[a+1:])
        
        