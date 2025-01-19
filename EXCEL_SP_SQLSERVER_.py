import PySimpleGUI as sg
# conexion a bd
from sqlalchemy import create_engine
import pyodbc
from sqlalchemy.orm import sessionmaker
import json
import pandas as pd
from pathlib import Path 
import os 
from datetime import datetime


def conectar():
        print(pyodbc.drivers())
        SERVER='192.168.80.130'
        DATABASE ='VTA_LOCALES'
        DRIVER = 'SQL Server Native Client 11.0'
        USERNAME='usuario'
        PASSWORD='password'
        DATABASE_CONNECTION = f'mssql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}'
    
        try:
            engine = create_engine("mssql+pyodbc://"+USERNAME+":"+PASSWORD+"@"+SERVER+"/"+DATABASE+"?driver=ODBC+Driver+11+for+SQL+Server",  fast_executemany=True)
            # Crear sesión con el engine de base de datos
            
            session = sessionmaker(bind=engine)
            session = session()
            connection= engine.connect()
            print(f" Successfully Connected to the database: {DATABASE}")
            session.query = "EXEC pac_SF_MOV_Contabilidad @P_FECHA_DESDE="  + "'" + FECHAINI + "'" +' , '+"@P_FECHA_HASTA="+ "'" + FECHAFIN + "'"
            data    = pd.read_sql_query(session.query ,  connection)
            data.dtypes
           
            try:             
                 
                nombre_archivo= "Datos_"+   datetime.now().strftime("%d-%b-%Y %H%M%S")+ ".CSV"
                data.to_csv( nombre_archivo+'.csv' ,index = False, encoding='latin1')                 
                connection.close()         
            except Exception as ex:
                 print(f" Sorry can't found the path: {ex}")                
        except Exception as ex:
            print(f" Sorry Could not connect to the database: {ex}")

   
    
if __name__== "__main__":
   

    sg.theme('SandyBeach')     
    layout = [
    [sg.Text('Ingrese Fecha Desde y Hasta AAAAMMDD')],
    [sg.Text('Fecha Desde', size =(10, 1)), sg.InputText()],
    [sg.Text('Fecha Hasta', size =(10, 1)), sg.InputText()],
    [sg.Button('Ok'), sg.Button('Cancel')] ]
  
    window = sg.Window('Reporte de venta Mensual ', layout)
    event, values = window.read()
    print(event, values[0], values[1])
    FECHAINI = values[0] #'20230101'
    FECHAFIN = values[1] #'20230801'
    
    try: 
        conectar()
        print(f" Successfully ")
        
                
        layout = [
         [sg.Text(text='Archivo csv Creado correctamente, presione CERRAR' ,font=('Arial Bold', 10), size=20,  expand_x=True,  justification='center')],
          [sg.Text(text=pyodbc.drivers() ,font=('Arial Bold', 5), size=10,  expand_x=True,  justification='left')],
       
         [ sg.Button('Cerrar')]]

        window = sg.Window('Archivo csv creado :'+'C:\\VENTAS', layout, size=(715,150))  

        event, values = window.read()
        window.close()
   
    except Exception  as ex:   
        print(f" Sorry Could not create file: {ex}")
       
        window.close()
        
    
    
