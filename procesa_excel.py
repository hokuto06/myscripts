import pandas as pd

def map_connected_device(file_path, output_path):
    """
    Procesa un archivo Excel y guarda en la columna index 8 (I) el nombre (index 2, C)
    del dispositivo cuya MAC (index 1, B) coincide con la MAC de la columna index 5 (F) 
    del dispositivo actual.

    Args:
        file_path (str): Ruta del archivo Excel de entrada.
        output_path (str): Ruta donde se guardará el archivo Excel procesado.
    """
    try:
        # Leer el archivo Excel sin encabezados
        df = pd.read_excel(file_path, engine='openpyxl', header=None)

        # Verificar que las columnas necesarias existan
        required_indices = [1, 2, 5]  # B=1, C=2, F=5
        if max(required_indices) >= df.shape[1]:
            print(f"Error: El archivo debe contener al menos {max(required_indices) + 1} columnas.")
            return

        # Crear un diccionario para mapear MAC (index 1) -> Name (index 2)
        mac_to_name = dict(zip(df.iloc[:, 1].astype(str), df.iloc[:, 2].astype(str)))

        # Asignar a la columna index 8 (I) el nombre correspondiente a la MAC en index 5 (F)
        df.iloc[:, 5] = df.iloc[:, 5].map(mac_to_name)

        # Guardar el archivo procesado
        df.to_excel(output_path, index=False, header=False, engine='openpyxl')
        print(f"Archivo procesado guardado en {output_path}")

    except Exception as e:
        print(f"Error al procesar el archivo Excel: {e}")

#map_connected_device("devices_output.xlsx", "processed_devices.xlsx")

def delete_content():
    # Cargar el archivo Excel
    file_path = "processed_devices.xlsx"  # Reemplaza con el nombre de tu archivo
    sheet_name = "Sheet1"  # Reemplaza con el nombre de tu hoja, si es necesario

    # Leer el archivo Excel
    df = pd.read_excel(file_path, sheet_name=sheet_name)

    # Eliminar todo hasta el último guion en la columna 0
    df.iloc[:, 2] = df.iloc[:, 2].str.replace(r'^.*-', '', regex=True)

    # Guardar los cambios en un nuevo archivo Excel
    df.to_excel("archivo_modificado.xlsx", index=False)

# delete_content()

def concatenate_simple():
    file_path = "archivo_modificado.xlsx"
    df = pd.read_excel(file_path)
    columna_2 = df.iloc[29:, 2]
    for hab in columna_2:
        if pd.notnull(hab):
            print("Hab "+str(hab))

# concatenate_simple()

def concatenate_for_unifi_db():
    #'db.tag.insert({"name" : "prueba","site_id" : "64c08dd9d51d7f0296e44f5f","member_table":["60:22:32:1e:e0:27"]})
    file_path = "buetx.xlsx"
    site_id = "64c08dd9d51d7f0296e44f5f"
    try:
        # Leer el archivo Excel
        df = pd.read_excel(file_path, engine="openpyxl", header=None)

        required_columns = [1, 0] 
        if max(required_columns) >= df.shape[1]:
            print(f"Error: El archivo debe contener al menos {max(required_columns) + 1} columnas.")
            return

        # Iterar sobre las filas para generar los comandos
        for index, row in df.iterrows():
            name = row[1]  # Columna 2 (name)
            mac = row[0]   # Columna 3 (mac)

            # Validar que no haya valores vacíos
            if pd.isna(name) or pd.isna(mac):
                print(f"Fila {index + 1}: Datos incompletos. Saltando esta fila.")
                continue

            # Generar el comando db.tag.insert
            insert_command = f'db.tag.insert({{"name" : "{name}","site_id" : "{site_id}","member_table":["{mac}"]}})'
            print(insert_command)

    except Exception as e:
        print(f"Error al procesar el archivo Excel: {e}")

concatenate_for_unifi_db()