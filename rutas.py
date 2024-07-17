import requests

GRAPHOPPER_API_KEY = 'e70e0504-c80d-4d3a-989e-9e1338a55b9a'

# Función para obtener coordenadas de una ciudad
def get_coordinates(ciudad):
    url = f"https://graphhopper.com/api/1/geocode?q={ciudad}&locale=es&key={GRAPHOPPER_API_KEY}"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"No se pudieron obtener las coordenadas para {ciudad}. Verifique el nombre de la ciudad y el token.")
    
    data = response.json()
    if 'hits' not in data or not data['hits']:
        raise Exception(f"No se encontraron coordenadas para {ciudad}.")
    
    return data['hits'][0]['point']['lat'], data['hits'][0]['point']['lng']

# Función para obtener la ruta entre dos coordenadas
def get_route(from_coords, to_coords, vehiculo):
    url = f"https://graphhopper.com/api/1/route?point={from_coords[0]},{from_coords[1]}&point={to_coords[0]},{to_coords[1]}&vehicle={vehiculo}&locale=es&key={GRAPHOPPER_API_KEY}&instructions=true"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception("Error al obtener la ruta. Verifique los nombres de las ciudades y su token.")
    
    data = response.json()
    if 'paths' not in data or not data['paths']:
        raise Exception("No se encontró una ruta entre las ciudades especificadas.")
    
    return data

# Función para calcular el combustible necesario (asumimos un consumo medio de 8 litros cada 100 km)
def calculate_fuel(distance_km):
    consumo_medio_por_100_km = 8
    return (distance_km / 100) * consumo_medio_por_100_km

# Menú principal
def main():
    while True:
        print("Menu de opciones:")
        print("1. Medir la distancia entre dos ciudades")
        print("s. Salir del programa")
        choice = input("Seleccione una opción: ")

        if choice == '1':
            ciudad_origen = input("Ciudad de Origen (en Chile): ")
            ciudad_destino = input("Ciudad de Destino (en Argentina): ")
            vehiculo = input("Ingrese el tipo de medio de transporte (car, bike, foot): ").lower()

            if vehiculo not in ['car', 'bike', 'foot']:
                print("Tipo de medio de transporte no válido. Por favor, ingrese 'car', 'bike' o 'foot'.")
                continue

            try:
                from_coords = get_coordinates(ciudad_origen)
                to_coords = get_coordinates(ciudad_destino)
                route_data = get_route(from_coords, to_coords, vehiculo)

                distance_km = route_data['paths'][0]['distance'] / 1000
                distance_mi = distance_km * 0.621371
                time_seconds = route_data['paths'][0]['time'] / 1000
                fuel_needed = calculate_fuel(distance_km)

                hours, remainder = divmod(time_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)

                print(f"\nDistancia: {distance_km:.2f} km ({distance_mi:.2f} mi)")
                print(f"Duración del viaje: {int(hours)} horas, {int(minutes)} minutos, {int(seconds)} segundos")
                print(f"Combustible requerido: {fuel_needed:.2f} litros")

                print("\nNarrativa del viaje:")
                for instruction in route_data['paths'][0]['instructions']:
                    print(instruction['text'])

            except Exception as e:
                print(f"Error: {e}")

        elif choice == 's':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()