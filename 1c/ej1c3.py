"""
Enunciado:
Este ejercicio introduce el uso de clases y programación orientada a objetos (POO)
para modelar y procesar datos de una API pública.

Utilizaremos la API de GBFS (General Bikeshare Feed Specification) del sistema de
bicicletas compartidas de Barcelona para consultar el estado en tiempo real de las estaciones,
modelando los datos obtenidos como objetos Python.

Tareas:
1. Completar la implementación de las clases que representan los diferentes elementos
   del sistema (estación, estado, tipos de bicicletas disponibles)
2. Implementar un cliente que consulte la API y transforme los datos JSON en objetos Python
3. Añadir métodos para analizar la disponibilidad de bicicletas en las estaciones

Esta práctica refuerza conceptos de POO en Python como:
- Uso de enumeraciones (Enum)
- Uso de dataclasses para modelos de datos
- Diseño orientado a objetos
- Transformación de datos JSON a objetos Python
- Manejo de errores y excepciones
"""

import requests
import enum
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from datetime import datetime


class StationStatus(enum.Enum):
    """
    Enumeración que representa los posibles estados de una estación.
    """
    # Define aquí los estados posibles (IN_SERVICE, MAINTENANCE, etc.)
    # según la documentación de la API
    IN_SERVICE = 1
    MAINTENANCE = 2


@dataclass
class VehicleType():
    """
    Clase que representa un tipo de vehículo y su cantidad disponible.
    """
    # Añade aquí los atributos necesarios: tipo de vehículo (vehicle_type_id) y cantidad (count)
    def __init__(self, vehicle_type_id, count):
        # Inicialización de los atributos
        self.vehicle_type_id = vehicle_type_id
        self.count = count


class StationStatusInfo:
    """
    Clase que representa el estado de una estación de bicicletas compartidas.
    
    Atributos:
        station_id: Identificador único de la estación
        status: Estado actual de la estación (enum StationStatus)
        num_bikes_available: Número total de bicicletas disponibles
        num_bikes_disabled: Número de bicicletas fuera de servicio
        num_docks_available: Número de anclajes disponibles
        is_renting: Indica si la estación permite alquilar bicicletas
        is_returning: Indica si la estación permite devolver bicicletas
        last_reported: Timestamp del último reporte de estado
        vehicle_types_available: Lista de tipos de vehículos disponibles
    """

    def __init__(self, station_data):
        """
        Inicializa una instancia de StationStatusInfo a partir de los datos
        de la estación proporcionados por la API.

        Args:
            station_data: Diccionario con los datos de la estación obtenidos de la API
        """
        # Implementa aquí la inicialización de todos los atributos
        # a partir del diccionario station_data

        self.station_id = station_data['station_id']
        self.status = station_data['status']
        if self.status == 'IN_SERVICE':
            self.status = StationStatus.IN_SERVICE
        else:
            self.status = StationStatus.MAINTENANCE
        self.num_bikes_available = station_data['num_bikes_available']
        self.num_bikes_disabled = station_data['num_bikes_disabled']
        self.num_docks_available = station_data['num_docks_available']
        self.is_renting = station_data['is_renting']
        self.is_returning = station_data['is_returning']
        self.last_reported = station_data['last_reported']
        self.vehicle_types_available = station_data['vehicle_types_available']

    @property
    def is_operational(self) -> bool:
        """
        Indica si la estación está completamente operativa
        (en servicio y permite alquilar y devolver bicicletas)

        Returns:
            bool: True si la estación está operativa, False en caso contrario
        """
        # Implementa aquí la lógica para determinar si la estación está operativa
        if self.status == StationStatus.IN_SERVICE and self.is_renting == True and self.is_returning == True:
            return True
        else:
            return False

    def get_available_bikes_by_type(self) -> Dict[str, int]:
        """
        Devuelve un diccionario con la cantidad de bicicletas disponibles por tipo.

        Returns:
            Dict[str, int]: Diccionario donde la clave es el tipo de bicicleta
                            y el valor es la cantidad disponible
        """
        # Implementa aquí la lógica para devolver un diccionario
        # con la cantidad de bicicletas disponibles por tipo
        #available_bikes_by_type_list = []
        if self.vehicle_types_available:
            diccionario_final = {}
            for diccionario in self.vehicle_types_available:
                clave_final = diccionario['vehicle_type_id']
                valor_final = diccionario['count']
                diccionario_final[clave_final] = valor_final
        return diccionario_final

    def __str__(self) -> str:
        """
        Devuelve una representación en string de la estación con su estado actual.

        Returns:
            str: Representación en texto del estado de la estación
        """
        # Implementa aquí la lógica para devolver una representación en texto
        # de la estación y su estado actual
        return (f"Estación {self.station_id}: "
                f"{self.num_bikes_available} bicicletas disponibles, "
                f"{self.num_bikes_disabled} fuera de servicio. "
                f"Estado: {self.status}")


class BarcelonaBikingClient:
    """
    Cliente para consultar el estado de las estaciones de bicicletas de Barcelona.
    """

    def __init__(self):
        """
        Inicializa el cliente con la URL base de la API.
        """
        self.base_url = "https://barcelona.publicbikesystem.net/customer/gbfs/v2/en"
        self.station_status_url = f"{self.base_url}/station_status"

    def get_stations_status(self) -> Tuple[List[StationStatusInfo], Optional[datetime]]:
        """
        Obtiene el estado actual de todas las estaciones de bicicletas.

        Returns:
            Tuple[List[StationStatusInfo], Optional[datetime]]:
                - Lista de objetos StationStatusInfo, uno por cada estación
                - Timestamp de la última actualización de los datos, o None si hay error
        """
        # Implementa aquí la lógica para:
        # 1. Realizar una petición GET a la URL de station_status
        # 2. Verificar que la respuesta sea correcta (código 200)
        # 3. Crear objetos StationStatusInfo para cada estación en la respuesta
        # 4. Extraer el timestamp de last_updated de la respuesta
        # 5. Manejar posibles errores (conexión, formato, etc.)
        try:
            # Realizamos la petición GET a la url
            resp = requests.get(self.station_status_url)
        # Verificamos que la respuesta es correcta (código 200)
            if resp.status_code == 200:
                # Devolvemos los datos en formato JSON
                data_json = resp.json()
                stations_list = data_json.get('data', {}).get('stations', {})
                last_updated = data_json.get('last_updated')
                # Verificamos que stations_data no es None y tiene la estructura esperada
                if not stations_list:
                    return None
                stations_list_tupla = []
                for station in stations_list:
                    station = StationStatusInfo(station)
                    stations_list_tupla.append(station)
                stations_tupla = (stations_list_tupla, last_updated)
                return stations_tupla
            else:
                # Si status_code no es 200, imprimimos un mensaje de error
                print(f"Error: La petición no fue exitosa. Código de estado: {resp.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            # Capturamos cualquier error que pueda ocurrir durante la petición
            print(f"Error al realizar la petición: {e}")
            stations_tupla = ([], None)
            return stations_tupla

    def find_station_by_id(self, station_id: str) -> Optional[StationStatusInfo]:
        """
        Busca una estación específica por su ID.

        Args:
            station_id: ID de la estación a buscar

        Returns:
            Optional[StationStatusInfo]: Objeto con la información de la estación,
                                         o None si no se encuentra
        """
        # Implementa aquí la lógica para buscar y devolver una estación por su ID

        for station in BarcelonaBikingClient.get_stations_status(self):
            i = 0
            if station[i].station_id == station_id:
                return station[i]
            else:
                return None

    def get_operational_stations(self) -> List[StationStatusInfo]:
        """
        Obtiene la lista de estaciones que están completamente operativas.

        Returns:
            List[StationStatusInfo]: Lista de estaciones operativas
        """
        # Implementa aquí la lógica para filtrar y devolver solo las estaciones operativas
        operational_station_list = []
        results, updated = BarcelonaBikingClient.get_stations_status(self)
        for station in results:
            if station.status == StationStatus.IN_SERVICE:
                operational_station_list.append(station)
        return operational_station_list

    def get_stations_with_available_bikes(self, min_bikes: int = 1) -> List[StationStatusInfo]:
        """
        Obtiene la lista de estaciones que tienen al menos min_bikes disponibles.
        
        Args:
            min_bikes: Número mínimo de bicicletas requeridas (por defecto 1)

        Returns:
            List[StationStatusInfo]: Lista de estaciones con bicicletas disponibles
        """
        # Implementa aquí la lógica para filtrar y devolver las estaciones
        # con al menos min_bikes disponibles
        available_bikes_station_list = []
        for station in BarcelonaBikingClient.get_stations_status(self):
            i = 0
            if station[i].num_bikes_available >= min_bikes:
                available_bikes_station_list.append(station[i])
                i += 1
            return available_bikes_station_list


if __name__ == "__main__":
    # Ejemplo de uso del cliente
    client = BarcelonaBikingClient()

    # Obtener el estado de todas las estaciones
    stations, last_updated = client.get_stations_status()

    if stations:
        # Mostrar información sobre el conjunto de datos
        print(f"Datos actualizados: {datetime.fromtimestamp(last_updated) if last_updated else 'Desconocido'}")
        print(f"Total de estaciones: {len(stations)}")

        # Mostrar estaciones operativas
        operational = client.get_operational_stations()
        print(f"\nEstaciones operativas: {len(operational)} de {len(stations)}")

        # Mostrar estaciones con bicicletas disponibles
        with_bikes = client.get_stations_with_available_bikes(min_bikes=5)
        print(f"\nEstaciones con al menos 5 bicicletas: {len(with_bikes)}")

        if stations:
            print("\nDetalle de algunas estaciones:")
            for station in stations[:3]:  # Mostrar solo las primeras 3
                print(f"\n{station}")
                bikes_by_type = station.get_available_bikes_by_type()
                for bike_type, count in bikes_by_type.items():
                    print(f"  - {bike_type}: {count} disponibles")
    else:
        print("No se pudieron obtener los datos de las estaciones.")
