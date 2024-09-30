import matplotlib.pyplot as plt

a = "26SEP2019:09:24:50"

print(a[0:2])

t = ("N","F")
if "M" in t:
    if "F" in t: print("M-F")
    elif "N" in t : print("M-N")
    else: print("M-M")
elif "F" in t :
    if "N" in t : print("F-N")
    else: print("F-F")
else: print("N-N")




d = {("a","f"):1,("b","f"):2}
ls = [k[0] for k,v in d.items() for i in range(v)]
print(ls)
