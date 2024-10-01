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
from datetime import datetime

def leer_fechas_matrimonios(archivo_csv):
    """Lee las fechas de los matrimonios desde un archivo CSV."""
    fechas = []
    with open(archivo_csv, 'r') as csvfile:
        lector = csv.reader(csvfile)
        next(lector)  # Saltar la cabecera
        for fila in lector:
            try:
                fecha_matrimonio = datetime.strptime(fila[0], "%Y-%m-%d")
                fechas.append(fecha_matrimonio)
            except ValueError:
                pass  # Ignora registros con formato de fecha inválido
    return fechas

def contar_matrimonios_2018(fechas):
    """Cuenta los matrimonios registrados en 2018 a partir de una lista de fechas."""
    contador = 0
    for fecha in fechas:
        if fecha.year == 2018:
            contador += 1
    return contador


def contar_divorcios_2018(diccionario):
  contador = 0
  for clave, valor in diccionario.items():
    if clave[2] == '2018':
      contador += valor
  return contador




#%%
# --------- Ejercicio 4 -------
def proporciones_divorcios_por_genero_2018(diccionario):
    proporciones = {
        "Masculino-Masculino": 0,
        "Masculino-Femenino": 0,
        "Femenino-Femenino": 0,
        "Masculino-No declara": 0,
        "Femenino-No declara": 0,
        "No declara-No declara": 0
    }
    total_divorcios_2018 = 0

    # Recorrer el diccionario
    for clave, valor in diccionario.items():
        # Verificar que la clave tiene exactamente 4 elementos
        if len(clave) == 4:
            genero_1, genero_2, anio_matrimonio, anio_divorcio = clave
            
            # Convertir años a enteros para comparar correctamente
            if int(anio_matrimonio) == 2018 and int(anio_divorcio) >= 2018:
                tipo_matrimonio = f"{genero_1}-{genero_2}"
                
                # Sumar al total de divorcios
                proporciones[tipo_matrimonio] = proporciones.setdefault(tipo_matrimonio, 0) + valor
                total_divorcios_2018 += valor
        else:
            print(f"Clave con formato incorrecto: {clave}, omitiendo este registro.")
    
    # Calcular las proporciones
    if total_divorcios_2018 > 0:
        for tipo in proporciones:
            proporciones[tipo] /= total_divorcios_2018
    else:
        print("No hay divorcios registrados para parejas que se casaron en 2018.") 
    
    return proporciones


# Función que integra la separación de tipos y el cálculo de proporciones
def calcular_proporciones_con_separacion(diccionario):
    # Llamar a la función separa_tipos que ya tienes implementada
    tipos_separados = separa_tipos(diccionario)  # Separa los tipos de matrimonios
    
    proporciones_totales = {}

    # Iterar sobre los diccionarios separados que están dentro de la tupla
    for sub_diccionario in tipos_separados:
        # Verificar que sea un diccionario
        if isinstance(sub_diccionario, dict):
            # Calcular las proporciones para el sub-diccionario de cada tipo de matrimonio
            proporciones_por_tipo = proporciones_divorcios_por_genero_2018(sub_diccionario)
            
            # Añadir la proporción del tipo actual a las proporciones totales
            for tipo, proporcion in proporciones_por_tipo.items():
                proporciones_totales[tipo] = proporciones_totales.get(tipo, 0) + proporcion
    
    return proporciones_totales


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
dic = catalogar(archivo)
#%%


# ------ Ejercicio 1 ----------
duracion = duracion_matrimonios_divorciados(dic)
print(f"La duracion maxima de matrimonios que se divorciaron es {duracion_matrimonios_divorciados(dic)[0]} años.")
print(f"La duracion minima de matrimonios que se divorciaron es {duracion_matrimonios_divorciados(dic)[1]} años.")
print(f"La duracion promedio de matrimonios que se divorciaron es {duracion_matrimonios_divorciados(dic)[2]:.2f} años.")
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

prom_tipos = promedio_por_tipos(dic)
for k,v in prom_tipos.items():
    print(f"La duracion promedio de matrimonios {k} que se divorciaron es {v:.2f} años.")
    #%%
# -------- Ejercicio 3 ---------
# Ejemplo de uso
archivo_csv = 'matrimonios_2018.csv'
fechas_matrimonios = leer_fechas_matrimonios(archivo_csv)
numero_matrimonios_2018 = contar_matrimonios_2018(fechas_matrimonios)


# Llamar a las funciones
matrimonios_2018 = contar_matrimonios_2018(fechas_matrimonios)
divorcios_2018 = contar_divorcios_2018(dic)

# Calcular la proporción de divorcios
proporcion_divorcios = divorcios_2018/ matrimonios_2018 if matrimonios_2018 > 0 else 0

print("Total de matrimonios en 2018:", matrimonios_2018)
print("Total de divorcios de matrimonios de 2018:", divorcios_2018)
print("Proporción de divorcios respecto al total de matrimonios en 2018:", f"{proporcion_divorcios:.2%}")


labels = ['Casados', 'Divorciados']
sizes = [matrimonios_2018 - divorcios_2018, divorcios_2018]
colors = ['lightskyblue','lightcoral']
explode = (0.1, 0)  # Resalta la primera porción

# Crear el gráfico de torta
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
plt.title('Distribución de Matrimonios del 2018')
plt.show()
#%%
# --------- Ejercicio 4 ---------
# Ejemplo de uso
# Supongo que ya tienes el diccionario de registros de divorcios `dic`
proporciones_2018 = calcular_proporciones_con_separacion(dic)

# Visualización de las proporciones usando un gráfico de barras
import matplotlib.pyplot as plt

plt.bar(proporciones_2018.keys(), proporciones_2018.values(), color="skyblue", width=0.8)
plt.xlabel("Tipo de Matrimonio")
plt.ylabel("Proporción de Divorcios en 2018")
plt.title("Proporción de Divorcios por Género en 2018")
plt.xticks(rotation=45)  # Rotar las etiquetas del eje x para mejor legibilidad
plt.show()
#colors = ['lightskyblue', 'lightcoral', 'lightseagreen', 'lightpink', 'lightgoldenrodyellow', 'lightgreen']
#explode = (0.1, 0, 0, 0, 0, 0)  # Resalta la primera porción
#plt.pie(proporciones_2018.values(), explode=explode, labels=proporciones_2018.keys(), colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)

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

prom_d1 = sum(dic_pre.values()) / (inicio_pandemia-inicio_dataset).days
prom_d2= sum(dic_pandemia.values()) / (fin_pandemia-inicio_pandemia).days
prom_d3 = sum(dic_post.values()) / (fin_dataset-fin_pandemia).days

proms = [prom_d1,prom_d2,prom_d3]
labels = ['Pre Pandemia', 'Pandemia', 'Post Pandemia']
colors = ['yellowgreen', 'lightcoral', 'lightskyblue']
plt.bar(labels, proms, color=colors)
plt.title('Promedio de Divorcios por Período')
plt.show()


duracion_pre = duracion_promedio(dic_pre)
duracion_pandemia = duracion_promedio(dic_pandemia)
duracion_post = duracion_promedio(dic_post)

duraciones = [duracion_pre,duracion_pandemia,duracion_post]
print(duraciones)
plt.bar(labels, duraciones, color=colors)
plt.title('Duracion Promedio de Divorcios por Período')
plt.show()


tipos_pre = [sum(d.values()) / (inicio_pandemia-inicio_dataset).days for d in separa_tipos(dic_pre)] 
tipos_pandemia = [sum(d.values()) / (fin_pandemia-inicio_pandemia).days for d in separa_tipos(dic_pandemia)] 
tipos_post = [sum(d.values()) / (fin_dataset-fin_pandemia).days for d in separa_tipos(dic_post)] 

prop_pre = [ x / sum(tipos_pre) for x in tipos_pre]
prop_pandemia = [ x / sum(tipos_pandemia) for x in tipos_pandemia]
prop_post = [ x / sum(tipos_post) for x in tipos_post]

#valores = np.array([prop_pre, prop_pandemia,prop_post]).T
valores = np.array([tipos_pre, tipos_pandemia,tipos_post]).T

fig, ax = plt.subplots()

# Crear las barras apiladas
for i in range(len(valores)):
    if i == 0:
        ax.bar(labels, valores[i], label=f'Valor {i+1}')
    else:
        ax.bar(labels, valores[i], bottom=np.sum(valores[:i], axis=0), label=f'Valor {i+1}')

# Añadir etiquetas, título y leyenda
ax.set_xlabel('Valores')
ax.set_ylabel('Proporciones')
ax.set_title('Proporcion de Divorcios por Tipo por Periodo')
plt.show()
#%%
print(fechas_matrimonios)

