import pymongo
from pymongo import MongoClient

cluster = MongoClient(
    "mongodb+srv://Tarea3:Programacion@cluster0.iomhm.mongodb.net/TareaUip?retryWrites=true&w=majority")

db = cluster["TareaUip"]
collection = db["Slang"]


def checkExistPalabra(palabra):
    check = collection.find_one(
        {"palabra": palabra})
    if(check == None):
        return False
    else:
        return True


def updatePalabra(oldPalabra, newPalabra, newDefinicion):
    collection.update_one({"palabra": oldPalabra}, {"$set": {
        "palabra": newPalabra,
        "definicion": newDefinicion
    }})


def deletePalabra(palabra):
    collection.delete_one({"palabra": palabra})


def showAllPalabras():
    palabras = collection.find()
    i = 0
    for row in palabras:
        i += 1
        print(
            f'{i}. Palabra: {row["palabra"]} Definicion: {row["definicion"]}')


while True:

    # menu
    print("\n Ingrese el numero que corresponde a la opcion que desea \n")

    menuOpt = int(input(" 1 Agregar nueva palabra \n 2 Editar palabra existente \n 3 Eliminar palabra existente \n 4 Ver listado de palabras \n 5 Buscar significado de palabra \n 6 Salir \n"))

    if(menuOpt == 1):
        # obtenemos la palabra y definicion
        inputPalabra = input("\n Ingrese la palabra a agregar \n")
        inputDefinicion = input(
            "\n por ultimo ingrese la definicion de la palabra \n")
        if(len(inputPalabra) and len(inputDefinicion)):

            if(checkExistPalabra(inputPalabra)):
                print("\n Esta palabra ya existe por favor de agregar otra")
            else:
                collection.insert_one({
                    "palabra": inputPalabra,
                    "definicion": inputDefinicion
                })
        else:
            print("\n Por favor llenar ambos campos de informacion")

    elif(menuOpt == 2):
        inputPalabra = input("\n Ingrese la palabra que desea modificar \n")

        palabraNueva = input("\n Ingrese el nuevo valor de esta palabra \n")

        definicionNueva = input(
            "\n Ingrese la nueva definicion de la palabra \n")

        if(len(palabraNueva) and len(definicionNueva) and len(inputPalabra)):
            if(checkExistPalabra(inputPalabra)):
                updatePalabra(inputPalabra, palabraNueva, definicionNueva)
            else:
                print("\n La palabra no existe!, vuelva a intentarlo")

        else:
            print("\n Por favor llenar los campos de informacion")

    elif(menuOpt == 3):
        inputPalabra = input("\n Ingrese la palabra que desea eliminar \n")

        if(len(inputPalabra)):
            if(checkExistPalabra(inputPalabra)):
                deletePalabra(inputPalabra)

            else:
                print("\n La palabra no existe!")

        else:
            print("\n Por favor llenar los campos de informacion")

    elif(menuOpt == 4):
        showAllPalabras()
    elif(menuOpt == 5):
        inputPalabra = input(
            "\n Ingrese la palabra que desea ver su significado \n")
        if(len(inputPalabra)):
            if(checkExistPalabra(inputPalabra)):
                getPalabra = collection.find_one(
                    {"palabra": inputPalabra})
                print(f'La definicion es: {getPalabra["definicion"]}')
            else:
                print("\n La palabra no existe!")

        else:
            print("\n Por favor llenar los campos de informacion")

    elif(menuOpt == 6):
        break

    else:
        print("\n Ingrese una opcion valida \n")
