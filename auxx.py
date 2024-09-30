import matplotlib.pyplot as plt
from datetime import datetime

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


diferencia = (datetime.strptime("2020-03-20", "%Y-%m-%d")-datetime.strptime("2015-11-02", "%Y-%m-%d")).days
print(diferencia)



labels = ['Manzanas', 'Bananas', 'Cerezas', 'Dátiles']
sizes = [35, 25, 25, 15]
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
explode = (0.1, 0, 0, 0)  # Resalta la primera porción

# Crear el gráfico de torta
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)

# Añadir título
plt.title('Distribución de Frutas')

# Mostrar el gráfico
plt.show()


def a():
    c=2
    b=3
    return c,b

f  = list(a())

print(type(f))


# Datos
grupos = ['G1', 'G2', 'G3', 'G4', 'G5']
valores1 = [12, 19, 14, 27, 16]
valores2 = [21, 30, 15, 17, 20]

fig, ax = plt.subplots()

# Gráfico de barras apiladas
ax.bar(grupos, valores1)
ax.bar(grupos, valores2, bottom = valores1)

plt.show() 
 
