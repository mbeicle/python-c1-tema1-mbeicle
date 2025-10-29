"""
Enunciado:
Este ejercicio introduce el uso de bibliotecas especializadas para acceder a APIs de forma
sencilla y estructurada. En concreto, utilizaremos la biblioteca pybikes que proporciona
wrappers para múltiples sistemas de bicicletas compartidas en todo el mundo.

En lugar de construir nuestro propio cliente HTTP y procesar manualmente los datos JSON,
aprenderemos a utilizar herramientas existentes que hacen este trabajo por nosotros.

Tareas:
1. Explorar los sistemas de bicicletas disponibles
2. Obtener información sobre el sistema de Barcelona (Bicing)
3. Analizar los datos de las estaciones

Esta práctica ilustra cómo las bibliotecas especializadas simplifican el acceso a APIs
y permiten concentrarse en el análisis de datos en lugar de en los detalles técnicos
de la comunicación con la API.
"""

import pybikes
import pandas as pd
import time
from typing import List, Dict, Any, Optional
import matplotlib.pyplot as plt
import sys


def listar_sistemas_disponibles() -> List[str]:
    """
    Obtiene una lista de todos los sistemas de bicicletas disponibles en pybikes.

    Returns:
        List[str]: Lista de identificadores de sistemas disponibles
    """
    # Implementa aquí la lógica para obtener y devolver la lista
    # de sistemas disponibles en pybikes
    sistemas = []
    files_sistemas = pybikes.getDataFiles()
    for sistema in files_sistemas:
        sistema = sistema.split('.')[0]
        sistemas.append(sistema)

    return sistemas


def buscar_sistema_por_ciudad(ciudad: str) -> List[str]:
    """
    Busca sistemas de bicicletas que contengan el nombre de la ciudad especificada.

    Args:
        ciudad (str): Nombre de la ciudad a buscar

    Returns:
        List[str]: Lista de sistemas que coinciden con la búsqueda
    """
    # Implementa aquí la lógica para buscar y devolver sistemas
    # que coincidan con la ciudad especificada
    sistemas_barcelona = []
    sistemas = []
    files_sistemas = pybikes.getDataFiles()
    for sistema in files_sistemas:
        sistema = sistema.split('.')[0]
        sistemas.append(sistema)
    for sistema in sistemas:
        sistema_data = pybikes.getDataFile(sistema)
        if 'instances' in sistema_data:
            for instance in sistema_data['instances']: 
                if 'city' in instance['meta']:
                    if instance['meta']['city'] == ciudad:
                        sistemas_barcelona.append(sistema)
                        print(sistemas_barcelona)

    return sistemas_barcelona


def obtener_info_sistema(tag: str) -> Dict[str, Any]:
    """
    Obtiene la información del sistema especificado.

    Args:
        tag (str): Identificador del sistema (por ejemplo, 'bicing')

    Returns:
        Dict[str, Any]: Metadatos del sistema o None si no existe
    """
    # Implementa aquí la lógica para obtener y devolver
    # los metadatos del sistema especificado
    try:
        sistema_bicing = pybikes.getDataFile(tag)
        if 'instances' in sistema_bicing:
                for instance in sistema_bicing['instances']:
                    if 'city' in instance['meta']:
                        if instance['meta']['city'] == 'Barcelona':
                            info = instance['meta']
    except FileNotFoundError as e:
        # Manejamos el caso en que no exista el sistema
        print(f"Sistema inexsistente: {e}")
        return None
    return info


def obtener_estaciones(tag: str) -> Optional[List]:
    """
    Obtiene la lista de estaciones del sistema especificado.

    Args:
        tag (str): Identificador del sistema (por ejemplo, 'bicing')

    Returns:
        Optional[List]: Lista de objetos estación o None si hay error
    """
    # Implementa aquí la lógica para obtener y devolver
    # la lista de estaciones del sistema especificado
    try:
        sistema_bicing = pybikes.get(tag)
        sistema_bicing.update()
        info = sistema_bicing.stations
    except Exception as e:
        # Manejamos el caso en que no se encuentre el sistema
        print(f"Sistema inexsistente: {e}")
        return None
    return info

def crear_dataframe_estaciones(estaciones: List) -> pd.DataFrame:
    """
    Convierte la lista de estaciones en un DataFrame de pandas.

    Args:
        estaciones (List): Lista de objetos estación

    Returns:
        pd.DataFrame: DataFrame con la información de las estaciones
    """
    # Implementa aquí la lógica para convertir la lista de estaciones
    # en un DataFrame de pandas con al menos las columnas:
    # nombre, latitud, longitud, bicicletas disponibles, espacios libres
    df_estaciones = pd.DataFrame()
    # Creamos una lista de diccionarios con la información de cada estación
    try:
        # Crear una lista con la información de cada estación
        estaciones_list =[]
        for estacion in estaciones:
            datos = pybikes.BikeShareStation.to_dict(estacion)
            estaciones_list.append(datos)
        df_estaciones = pd.DataFrame(estaciones_list)
    except KeyError as e:
        # Manejamos el caso en que no se encuentre la clave buscada
        print(f"Error al crear el dataframe, los datos no tienen el formato esperado: {e}")
        return None

    return df_estaciones


def visualizar_estaciones(df: pd.DataFrame) -> None:
    """
    Genera una visualización simple de la disponibilidad de bicicletas.

    Args:
        df (pd.DataFrame): DataFrame con la información de las estaciones
    """
    # Implementa aquí la lógica para crear un gráfico de barras que muestre
    # las 10 estaciones con más bicicletas disponibles
    
    # ordenamos el dataframe por la columna 'free' en orden descendente
    df_ordenado = df.sort_values(by='free', ascending=False)
    df_corto = df_ordenado.head(10)

    # creamos el gráfico de barras
    #df_corto.plot(kind='bar', x='name', y='free', legend=True)
    plt.barh(df_corto['name'], df_corto['free'])
    # personalizamos el gráfico
    plt.xlabel("Bicicletas disponibles")
    plt.ylabel("Estaciones")
    plt.title("Estaciones con más bicicletas disponibles")

    # mostramos el gráfico
    plt.show()

    return 


if __name__ == "__main__":
    # Listar sistemas disponibles
    print("\nSistemas de bicicletas disponibles:")
    sistemas = listar_sistemas_disponibles()
    print(f"Total: {len(sistemas)} sistemas")
    print(f"Algunos ejemplos: {sistemas[:5]}")

    # Buscar sistemas en Barcelona
    print("\nBuscando sistemas en Barcelona:")
    sistemas_barcelona = buscar_sistema_por_ciudad("Barcelona")
    print(f"Encontrados: {len(sistemas_barcelona)}")
    for sistema in sistemas_barcelona:
        print(f"- {sistema}")

    # Si se encuentra el sistema de Barcelona (Bicing), obtener información
    if "bicing" in sistemas:
        print("\nInformación del sistema Bicing de Barcelona:")
        info = obtener_info_sistema("bicing")
        for key, value in info.items():
            print(f"{key}: {value}")

        # Obtener estaciones
        print("\nObteniendo estaciones...")
        estaciones = obtener_estaciones("bicing")
        if estaciones:
            print(f"Obtenidas {len(estaciones)} estaciones")

            # Convertir a DataFrame
            print("\nConvirtiendo a DataFrame...")
            df = crear_dataframe_estaciones(estaciones)
            print(df.head())

            # Estadísticas básicas
            print("\nEstadísticas de bicicletas disponibles:")
            print(df['bikes'].describe())

            # Visualización
            print("\nVisualizando estaciones con más bicicletas disponibles...")
            visualizar_estaciones(df)
        else:
            print("No se pudieron obtener las estaciones.")
    else:
        print("El sistema 'bicing' no está disponible en pybikes.")
