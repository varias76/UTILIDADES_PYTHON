import pandas as pd
from datetime import datetime

def generar_insert_sql(archivo_excel, hoja, salida_sql):
    """
    Genera sentencias SQL para un procedimiento almacenado basado en un archivo Excel.

    Parámetros:
    - archivo_excel: Ruta del archivo Excel.
    - hoja: Nombre de la hoja en el Excel.
    - salida_sql: Ruta del archivo SQL de salida.
    """
    try:
        # Leer el archivo Excel
        df = pd.read_excel(archivo_excel, sheet_name='Hoja1')
        print(df)
        # Verificar columnas necesarias
        if 'CORRELATIVO' not in df.columns or 'CORR_PROV' not in df.columns:
            raise ValueError("El archivo Excel debe contener las columnas 'CORRELATIVO' y 'CORR_PROV'.")

        # Formato de la fecha actual print(fecha_actual)
        fecha_actual =str(datetime.now().strftime('%Y%m%d'))
       
          # Generar sentencias SQL
        sentencias_sql = []
        sentencias_sql.append('declare @activo integer')
        for index, row in df.iterrows():
            try:
                correlativo = row['CORRELATIVO']
                proveedor = row['CORR_PROV']
          
                sentencia = (
                    f"EXEC SPI_ARTICULO_PROVEEDOR {correlativo}, {proveedor}, "
                    f"'{fecha_actual}', @ACTIVO, 'DPEREZ';"
                ) 
                sentencias_sql.append(sentencia)
               
            except Exception as e:
                print(f"Error procesando fila {index}: {e}")

       # Guardar en un archivo .sql
        with open(salida_sql, 'w', encoding='utf-8') as archivo:
            archivo.write("\n".join(sentencias_sql))  # Escribir todas las sentencias SQL

        print(f"Archivo SQL generado exitosamente en: {salida_sql}")

    except Exception as e:
        print(f"Error general: {e}")

# Configuración de entrada y salida
archivo_excel = r"C:\MASIVO_EXCEL.xlsx"  # Ruta completa del archivo Excel
hoja = "Hoja1"  # Nombre de la hoja en el Excel
salida_sql = r"C:\sentencias_sql.sql"  # Ruta completa del archivo SQL de salida




if __name__== "__main__":
    generar_insert_sql(archivo_excel, hoja, salida_sql)
