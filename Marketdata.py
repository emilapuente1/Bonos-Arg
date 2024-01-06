# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 11:15:01 2023

@author: EMILIANO
"""

#DataScience 2023
#Alphacast
#Como conectarse y bajar datasets para analisis

from alphacast import Alphacast

#Necesitan una cuenta activa en
#https://www.alphacast.io/home
#El API Key esta en su perfil de usuario
alphacast = Alphacast("ak_FuWkKZRDINFktMy8VIOt")

#el numero de dataset esta en la URL de cada dataset
#dentro de Alphacast
#5288 se refiere al dataset FX Argentina
#que contiene el historico del dolar
dataset = alphacast.datasets.dataset(5309)


# Transformar en dataframe
df = dataset.download_data(format = "pandas", 
                           startDate=None,
                           endDate=None, 
                           filterVariables = [], 
                           filterEntities = {})


#exportar a Excel
#Cambiar el path de acuerdo a la carpeta que usen
path="I:/Mis Documentos/Onedrive/Python/"

#La idea de exportar a Excel es luego importarlo
#En otro script para hacer el analisis concreto
#Esto evita que cada vez que cambian algo se bajen
#el dataset una y otra vez de Alphacast
#Ver el otro ejemplo para el analisis concreto
df.to_excel(path+"Commodities global.xlsx",index=False)

