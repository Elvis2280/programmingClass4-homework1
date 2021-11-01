from flask import Flask, render_template, request

import redis
keyPalabra = "palabra"
keyDefinicion = "definicion"

r = redis.Redis(host='127.0.0.1', port=6379)
r.set("id", -1)


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
    palabras = []

    for i in range(cantPalabras):
        palabras.append({"name": r.lindex(keyPalabra, i).decode(
            "utf-8"), "definicion": r.lindex(keyDefinicion, i).decode("utf-8")})
    return palabras


print(r.keys())

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/agregar-palabra', methods=['GET', 'POST'])
def agregarPalabra():
    if request.method == 'POST':
        palabra = request.form["word"]
        definicion = request.form["meaning"]
        if checkExistPalabra(palabra) == False:
            addPalabraDef(palabra, definicion)
            return render_template("agregar-palabra.html", message="!!Palabra añadida :)")
        else:
            return render_template("agregar-palabra.html", message="!!La palabra ya existe :(")

    return render_template("agregar-palabra.html")


@app.route('/actualizar-palabra', methods=['GET', 'POST'])
def editarPalbra():
    if request.method == 'POST':
        oldPalabra = request.form["oldWord"]
        newPalabra = request.form["word"]
        newDefinicion = request.form["meaning"]

        if checkExistPalabra(oldPalabra):
            updatePalabra(oldPalabra, newPalabra, newDefinicion)

            return render_template("actualizar-palabra.html", message=False)
        else:

            return render_template("actualizar-palabra.html", message=True)

    return render_template("actualizar-palabra.html")


@app.route('/eliminar-palabra', methods=['GET', 'POST'])
def eliminarPalabra():
    if request.method == 'POST':
        palabra = request.form["word"]

        if checkExistPalabra(palabra):
            deletePalabra(palabra)
            showAllPalabras()
            return render_template("eliminar-palabra.html", message=False)
        else:
            showAllPalabras()
            return render_template("eliminar-palabra.html", message=True)

    return render_template("eliminar-palabra.html")


@app.route('/listado-palabra', methods=['GET', 'POST'])
def listadoPalabra():
    allPalabras = showAllPalabras()

    return render_template("listado-palabra.html", palabras=allPalabras)


@app.route('/buscar-significado', methods=['GET', 'POST'])
def buscarSignificado():
    if request.method == 'POST':
        palabra = request.form["palabra"]
        if checkExistPalabra(palabra):
            cantPalabras = r.llen(keyPalabra)
            for i in range(cantPalabras):
                currentPalabra = r.lindex(keyPalabra, i).decode('utf-8')
                if(currentPalabra == palabra):
                    getPalabra = {"palabra": palabra, "definicion": r.lindex(
                        keyDefinicion, i).decode("utf-8")}

                    return render_template("buscar-significado.html", showPalabra=getPalabra)
        else:
            return render_template("buscar-significado.html", message=True)
    return render_template("buscar-significado.html")
