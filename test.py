a = [0,1,2]
b = [0,3,6]
c = [0,9,18]
d = [0,27,54]
e = [0,81,162]
ans = []

for i in a:
    for ii in b:
        for iii in c:
            for iiii in d:
                for iiiii in e:
                    l = i + ii + iii + iiii + iiiii
                    if l in ans:
                        print(f"Fails at {l}")
                    else:
                        ans.append(l)

for i in range(243):
    print(i)
    if i not in ans:
        print(f'{i} not in')
