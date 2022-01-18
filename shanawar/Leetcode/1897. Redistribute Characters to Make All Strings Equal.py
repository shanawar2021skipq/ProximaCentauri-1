class Solution(object):
    def makeEqual(self, words):
        """
        :type words: List[str]
        :rtype: bool
        """
        joint = ''.join(words)
        dic = {}
        
        for i in joint :
            if i not in dic :
                dic[i] = joint.count(i)
                
        for v in dic.values() :
            if v % len(words) != 0 : return False 
        return True
