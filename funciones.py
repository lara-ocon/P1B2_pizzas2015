import pandas as pd
import numpy as np
import re

def transformar_fechas(df):
    """
    vamos a crear una función que tome el df de las orders
    con sus fechas correspondientes y transforme las fechas
    a su formato correspondiente
    """
    df['date'] = pd.to_datetime(df['date'], dayfirst=True)
    return df


def extraer_rango_orders_semana(df_order_dates):
    """
    creamos una función que devuelva una lista que contenga
    para cada semana su rango de orders. Es decir, las orders 
    están enumeradas por un identificador, el cual va en orden
    ascendente. Por lo que solo con el limite inferior y superior
    de cada semana podemos saber que orders corresponden a cada semana
    """
    # Inicializamos los rangos de orders para cada semana
    orders_semanas = [[np.inf, -np.inf] for t in range(53)]

    # veo que dia de la semana es el 1 de enero de 2016
    primer_lunes = pd.to_datetime("01-01-2016").dayofweek
    
    # vamos recorriendo el dataframe y calculando a que semana del año
    # pertenecen dichas ordes mediante la operacion: 
    # day_of_year+primer_lunes // 7

    i = 0
    while i < len(df_order_dates):
        orders_semana = orders_semanas[(df_order_dates.loc[i, 'date'].day_of_year + primer_lunes) // 7]
        if (df_order_dates.loc[i, 'order_id']) > orders_semana[1]:
            orders_semana[1] = df_order_dates.loc[i, 'order_id']
        if (df_order_dates.loc[i, 'order_id']) < orders_semana[0]:
            orders_semana[0] = df_order_dates.loc[i, 'order_id']
        
        orders_semanas[(df_order_dates.loc[i, 'date'].day_of_year + primer_lunes) // 7] = orders_semana
        
        i +=1 

    # print("orders semanas es:", orders_semanas)
    return orders_semanas


# Creamos una función que nos devuelva un df con el numero de 
# pizzas de cada tipo que se han pedido en cada semana

def pizzas_por_semana(orders_semanas, df_order_details, pizzas_id):
    """
    Esta función recibe la lista que contiene los rangos de las orders
    por semana (orders_semanas), el df con los detalles de las orders para 
    cada semana (df_order_details) y una lista con todas las pizzas.

    Nos devolverá un dataframe con el numero de pizzas de cada tipo que
    se han pedido cada semana. Para ello, dado que las pizzas se pueden
    pedir de distinto tamaño, llamará a la función "obtener_nombre_y_can_pizza"
    que estimará según el tamaño de la pizza, a cuantas pizzas 'normales'
    corresponde ese tamaño.
    """

    df_pizzas_semana = pd.DataFrame()      # creamos el dataframe
    datos = {}
    for i in range(53):                    # creamos los indices del dataframe
         # inicializamos la cantidad de cada pizza en 0
        datos[f'semana {i}'] = [0 for i in range(len(pizzas_id))]
    df_pizzas_semana = pd.DataFrame(datos, index=pizzas_id) 

    i = 0
    semana = 0                              # empezamos en la semana 0
    while semana < len(orders_semanas) and i < len(df_order_details):
        # buscamos la primera order de la semana correspondiente
        while (i < len(df_order_details)) and (df_order_details.loc[i, 'order_id'] < orders_semanas[semana][0]):
            i += 1
        # en el momento que lo encontramos, empezamos a añadir las pizzas hasta
        # salir del rango de orders de esa semana
        while (i < len(df_order_details)) and (df_order_details.loc[i, 'order_id'] <= orders_semanas[semana][1]):
            pizza, cantidad = obtener_nombre_y_can_pizza(df_order_details.iloc[i])
            df_pizzas_semana.loc[pizza, f'semana {semana}'] += cantidad
            i += 1
        semana += 1                         # hemos terminado, pasamos a la siguiente semana
    
    return df_pizzas_semana


def obtener_nombre_y_can_pizza(order):
    """
    Dado que en order details, además del id de pizza que se pide tenemos el tamaño
    de dicha pizza, y la cantidad de pizzas que se piden, vamos a crear una función
    que interprete para cada tamaño de pizza, cuantas pizzas se corresponden a un 
    tamaño de pizza "normal" y lo multiplique por la cantidad de dicha pizza.
    Esto nos servirá a la hora de calcular los ingredientes necesarios puesto que 
    no es lo mismo los ingredientes necesarios para una pizza xxl que una m.
    Como los tamaños van de s a xxl usaremos la siguiente correspondencia:
    s = 1, m = 1.5, l = 2, xl = 2.5, xxl = 3
    """

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
    
    return pizza, cantidad*tam


def extraer_ingredientes_semanas(df_pizzas_semana, dic_ingredientes):
    """
    Creamos una función que nos devuelva un df con los ingredientes 
    que han sido necesarios cada semana. 

    Para ello, vamos recorriendo el dataframe que hemos creado con el 
    total de pizzas que se han pedido cada semana, y sumando en el 
    dataframe de ingredientes, la cantidad necesaria de cada ingrediente
    para hacer esas 'x' pizzas
    """

    # Inicializamos el dataframe que contendrá los ingredientes necesarios por semana
    total_ingredientes = []
    datos = {}
    for ingredientes in  list(dic_ingredientes.values()) :
        for ingrediente in ingredientes:
            if ingrediente not in total_ingredientes:
                total_ingredientes.append(ingrediente)
                datos[ingrediente] = [0 for i in range(53)]

    semanas = [f"semana {i}" for i in range(53)]

    # ya podemos crear el dataframe con los ingredientes inicializados a 0
    df_ingredientes_semanas = pd.DataFrame(datos, index=semanas)
    
    for pizza in df_pizzas_semana.index:
        
        ingredientes = dic_ingredientes[pizza]

        for j in range(len(df_ingredientes_semanas)):
            # voy recorriendo las filas del df de ingredientes (semanas) 
            # y obtengo cuantas pizzas de ese tipo se hacen cada semana
            num = df_pizzas_semana.loc[pizza, f"semana {j}"]
            # añado el numero a cada ingrediente
            for ingrediente in ingredientes:
                df_ingredientes_semanas.loc[f"semana {j}", ingrediente] += num
    
    # print("Ingredientes por semana:\n",df_ingredientes_semanas)
    return df_ingredientes_semanas


def obtener_prediccion_ingredientes(df_ingredientes_semanas):
    """
    Esta función toma el dataframe de los ingredientes que se han ido
    necesitando para cada semana, y hace la media de cada ingrediente
    para todas las semanas. Después multiplica es media por 1.2, para
    así asegurarnos que no pueda haber escasez de ingredientes una 
    semana concreta.
    """
    predicciones = df_ingredientes_semanas.mean()*1.5
    df_prediccion = pd.DataFrame(data=predicciones, columns=['cantidad'])
    # print("predicción es: ", df_prediccion)
    return df_prediccion


def extraer_ingredientes(df):
    """
    creamos una función que devuelva un diccionario con los
    ingredientes de cada pizza
    """
    dic = {}
    for i in range(len(df)):
        pizza = df.iloc[i]
        clave = pizza['pizza_type_id']
        ingredientes = pizza['ingredients'].strip().split(", ")
        dic[clave] = ingredientes
    return dic