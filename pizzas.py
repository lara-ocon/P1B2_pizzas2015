import pandas as pd
import sys
import datetime
import re



def extract(fichero):
    df = pd.read_csv(fichero)
    return df


def extraer_ingredientes(df):
    # me guardo en un diccionario los ingredientes para cada pizza
    dic = {}
    for i in range(len(df)):
        pizza = df.iloc[i]
        clave = pizza['pizza_type_id']
        ingredientes = pizza['ingredients'].strip().split(", ")
        dic[clave] = ingredientes
    return dic


def extraer_orders_por_semana(df_orders_fechas):
    # como el dataframe esta en orden, me voy al primer lunes
    # y guardo las orders para esa semana (como tambien estan enumeradas
    # en orden con el rengo me vale), de esta forma obtengo el rango de 
    # orders para cada semana

    # primero busco el primer lunes
    orders_por_semana = []
    i = 0
    lunes = False
    while i < len(df_orders_fechas) and not lunes:
        order = df_orders_fechas.iloc[i]
        fecha = pd.to_datetime(order['date'], dayfirst=True)
        if fecha.day_of_week == 0:
            # me guardo por qué numero de order empieza esa semana
            orders_por_semana.append(order['order_id'])
            lunes = True
        else:
            i += 1
    # busco el siguiente lunes
    siguiente_lunes = fecha + datetime.timedelta(days = 7)
    while i < len(df_orders_fechas):
        order = df_orders_fechas.iloc[i]
        fecha = pd.to_datetime(order['date'], dayfirst=True)
        if fecha == siguiente_lunes:
            # es la primera order de la semana siguiente, añado su id
            orders_por_semana.append(order['order_id'])
            siguiente_lunes = siguiente_lunes + datetime.timedelta(days = 7)
        i += 1
        
    # esto funciona pero no tengo en cuenta que la ultima semana del dataframe puede 
    # no ser entera, compruebo esto viendo si es domingo o no
    # if pd.to_datetime(df_orders_fechas.loc[len(df_orders_fechas) - 1]['date'], dayfirst=True).day_of_week != 6:
        # si la ultima no cae en domingo es que la semana esta incompleta luego
        # no me vale
        #orders_por_semana.pop()
    
    # esto lo he quitado porque necesito saber donde acaba la ultima semana

    return orders_por_semana


def crear_df_pizzas_semana(nombres_pizzas, orders_por_semana, detalles_orders):
    # a las pizzas de tamaño s las cuento como 1, y las de tamaño xxl como 3
    # por esta regla de 3, las m = 1.5, l = 2, xl = 2.5

    df_pizzas_semana = pd.DataFrame()
    # añado una columna que serán pizzas, las filas serán las semanas

    df_pizzas_semana['pizzas'] = nombres_pizzas
    print("inicialmente esta asi", df_pizzas_semana)

    t = 0 # posicion en el dataframe de detalles_orders
    # me situo en la primera order del dataframe (la primera order del primer lunes)
    print(orders_por_semana)
    while orders_por_semana[0] != int(detalles_orders.loc[t]['order_id']):
        t += 1
    print("El primer lunes etsa en la linea, ", t)

    for i in range(len(orders_por_semana) - 1):
        # añado la semana:
        df_pizzas_semana[f"semana {i}"] = [0 for i in range(len(nombres_pizzas))]
        #print("\nañado una semana\n")
        #print(df_pizzas_semana)

        # creo un diccionario cuyas claves son los nombres de las pizzas
        dic_pizzas = {}
        for s in range(len(nombres_pizzas)):
            dic_pizzas[nombres_pizzas.loc[s]] = 0
        #print(dic_pizzas)
        
        # ahora voy añadiendo al diccionario las pizzas para cada semana
        num_order = orders_por_semana[i]
        # mientras no llegue al order correspondiente de la siguiente semana

        # dado que las orders hasta la semana estan en orden
        terminado = False
        while t < len(detalles_orders) and not terminado:
            order = detalles_orders.iloc[t]
            if int(order['order_id']) in range (orders_por_semana[i], orders_por_semana[i + 1]):
        
                # si la pizza esta dentro de la semana, añadimos la pizza al diccionario
                dic_pizzas = añadir_pizza(dic_pizzas, order)
                t += 1
            else:
                terminado = True
        df_pizzas_semana[f"semana {i}"] = list(dic_pizzas.values())
        #print("dic de la semana", dic_pizzas)
    return df_pizzas_semana

def añadir_pizza(dic, order):
    # añado la pizza asociada a ese order
    pizza = order['pizza_id']
    tam = 3
    # vemos su tamaño
    if re.search("_s$", pizza):
        pizza = re.sub("_s$","", pizza)
        tam = 1
    elif re.search("_m$", pizza):
        pizza = re.sub("_m$","", pizza)
        tam = 1.5
    elif re.search("_l$", pizza):
        pizza = re.sub("_l$","", pizza)
        tam = 2
    elif re.search("_xl$", pizza):
        pizza = re.sub("_xl$","", pizza)
        tam = 2.5
    elif re.search("_xxl$", pizza):
        pizza = re.sub("_xxl$","", pizza)
        tam = 3
    
    cantidad = order['quantity']

    # añado el num de unidades de esa pizza al diccionario
    dic[pizza] += cantidad*tam

    return dic


def extraer_ingredientes(df):
    dic = {}
    for i in range(len(df)):
        pizza = df.iloc[i]
        clave = pizza['pizza_type_id']
        ingredientes = pizza['ingredients'].strip().split(", ")
        dic[clave] = ingredientes
    return dic


def extraer_ingredientes_semanas(df_ingredientes_semanas, df_pizzas_semana, dic_ingredientes):
    for i in range(len(df_pizzas_semana)):
        fila = df_pizzas_semana.iloc[i]
        nombre_pizza = df_pizzas_semana.loc[i]['pizzas']
        ingredientes = dic_ingredientes[nombre_pizza]

        for j in range(38):
            # para las 38 saco cuantas pizzas de ese tipo necesito
            num = fila[f"semana {j}"]
            # añado el numero a cada ingrediente
            for ingrediente in ingredientes:
                df_ingredientes_semanas.loc[ingrediente, f"semana {j}"] += num
                """
                indice = df_ingredientes_semanas[df_ingredientes_semanas['ingredientes'] == ingrediente].index[0]
                df_ingredientes_semanas.loc[int(indice), f"semana {j}"] += num
                """

    return df_ingredientes_semanas


def obtener_prediccion(df_ingredientes_semanas, ingredientes):
    df_ingredientes_semanas = df_ingredientes_semanas.transpose()
    dic = {}
    for ingrediente in ingredientes:
        media =  df_ingredientes_semanas[ingrediente].mean()
        dic[ingrediente] = media*1.3 # pedimos que compre de mas por si
    return dic





if __name__ == "__main__":

    df_pizza_types = extract('pizza_types.csv')

    nombres_pizzas = df_pizza_types['pizza_type_id']
    print(nombres_pizzas)
    print(list(nombres_pizzas))

    diccionario_ingredientes = extraer_ingredientes(df_pizza_types)

    df_orders_fechas = extract('orders.csv')

    orders_por_semana = extraer_orders_por_semana(df_orders_fechas)

    print(orders_por_semana)

    detalles_orders = extract('order_details.csv')

    # veamos de media cuanto se necesita de cada ingrediente
    df_pizzas_semana = crear_df_pizzas_semana(nombres_pizzas, orders_por_semana, detalles_orders)

    print(df_pizzas_semana)

    

    # creamos diccionario con ingredientes para cada pizza
    df_ingredientes = extract('pizza_types.csv')
    dic_ingredientes = extraer_ingredientes(df_ingredientes)
    total_ingredientes = []
    for ingredientes in  list(dic_ingredientes.values()) :
        for ingrediente in ingredientes:
            if ingrediente not in total_ingredientes:
                total_ingredientes.append(ingrediente)
    
    datos = {}
    for i in range(38):
        datos[f'semana {i}'] = [0 for i in range(len(total_ingredientes))]

    # ahora creamos un dataframe con los ingredientes de cada semana
    df_ingredientes_semanas = pd.DataFrame(datos, index=total_ingredientes)

    """
    df_ingredientes_semanas['ingredientes'] = total_ingredientes
    for i in range(38):
        df_ingredientes_semanas[f'semana {i}'] = [0 for i in range(len(total_ingredientes))]
    """

    print(df_ingredientes_semanas)

    df_ingredientes_semanas = extraer_ingredientes_semanas(df_ingredientes_semanas, df_pizzas_semana, dic_ingredientes)

    print(df_ingredientes_semanas.transpose())
    print(df_ingredientes_semanas.describe())
    print(df_ingredientes_semanas.transpose().describe())

    dic = obtener_prediccion(df_ingredientes_semanas, total_ingredientes)
    print(dic)



            


