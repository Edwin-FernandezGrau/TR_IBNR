#!/usr/bin/env python
# coding: utf-8

# importamos elementos necesarios
import pandas as pd
import chainladder as cl
import warnings
import streamlit as st
import base64

warnings.filterwarnings("ignore", category=DeprecationWarning)


st.set_page_config(page_title= "IBNR CRECER",layout="wide") 
st.title("Chainladder IBNR CRECER ")


################## TRIANGULOS EN PYTHON

nombre_archivo = "BASEMOD"


uploaded_file = st.file_uploader("Choose an excel file", type="xlsx")


if not  uploaded_file:
        st.error("Es necesario cargar la base de siniestros")

base0 = pd.read_excel(uploaded_file, header = 0 , engine = "openpyxl")
st.dataframe(base0)
 
variables = list(base0.columns)

var_origen = st.sidebar.selectbox("Seleccione variable de origen ", variables , index= 1 )         ####filas del triangulo   
var_desarrollo = st.sidebar.selectbox("Seleccione variable desarrollo",variables , index= 2 )      #columnas del triangulo
var_movimiento = st.sidebar.selectbox("Seleccione variable Tipo de movimiento ",  variables, index= 3 ) 
var_tri = st.sidebar.selectbox("Seleccione variable a triangular ",  variables, index= 3 )

   
#posibilidad de filtrar moneda
    
f_mon = st.sidebar.radio("Desea filtrar moneda",
                  ('Si', 'No'))

if f_mon == 'Si':
        var_moneda = st.sidebar.selectbox("Seleccione variable moneda ", variables , index= 1 )
        moneda_f =   st.sidebar.selectbox("Seleccione variable moneda ", list(base0[var_moneda].unique())  , index= 0 )
        base = base0[base0[var_moneda] == moneda_f]
else:
        base = base0


   
base_r = base[base[var_movimiento] == "R"]
base_p = base[base[var_movimiento] == "P"]

st.write("Revisamos inconsistencia de fechas")
inconsistencias = base0.loc[base0[var_origen] > base0[var_desarrollo]] 

if inconsistencias.empty == False :
         st.dataframe(inconsistencias)
         base0.loc[base0[var_origen] > base0[var_desarrollo],var_desarrollo()] = base0[var_origen]
else:
    st.write("No existe inconsistencia entre la variable  de origen y la de desarrollo")         


##### TRIANGULO INCREMENTAL DE INCURRIDOS (Tipo de movimiento R)
st.markdown("**Triangulo de incurridos incremental**")

tri_r_incr = cl.Triangle(base_r, origin= var_origen , development= var_desarrollo ,columns=[var_tri])
tr_incurridos_increm = tri_r_incr.to_frame()
tr_incurridos_increm.index = tr_incurridos_increm.index.strftime('%Y-%m')
st.dataframe(tr_incurridos_increm.round(2).fillna(""))
tr_incurridos_increm = tr_incurridos_increm.fillna("")


##### TRIANGULO INCREMENTAL DE PAGOS (Tipo de movimiento P)   
st.markdown("**Triangulo de pagos incremental**")     
tri_p_incr = cl.Triangle(base_p, origin= var_origen , development= var_desarrollo ,columns=['Monto en soles'])
tr_pagos_increm = tri_p_incr.to_frame()
tr_pagos_increm.index = tr_pagos_increm.index.strftime('%Y-%m')
st.dataframe(tr_pagos_increm.round(2).fillna(""))
tr_pagos_increm = tr_pagos_increm.fillna("")



##### TRIANGULO ACUMULADO DE INCURRIDOS (Tipo de movimiento R)
st.markdown("**Triangulo de incurridos acumulado**")
tri_r_acum = tri_r_incr.incr_to_cum()
tr_incurridos_acum = tri_r_acum.to_frame()
tr_incurridos_acum.index = tr_incurridos_acum.index.strftime('%Y-%m')
st.dataframe(tr_incurridos_acum.round(2).fillna(""))
tr_incurridos_acum = tr_incurridos_acum.fillna("")


##### TRIANGULO ACUMULADO DE PAGOS (Tipo de movimiento R)
st.markdown("**Triangulo de pagos acumulado**")
tri_p_acum = tri_p_incr.incr_to_cum()
tr_pagos_acum = tri_p_acum.to_frame()
tr_pagos_acum.index = tr_pagos_acum.index.strftime('%Y-%m')
st.dataframe(tr_pagos_acum.round(2).fillna("") )
tr_pagos_acum = tr_pagos_acum.fillna("")


######## TRIANGULOS DE RESERVAS 
st.markdown("**Triangulo de reservas**")
tri_inc_incr = tri_r_incr - tri_p_incr
tr_reservas_increm = tri_inc_incr.to_frame() 
tr_reservas_increm.index = tr_reservas_increm.index.strftime('%Y-%m')
st.dataframe(tr_reservas_increm.round(2).fillna(""))
tr_reservas_increm = tr_reservas_increm.fillna("")


######## TRIANGULOS ACUMULADO DE RESERVAS
st.markdown("**Triangulo acumulado de reservas**")
tri_inc_acum = tri_inc_incr.incr_to_cum()
tr_reservas_acum = tri_inc_acum.to_frame()
tr_reservas_acum.index = tr_reservas_acum.index.strftime('%Y-%m')
st.dataframe(tr_reservas_acum.round(2).fillna("") )
tr_reservas_acum = tr_reservas_acum.fillna("")


######## TRIANGULOS FINAL ACUMULADO
st.markdown("**Triangulo final acumulado**")
tri_inc_acum_f = tri_inc_acum +tri_p_acum
tr_final_acum = tri_inc_acum_f.to_frame() 
tr_final_acum.index = tr_final_acum.index.strftime('%Y-%m')
st.dataframe(tr_final_acum.round(2).fillna(""))
tr_final_acum = tr_final_acum.fillna("")


######## TRIANGULOS RATIOS INICIAL
st.markdown("**Triangulo de Ratios**")


######## TRIANGULOS RATIOS AJUSTADO
# excluimos los meses iniciales de covid y el periodo 202011(punto1) x se muy alto
#lista_excl = [('2020-04',1),('2020-04',2),('2020-04',3),('2020-04',4),('2020-04',5),('2020-04',6),('2020-04',7),('2020-04',8),('2020-04',9),
#              ('2020-05',1),('2020-05',2),('2020-05',3),('2020-05',4),('2020-05',5),('2020-05',6),('2020-05',7),('2020-05',8),
#              ('2020-06',1),('2020-06',2),('2020-06',3),('2020-06',4),('2020-06',5),('2020-06',6),('2020-06',7),
#              ('2020-11',1)]
#ajustado

Dev_cond2 = cl.Development(average='simple')
#Dev_cond2 = cl.Development(average='simple', drop = lista_excl)


############# FACTORES DE DESARROLLO POR PERIODO

fdi_tr = Dev_cond2.fit_transform(tri_inc_acum_f).ldf_
fdi = fdi_tr.to_frame()
############# FACTORES DE DESARROLLO ACUMULADOS
fda_tr = Dev_cond2.fit_transform(tri_inc_acum_f).cdf_
fda  = fda_tr.to_frame()



### Sin embargo hay factore individuales menores a 1 
# entonces los reemplazaremos por 1 y hallaremos los nuevos FDA

fdi2 = fdi.stack().to_frame("default")                 # alos fdi iniciales los llamaremos default
fdi2["min"] = 1                                        #crearemos una columna con 1 para comparar
fdi2["final"] = fdi2[["default", "min"]].max(axis=1)   # nos quedamos con el maximo de ambos 
fdi2 =fdi2.droplevel(0,0)                              # eliminamos el primer indice
fdi2["key"] = fdi2.index                               # creamos una columna igual al indice
fdi2[['first','last']] = fdi2.key.str.split("-",expand=True,)  #separamos la columna creada ( 1-2) igual a 1 y 2
fdi2 = fdi2[['first','final']]                         # nos quedamos con las columnas finales
fdi2['first'] = fdi2['first'].astype(int)              #convertimos el indice en int para que haga match con el triangulo
                                           #confirmamos que le tipo es int

fdi2 = fdi2.set_index("first",drop = True)             # lo convertimos en indice
fdi2 = dict(zip(fdi2.index,fdi2["final"]))             #lo convertimos en diccionario


Dev_cond2 = cl.DevelopmentConstant(patterns=fdi2, style='ldf' )   # lo pasamos a condicion de desarrollo

tri_lratios_ajus = Dev_cond2.fit_transform(tri_inc_acum_f).link_ratio
tr_lratios_ajus = tri_lratios_ajus.to_frame()
tr_lratios_ajus.index = tr_lratios_ajus.index.strftime('%Y-%m')
st.dataframe(tr_lratios_ajus.round(3).style.background_gradient(cmap="Blues"), height = 800)


############# FACTORES DE DESARROLLO POR PERIODO FINALES 
st.markdown("**Factores de Desarrollo por Periodo**")
fdi_tr = Dev_cond2.fit_transform(tri_inc_acum_f).ldf_
fdi = fdi_tr.to_frame()
st.dataframe(fdi)

############# FACTORES DE DESARROLLO ACUMULADOS FINALES
st.markdown("**Factores de Desarrollo por Acumulado**")
fda_tr = Dev_cond2.fit_transform(tri_inc_acum_f).cdf_
st.dataframe(fda)


#Dev_cond2.fit_transform(tri_inc_acum_f)
#cl.Chainladder().fit(Dev_cond2.fit_transform(tri_inc_acum_f)).ultimate_
# apartir de los ultimates reconstruye el triangulo
#cl.Chainladder().fit(Dev_cond2.fit_transform(tri_inc_acum_f)).full_expectation_



######### TRIANGULO FALTANTE PROYECTADO 

tr_proyectado = cl.Chainladder().fit(Dev_cond2.fit_transform(tri_inc_acum_f)).full_triangle_.to_frame()
#cl.Chainladder().fit(Dev_cond2.fit_transform(tri_inc_acum_f)).ibnr_
#cl.MackChainladder().fit(Dev_cond2.fit_transform(tri_inc_acum_f)).ibnr_


##### RESULTADOS ##############

c_latest = cl.Chainladder().fit(Dev_cond2.fit_transform(tri_inc_acum_f)).latest_diagonal.to_frame()
c_latest.columns.values[0] = "Latest"

c_ibnr = cl.Chainladder().fit(Dev_cond2.fit_transform(tri_inc_acum_f)).ibnr_.to_frame()
c_ibnr.columns.values[0] = "IBNR"

c_ultimate = cl.Chainladder().fit(Dev_cond2.fit_transform(tri_inc_acum_f)).ultimate_.to_frame()
c_ultimate.columns.values[0] = "Ultimate"

resumen =  c_latest
resumen["IBNR"] = c_ibnr
resumen["Ultimate"] = c_ultimate
resultado  = resumen.fillna(0)
resultado.index = resultado.index.strftime('%Y-%m')



#-- insertamos los FDA en el resumen

fda2 = fda.stack().reset_index(drop=True)
fda2[len(fda2)]=1   # agregamos un 1 al final
fda2 = fda2.loc[::-1] # invertimos el orden 
fda2.index = resultado.index # que su index sean los periodos
resultado.insert(1,"FDA",fda2) # lo agregamos al resumen


st.dataframe(resultado)

llaves = pd.DataFrame(fda.columns.tolist(), columns =[" key"]) #extremos el nombre de las columnas de los fda
llaves = llaves.loc[::-1] # invertimos el orden 


#################### EXPORTAMOS A EXCEL   #######################################################

### creamos un excel
writer = pd.ExcelWriter(' Resumen '+ nombre_archivo+ " " +'.xlsx')
workbook=writer.book

#------------ agregamos hoja base input -------------------------------------------
worksheet=workbook.add_worksheet('BASE')

writer.sheets['BASE'] = worksheet

worksheet.write_string(1, 1, "Base de siniestros")
base0.to_excel(writer,sheet_name='BASE',
                              startrow=2 , startcol=1)


#------------ agregamos hoja triangulo incurridos -------------------------------------------
worksheet=workbook.add_worksheet('Tri incurridos')

writer.sheets['Tri incurridos'] = worksheet

worksheet.write_string(1, 1, "Triangulo de incurridos incremental")
tr_incurridos_increm.to_excel(writer,sheet_name='Tri incurridos',
                              startrow=2 , startcol=1)

worksheet.write_string(tr_incurridos_increm.shape[0] + 4, 1, "Triangulo de incurridos acumulado")
tr_incurridos_acum.to_excel(writer,sheet_name='Tri incurridos',
                            startrow=tr_incurridos_increm.shape[0] + 5, startcol=1)



#------------ agregamos hoja triangulo pagos -------------------------------------------
worksheet=workbook.add_worksheet('Tri pagos')

writer.sheets['Tri pagos'] = worksheet

worksheet.write_string(1, 1, "Triangulo de pagos incremental")
tr_pagos_increm.to_excel(writer,sheet_name='Tri pagos',
                              startrow=2 , startcol=1)

worksheet.write_string(tr_pagos_increm.shape[0] + 4, 1, "Triangulo de pagos acumulado")
tr_pagos_acum.to_excel(writer,sheet_name='Tri pagos',
                            startrow=tr_pagos_increm.shape[0] + 5, startcol=1)


#------------ agregamos hoja triangulo reservas -------------------------------------------
worksheet=workbook.add_worksheet('Tri reservas')

writer.sheets['Tri reservas'] = worksheet

worksheet.write_string(1, 1, "Triangulo de reservas incremental")
tr_reservas_increm.to_excel(writer,sheet_name='Tri reservas',
                              startrow=2 , startcol=1)

worksheet.write_string(tr_reservas_increm.shape[0] + 4, 1, "Triangulo de reservas acumulado - Evolución de Reservas")
tr_reservas_acum.to_excel(writer,sheet_name='Tri reservas',
                            startrow=tr_reservas_increm.shape[0] + 5, startcol=1)


#------------ agregamos hoja triangulo final más link ratios inicial -------------------------------------------
worksheet=workbook.add_worksheet('Tri final')

writer.sheets['Tri final'] = worksheet

worksheet.write_string(1, 1, "Triangulo final acumulado")
tr_final_acum.to_excel(writer,sheet_name='Tri final',
                              startrow=2 , startcol=1)

worksheet.write_string(tr_final_acum.shape[0] + 4, 1, "Link Ratios Iniciales")
tr_lratios_ajus.to_excel(writer,sheet_name='Tri final',
                            startrow=tr_final_acum.shape[0] + 5, startcol=1)



#------------ agregamos hoja de link ratios ajustados y Factores  -------------------------------------------
worksheet=workbook.add_worksheet('L-ratios y FDs')

writer.sheets['L-ratios y FDs'] = worksheet

worksheet.write_string(1, 1, "Triangulo de link Ratios ajustados")
tr_lratios_ajus.to_excel(writer,sheet_name='L-ratios y FDs',
                              startrow=2 , startcol=1)

worksheet.write_string(tr_lratios_ajus.shape[0] + 4, 1, "FDI")
fdi.to_excel(writer,sheet_name='L-ratios y FDs',
             startrow=tr_lratios_ajus.shape[0] + 5, startcol=1)


worksheet.write_string(tr_lratios_ajus.shape[0] + 5 + fdi.shape[0] + 3, 1, "FDA")
fda.to_excel(writer,sheet_name='L-ratios y FDs',
             startrow=tr_lratios_ajus.shape[0] + 6 + fdi.shape[0] + 3,
             startcol=1)


#------------ agregamos hoja resultados  -------------------------------------------
worksheet=workbook.add_worksheet('Resultado')

writer.sheets['Resultado'] = worksheet
worksheet.write_string(1, 1, "Tabla de Resultados IBNR") 
resultado.to_excel(writer,sheet_name='Resultado',startrow=3 , startcol=1)
llaves.to_excel(writer,sheet_name='Resultado',startrow=4 , startcol=8)

#totales
worksheet.write_string( resultado.shape[0] + 5, 1, "Total")
worksheet.write_number( resultado.shape[0] + 5, 2, sum(resultado["Latest"])) 
worksheet.write_number( resultado.shape[0] + 5, 4, sum(resultado["IBNR"])  ) 
worksheet.write_number( resultado.shape[0] + 5, 5, sum(resultado["Ultimate"])  ) 


#------------ agregamos hoja inconsistencias  -------------------------------------------



inconsistencias.to_excel(writer,sheet_name='Inconsistencias',startrow=3 , startcol=1)


writer.save()




data_final0 = tr_incurridos_increm

data_final0 =  data_final0.append(pd.Series(name=''))
data_final0.loc['TR Pagos Incremental'] = tr_pagos_increm.columns
data_final0  = data_final0.append(tr_pagos_increm)


data_final0 =  data_final0.append(pd.Series(name=''))
data_final0.loc['TR Reservas incremental'] = tr_reservas_increm.columns
data_final0  = data_final0.append(tr_reservas_increm)



data_final = tr_incurridos_acum

data_final =  data_final.append(pd.Series(name=''))
data_final.loc['TR Pagos Acum'] = tr_incurridos_acum.columns
data_final  = data_final.append(tr_pagos_acum)


data_final =  data_final.append(pd.Series(name=''))
data_final.loc['TR Reservas acumulado'] = tr_reservas_acum.columns
data_final  = data_final.append(tr_reservas_acum)


data_final =  data_final.append(pd.Series(name=''))
tr_lratios_ajus["ultimo"]=""
tr_lratios_ajus.columns = data_final.columns
data_final.loc['TR Link Ratios '] = tr_reservas_acum.columns
data_final  = data_final.append(tr_lratios_ajus)


data_final =  data_final.append(pd.Series(name=''))
fdi["ultimo"]=""
fdi.columns = data_final.columns
data_final.loc['FDI '] = fdi.columns
data_final  = data_final.append(fdi)


data_final =  data_final.append(pd.Series(name=''))
fda["ultimo"]=""
fda.columns = data_final.columns
data_final.loc['FDA'] = fda.columns
data_final  = data_final.append(fda)


data_final  = data_final.fillna("")






csv = data_final0.to_csv()
b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
href = f'<a href="data:file/csv;base64,{b64}">Download CSV Triangulos incrementales </a> (save as Triangulos incrementales.csv)'
st.markdown(href, unsafe_allow_html=True)


csv = data_final.to_csv()
b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
href = f'<a href="data:file/csv;base64,{b64}">Download CSV Triangulos acumulados y FDs </a> (save as Triangulos.csv)'
st.markdown(href, unsafe_allow_html=True)


resultado.loc["Total"] = resultado.sum()
resultado.loc[("Total"),("FDA")] = ""
csv = resultado.to_csv()
b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
href = f'<a href="data:file/csv;base64,{b64}">Download CSV Resultado </a> (save as Resultados.csv)'
st.markdown(href, unsafe_allow_html=True)

