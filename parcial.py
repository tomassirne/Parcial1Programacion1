#%%
import csv
import matplotlib.pyplot as plt
from datetime import datetime

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
def promedio_por_tipos(divorcios):
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
            elif "No declara" in k : dic_mn[k] = v 
            else: dic_mm[k] = v
        elif "Femenino" in k :
            if "No declara" in k : dic_fn[k] = v
            else: dic_ff[k] = v
        else: dic_nn[k] = v

    return {"Masculino-Masculino": duracion_promedio(dic_mm),"Masculino-Femenino": duracion_promedio(dic_mf),"Masculino-No declara": duracion_promedio(dic_mn),"Femenino-Femenino": duracion_promedio(dic_ff),"Femenino-No declara": duracion_promedio(dic_mm),"No declara-No declara": duracion_promedio(dic_mm)}
#%%
# ------ Ejercicio 3 -----------

def proporcion_divorcios_en_2018(diccionario):
    total_matrimonios_2018 = 0
    matrimonios_divorciados_2018 = 0

    for clave in diccionario:
        fecha_matrimonio = clave[2]  # FECHA_MATRIMONIO
        fecha_divorcio = clave[3]    # FECHA_DIVORCIO (si existe)

        # Convertir fecha de matrimonio en objeto datetime
        fecha_matrimonio = datetime.strptime(fecha_matrimonio, "%Y-%m-%d")

        # Verificar si el matrimonio fue en 2018
        if fecha_matrimonio.year == 2018:
            total_matrimonios_2018 += 1

            # Verificar si existe una fecha de divorcio
            if fecha_divorcio:
                fecha_divorcio = datetime.strptime(fecha_divorcio, "%Y-%m-%d")
                matrimonios_divorciados_2018 += 1

    if total_matrimonios_2018 == 0:
        return 0  # Evitar división por cero si no hay matrimonios en 2018

    # Calcular la proporción
    proporcion = matrimonios_divorciados_2018 / total_matrimonios_2018
    return proporcion



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
    for clave, valor in diccionario.items():
        genero_1, genero_2, anio_matrimonio, anio_divorcio = clave
        if anio_matrimonio == '2018' and anio_divorcio > '2018':
            tipo_matrimonio = f"{genero_1}-{genero_2}"
            # Aquí utilizamos setdefault para asegurar que la clave exista
            proporciones[tipo_matrimonio] = proporciones.setdefault(tipo_matrimonio, 0) + valor
            total_divorcios_2018 += valor


    # Calcular las proporciones
    if total_divorcios_2018 > 0:
        for tipo in proporciones:
            proporciones[tipo] /= total_divorcios_2018
    else:
        print("No hay divorcios registrados para parejas que se casaron en 2018.")

    return proporciones
        



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


def print_tabla(divorcios_por_año):
    print("Cantidad de divorcios por Año:")
    for año,divorcio in divorcios_por_año.items():
        print(f"{año}: {divorcio}")


def graficar_divorcios(divorcios):
    #Creao un dic del tipo {año: cant_divorcios}
    divorcios_por_año = {}
    for (_,_,_,ffin),v in divorcios.items():
        k = int(ffin)
        if k in divorcios_por_año.keys(): divorcios_por_año[k] += v
        else: divorcios_por_año[k] = v

    divorcios_por_año = dict(sorted(divorcios_por_año.items()))

    print_tabla(divorcios_por_año)


    #Creo 3 dics separando en prepandemia, pandemia y postpandemia
    divorcios_pandemia = {}
    divorcios_pre_pandemia = {}
    divorcios_post_pandemia = {}
    for año,div in divorcios_por_año.items():
        if año <= 2020: divorcios_pre_pandemia[año] = div
        if año in [2020,2021,2022]: divorcios_pandemia[año] = div
        if año >= 2022: divorcios_post_pandemia[año] = div

    plt.plot(list(divorcios_pre_pandemia.keys()),list(divorcios_pre_pandemia.values()),color='b',marker='o', linestyle='-')
    plt.plot(list(divorcios_pandemia.keys()),list(divorcios_pandemia.values()),color='r',marker='o', linestyle='-')
    plt.plot(list(divorcios_post_pandemia.keys()),list(divorcios_post_pandemia.values()),color='b',marker='o', linestyle='-')
    plt.xlabel("Año")
    plt.ylabel("Divorcios")
    plt.suptitle("Cantidad de Divorcios por Año", fontsize = 14)
    plt.title('En rojo vemos los años afectados por la pandemia. En azul, el resto de los años',fontsize= 10)
    plt.show()


def meses_divorcio(archivo,año):
    with open(archivo, 'rt', encoding='utf-8-sig') as f:
        rows = csv.reader(f)
        headers = next(rows)
        meses = set()

        for row in rows:
            record = dict(zip(headers, row))
            if record["FECHA_MATRIMONIO"][5:9] == str(año): meses.add(record["FECHA_MATRIMONIO"][2:5])
        
    return meses
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
# Usar la función con el diccionario generado por catalogar()
diccionario = catalogar("dataset_divorcios.csv")
proporcion = proporcion_divorcios_en_2018(dic)

# Mostrar el resultado
print(f"Proporción de matrimonios registrados en 2018 que se divorciaron: {proporcion:.2%}")
#%%
# --------- Ejercicio 4 ---------
# llamada de funcion
proporciones_2018 = proporciones_divorcios_por_genero_2018(dic)
plt.bar(proporciones_2018.keys(), proporciones_2018.values(), color=["skyblue"], width=0.8)
plt.xlabel("Tipo de Matrimonio")
plt.ylabel("Proporción de Divorcios en 2018")
plt.title("Proporción de Divorcios por Género en 2018")
plt.xticks(rotation=45)  # Rotar las etiquetas del eje x para mejor legibilidad
plt.show()
#%%
# ------ Ejercicio 5 ----------
graficar_divorcios(dic)
print("Teniendo en cuenta que la pandemia abarcó del año 2020 al 2022, observamos que la misma aumentó la cantidad de divorcios")
print("Cabe destacar que el año 2020 fue un año particular por dos razones. En primer lugar, la pandemia empezo a afectar a Argentina en Marzo, por lo tanto el mes de Enero y Febrero continuan con la tendencia de los años prepandemia. En segundo lugar fue caracterizado por un encierro casi absoluto de la poblacion, lo que produjo que no se pudiera tramitar el divorcio")
print("Esto justifica que el año 2020 fuese un año bajo en cantidad de divorcios a pesar de que la pandemia aumentó los mismos.")
#Para demostrar que no se registraron divorcios en todos los meses del 2020, crearemos la siguiente funcion:
print(meses_divorcio(archivo,2020))


dic_pre,dic_pandemia,dic_post = catalogar_pademia(archivo)
"""
Pre Pandemia: 02 nov 2015 - 20 mar 2020 => 1600 dias
Pandemia: 20 mar 2020 - 31 mar 2022 => 741 dias
Post Pandemia: 31 mar 2022 - 20 sep 2024 => 904 dias
"""
inicio_dataset = datetime.strptime("2015-11-02", "%Y-%m-%d")
inicio_pandemia = datetime.strptime("2020-03-20", "%Y-%m-%d")
fin_pandemia = datetime.strptime("2022-03-31", "%Y-%m-%d")
fin_dataset = datetime.strptime("2024-09-20", "%Y-%m-%d")

prom_d1 = sum(dic_pre.values()) / (inicio_pandemia-inicio_dataset).days
prom_d2= sum(dic_pandemia.values()) / (fin_pandemia-inicio_pandemia).days
prom_d3 = sum(dic_post.values()) / (fin_dataset-fin_pandemia).days

proms = [prom_d1,prom_d2,prom_d3]
labels = ['Pre Pandemia', 'Pandemia', 'Post Pandemia']

plt.bar(labels, proms, color=['blue', 'green', 'red'])

# Añade títulos y etiquetas
plt.xlabel('Periodo')
plt.ylabel('Promedio de Divorcios')
plt.title('Promedio de Divorcios por Período')

# Muestra el gráfico
plt.show()

#%%
