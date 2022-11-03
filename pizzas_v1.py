# que hay que comprar, aplicando alguna politica (extra) pues de lo mas optimo...

import pandas as pd
import sys
import datetime
import re

def extract(fichero):
    print("llano a extract")
    df = pd.read_csv(fichero)
    print("extraigo")
    return df

def transform():
    # voy a guardar
    ...

def extraer_ingredientes(df):
    dic = {}
    for i in range(len(df)):
        pizza = df.iloc[i]
        clave = pizza['pizza_type_id']
        ingredientes = pizza['ingredients'].strip().split(", ")
        dic[clave] = ingredientes
    return dic


def extraer_orders_semana(df_orders_fechas, fechas_semana):
    orders_nums = []
    for i in range(len(df_orders_fechas)):
        order = df_orders_fechas.iloc[i]
        fecha = pd.to_datetime(order['date'], dayfirst=True)
        if i in range(60, 75):
            print(fecha)
        if fecha in fechas_semana:
            orders_nums.append(order['order_id'])
    return orders_nums

def extraer_num_pizzas_semana(detalles_orders, orders_nums_semana):
    # dado que las orders hasta la semana estan en orden
    i = 0
    terminado = False
    dic = {}
    while i < len(detalles_orders) and not terminado:
        order = detalles_orders.iloc[i]
        if order['order_id'] in orders_nums_semana:
            # añadimos la pizza al diccionario si no esta, 
            # en caso de estarlo sumamos las unidades de dicha pizza
            if order['pizza_id'] not in dic:
                dic[order['pizza_id']] = 0 # lo inicializamos
            # añadimos la cantidad
            dic[order['pizza_id']] += int(order['quantity'])
        
        if order['order_id'] > max(orders_nums_semana):
            # ya me he pasado
            terminado = True
        else:
            i += 1
    return dic


def extraer_num_ingredientes(diccionario_ingredientes, num_pizzas):
    dic_num_ingredientes = {}
    for pizza in list(num_pizzas.keys()):
        total = num_pizzas[pizza] # total pizzas de ese tipo
        # la pizza va seguido de _s, _m, _l luego si es s voy a poner 1
        # ingrediente de cada, si es m 2 de cada, si es l 3 de cada

        # EN ESTA FUNCION CONSIDERO TODOS LOS TAMAÑOS IGUALES; NO HAGO
        # LO DE ARRIBA

        ingredientes = diccionario_ingredientes[pizza[0:len(pizza) - 2].strip("_")] # ingredientes para 1 pizza de ese tipo
        for ingrediente in ingredientes:
            if ingrediente not in dic_num_ingredientes:
                dic_num_ingredientes[ingrediente] = 0 # lo inicializo
            dic_num_ingredientes[ingrediente] += total # le sumo cuantos necesito de ese
    
    return dic_num_ingredientes






if __name__ == "__main__":
    print("Hola")
    df_pizza_types = extract('pizza_types.csv')
    print(df_pizza_types)
    diccionario_ingredientes = extraer_ingredientes(df_pizza_types)
    print(diccionario_ingredientes)

    fecha_actual = None
    fecha_valida = False
    while not fecha_valida:
        try:
            fecha_actual = pd.to_datetime(input("Introduce la fecha actual: "), dayfirst=True)
            fecha_valida = True
            print("has introducido la fecha: ", fecha_actual)
        except KeyboardInterrupt:
            sys.exit(1)
    
    print("estamos a: ", fecha_actual)
    # una vez tengo la fecha, obtengo el dia de la semana para sacar
    # el rango de la semana siguiente

    dia_semana = fecha_actual.day_of_week # van del 0 al 6
    print("el dia de la semana es", dia_semana)
    dias_hasta_siguiente = 7 - dia_semana # si es lunes dará 7

    semana_siguiente = fecha_actual + datetime.timedelta(days = dias_hasta_siguiente)
    print("la semana que viene empieza el: ", semana_siguiente)


    # NO ES ASI, me dicen en que semana estoy y saco los ingredientes
    # de las orders de ESA SEMANA
    fechas_semana = [] # aqui pondre todos los dias de la semana_actual
    dias_hasta_lunes = fecha_actual.day_of_week # van del 0 al 6
    fecha = fecha_actual - datetime.timedelta(days = dias_hasta_lunes)
    fechas_semana.append(fecha)
    # he añadido el lunes, añado el resto
    for i in range(1, 7):
        fechas_semana.append(fecha + datetime.timedelta(days = i))
    
    # ahora solo saco las orders de esta semana

    df_orders_fechas = extract('orders.csv')
    print("tengo el df de las orders")
    orders_nums_semana = extraer_orders_semana(df_orders_fechas, fechas_semana)
    print(orders_nums_semana)

    # ya tengo los numeros de orders para esa semana, ahora voy y cuento
    # cuantas pizzas de cada tipo voy a tener que hacer

    detalles_orders = extract('order_details.csv')
    num_pizzas = extraer_num_pizzas_semana(detalles_orders, orders_nums_semana)
    print(num_pizzas)

    # una vez tengo el numero de pizzas, sumo los ingredientes para cada pizza
    total_ingredientes = extraer_num_ingredientes(diccionario_ingredientes, num_pizzas)
    print(total_ingredientes)

    # lo paso a un dataframe
    df_ingredientes_semana = pd.DataFrame()
    df_ingredientes_semana['ingredientes'] = list(total_ingredientes.keys())
    df_ingredientes_semana['cantidad'] = list(total_ingredientes.values())
    print(df_ingredientes_semana)
    df_ingredientes_semana.to_csv("prueba_ingredientes_semana1.csv")



        


