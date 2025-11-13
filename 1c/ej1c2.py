"""
Enunciado:
Desarrolla un cliente para consultar la información de estaciones del sistema de bicicletas 
compartidas de Barcelona utilizando la API GBFS (General Bikeshare Feed Specification).

Tareas:
1. Consultar el endpoint de información de estaciones
2. Extraer datos específicos de cada estación
3. Convertir coordenadas de estaciones a un DataFrame de pandas
4. Procesar y estructurar la información recibida

Esta práctica te ayudará a entender cómo trabajar con APIs reales y procesar datos
en diferentes formatos utilizando pandas.

Tu tarea es completar la implementación de las funciones indicadas.
"""

import requests
from typing import Optional, Dict, Tuple
import pandas as pd

def get_stations_data()-> Optional[Dict]:
    """
    Realiza una petición a la API para obtener información de las estaciones
    y extrae el objeto 'data' de la respuesta.
    
    Returns:
        dict: El objeto 'data' que contiene la lista de estaciones
        None: Si ocurre un error en la petición o el objeto 'data' no existe
    """
    # URL del endpoint de información de estaciones
    url = "https://barcelona.publicbikesystem.net/customer/gbfs/v2/en/station_information"
    
    # Implementa aquí la lógica para:
    # 1. Realizar una petición GET a la URL
    # 2. Verificar que la respuesta sea correcta (código 200)
    # 3. Extraer y devolver el objeto 'data' del JSON recibido
    # 4. Manejar posibles errores (conexión, formato, etc.)
    try:
        # Realizamos la petición GET a la url
        resp = requests.get(url)
        # Verificamos que la respuesta es correcta (código 200)
        if resp.status_code == 200:
            # Devolvemos los datos en formato JSON
            data_json = resp.json()
            result = data_json['data']
            return result
        return None
    except requests.exceptions.RequestException:
        # Capturamos cualquier error que pueda ocurrir durante la petición
        return None


def get_station_info(stations_data, station_id)-> Optional[Dict]:
    """
    Busca y devuelve la información de una estación específica según su ID.

    Args:
        stations_data (dict): Datos de estaciones obtenidos con get_stations_data()
        station_id (str): ID de la estación a buscar

    Returns:
        dict: Información de la estación solicitada
        None: Si no se encuentra la estación o los datos de entrada son inválidos
    """
    # Implementa aquí la lógica para:
    # 1. Verificar que stations_data no es None y tiene la estructura esperada
    # 2. Buscar la estación con el ID proporcionado en la lista de estaciones
    # 3. Devolver la información completa de esa estación
    # 4. Si no existe, devolver None

    # Verificamos que stations_data no es None y tiene la estructura esperada
    if not stations_data or not isinstance(stations_data, dict) or 'stations' not in stations_data: # solución
        return None
    # Buscamos la estación con el ID proporcionado
    stations = stations_data['stations']
    for station in stations:
        if station['station_id'] == station_id:
            return station
    return None


def get_station_coordinates(station_info)-> Optional[pd.DataFrame]:
    """
    Extrae las coordenadas (latitud y longitud) de una estación.

    Args:
        station_info (dict): Información de una estación específica

    Returns:
        tuple: Par (latitud, longitud) de la estación
        None: Si station_info es None o no contiene las coordenadas
    """
    # Implementa aquí la lógica para:
    # 1. Verificar que station_info no es None
    # 2. Extraer los valores de latitud y longitud del diccionario
    # 3. Devolver ambos valores como una tupla (lat, lon)
    # 4. Manejar casos donde los campos no existan

    # Verificamos que station_info no es None
    if not station_info or not isinstance(station_info, dict):      # solución
        return None
    
    # Extraemos los valores de latitud y longitud del diccionario
    station_lat = station_info.get('lat')
    station_lon = station_info.get('lon') 

    # Devolvemos los valores como tupla
    if station_lat is not None and station_lon is not None:
        return (station_lat, station_lon)
    return None


def create_stations_dataframe(stations_data)-> Optional[pd.DataFrame]:
    """
    Crea un DataFrame de pandas con información básica de todas las estaciones.

    Args:
        stations_data (dict): Datos de estaciones obtenidos con get_stations_data()

    Returns:
        pandas.DataFrame: DataFrame con columnas 'station_id', 'latitude', 'longitude', 'name'
        None: Si stations_data es None o no tiene la estructura esperada
    """
    # Implementa aquí la lógica para:
    # 1. Verificar que stations_data no es None y tiene la estructura esperada
    # 2. Crear una lista de diccionarios con la información básica de cada estación
    # 3. Convertir esa lista en un DataFrame de pandas
    # 4. El DataFrame debe tener las columnas: 'station_id', 'latitude', 'longitude', 'name'

    # Verificamos que stations_data no es None

    if not stations_data or not isinstance(stations_data, dict) or 'stations' not in stations_data:    # solución
        return None
    
    df_stations = pd.DataFrame()
    
    # Creamos una lista de diccionarios con la información de cada estación
    stations_list =[]
    for station in stations_data['stations']:
        stations_list.append(station)
    df_stations = pd.DataFrame(stations_list)
    df_stations.rename(columns={'lat': 'latitude', 'lon': 'longitude'}, inplace=True)

    return df_stations


if __name__ == '__main__':
    # Obtener los datos de todas las estaciones
    stations_data = get_stations_data()

    if stations_data:
        # Ejemplo: Obtener información de la estación con ID "1"
        station_1 = get_station_info(stations_data, "1")
        if station_1:
            print(f"Estación encontrada: {station_1['name']}")

            # Obtener coordenadas
            coordinates = get_station_coordinates(station_1)
            if coordinates:
                lat, lon = coordinates
                print(f"Coordenadas: ({lat}, {lon})")

        # Crear DataFrame con todas las estaciones
        invalid_data = {"other_field": "value"}
        df = create_stations_dataframe(invalid_data)

        #df = create_stations_dataframe(stations_data)
        if df is not None:
            print("\nPrimeras 5 estaciones:")
            print(df.head())
            print(f"\nTotal de estaciones: {len(df)}")
    else:
        print("No se pudieron obtener los datos de las estaciones.")
