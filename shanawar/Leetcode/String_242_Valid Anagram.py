class Solution(object):
    def isAnagram(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: bool
        
        count if characters in strings are equal
        """
        if (len(s)!=len(t)):
            return False
        for i in s:
            if (s.count(i) == t.count(i)):
                continue
            elif (t.count(i) != s.count(i)):
                return False
        return True


        
        