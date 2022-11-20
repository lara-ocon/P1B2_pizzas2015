# Practica1_bloque2
Practica de la predicción de ingredientes pizzería.

El objetivo de esta Práctica es extraer los datos de la Pizzería Maven Pizzas de 2015, y transformarlos para así
cargar una predicción de la cantidad de ingredientes que necesitaría la pizzería cada semana.

Para obtener esta predicción hemos cargado primero todos los csv en dataframe para poder trabajar con ellos con la librería pandas.

En primer lugar, hemos obtenido una lista que contiene el rango de orders de cada semana. Es decir, las orders estan enumeradas con un identificador, y dado que este va en orden ascendente, con saber la primera order que se hace una semana y la última nos es suficiente para aglomerar todos los pedidos que se hacen una semana determinada.

Sabiendo esto y accediendo a la información de order_details.csv, podemos ver a través del order_id las pizzas (y el tamaño de dichas pizzas) que se piden en cada order. De esta forma, podemos ver cuantas pizzas de cada tipo se piden cada semana. Dado que los tamaños de pizza van de S a XXL, he considerado como tamaño normal la S, y para el resto de tamaños he considerado la siguiente correspondencia: s = 1, m = 1.5, l = 2, xl = 2.5, xxl = 3. Esto lo he hecho dado que no es lo mismo la cantidad de ingredientes que se necesitan para una pizza de tamaño s, que para una pizza de tamaño XXL.

Sabiendo ya aproximadamente cuantas pizzas de tamaño "estándar" se necesitan cada semana. Creamos un dataframe que contenga los ingredientes, y la cantidad necesaria de cada ingrediente para cada semana. Para ello, multiplicamos la cantidad pedida de cada pizza por sus ingredientes, y se los sumamos a su fila correspondiente.

Una vez ya sabemos la cantidad de cada tipo de ingrediente que se ha necesitado cada semana, solo nos queda calcular la predicción. Para ello, tomamos la media para cada tipo de ingrediente y multiplicamos por 1.5 (esto es para evitar que pueda haber escasez de algun ingrdiente). Finalmente, cargamos dicha predicción en "predicciones.csv".
