import pandas as pd

# Cargar el archivo Excel (reemplaza 'archivo.xlsx' con la ruta a tu archivo)
ruta_archivo = 'datos.xlsx'
df = pd.read_excel(ruta_archivo)

# Concatenar las columnas 0, 3 y 7 con '-' como separador
df['Concatenado'] = df.iloc[:, [0, 5, 7]].fillna('').apply(lambda row: '-'.join(row.astype(str)), axis=1)

# Guardar el resultado en un nuevo archivo Excel
df.to_excel('resultado_concatenado.xlsx', index=False)

print("El archivo con los datos concatenados se ha guardado como 'resultado_concatenado.xlsx'")
