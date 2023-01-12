def solucion():
     import csv

     with open("AMAZON.csv") as archivo, open("analisis_archivo.csv", "w", newline = '') as archivo_nuevo:
        lector = csv.reader(archivo)
        escritor = csv.writer(archivo_nuevo, delimiter = '\t')

        next(lector) #Se salta el encabezado
        encabezado_nuevo = ["Fecha", "Comportamiento de la accion", "Ajuste Cuadratico de Close"]
        escritor.writerow(encabezado_nuevo)
        values_list = ["2021-05-03", 3484.729980, "2021-05-03", 3386.489990, 0, "2021-05-03", -1000000]
        i = 0   #Contador de datos/renglones para calcular promedio volumen
        for renglon in lector:
            renglon_a_escribir = [renglon[0], concepto(renglon[4], renglon[1]), operacion(renglon[4], renglon[5])]
            escritor.writerow(renglon_a_escribir)
            values_list = valores_json(renglon, values_list)
            i += 1
        values_list[4] = values_list[4] / i
        creador_json(values_list)
        

def concepto(str_close, str_open):
    close = eval(str_close)
    open = eval(str_open)

    if close - open > 0:
        concepto = "SUBE"
    if close - open < 0:
        concepto = "BAJA"
    if close - open == 0:
        concepto = "ESTABLE"
    
    return concepto

def operacion(str_close, str_adj_close):
    import math

    close = eval(str_close)
    adj_close = eval(str_adj_close)

    operacion = math.sqrt(math.pow((close - adj_close), 2))

    return operacion

#lista_valores = [fecha_open_bajo, str_open_bajo, fecha_close_alto, str_close_alto, suma_vol, fecha_dif_mayor, dif_mayor]
#linea         = [Date, Open, High, Low, Close, Adj Close, Volume]
def valores_json(linea, lista_valores):

    #Buscar el open más bajo y su fecha
    if eval(linea[1]) < lista_valores[1]:
        lista_valores[0] = linea[0]
        lista_valores[1] = eval(linea[1])

    #Buscar el close más alto y su fecha
    if eval(linea[4]) > lista_valores[3]:
        lista_valores[2] = linea[0]
        lista_valores[3] = eval(linea[4])

    #Buscar la diferencia absoluta más grande y su fecha
    low = eval(linea[3])
    high = eval(linea[2])
    dif_abs = abs(low - high)
    if dif_abs > lista_valores[6]:
        lista_valores[5] = linea[0]
        lista_valores[6] = dif_abs
    
    #Sumar los volumenes para calcular el promedio:
    lista_valores[4] = lista_valores[4] + eval(linea[6])

    return lista_valores

def creador_json(lista_valores):
    import json

    lista_claves = ["date_lowest_volume","lowest_volume", "date_lowest_open", "lowest_open","date_highest_close", "highest_close",\
        "mean_volume", "date_greatest_difference", "greatest_difference"]
    diccionario_json = {}
    for tupla in zip(lista_claves, lista_valores):
        diccionario_json[tupla[0]] = tupla[1]

    objeto_json = json.dumps(diccionario_json)
    with open("detalles.json", "w") as archivo_json:
        archivo_json.write(objeto_json)

#solucion()
   
    
    
   