# Practica 1 Bloque 2 - Adquisición de Datos - IMAT
# Predicción Ingredientes de la Semana Pizzería "Maven Pizzas"
# Hecho por: Lara Ocón Madrid


"""
En esta práctica vamos a tomar los datos de la pizzería Maven Pizzas y calcular 
para cada semana del año la cantidad de cada ingrediente que se ha necesitado. 

Una vez obtenida la cantidad de cada ingrediente para cada semana, calcularemos 
la media de cada uno de ellos y multiplicaremos dicha media por 1.2 (valor que he 
decidido tomar para que no haya falta de ingredientes una semana).

Es decir, emplearemos una ETL, extrayendo los datos, transfromándolos para quedarnos
con lo que necesitamos cada semana, y cargando dicha predicción en un csv.
"""

# Importamos las librerías necesarias
import pandas as pd
import funciones as f
import sys
import signal


def handler_signal(signal, frame):
    # Controlamos la señal de control C, para salir correctamente del programa

    print("\n\n [!] Out .......\n")
    sys.exit(1)


# Funciones de la ETL:

def extract(fichero):
    """
    Función extraccion de datos desde ficheros csv
    """
    df = pd.read_csv(fichero)
    return df


def transform(df_pizza_types, df_orders_fechas, detalles_orders):
    """
    Con esta función vamos a obtener los 4 dataframes que vamos a necesitar:
    - df_pizza_types: Nos dará la información acerca de los ingredientes que
                        necesitará cada pizza, lo que transformaremos en un
                        diccionario {pizza : ingredientes} para poder trabajar
                        más rápido.
    - df_orders_fechas: Nos dará la información que necesitamos para saber que 
                        orders se hicieron cada semana.
    - detalles_orders: Nos permitirá ver que pizzas se pidieron en cada order.
    - df_ingredientes: 
    """

    # En primer lugar, nos guardamos los nombres de las pizzas y un 
    # diccionario que guarde los ingredientes necesarios para cada pizza:
    pizzas_id = df_pizza_types['pizza_type_id']
    dic_ingredientes = f.extraer_ingredientes(df_pizza_types)

    # Vamos a transformar las fechas del dataframe de orders fechas a objetos 
    # pd.datetime con la función de "transformar_fechas"
    df_orders_fechas = f.transformar_fechas(df_orders_fechas)

    # Ahora obtenemos una lista con los rangos de orders que se hacen cada
    # semana del año:
    print("\n"+"\033[1;34m"+"Obteniendo identificadores de pedidos para cada semana..."+"\033[0;m"+"\n")
    orders_por_semana = f.extraer_rango_orders_semana(df_orders_fechas)

    # Sabiendo las orders por semana, creamos un dataframe con el numero
    # de pizzas de cada tipo que se pidieron para cada semana del año.
    print("\n"+"\033[1;35m"+"Obteniendo información acerca de los pedidos ..."+"\033[0;m"+"\n")
    df_pizzas_semana = f.pizzas_por_semana(orders_por_semana, detalles_orders, pizzas_id)

    # Ahora creamos un dataframe con los ingredientes que se han necesitado
    # cada semana para realizar dichas pizzas
    print("\n"+"\033[1;36m"+"Calculando predicción ..."+"\033[0;m"+"\n")
    df_ingredientes_semanas = f.extraer_ingredientes_semanas(df_pizzas_semana, dic_ingredientes)


    # Finalmente, hacemos la predicción. Para ello, hacemos la media por semana
    # para cada ingrediente, y multiplicamos dicha cantidad por 1.2 para
    # evitar que haya escasez de algun ingrediente alguna semana.
    df_prediccion = f.obtener_prediccion_ingredientes(df_ingredientes_semanas)

    return df_prediccion

def cargar_predicciones(df_prediccion):
    """
    En esta función vamos a cargar el dataframe con la predicción de los 
    ingredientes necesarios para la semana en un fichero csv
    """
    df_prediccion.to_csv("predicciones.csv")
    print("\n"+"\033[1;32m"+"Predicción cargada en un csv !!!"+"\033[0;m"+"\n")


if __name__ == "__main__":
    # Controlamos la salida por la señal ctrl+C
    signal.signal(signal.SIGINT, handler_signal)

    # En primer lugar, vamos a extraer todos los ficheros que vamos a
    # necesitar:

    # EXTRACCIÓN DE DATOS:
    df_pizza_types = extract('ficheros/pizza_types.csv')
    df_orders_fechas = extract('ficheros/orders.csv')
    detalles_orders = extract('ficheros/order_details.csv')
    df_ingredientes = extract('ficheros/pizza_types.csv')

    # TRANSFORMACIÓN DE DATOS:
    df_prediccion = transform(df_pizza_types, df_orders_fechas, detalles_orders)

    # CARGAMOS LOS DATOS:
    cargar_predicciones(df_prediccion)

