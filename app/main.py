import subprocess
import sys
try:
    from flask import Flask, render_template, request, jsonify
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
    from flask import Flask, render_template, request, jsonify
try:
    from pydantic import ValidationError
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pydantic"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pydantic[email]"])
    from pydantic import ValidationError


from cliente import Cliente
from dbhelper import DBHelper


app=Flask(__name__)

@app.route("/")
def main():
    return render_template("base.html")


@app.post("/crearCliente")
def crearCliente():
    try:
        cliente=Cliente(**request.get_json())
        DBHelper.crearCliente(cliente)
        return jsonify({"message": "Cliente añadido correctamente"}),200
    except ValidationError:
        return jsonify({"message": "Problema al añadir cliente"}),500
        
@app.get("/obtenerCliente/<str:DNI>")
def obtenerDatosCliente(DNI):
    try:
        cliente=DBHelper.obtenerCliente(DNI)
        return jsonify({
            "nombre":cliente.nombre,
            "email":cliente.email,
            "capital_solicitado":cliente.capital_solicitado
        }),200
    except ValidationError:
        return jsonify({"message": "Problema al obtener cliente"}),500


if __name__=="__main__":
    DBHelper.crearTabla()
    app.run()


