import requests

numbers = [2, 4, 8.8]

print(max(numbers))


def getAllData(link):
    requestData = requests.get(link).json()
    allData = requestData["results"]

    while requestData["next"]:
        requestData = requests.get(requestData["next"]).json()
        allData += requestData["results"]
    return allData


while True:
    menupot = int(input("Menu \n 1. ¿En cuántas películas aparecen planetas cuyo clima sea árido? \n 2. Cuántos Wookies aparecen en la sexta película? \n 3. ¿Cuál es el nombre de la aeronave más grande en toda la saga? \n 4. Salir \n"))

    if menupot == 1:
        planets = requests.get("https://swapi.dev/api/planets/").json()
        totalPlanets = 0
        for planet in planets["results"]:
            if(planet["climate"] == "arid"):
                totalPlanets += len(planet["films"])

        print(f'El total de peliculas con clima arido es de: {totalPlanets}')

    elif menupot == 2:
        allPeople = getAllData("https://swapi.dev/api/people/")
        num = 0
        for people in allPeople:
            if len(people["species"]) > 0:
                if people["species"][0] == "https://swapi.dev/api/species/3/":
                    for movies in people["films"]:
                        if movies == "https://swapi.dev/api/films/6/":
                            num += 1

        print(f'El total de Wookies en la pelicula 6 es: {num}')

    elif menupot == 3:
        allShips = getAllData("https://swapi.dev/api/vehicles/")
        allSizes = []
        for vehicle in allShips:
            if vehicle["length"] != "unknown":
                allSizes.append(float(vehicle["length"]))

        bigShip = (max(allSizes))

        for vehicle in allShips:
            if vehicle["length"] != "unknown":
                if float(vehicle["length"]) == bigShip:
                    print(
                        f'\n La aeronave mas grande de toda la saga es: {vehicle["name"]} \n')

    elif menupot == 4:
        break
    else:
        print("elija una opcion valida")
