a = "26SEP2019:09:24:50"

print(a[5:9])

t = ("N","F")
if "M" in t:
    if "F" in t: print("M-F")
    elif "N" in t : print("M-N")
    else: print("M-M")
elif "F" in t :
    if "N" in t : print("F-N")
    else: print("F-F")
else: print("N-N")


tu = (2,5,3)
t[1] = 6
print(t)