# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 09:42:16 2024

@author: EMILIANO
"""
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3
import matplotlib.dates as mdates

db_path = 'I:/Mis Documentos/Onedrive/Python/Practica/Bonos Arg/'
db_file = "Bonosusd.db"

conn = sqlite3.connect(db_path + db_file)

query = 'SELECT Date, AL30D FROM Bonares ORDER BY Date'
al30d = pd.read_sql(query, conn)
al30d = al30d.dropna()
pd.DataFrame(al30d).plot

fig, ax = plt.subplots(figsize=(20,10))


plt.plot(al30d['Date'], al30d['AL30D'], 
         color='#C62C1D', 
         lw=2.5,
         marker='o')


#rotar titulos de ticks
#obtener titulos actuales
xlabels=ax.get_xticklabels()
#aplicar rotacion, cambiar x por y para el otro eje
plt.setp(xlabels,rotation=45)

plt.ylim(0,100)

#los spines son las 4 lineas que encierran el Axes, hacerlos invisible nos da otro efecto visual
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

#es posible determinar la grilla por eje, eligiendo color,estilo y transparencia a gusto
ax.yaxis.grid(color='black', linestyle='dashed', alpha=1)
ax.xaxis.grid(color='gray', linestyle='dashed', alpha=0.7)

#titulos para cada eje
plt.ylabel('Precio del AL30 en USD')
plt.xlabel('Fecha')

# #titulo del plot con ubicacion a la izquierda y fuente 14
# plt.title('Reddit vs WallStreet - $GME Weekly Adj Close', 
#           loc='left', 
#           fontsize=14)

#Usamos un truco que es el titulo de la figura para que quede como titulo principal
#las opciones son claras, excepto ha que es la alineacion vertical.
fig.suptitle('BONAR 2030 - USD',
             x=0.125, 
             y=0.98, 
             ha='left', 
             fontsize=18)

#anotaciones libres de texto
#una para linea de copyright
#usamos valores negativos como truco para ubicarnos por debajo del 0 del eje visualemente
plt.text(-0.5,
         -60, 
         'Fuente: Alphacast Plot:@emilapuente', 
         ha='left', 
         fontsize = 11, 
         alpha=0.9)

#anotacion sobre el grafico, las coordenadas nuevamente coinciden con los ejes graficados
#3 es el cuarto dato de la serie x (0,1,2,3)
plt.text(3, 
         200, 
         'This is the top', 
         ha='left', 
         fontsize = 21, 
         alpha=0.9)

plt.show()
