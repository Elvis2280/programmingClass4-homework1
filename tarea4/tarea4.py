import redis
keyPalabra = "palabra"
keyDefinicion = "definicion"

r = redis.Redis(host='127.0.0.1', port=6379)
r.set("id", -1)
print(r.keys())


def checkExistPalabra(palabra):
    cantPalabras = r.llen(keyPalabra)
    palabraExist = False
    for i in range(cantPalabras):
        currentPalabra = r.lindex(keyPalabra, i).decode('utf-8')
        if(currentPalabra == palabra):
            palabraExist = True
            break
    return palabraExist


def addPalabraDef(palabra, definicion):
    r.incr("id")
    r.rpush(keyPalabra, palabra)
    r.rpush(keyDefinicion, definicion)
    print("\n palabra agregada correctamente!")


def updatePalabra(oldPalabra, newPalabra, newDefinicion):
    cantPalabras = r.llen(keyPalabra)
    for i in range(cantPalabras):
        currentPalabra = r.lindex(keyPalabra, i).decode('utf-8')
        if(currentPalabra == oldPalabra):
            r.lset(keyPalabra, i, newPalabra)
            r.lset(keyDefinicion, i, newDefinicion)
            break

    print("\n La palabra " + oldPalabra + " fue actualizada!")


def deletePalabra(palabra):
    cantPalabras = r.llen(keyPalabra)
    for i in range(cantPalabras):
        currentPalabra = r.lindex(keyPalabra, i).decode('utf-8')
        currentDefinicion = r.lindex(keyDefinicion, i).decode('utf-8')
        if(currentPalabra == palabra):
            r.lrem(keyPalabra, i, currentPalabra)
            r.lrem(keyDefinicion, i, currentDefinicion)
            break
    print("\n Palabra eliminada!")


def showAllPalabras():
    cantPalabras = r.llen(keyPalabra)
    for i in range(cantPalabras):
        print(f'{i + 1}. Palabra: {r.lindex(keyPalabra, i).decode("utf-8")} \n   Definicion: {r.lindex(keyDefinicion, i).decode("utf-8")}')


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
                addPalabraDef(inputPalabra, inputDefinicion)
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
                cantPalabras = r.llen(keyPalabra)
                for i in range(cantPalabras):
                    currentPalabra = r.lindex(keyPalabra, i).decode('utf-8')
                    if(currentPalabra == inputPalabra):
                        print(
                            f'La definicion es: {r.lindex(keyDefinicion, i).decode("utf-8")}')
                        break

            else:
                print("\n La palabra no existe!")

        else:
            print("\n Por favor llenar los campos de informacion")

    elif(menuOpt == 6):
        break

    else:
        print("\n Ingrese una opcion valida \n")
