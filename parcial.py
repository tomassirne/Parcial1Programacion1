#%%
import csv
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

# ------ Ejercicio 0 ----------
def catalogar(archivo):
    with open(archivo, 'rt', encoding='utf-8-sig') as f:
        rows = csv.reader(f)
        headers = next(rows)
        diccionario = {}

        for row in rows:
            record = dict(zip(headers, row))
            if record["GENERO_1"] == "": record["GENERO_1"] = "No declara"
            if record["GENERO_2"] == "": record["GENERO_2"] = "No declara"
            
            #Hay dos registros cuya fecha de matrimonio es 01/01/1760 y fecha de divorcio es en 2024. 
            #Asimismo hay un registro con fecha de matrimonio en el año 3201.
            #Entendemos que son errores del dataset por lo tanto los filtraremos
            if record["FECHA_MATRIMONIO"][5:9] == "1760" or record["FECHA_MATRIMONIO"][5:9] == "3201": pass
            else: 
                clave = (record["GENERO_1"],record["GENERO_2"],record["FECHA_MATRIMONIO"][5:9],record["FECHA_CREACION"][5:9])
            

                if clave in diccionario: diccionario[clave] += 1
                else: diccionario[clave] = 1
        
    return diccionario
#%%

# ------ Ejercicio 1 ----------
def duracion_maxima(divorcios):
    return max([int(ffin) - int(finicio) for (gen1,gen2,finicio,ffin) in divorcios.keys()])

def duracion_minima(divorcios):
    return min([int(ffin) - int(finicio) for (gen1,gen2,finicio,ffin) in divorcios.keys()])

def duracion_promedio(divorcios):
    return sum([(int(ffin) - int(finicio)) * divorcios[(gen1,gen2,finicio,ffin)] for (gen1,gen2,finicio,ffin) in divorcios.keys()]) / sum(divorcios.values())

def duracion_matrimonios_divorciados(divorcios):
    return duracion_maxima(divorcios), duracion_minima(divorcios), duracion_promedio(divorcios)
#%%


# ------ Ejercicio 2 ----------
def separa_tipos(divorcios):
    #Creo un dic para cada tipo de matrimonio:  
    # m -> masculino, f -> femenino, n-> no declara
    dic_mm = {}  
    dic_ff = {}  
    dic_mf = {}  
    dic_nn = {} 
    dic_fn = {} 
    dic_mn = {}  

    for k,v in divorcios.items():
        if "Masculino" in k:
            if "Femenino" in k: dic_mf[k] = v 
            elif "No declara" in k or "X" in k or "Indefinido" in k : dic_mn[k] = v 
            else: dic_mm[k] = v
        elif "Femenino" in k :
            if "No declara" in k or "X" in k or "Indefinido" in k : dic_fn[k] = v
            else: dic_ff[k] = v
        else: dic_nn[k] = v
    
    return dic_mm,dic_ff,dic_mf,dic_nn,dic_fn,dic_mn

def promedio_por_tipos(divorcios): 
    dic_mm,dic_ff,dic_mf,dic_nn,dic_fn,dic_mn = separa_tipos(divorcios)

    return {"Masculino-Masculino": duracion_promedio(dic_mm),"Masculino-Femenino": duracion_promedio(dic_mf),"Masculino-No declara": duracion_promedio(dic_mn),"Femenino-Femenino": duracion_promedio(dic_ff),"Femenino-No declara": duracion_promedio(dic_fn),"No declara-No declara": duracion_promedio(dic_nn)}
#%%
# ------ Ejercicio 3 -----------

def catalogar_matrimonios(archivo):
    with open(archivo, 'rt', encoding='utf-8-sig') as f:
        rows = csv.reader(f)
        headers = next(rows)
        diccionario = {}

        for row in rows:
            record = dict(zip(headers, row))
            if record["genero_1"] == "": record["genero_1"] = "No declara"
            if record["genero_2"] == "": record["genero_2"] = "No declara"
        
            clave = (record["genero_1"],record["genero_2"],record["fecha_matrimonio"][0:4])

            if clave in diccionario: diccionario[clave] += 1
            else: diccionario[clave] = 1
    return diccionario

def contar_matrimoniosdiv_2018(diccionario):
  contador = 0
  for clave, valor in diccionario.items():
    if clave[2] == '2018':
      contador += valor
  return contador


#%%
# ------ Ejercicio 5 ----------
def catalogar_pademia(archivo):
    with open(archivo, 'rt', encoding='utf-8-sig') as f:
        rows = csv.reader(f)
        headers = next(rows)
        dic_pre = {}
        dic_pandemia = {}
        dic_post = {}

        for row in rows:
            record = dict(zip(headers, row))
            if record["GENERO_1"] == "": record["GENERO_1"] = "No declara"
            if record["GENERO_2"] == "": record["GENERO_2"] = "No declara"
            
            #Hay dos registros cuya fecha de matrimonio es 01/01/1760 y fecha de divorcio es en 2024. 
            #Asimismo hay un registro con fecha de matrimonio en el año 3201.
            #Entendemos que son errores del dataset por lo tanto los filtraremos
            if record["FECHA_MATRIMONIO"][5:9] == "1760" or record["FECHA_MATRIMONIO"][5:9] == "3201": pass

            else:
                clave = (record["GENERO_1"],record["GENERO_2"],record["FECHA_MATRIMONIO"][5:9],record["FECHA_CREACION"][5:9])

                if int(record["FECHA_CREACION"][5:9]) < 2020 or (int(record["FECHA_CREACION"][5:9]) == 2020 and (record["FECHA_CREACION"][2:5] in ["JAN","FEB"] or (record["FECHA_CREACION"][2:5] == "MAR" and int(record["FECHA_CREACION"][0:2]) < 20 ))) :
                    if clave in dic_pre: dic_pre[clave] += 1
                    else: dic_pre[clave] = 1
                elif int(record["FECHA_CREACION"][5:9]) > 2022 or (int(record["FECHA_CREACION"][5:9]) == 2022 and record["FECHA_CREACION"][2:5] in ["JAN","FEB","MAR"]):
                    if clave in dic_post: dic_post[clave] += 1
                    else: dic_post[clave] = 1
                else:
                    if clave in dic_pandemia: dic_pandemia[clave] += 1
                    else: dic_pandemia[clave] = 1
        
    return dic_pre,dic_pandemia,dic_post

#%%




# ------ Ejercicio 0 ----------
archivo = "dataset_divorcios.csv"
dic_div = catalogar(archivo)
#%%


# ------ Ejercicio 1 ----------
duracion = duracion_matrimonios_divorciados(dic_div)
print(f"La duracion maxima de matrimonios que se divorciaron es {duracion_matrimonios_divorciados(dic_div)[0]} años.")
print(f"La duracion minima de matrimonios que se divorciaron es {duracion_matrimonios_divorciados(dic_div)[1]} años.")
print(f"La duracion promedio de matrimonios que se divorciaron es {duracion_matrimonios_divorciados(dic_div)[2]:.2f} años.")
#%%


# ------ Ejercicio 2 ----------

"""
Tipos de Matrimonio:
    Masculino - Masculino
    Masculino - Femenino
    Femenino - Femenino
    Masculino - No declara
    Femenino - No declara
    No declara - No declara
"""

prom_tipos = promedio_por_tipos(dic_div)
for k,v in prom_tipos.items():
    print(f"La duracion promedio de matrimonios {k} que se divorciaron es {v:.2f} años.")

#%%
# -------- Ejercicio 3 ---------
archivo_csv = 'matrimonios_2018.csv'
dic_matrimonios = catalogar_matrimonios(archivo_csv)
matrimonios_2018 = contar_matrimoniosdiv_2018(dic_matrimonios)

divorcios_2018 = contar_matrimoniosdiv_2018(dic_div)

# Calcular la proporción de divorcios
proporcion_divorcios = divorcios_2018/ matrimonios_2018

print("Total de matrimonios en 2018:", matrimonios_2018)
print("Total de divorcios de matrimonios de 2018:", divorcios_2018)
print("Proporción de divorcios respecto al total de matrimonios en 2018:", f"{proporcion_divorcios:.2%}")


labels = ['Casados', 'Divorciados']
sizes = [matrimonios_2018 - divorcios_2018, divorcios_2018]
colors = ['lightskyblue','lightcoral']
explode = (0.1, 0)

# Crear el gráfico de torta
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
plt.title('Distribución de Matrimonios del 2018 y sus Divorcios')
plt.show()
#%%
# --------- Ejercicio 4 ---------
matrimonios_separados = separa_tipos(dic_matrimonios)
divorcios_separados = separa_tipos(dic_div)

recuento_divorcios = [contar_matrimoniosdiv_2018(tipo) for tipo in divorcios_separados]
recuento_matrimonios = [contar_matrimoniosdiv_2018(tipo) for tipo in matrimonios_separados]

prop_divorcios = [recuento_divorcios[i] / recuento_matrimonios[i] for i in range(len(recuento_divorcios))]
prop_matrimonios = [(recuento_matrimonios[i]-recuento_divorcios[i]) /recuento_matrimonios[i] for i in range(len(recuento_matrimonios))]

# Gráfico de barras apiladas
fig, ax = plt.subplots()
tipos= ["M-M","F-F","M-F","N-N","F-N","M-N"]
ax.bar(tipos, prop_matrimonios, label="Casados",color='lightskyblue')
ax.bar(tipos, prop_divorcios, bottom = prop_matrimonios, label="Divorciados", color='lightcoral')
plt.title("Proporción de Matrimonios del 2018 y sus Divorcios por Tipos")
ax.legend(loc = 'lower right')
plt.show()

for i in range(len(tipos)):
    print(f"El total de matrimonios {tipos[i]} en 2018 fue de: {recuento_matrimonios[i]}. De los cuales, {recuento_divorcios[i]} se divorciaron. ({prop_divorcios[i]*100 :.1f}%)")

print(f"De los matrimonio que alguno de sus integrantes no declaró genero hay pocos datos y estos no constituyen una muestra significativa; por lo tanto no es conveniente sacar conclusiones de los mismos.")
print(f'------------------------------------')
print(f'En el ejercicio 2, notamos que la duracion promedio de los matrimonios que se divorcian siendo del mismo genero, duran un aproximado de 6 años; por lo tannto es natural que estos tipos de matrimonios tengan la proporcion mas alta, calculando el periodo(periodo 2018-2024)')
print(f'------------------------------------')
print(f'Si hacemos este analisis dentro de un par de años, los resultados seran posiblementes distintos, ya que habra mas tiempo para posibles divorcios de otros tipos de matrimonio.')
#%%
# ------ Ejercicio 5 ----------
"""
Pre Pandemia: 02 nov 2015 - 20 mar 2020 => 1600 dias
Pandemia: 20 mar 2020 - 31 mar 2022 => 741 dias
Post Pandemia: 31 mar 2022 - 20 sep 2024 => 904 dias
"""
dic_pre,dic_pandemia,dic_post = catalogar_pademia(archivo)

inicio_dataset = datetime.strptime("2015-11-02", "%Y-%m-%d")
inicio_pandemia = datetime.strptime("2020-03-20", "%Y-%m-%d")
fin_pandemia = datetime.strptime("2022-03-31", "%Y-%m-%d")
fin_dataset = datetime.strptime("2024-09-20", "%Y-%m-%d")
tiempo_dataset = (fin_dataset-inicio_dataset).days

prom_d1 = sum(dic_pre.values()) / (inicio_pandemia-inicio_dataset).days
prom_d2= sum(dic_pandemia.values()) / (fin_pandemia-inicio_pandemia).days
prom_d3 = sum(dic_post.values()) / (fin_dataset-fin_pandemia).days


proms = [prom_d1,prom_d2,prom_d3]

# Gráfico de barras
labels = ['Pre Pandemia', 'Pandemia', 'Post Pandemia']
colors = ['yellowgreen', 'lightcoral', 'lightskyblue']
plt.bar(labels, proms, color=colors)
plt.title('Promedio de Divorcios por Período')
plt.show()

total = sum(dic_pre.values())+sum(dic_pandemia.values())+sum(dic_post.values())
prop = [sum(dic_pre.values())/total,sum(dic_pandemia.values())/total,sum(dic_post.values())/total]

# Gráfico de torta
colors = ['lightskyblue', 'lightcoral', 'lightseagreen']
explode = (0, 0.1, 0) 
plt.pie(prop, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
plt.title("Proporcion de Divorcios en el Dataset")
plt.show()


print("Conclusiones:")
print("La pandemia elevó el número de divorcios")
print(f"Habiendo abarcado solo un {(fin_pandemia-inicio_pandemia).days /tiempo_dataset *100 :.1f}% del tiempo, en pandemia se divorciaron un {prop[1] *100 :.1f}% de los divorcios del dataset ")
#%%

