import csv


def catalogar(archivo):
    with open(archivo, 'rt', encoding='utf-8-sig') as f:
        rows = csv.reader(f)
        headers = next(rows)
        diccionario = {}

        for row in rows:
            record = dict(zip(headers, row))
            if record["GENERO_1"] == "": record["GENERO_1"] = "No declara"
            if record["GENERO_2"] == "": record["GENERO_2"] = "No declara"
        
            clave = (record["GENERO_1"],record["GENERO_2"],record["FECHA_MATRIMONIO"][5:9],record["FECHA_CREACION"][5:9])
            

            if clave in diccionario: diccionario[clave] += 1
            else: diccionario[clave] = 1
        

    return diccionario

dic = catalogar("dataset_divorcios.csv")
print(dic)
print(len(dic.keys()))


