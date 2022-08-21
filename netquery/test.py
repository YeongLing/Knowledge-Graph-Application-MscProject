class Solution:
    def shiftingLetters(self, s, shifts):
        s=list(s.encode())
        diff=[0 for i in range(len(s))]
        diff[0]=0
        for i in range(1,len(s)):
            diff[i]=s[i]-s[i-1]
        for shift in shifts:
            start,end=shift[0],shift[1]
            if shift[2]==0:
                diff[start]-=1
                if end<len(s)-1:
                    diff[end+1]+=1
            else:
                diff[start]+=1
                if end<len(s)-1:
                    diff[end+1]-=1
        for j in range(len(diff)):
            if j==0:
                temp=s[0]+diff[0]
            else:
                temp=s[j-1]+diff[j]
            while not ord('a')<=temp<=ord('z'):
                if temp>ord('z'):
                    temp-=26
                else:
                    temp+=26
            s[j]=temp
        return ''.join(map(chr,s))

solution=Solution()
s = 'abc'
shifts = [[0,1,0],[1,2,1],[0,2,1]]
print(solution.shiftingLetters(s,shifts))
