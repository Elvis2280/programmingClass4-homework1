import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import session
# Elvis Miranda 4-803-2349

# lo usamos para conectarnos a la database con sqlalchemy
# debemos pasarle los datos como password, username port etc de nuestra configuracion en mariadb
engine = sqlalchemy.create_engine(
    "mariadb+mariadbconnector://root:2280@127.0.0.1:3306/slang")

Base = declarative_base()

# creamos la tabla y los valores de la misma en este caso tenemos id, palabra y definicion como columnas


class slang(Base):
    __tablename__ = 'diccionario'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    palabra = sqlalchemy.Column(sqlalchemy.Text, unique=True)
    definicion = sqlalchemy.Column(sqlalchemy.Text)

# verifica si la palabra existe en la base de datos


def checkExistPalabra(palabra):
    check = session.query(session.query(slang).filter(
        slang.palabra == palabra).exists()).scalar()
    return check

# añadimos una nueva palabra a la base de datos


def addPalabraDef(palabra, definicion):
    newPalabra = slang(palabra=palabra,
                       definicion=definicion)
    session.add(newPalabra)
    session.commit()
    print("\n palabra agregada correctamente!")

# actualiza una palabra existente


def updatePalabra(oldPalabra, newPalabra, newDefinicion):
    select = session.query(slang).filter(
        slang.palabra == oldPalabra).one()
    select.palabra = newPalabra
    select.definicion = newDefinicion
    session.commit()
    print("\n La palabra " + oldPalabra + " fue actualizada!")

# borra una palabra existente


def deletePalabra(palabra):
    session.query(session.query(slang).filter(
                  slang.palabra == palabra).delete())
    session.commit()
    print("\n Palabra eliminada!")

# mostrar los valores de la columna palabra


def showAllPalabras():
    palabras = session.query(slang).all()
    print("\n Lista de palabras \n")
    i = 0
    for row in palabras:
        i += 1
        print(f'{i}. {row.palabra}')


Base.metadata.create_all(engine)

# crea la sesion para comunicarse con mariadb a nuestra database
Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()


while True:

    # menu
    print("\n Ingrese el numero que corresponde a la opcion que desea \n")

    menuOpt = int(input(" 1 Agregar nueva palabra \n 2 Editar palabra existente \n 3 Eliminar palabra existente \n 4 Ver listado de palabras \n 5 Buscar significado de palabra \n 6 Salir \n"))

    if(menuOpt == 1):
        # obtenemos la palabra y definicion
        inputPalabra = input("\n Ingrese la palabra a agregar \n")
        inputDefinicion = input(
            "\n por ultimo ingrese la definicion de la palabra \n")
        if(len(inputPalabra) or len(inputPalabra)):
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

        if(len(palabraNueva) or len(definicionNueva) or len(inputPalabra)):
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
                palabra = session.query(slang).filter(
                    slang.palabra == inputPalabra).scalar()
                print(f'La definicion es: {palabra.definicion}')
            else:
                print("\n La palabra no existe!")

        else:
            print("\n Por favor llenar los campos de informacion")

    elif(menuOpt == 6):
        break

    else:
        print("\n Ingrese una opcion valida \n")
