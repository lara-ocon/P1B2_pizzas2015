# Practica1_bloque2

Predicción Ingredientes pizzería "Maven Pizzas" - Adquisición de Datos - IMAT
Hecho por Lara Ocón Madrid

El objetivo de esta Práctica es extraer los datos de la Pizzería Maven Pizzas de 2015, y transformarlos para así
cargar una predicción de la cantidad de ingredientes que necesitaría la pizzería cada semana.

Para ejecutar el programa, es necesario tener en el directorio de trabajo la carpeta ficheros (que contendrá los csv que vamos a analizar), el fichero funciones.py (que contendrá funciones específicas para analizar cada csv) y pizzas.py (ETL que vamos a ejecutar).
También, será necesario tener instaladas las librerías indicadas en el fichero "requirements.txt".

Dento del repositorio, podemos encontrar también la carpeta informe_calidad donde encontramos "crear_informe.py" que carga todos los csv y devuelve "informe_calidad_datos.md" que como su nombre indica analiza para cada csv su informe de calidad de datos. Para ejecutarlo y que pueda cargar los csv dentro de la carpeta dicheros es necesario ejecutarlo de la siguiente forma: "python3 informe_calidad/crear_informe.py" (en otras palabras, ejecutarlo desde el programa principal).

Al ejecutar "pizzas.py" iniciaremos nuestra ETL que hará lo siguiente:

1) Extracción de datos: Extraemos los csv que vamos a necesitar y los cargamos en pandas dataframes.

2) Transformación de datos:

    En primer lugar, hemos obtenido una lista que contiene el rango de orders de cada semana. Es decir, las orders estan enumeradas con un identificador, y dado que este va en orden ascendente, con saber la primera order que se hace una semana y la última nos es suficiente para aglomerar todos los pedidos que se hacen una semana determinada.

    Sabiendo esto y accediendo a la información de order_details.csv, podemos ver a través del order_id las pizzas (y el tamaño de dichas pizzas) que se piden en cada order. De esta forma, podemos ver cuantas pizzas de cada tipo se piden cada semana. Dado que los tamaños de pizza van de S a XXL, he considerado como tamaño normal la S, y para el resto de tamaños he considerado la siguiente correspondencia: s = 1, m = 1.5, l = 2, xl = 2.5, xxl = 3. Esto lo he hecho dado que no es lo mismo la cantidad de ingredientes que se necesitan para una pizza de tamaño s, que para una pizza de tamaño XXL.

    Sabiendo ya aproximadamente cuantas pizzas de tamaño "estándar" se necesitan cada semana. Creamos un dataframe que contenga los ingredientes, y la cantidad necesaria de cada ingrediente para cada semana. Para ello, multiplicamos la cantidad pedida de cada pizza por sus ingredientes, y se los sumamos a su fila correspondiente.

    Una vez ya sabemos la cantidad de cada tipo de ingrediente que se ha necesitado cada semana, solo nos queda calcular la predicción. Para ello, tomamos la media para cada tipo de ingrediente y multiplicamos por 1.2 (esto es para evitar que pueda haber escasez de algun ingrdiente). Finalmente, cargamos dicha predicción en "predicciones.csv".

3) Carga de datos: Cargamos el dataframe con la prediccion en "predicciones.csv"

