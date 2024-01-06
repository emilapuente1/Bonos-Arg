import pandas as pd
import sqlite3


path="I:/Mis Documentos/Onedrive/Python/"
df=pd.read_excel(path+"datasetBonos.xlsx")
# df.info()
df.set_index('Date',inplace=True)

bonosarg= ["AL29","AL29D","AL30","AL30D","AL35","AL35D","AE38","AE38D","AL41","AL41D","GD30","GD30D"]
fecha_inicio = "2020-09-07"

bonoscanje=df.loc[fecha_inicio:,bonosarg]
bonoscanje.dropna(inplace=True)

bonoscanje.to_excel(path+"datasetBonoscanje.xlsx",index=False)

# bonoscanje.info(null_counts=True)
last = bonoscanje[bonosarg].iloc[-1]

print(last)

# # CONEXION a Base de Datos SQLITE

# # Nos conectamos a la base de datos, si no existe la va a crear
db_conexion = sqlite3.connect('bonoscanje.db')
db_cursor = db_conexion.cursor()

# # Creamos la tabla Bonareas

bonoscanje.to_sql(
    "bonares",
    con=db_conexion,
    if_exists = 'replace',
    index=True)

db_conexion.commit()
