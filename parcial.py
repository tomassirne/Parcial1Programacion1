#%%
import csv
import matplotlib.pyplot as plt

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

# ------ Ejercicio 5 ----------
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





# ------ Ejercicio 0 ----------
archivo = "dataset_divorcios.csv"
dic = catalogar(archivo)



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



# ------ Ejercicio 5 ----------
graficar_divorcios(dic)
print("Teniendo en cuenta que la pandemia abarcó del año 2020 al 2022, observamos que la misma aumentó la cantidad de divorcios")
print("Cabe destacar que el año 2020 fue un año particular por dos razones. En primer lugar, la pandemia empezo a afectar a Argentina en Marzo, por lo tanto el mes de Enero y Febrero continuan con la tendencia de los años prepandemia. En segundo lugar fue caracterizado por un encierro casi absoluto de la poblacion, lo que produjo que no se pudiera tramitar el divorcio")
print("Esto justifica que el año 2020 fuese un año bajo en cantidad de divorcios a pesar de que la pandemia aumentó los mismos.")
#Para demostrar que no se registraron divorcios en todos los meses del 2020, crearemos la siguiente funcion:
print(meses_divorcio(archivo,2020))
