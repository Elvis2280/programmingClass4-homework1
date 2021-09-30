# Elvis Miranda 4-803-2349
import sqlite3

con = sqlite3.connect("slang.db")
cur = con.cursor()

# Create table called slang if not exists
cur.execute('''CREATE TABLE IF NOT EXISTS slang
               (palabra text UNIQUE, definicion text)''')

# comprueba si la palabra existe


def checkWordExist(palabra):
    c = cur.execute("""SELECT EXISTS (SELECT 1 
                                     FROM slang 
                                     WHERE palabra=?
                                     LIMIT 1)""", (palabra, )).fetchone()[0]
    return c


while True:
    # menu
    print("\n Ingrese el numero que corresponde a la opcion que desea \n")

    menuOpt = int(input(" 1 Agregar nueva palabra \n 2 Editar palabra existente \n 3 Eliminar palabra existente \n 4 Ver listado de palabras \n 5 Buscar significado de palabra \n 6 Salir \n"))

    if(menuOpt == 1):
        # obtenemos la palabra y definicion
        palabra = input("\n Ingrese la palabra a agregar \n")
        definicion = input(
            "\n por ultimo ingrese la definicion de la palabra \n")

        c = checkWordExist(palabra)
        if c == False:
            # guardamos los datos en una variable params y lo usamos ejecutando el comando sqlite para insertar valores
            params = (palabra, definicion)
            cur.execute("INSERT INTO slang VALUES (?, ?)", params)

            # guardamos los cambios
            con.commit()

        else:
            print("\n La palabra ya existe. \n")

    elif(menuOpt == 2):
        palabra = input("\n Ingrese la palabra que desea modificar \n")

        palabraNueva = input("\n Ingrese el nuevo valor de esta palabra \n")

        definicion = input("\n Ingrese la nueva definicion de la palabra \n")

        params = (palabraNueva, definicion, palabra)
        c = checkWordExist(palabra)

        if c:
            # si existe remplazamos esa palabra por los nuevos valores
            cur.execute("""
            UPDATE slang
            SET palabra = ?,
                definicion= ?
            WHERE palabra = ?;
            """, params)
            con.commit()

        else:
            print("No pudimos encontrar la palabra vuelva a intentarlo")

    elif(menuOpt == 3):
        palabra = input("\n Ingrese la palabra que desea eliminar \n")
        c = checkWordExist(palabra)
        if c:
            cur.execute("""
                    DELETE FROM slang
                    WHERE palabra = ?
                    """, (palabra, ))
            con.commit()

        else:
            print("No pudimos encontrar la palabra vuelva a intentarlo")

    elif(menuOpt == 4):
        data = cur.execute("""SELECT * FROM slang""")
        i = 1
        for palabra in data:
            print(f"{i}. {palabra[0]}")
            i += 1
    elif(menuOpt == 5):

        palabra = input(
            "\n Ingrese la palabra que desea ver su significado \n")
        c = checkWordExist(palabra)
        if c:
            data = cur.execute(
                """SELECT * FROM slang WHERE palabra = ?""", (palabra, ))
            for palabra in data:
                print(f"\nEl significado es: \n {palabra[1]}")

        else:
            print("No pudimos encontrar la palabra vuelva a intentarlo")

    elif(menuOpt == 6):
        break

    else:
        print("\n Ingrese una opcion valida \n")
con.close()
