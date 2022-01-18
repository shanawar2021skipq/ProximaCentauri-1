# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution(object):
    def levelOrder(self, root):
        """
        :type root: TreeNode
        :rtype: List[List[int]]
        """
        def _level(root, level, dict_levels):
            if root is None:
                return
            dict_levels[level] = dict_levels.get(level, []) + [root.val]
            _level(root.left, level + 1, dict_levels)
            _level(root.right, level + 1, dict_levels)
            
        d = {}
        _level(root, 0, d)
        return d.values()
        