from myUnifiApi import UnifiApiController
import pandas as pd
import argparse
import json
import os
from pprint import pprint

def saveOnExcel(rows):
    df = pd.DataFrame(rows)
    output_file = "devices_output.xlsx"
    df.to_excel(output_file, index=False)
    print(f"Archivo guardado como {output_file}")

# test_api = UnifiApiController(ipController="172.20.197.148", userController="rsupport", passwordController="elrbsestNF!25")
# devices = test_api.getDevices()
# saveOnExcel(devices)

################################

CONFIG_FILE = "controller_config.json"

def save_controller_config(ip, username, password):
    config = {"ip": ip, "username": username, "password": password}
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)
    print(f"Configuración guardada en {CONFIG_FILE}")


def load_controller_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return None

def get_controller_instance():
    config = load_controller_config()

    if not config:
        # Si no hay configuración almacenada, solicita los datos
        ip = input("Ingresa la IP del controlador: ")
        username = input("Ingresa el usuario: ")
        password = input("Ingresa la contraseña: ")
        save_controller_config(ip, username, password)
        config = {"ip": ip, "username": username, "password": password}

    # Crear la instancia del controlador
    return UnifiApiController(
        ipController=config["ip"],
        userController=config["username"],
        passwordController=config["password"]
    )

def get_tags():
    controller = get_controller_instance()
    tags = controller.get_tags()
    pprint(tags)

def update_tags_in_excel():
    # Cargar el archivo Excel con las MACs
    file_path = "devices_output.xlsx"
    try:
        df = pd.read_excel(file_path, engine="openpyxl")
    except Exception as e:
        print(f"Error al leer el archivo Excel: {e}")
        return

    # Verificar que el archivo contenga la columna de MACs
    if "MAC" not in df.columns:
        print("El archivo Excel no contiene una columna 'MAC'.")
        return

    # Obtener los tags del controlador
    controller = get_controller_instance()
    tags = controller.get_tags()
    if not tags:
        print("No se pudieron obtener los tags del controlador.")
        return

    # Crear un diccionario para buscar rápidamente tags por MAC
    mac_to_tag = {}
    for tag in tags:
        for mac in tag.get("MACs", []):
            mac_to_tag[mac] = tag.get("Name", "N/A")

    # Actualizar la columna 8 (índice 7) con los tags correspondientes
    df["Tag"] = df["MAC"].map(mac_to_tag).fillna("Sin Tag")

    # Guardar el archivo actualizado
    output_file = "devices_output_with_tags.xlsx"
    try:
        df.to_excel(output_file, index=False, engine="openpyxl")
        print(f"Archivo actualizado guardado como {output_file}")
    except Exception as e:
        print(f"Error al guardar el archivo Excel: {e}")


def handle_get():
    """Maneja la operación de obtención de dispositivos."""
    controller = get_controller_instance()
    devices = controller.getDevices()
    print("\nLista de Dispositivos:")
    saveOnExcel(devices)

def test_tags():
    controller = get_controller_instance()
    controller.setDeviceTag()

def handle_set():
    file = "buetxsw.xlsx"
    # Parámetros predeterminados
    default_netmask = "255.255.255.0"
    default_gateway = "192.168.222.1"
    default_dns = "192.168.222.1"

    controller = get_controller_instance()

    try:
        # Leer el archivo Excel sin encabezados
        df = pd.read_excel(file, engine="openpyxl", header=None)

        # Verificar que las columnas necesarias existan por índice
        required_indices = [1]  # A=0, E=4, K=10
        if max(required_indices) >= df.shape[1]:
            print(f"Error: El archivo debe contener al menos {max(required_indices) + 1} columnas.")
            return

        # Iterar por cada fila del archivo Excel
        for index, row in df.iterrows():
            device_id = row[0]  # Columna A (índice 0)
            # device_ip = row[4]  # Columna E (índice 4)
            device_name = row[1]  # Columna L (índice 10)

            # Validar que los datos necesarios no estén vacíos
            if pd.isna(device_id) or pd.isna(device_id) or pd.isna(device_name):
                print(f"Fila {index + 1}: Datos incompletos. Saltando esta fila.")
                continue

            # Configurar el dispositivo
            print(f"Configurando dispositivo ID: {device_id}, Nombre: {device_name}")
            controller.setupDevice(
                device_id=device_id,
                device_name=device_name,
                # device_ip=device_ip,
                # device_netmask=default_netmask,
                # device_gateway=default_gateway,
                # device_dns=default_dns
            )

    except Exception as e:
        print(f"Error al procesar el archivo Excel: {e}")

def read_and_concatenate_columns():
    file_path = "buetx.xlsx"
    try:
        df = pd.read_excel(file_path, engine='openpyxl', header=None)
        required_indices = [8, 9, 2]  # I=8, J=9, C=2 (índices son base 0)
        if max(required_indices) >= df.shape[1]:
            print(f"Error: El archivo no tiene suficientes columnas para los índices {required_indices}")
            return
        concatenated = df.iloc[:, 8].astype(str) + '-' + df.iloc[:, 9].astype(str) + '-' + df.iloc[:, 2].astype(str)
        print("\n".join(concatenated))
    except Exception as e:
        print(f"Error al procesar el archivo Excel: {e}")

def main():
    parser = argparse.ArgumentParser(description="Script para gestionar dispositivos UniFi.")
    parser.add_argument("--tag", action="store_true", help="Intentar modificar tags.")
    parser.add_argument("--get", action="store_true", help="Obtener lista de dispositivos del controlador.")
    parser.add_argument("--gettags", action="store_true", help="Obtener lista de tags del controlador.")
    parser.add_argument("--set", action="store_true", help="Configurar dispositivos usando un archivo Excel.")
    # parser.add_argument("--set", type=str, metavar="FILE", help="Configurar dispositivos usando un archivo Excel.")
    parser.add_argument("--conc", action="store_true", help="Concatenar columnas de un archivo Excel.")
    parser.add_argument("--h", action="store_true", help="Mostrar las opciones disponibles.")
    args = parser.parse_args()

    if args.h:
        parser.print_help()

    elif args.get:
        handle_get()

    elif args.tag:
        test_tags()

    elif args.gettags:
        update_tags_in_excel()

    elif args.set:
        handle_set()

    elif args.conc:
        read_and_concatenate_columns()

    else:
        print("Opción no válida. Usa --h para ver las opciones.")

if __name__ == "__main__":
    main()