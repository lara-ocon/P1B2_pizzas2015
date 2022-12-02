# Informe de calidad de los datos ==================================================
import pandas as pd
# El informe de calidad de los datos se encuentra en el fichero informe_calidad_datos.md

# Funciones de creación de informes ==============================================
def create_report(dict):
    """
    En esta función vamos a crear un informe de calidad de los datos, que nos permita
    comprobar si los datos que tenemos son correctos o no. Para ello, vamos a comprobar
    si hay datos nulos, si hay datos duplicados, si hay datos que no corresponden a 
    los valores esperados, etc.
    """
    informe = open('informe_calidad/informe_calidad_datos.md', 'w')
    for csv in dict:
        print("\n"+"\033[1;32m"+"Creando informe de calidad de los datos del fichero "+csv+" ..."+"\033[0;m"+"\n")
        informe.write(f'\n## Informe de calidad de los datos del fichero {csv}' )
        informe.write('\nnº de filas: ' + str(dict[csv].shape[0]))
        informe.write('\nnº de columnas: ' + str(dict[csv].shape[1])) 
        informe.write('\nnº de datos nulos: ' + str(dict[csv].isnull().sum().sum()))
        informe.write('\ntipología de datos: ' + str(dict[csv].dtypes))
    
    informe.close()


# Ejecución =====================================================================
if __name__ == '__main__':
    df_order_details = pd.read_csv('ficheros/order_details.csv')
    df_order_dates = pd.read_csv('ficheros/orders.csv')
    df_pizza_types = pd.read_csv('ficheros/pizza_types.csv')
    df_pizzas = pd.read_csv('ficheros/pizzas.csv')
    df_predicciones = pd.read_csv('predicciones.csv')

    dict = {'order_details.csv': df_order_details, 'orders.csv': df_order_dates, 'pizza_types.csv': df_pizza_types, 'pizzas.csv': df_pizzas, 'predicciones.csv': df_predicciones}
    create_report(dict)
    


