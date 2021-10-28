import pymongo
from pymongo import MongoClient

cluster = MongoClient(
    "mongodb+srv://Tarea3:Programacion@cluster0.iomhm.mongodb.net/ParcialOne?retryWrites=true&w=majority")

db = cluster["ParcialOne"]
collection = db["Parcial"]


def checkProductoExist(codigo):
    check = collection.find_one(
        {"codigo": codigo})
    if(check == None):
        return False
    else:
        return True


def updateProducto(codigo, newNombre, newDescripcion, newCantidad):
    collection.update_one({"codigo": codigo}, {"$set": {
        "codigo": codigo,
        "nombre": newNombre,
        "descripcion": newDescripcion,
        "cantidad": newCantidad
    }})
    print("\n Los datos han sido actualizados")


def deleteProducto(codigo):
    collection.delete_one({"codigo": codigo})


def showAllProductos():
    productos = collection.find()
    i = 0
    for row in productos:
        i += 1
        print(
            f'{i}. codigo: {row["codigo"]} \nnombre: {row["nombre"]} \ndescripcion: {row["descripcion"]} \ncantidad: {row["cantidad"]}\n')


print("\nBienvenido al Sistema de Inventarios Elvis S.A \n")
while True:

    # menu
    print("\n Ingrese el numero que corresponde a la opcion que desea \n")

    menuOpt = int(input(" 1 Agregar nuevo producto \n 2 Editar un producto existente \n 3 Eliminar un producto existente \n 4 Ver inventario \n 5 Buscar un producto por codigo \n 6 Salir \n"))

    if(menuOpt == 1):
        # obtenemos la palabra y definicion
        inputCodigo = input("\n Ingrese el codigo del producto\n")
        inputNombre = input("\n Ingrese el nombre del producto a agregar\n")
        inputDescripcion = input("\n Ingrese la descripcion del producto\n")
        inputCantidad = input(
            "\n ingrese la cantidad del producto en unidades \n")
        if(len(inputNombre) and len(inputCantidad) and len(inputCodigo) and len(inputCantidad)):

            if(checkProductoExist(inputCodigo)):
                print("\n Este producto ya esta registrado!!!")
            else:
                collection.insert_one({
                    "codigo": inputCodigo,
                    "nombre": inputNombre,
                    "descripcion": inputDescripcion,
                    "cantidad": inputCantidad,

                })
        else:
            print("\n Por favor llenar todos los campos de informacion")

    elif(menuOpt == 2):
        inputCodigo = input("\n Ingrese el codigo del producto a modificar \n")
        inputNombre = input("\n Ingrese el nuevo nombre de este producto \n")
        inputDescripcion = input(
            "\n Ingrese la nueva descripcion de el producto \n")
        inputCantidad = input(
            "\n Ingrese la nueva cantidad de el producto \n")

        if(len(inputCodigo) and len(inputNombre) and len(inputDescripcion) and len(inputCantidad)):
            if(checkProductoExist(inputCodigo)):
                updateProducto(inputCodigo, inputNombre,
                               inputDescripcion, inputCantidad)
            else:
                print("\n El producto no existe!, vuelva a intentarlo")

        else:
            print("\n Por favor llenar los campos de informacion")

    elif(menuOpt == 3):
        inputCodigo = input(
            "\n Ingrese el codigo del producto que desea eliminar \n")

        if(len(inputCodigo)):
            if(checkProductoExist(inputCodigo)):
                deleteProducto(inputCodigo)

            else:
                print("\n El producto no existe!")

        else:
            print("\n Por favor llenar los campos de informacion")

    elif(menuOpt == 4):
        showAllProductos()
    elif(menuOpt == 5):
        inputCodigo = input(
            "\n Ingrese el codigo del producto que desea ver \n")
        if(len(inputCodigo)):
            if(checkProductoExist(inputCodigo)):
                getProducto = collection.find_one(
                    {"codigo": inputCodigo})
                print(
                    f'codigo: {getProducto["codigo"]} \nnombre: {getProducto["nombre"]} \ndescripcion: {getProducto["descripcion"]} \ncantidad: {getProducto["cantidad"]}\n')
            else:
                print("\n El producto no existe!")

        else:
            print("\n Por favor llenar los campos de informacion")

    elif(menuOpt == 6):
        break

    else:
        print("\n Ingrese una opcion valida \n")
