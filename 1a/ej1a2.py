"""
Enunciado:
Continuando con la biblioteca requests de Python.
En este ejercicio, aprenderás a trabajar con respuestas en formato JSON.

En este ejercicio, aprenderás a:
1. Realizar una petición GET a una API pública
2. Interpretar una respuesta en formato JSON
3. Extraer información específica de un objeto JSON

Tu tarea es completar la función indicada para realizar una consulta a la API
de ipify.org usando el formato JSON, que es más estructurado que el texto plano.
"""

import requests
import json

def get_user_ip_json():
    """
    Realiza una petición GET a api.ipify.org para obtener la dirección IP pública
    en formato JSON.

    Returns:
        str: La dirección IP si la petición es exitosa
        None: Si ocurre un error en la petición
    """
    # Completa esta función para:
    url = 'https://api.ipify.org?format=json'
    # 1. Realizar una petición GET a la URL https://api.ipify.org?format=json
    try:
        resp = requests.get(url)
    # 2. Verificar si la petición fue exitosa (código 200)
        resp.raise_for_status()
    # 3. Convertir la respuesta a formato JSON
        if 200 <= resp.status_code < 300:
            ip_decode = resp.content.decode('utf-8')
            ip_data = json.loads(ip_decode)
    # 4. Extraer y devolver la IP del campo "ip" del objeto JSON
            return ip_data['ip']
    # 5. Devolver None si hay algún error
        # Detectar error de cliente
        if 400 <= resp.status_code < 500:
            return None
    except Exception:
        print(f"Connection error")

def get_response_info():
    """
    Obtiene información adicional sobre la respuesta HTTP al consultar la API.
    
    Returns:
        dict: Diccionario con información de la respuesta (tipo de contenido,
              tiempo de respuesta, tamaño de la respuesta)
        None: Si ocurre un error en la petición
    """
    # Completa esta función para:
    url = 'https://api.ipify.org?format=json'
    # 1. Realizar una petición GET a la URL https://api.ipify.org?format=json
    try:
        resp = requests.get(url)
    # 2. Verificar si la petición fue exitosa (código 200)
        resp.raise_for_status()
    # 3. Crear y devolver un diccionario con:
    #    - 'content_type': El tipo de contenido de la respuesta
    #    - 'elapsed_time': El tiempo que tardó la petición (en milisegundos)
    #    - 'response_size': El tamaño de la respuesta en bytes
        if 200 <= resp.status_code < 300:
            elap_time = int(resp.elapsed.total_seconds()*1000)
            info ={'content_type': resp.headers['Content-Type'],
                   'elapsed_time': elap_time,
                   'response_size': len(resp.content)
                  }
            return info
    # 4. Devolver None si hay algún error
    # Detectar error de cliente
        if 400 <= resp.status_code < 500:
            return None
    except Exception:
        print(f"Connection error")

if __name__ == "__main__":
    # Ejemplo de uso de las funciones
    ip = get_user_ip_json()
    if ip:
        print(f"Tu dirección IP pública es: {ip}")

        # Mostrar información adicional de la respuesta
        info = get_response_info()
        if info:
            print("\nInformación de la respuesta:")
            print(f"Tipo de contenido: {info['content_type']}")
            print(f"Tiempo de respuesta: {info['elapsed_time']} ms")
            print(f"Tamaño de la respuesta: {info['response_size']} bytes")
    else:
        print("No se pudo obtener la dirección IP")
