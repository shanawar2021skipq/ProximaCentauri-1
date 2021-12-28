class Solution(object):
    def isPalindrome(self, s):
        """
        :type s: str
        :rtype: bool
        """
        simplestring=''
        a= (65,90)
        b= (97,122)
        s = s.lower()
        for letter in s:
            if (ord(letter) in range(65,90)) :
                simplestring+=letter
            elif (ord(letter) in range(97,122)):
                simplestring+=letter
            elif (ord(letter) in range(48,58)):
                simplestring+=letter
        print(simplestring)
        
        reverse = simplestring[::-1]
        print(reverse)
        if simplestring == reverse:
            return True
        