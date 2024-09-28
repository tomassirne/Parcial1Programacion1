import csv


def catalogar(archivo):
    with open(archivo, 'rt', encoding='utf-8-sig') as f:
        rows = csv.reader(f)
        headers = next(rows)
        diccionario = {}

        for row in rows:
            record = dict(zip(headers, row))
            clave = (record["GENERO_1"],record["GENERO_2"],record["FECHA_MATRIMONIO"],record["FECHA_CREACION"])
            

            if clave in diccionario: diccionario[clave] += 1
            else: diccionario[clave] = 1
        

    return diccionario

print(catalogar("dataset_divorcios.csv"))