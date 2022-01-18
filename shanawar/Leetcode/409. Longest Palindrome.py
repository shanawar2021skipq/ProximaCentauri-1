class Solution(object):
    def longestPalindrome(self, s):
        """
        :type s: str
        :rtype: int
        """
        d = collections.Counter(s)
        odd, ans = 0, 0
        
        for x in d:
            if d[x] % 2:
                odd += 1
            ans += d[x]

        return min(ans, ans - odd + 1)
