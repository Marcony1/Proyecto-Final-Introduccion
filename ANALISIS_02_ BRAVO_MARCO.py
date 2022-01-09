#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 21:46:26 2022

@author: Marcony1
"""

import pandas as pd
#%%

synergy_dataframe = pd.read_csv('synergy_logistics_database.csv', index_col=0,
                                encoding='utf-8', 
                                parse_dates=[4, 5])
#%%

# BORRRRAAAAARRRR
"""
Synergy logistics esta considerando la posibilidad de enfocar sus esfuerzos en
los el top  8 de la combinacion 'product', 'transport_mode' y 'company_name'.
Acorde a cada a;o, cuales son esas 10 rutas?
"""

# Combinacion unica de 'product', 'transport_mode' y 'company_name'.
combinaciones = synergy_dataframe.groupby(by=['origin', 'destination',
                                               'transport_mode', 'product'])

# Ya agrupados los datos en base a columnas que se indico, procedemos a obtener
# un df con la descripcion de cada una de mis combinaciones, la descripcion que
# interesa es la de 'total_value'
descripcion = combinaciones.describe()['total_value']

#%%

# Comienza código para responder pregunta 1

# Aquí vamos a analizar las rutas más concurridas
# Para importaciones
importaciones = synergy_dataframe[synergy_dataframe['direction'] == 'Imports'].copy()

combinaciones = importaciones.groupby(by=['origin', 'destination'])

descripcion = combinaciones.describe()['total_value']


conteo_importaciones = descripcion['count']


# Rutas de importación más concurridas
importaciones_sort = conteo_importaciones.sort_values(ascending=False).head(10)


#%%
# Aquí vamos a analizar las rutas más concurridas
# Para exportaciones
exportaciones = synergy_dataframe[synergy_dataframe['direction'] == 'Exports'].copy()

combinaciones2 = exportaciones.groupby(by=['origin', 'destination'])

descripcion2 = combinaciones2.describe()['total_value']


conteo_exportaciones = descripcion2['count']


# Rutas de importación más concurridas
exportaciones_sort = conteo_exportaciones.sort_values(ascending=False).head(10)

#%%
# Aquí vamos a analizar las rutas que transportan mayor valor.
tabla_bonita = descripcion.copy()

# Obtenemos el producto de count*mean, lo que nos da el total. 
tabla_bonita['multiplicacion'] = tabla_bonita['count'] * tabla_bonita['mean']

total = tabla_bonita['multiplicacion']


# Ordenaremos la serie mean de mayor a menor.
total_sort = total.sort_values(ascending=False).head(10)

#%%

# Comienza código para responder pregunta 2

# Para importaciones

importaciones_rutas = synergy_dataframe[synergy_dataframe['direction'] == 'Imports'].copy()

combinaciones_rutas = importaciones_rutas.groupby(by=['transport_mode'])

descripcion_rutas = combinaciones_rutas.describe()['total_value']


tabla_bonita_2 = descripcion_rutas.copy()

# Obtenemos el producto de count*mean, lo que nos da el total. 
tabla_bonita_2['multiplicacion'] = tabla_bonita_2['count'] * tabla_bonita_2['mean']

total_importaciones = tabla_bonita_2['multiplicacion']


# Ordenaremos la serie mean de mayor a menor.
total_importaciones_sort = total_importaciones.sort_values(ascending=False)

#%%

# Para exportaciones

exportaciones_rutas = synergy_dataframe[synergy_dataframe['direction'] == 'Exports'].copy()

combinaciones_rutas2 = exportaciones_rutas.groupby(by=['transport_mode'])

descripcion_rutas2 = combinaciones_rutas2.describe()['total_value']


tabla_bonita_3 = descripcion_rutas2.copy()

# Obtenemos el producto de count*mean, lo que nos da el total. 
tabla_bonita_3['multiplicacion'] = tabla_bonita_3['count'] * tabla_bonita_3['mean']

total_exportaciones = tabla_bonita_3['multiplicacion']


# Ordenaremos la serie mean de mayor a menor.
total_exportaciones_sort = total_exportaciones.sort_values(ascending=False)


#%%

# Metodos de transporte (Exportaciones e importaciones)

# Combinacion unica de 'product', 'transport_mode' y 'company_name'.
combinaciones_conj = synergy_dataframe.groupby(by=['transport_mode'])


descripcion_conj = combinaciones_conj.describe()['total_value']


tabla_bonita_conj = descripcion_conj.copy()

# Obtenemos el producto de count*mean, lo que nos da el total. 
tabla_bonita_conj['multiplicacion'] = tabla_bonita_conj['count'] * tabla_bonita_conj['mean']

total_conj = tabla_bonita_conj['multiplicacion']


# Ordenaremos la serie mean de mayor a menor.
total_conj_sort = total_conj.sort_values(ascending=False)


#%%

# Comienza código para responder pregunta 3

exports = synergy_dataframe[synergy_dataframe['direction'] == 'Exports']
imports = synergy_dataframe[synergy_dataframe['direction'] == 'Imports']

def sol_3(df, p):
    pais_total_value = df.groupby('origin').sum()['total_value'].reset_index()
    total_value_for_percent = pais_total_value['total_value'].sum()
    pais_total_value['percent'] = 100 * pais_total_value['total_value']/ total_value_for_percent
    pais_total_value.sort_values(by='total_value', ascending=False, inplace=True)
    pais_total_value['cumsum'] = pais_total_value['percent'].cumsum()
    lista_pequena = pais_total_value[pais_total_value['cumsum'] < p]
    
    return lista_pequena

res1 = sol_3(imports, 80)

res2 = sol_3(exports, 80)

res3 = sol_3(synergy_dataframe, 80)

print('Los países cuyas importaciones constituyen aproximadamente el 80% son: '
      , sol_3(imports, 80))

print('Los países cuyas exportaciones constituyen aproximadamente el 80% son: '
      , sol_3(exports, 80))

print('Los países cuyo valor comerciado constituye aproximadamente el 80% son: '
      , sol_3(synergy_dataframe, 80))

