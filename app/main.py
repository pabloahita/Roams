import subprocess
import sys
try:
    from flask import Flask, render_template
except ModuleNotFoundError:
    print("Instalando el módulo flask....")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
    from flask import Flask, render_template
try:
    from pydantic import ValidationError, EmailStr
except ModuleNotFoundError:
    print("Instalando los módulos pydantic y pydantic[email]....")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pydantic"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pydantic[email]"])
    from pydantic import ValidationError, EmailStr
try:
    from flask_restx import Api, Resource, fields
except ModuleNotFoundError:
    print("Instalando el módulo flask_restx...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask_restx"])
    from flask_restx import Api, Resource, fields

from cliente import Cliente #Clase cliente
from dbhelper import DBHelper


app=Flask(__name__)

api = Api(
    app,
    version="1.0",
    title="Prueba técnica Roams Back-end ",
    description="Autor: Pablo Ahíta del Barrio",
)

ns = api.namespace("clientes", description="Operaciones relacionadas con clientes")

flask_model = {}
for field_name, field_type in Cliente.__annotations__.items():
    if field_type == str or field_type == EmailStr:
        flask_model[field_name] = fields.String(required=True)
    elif field_type == int:
        flask_model[field_name] = fields.Integer(required=True)
    elif field_type == float:
        flask_model[field_name] = fields.Float(required=True)
    elif field_type == bool:
        flask_model[field_name] = fields.Boolean(required=True)
    else:
        flask_model[field_name] = fields.Raw(required=True)
    
cliente_model=api.model(Cliente.__name__, flask_model)

@ns.route("/")
class MainPage(Resource):
    @app.route("/")
    def get(self):
        """Página principal"""
        return render_template("base.html")
    
@ns.route("/crearCliente")
class CrearCliente(Resource):
    @ns.expect(cliente_model, validate=True)
    def post(self):
        """Crear un nuevo cliente"""
        try:
            cliente = Cliente(**api.payload)
            DBHelper.crearCliente(cliente)
            return {"message": "Cliente añadido correctamente"}, 200
        except ValidationError:
            return {"message": "Problema al añadir cliente"}, 500


@ns.route("/obtenerCliente/<string:DNI>")
@ns.param("DNI", "El DNI del cliente a obtener")
class ObtenerCliente(Resource):
    def get(self, DNI):
        """Obtener los datos de un cliente por su DNI"""
        try:
            cliente = DBHelper.obtenerCliente(DNI)
            if cliente is None:
                return {"message": f"No se encontró ningún cliente con DNI {DNI}"}, 40
            return {
                "nombre": cliente.nombre,
                "email": cliente.email,
                "capital_solicitado": cliente.capital_solicitado,
            }, 200
        except ValidationError:
            return {"message": "Problema al obtener cliente"}, 500


@ns.route("/modificarCliente/<string:DNI>")
@ns.param("DNI", "El DNI del cliente a modificar")
class ModificarCliente(Resource):
    @ns.expect(cliente_model, validate=True)
    def put(self, DNI):
        """Modificar los datos de un cliente"""
        try:
            cliente = Cliente(**api.payload)
            DBHelper.modificarCliente(cliente, DNI)
            return {"message": "Cliente modificado correctamente"}, 200
        except ValidationError:
            return {"message": "Problema al modificar cliente"}, 500


@ns.route("/eliminarCliente/<string:DNI>")
@ns.param("DNI", "El DNI del cliente a eliminar")
class EliminarCliente(Resource):
    def delete(self, DNI):
        """Eliminar un cliente por su DNI"""
        try:
            cliente=DBHelper.obtenerCliente(DNI)
            if cliente is None:
                return {"message": f"No se encontró ningún cliente con DNI {DNI}, no se puede eliminar"}, 404.
            DBHelper.eliminarCliente(DNI)
            return {"message": "Cliente eliminado satisfactoriamente"}, 200
        except:
            return {"message": "Problema al eliminar cliente"}, 500


# Iniciar la aplicación
if __name__ == "__main__":
    DBHelper.crearTabla()  # Crea la tabla si es necesario
    app.run(debug=True)