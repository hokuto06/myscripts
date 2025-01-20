import pandas as pd

# Cargar los archivos Excel y las hojas específicas
fc_buesc_path = 'FC_BUESC_2025.xlsx'
aps_on_switches_path = 'aps_on_switches.xlsx'

fc_buesc = pd.read_excel(fc_buesc_path, sheet_name='Access Point Sheraton', header=None)
aps_on_switches = pd.read_excel(aps_on_switches_path, sheet_name='Neighbors', header=None)

# Filtrar solo los datos relevantes a partir de la fila 9 en FC_BUESC_2025
fc_buesc_data = fc_buesc.iloc[8:].reset_index(drop=True)

# Nombrar las columnas relevantes en FC_BUESC_2025
fc_buesc_data.columns = [
    f'Columna_{i}' for i in range(len(fc_buesc_data.columns))
]  # Asignar nombres genéricos
fc_buesc_data.rename(
    columns={'Columna_3': 'MAC Address', 'Columna_8': 'Nomenclatura', 'Columna_9': 'Puerto'},
    inplace=True
)

# Renombrar columnas de aps_on_switches.xlsx
aps_on_switches.columns = ['Nomenclatura', 'MAC Address', 'Puerto']

# Unir ambos DataFrames basado en 'MAC Address'
fc_buesc_data = fc_buesc_data.merge(
    aps_on_switches,
    how='left',
    left_on='MAC Address',
    right_on='MAC Address',
    suffixes=('', '_aps')
)

# Actualizar las columnas 'Nomenclatura' y 'Puerto' en fc_buesc_data
fc_buesc_data['Nomenclatura'] = fc_buesc_data['Nomenclatura'].fillna
