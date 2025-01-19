import pandas as pd

# Cargar el archivo Excel (reemplaza 'archivo.xlsx' con la ruta a tu archivo)
ruta_archivo = 'datos.xlsx'
df = pd.read_excel(ruta_archivo, header=None)

# Concatenar las columnas 0, 3 y 7 con '-' como separador
df['Concatenado'] = df.iloc[:, [0, 3, 7]].fillna('').apply(lambda row: '-'.join(row.astype(str)), axis=1)

# Crear un encabezado personalizado
nombre_encabezado = ['id 1', 'ip', 'serial','sdaa','piso','loc','loc','type','concatenado']  # Ajusta según sea necesario
df.columns = nombre_encabezado[:len(df.columns)] + ['Concatenado']

# Guardar el resultado en un nuevo archivo Excel con el encabezado
df.to_excel('resultado_concatenado.xlsx', index=False)

print("El archivo con los datos concatenados y encabezado se ha guardado como 'resultado_concatenado.xlsx'")

