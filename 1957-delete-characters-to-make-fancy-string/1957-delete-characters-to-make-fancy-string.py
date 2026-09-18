class Solution(object):
    def makeFancyString(self, s):
        """
        :type s: str
        :rtype: str
        """
        n=len(s)
        if n<3:
            return s
        res=[s[0],s[1]]
        for i in range(2,n):
            if res[-1]==s[i] and res[-2]==s[i]:
                continue
            else:
                res.append(s[i])
        return "".join(res)

