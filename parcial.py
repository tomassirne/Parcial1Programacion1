#%%
import csv

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
from datetime import datetime

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


# ------ Ejercicio 0 ----------
dic = catalogar("dataset_divorcios.csv")
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
proporcion = proporcion_divorcios_en_2018(diccionario)

# Mostrar el resultado
print(f"Proporción de matrimonios registrados en 2018 que se divorciaron: {proporcion:.2%}")