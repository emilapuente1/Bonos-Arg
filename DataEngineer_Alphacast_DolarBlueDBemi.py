# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 18:31:28 2023

@author: Los precios ya tienen incorporado un dolar a...
"""
#Data Engineer 2023
#Clase 4
#Como armar una base de datos de Dolar Blue usando datos de Alphacast, SQL y Python

#esta libreria me permite conectarme a la DB SQLite
#instalar con pip install sqlite3
import sqlite3
import pandas as pd  

#esta libreria viene incorporada
#me permite utilizar tipos de datos que son fechas y horas, no el texto de la fecha
#esto me permite preguntar que dia es hoy, extraer el mes de una fecha y mas
import datetime as dt

#Esta libreria me permite interactuar con el sitio Alphacast
#Este ejemplo requiere tener una API Key de Alphacast
from alphacast import Alphacast


##Paso 1 Conectar a la DB y traer el ultimo registro
##Eso nos permitira saber que fechas faltan en nuestra DB
#Path de la base SQLite (cambiar segun corresponda)
db_path = 'I:/Mis Documentos/Onedrive/Python/Practica/'
db_file = "USDARS_historico.db"

#Me conecto a la base, la conexion queda dentro de la variable
#La variable luego la uso para interactuar con la base, por ejemplo escribir ahi
conn = sqlite3.connect(db_path + db_file)


#La ultima fecha de actualizacion es Ninguna (None)
#Al principio, porque puede ser la primera vez que 
#ejecutamos esto y la DB no existe todavia
#Poner None en la fecha de comienzo y fin hace que la 
#funcion de Alphacast baje todo el historial entero.
ultima_fecha=None


#Raw SQL Query
#Una consulta raw SQL es basicamente la misma que funciona fuera de Python
#y en un entorno SQL, como es la venta de Query de DB Browser
#Puedo pegar lo que ya hice ahi y se que funciona (recomendado) aca 
#El query trae el ultimo registro de la tabla (estar ordenada al reves)
#y de ese registro extraemos solo la fecha (hay otras columnas, mirar la DB)
query = 'SELECT Date FROM USDARS ORDER BY Date DESC LIMIT 1'


#try "intenta" conectarse a la base de datos
#si hay un error imprimira un error, sino ejecutara lo de adentro de try
#de una manera u otra, luego la base se cerrara en finally
try:
    
    #Pandas me permite leer una DB si tengo una conexion
    #Y un query valido SQL (ver arriba)
    last_date_df = pd.read_sql(query, conn)

    #La DB puede estar vacia (es nueva or ejemplo)
    #de no ser asi, queremos extraer la fecha como un texto y guardarla en una variable
    #no necesitamos el dataframe entero con su estructura de filas y columnas para 
    #un solo dato
    if not last_date_df.empty:
        ultima_fecha=last_date_df.iloc[0]['Date']
        print("La ultima fecha en 'USDARS' es: ", ultima_fecha)
    else:
        #Si no pudo leer la ultima fecha, la tabla esta vacia
        #la crearemos mas abajo
        print("No hay datos, intentando bajar todo el historial")

except Exception as e:
        print("La tabla no existe todavia,la crearemos")

finally:
    conn.close()


#Paso 2 : Importar datos de Alphacast

#obviamente modificar esto con TU apikey (esta en el profile)
alphacast = Alphacast("ak_FuWkKZRDINFktMy8VIOt")

#ver clase de DataScience de Alphacast
#cada dataset tiene un id, el del dolar es 5288
dataset = alphacast.datasets.dataset(5288)


# Vamos a necesitar convertir la fecha de string a datetime
# Conversion
# Explicar ISO format 
# "2023-12-03"
# "2023-12-03T10:15:30"
# ejemplos de crear fechas como referencia
# hoy=dt.date.today()
# ayer=hoy-dt.timedelta(days=1)

#Si la tabla esta vacia (es la primera vez que ejecutamos esto por ejemplo)
#esta variable va a valer None (ver arriba)
#Con lo cual intentar un casting podria darnos un error, y lo evitamos
#solo convirtiendo si la variable tiene asignado un valor (la ultima fecha en la tabla)
if ultima_fecha!=None:
    ultima_fecha = dt.datetime.fromisoformat(ultima_fecha)


#Bajar los datos de Alphacast
# e importar a pandas
# pero solo desde la ultima fecha que esta en la DB
# o sea la ultima fecha de actualizacion
# y hasta el ultimo dato disponible al momento de la consulta
df = dataset.download_data(format = "pandas", 
                           startDate=ultima_fecha,
                           endDate=None,
                           filterVariables = [], 
                           filterEntities = {})

#Si el dataframe viene vacio desde Alphacast
#Puede ser que no haya actualizaciones disponibles
#Por ejemplo si lo ejecutamos consecutivamente con el mercado cerrado
if df.empty:
    print ("DB al dia, no hay datos actualizados")
else: 
    # Paso 3 : Exportar a DB
    # Solo caemos aca si realmente hay datos actualizados para grabar en la DB

    #Conectar a DB
    #Agregar el path segun corresponda
    conn = sqlite3.connect('USDARS_historico.db')


    #escribir a DB
    #Usamos pandas nuevamente para escribir el dataframe
    #que contiene la bajada de datos de Alphacast
    #le pasamos el nombre de la tabla, la conexion
    #no escribimos el index del dataframe (false)/
    #porque la DB tiene una primary key
    #append hace que no "pise" datos anteriores, sino que agregue
    df.to_sql('USDARS', conn, if_exists='append', index=False)

    #cerrar conexion y terminar
    conn.close()



