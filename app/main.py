#Importación de módulos
import subprocess
import sys
try:
    from flask import Flask, request
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
    from flask import Flask, request
try:
    from pydantic import ValidationError
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pydantic"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pydantic[email]"])
    from pydantic import ValidationError
try:
    from flask_restx import Api, Resource, fields
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "flask_restx"])
    from flask_restx import Api, Resource, fields

from cliente import Cliente #Clase cliente
from dbhelper import DBHelper #Clase de conexión a la base de datos

app=Flask(__name__) #App

api = Api(
    app,
    version="1.0",
    title="Prueba técnica Roams Back-end",
    description="Autor: Pablo Ahíta del Barrio",
) #Creación de la api de Swagger

ns = api.namespace("", description="Presione aquí para acceder a las operaciones disponibles de esta prueba técnica") #Creación del namespace


cliente_model=api.model(Cliente.__name__, {
    'nombre': fields.String(required=True, description='El nombre del cliente'),
    'DNI': fields.String(required=True, description='El DNI del cliente'),
    'email': fields.String(required=True, description='Correo electrónico del cliente'),
    'capital_solicitado': fields.Float(required=True, description='Capital solicitado por el cliente')
})#Modelo de cliente

#Clase de creación de cliente
@ns.route("/crearCliente")
class CrearCliente(Resource):
    @ns.expect(cliente_model, validate=True)
    @ns.response(200,"Cliente añadido a la base de datos correctamente")
    @ns.response(400,"Error de validación en caso de que haya algún atributo incorrecto en el modelo de cliente")   
    @ns.response(409,"El cliente con un determinado DNI ya existe")  
    @ns.response(500,"Error del servidor")   
    def post(self):
        """Crea un nuevo cliente a partir de un JSON, comprobando previamente la validez de los campos mediante los field_validator del BaseModel llamado Cliente y asegurándose de que ese cliente no exista en la base de datos a través de su DNI"""
        try:
            cliente = Cliente(**api.payload) #Crea un objeto Cliente a partir del payload en formato JSON
            cliente_existente=DBHelper.obtenerCliente(cliente.DNI) #Llama a la base de datos para comprobar si el cliente no existe
            if cliente_existente is not None: #Si el cliente no existe, lanza conflicto
                return {"message":"El cliente que quiere agregar a la base de datos ya existe"},409 #Error de conflicto
            DBHelper.crearCliente(cliente) #Inserta cliente en la base de datos
            return {"message": "Cliente añadido correctamente"}, 200 #Resultado satisfactorio
        except ValidationError as e:
            errores=e.errors() #Lista de errores
            mensajes={} #Creación del json
            for error in errores: #Obtenemos la ubicación y mensaje de cada uno
                mensajes[error["loc"][0]]=error["msg"]
            return mensajes, 400 #Error de validación
        except:
            return {"message": "Problema al añadir cliente"}, 500 #Error de servidor

#Clase de obtención de cliente
@ns.route("/obtenerCliente")
@ns.param("DNI", "El DNI del cliente a obtener")
class ObtenerCliente(Resource):
    @ns.response(200,"Cliente obtenido de la base de datos correctamente")
    @ns.response(400,"Error de validación en caso de DNI incorrecto")
    @ns.response(404,"Cliente no encontrado con un determinado DNI")
    @ns.response(500,"Error del servidor")   
    def get(self):
        """Obtiene los datos de un cliente por su DNI, comprobando la validez del DNI antes de obtener dicho cliente"""
        try:
            DNI = request.args.get("DNI") #Obtiene el DNI por parámetro
            if not DNI:#Si no se ha introducido DNI
                return {"message": "No se ha introducido un DNI"}, 400 #Error de validación
            if not Cliente.dni_es_verdadero(DNI): #Si el DNI es inválido
                return {"message":"El DNI introducido no es válido"}, 400 #Error de validación de DNI
            cliente = DBHelper.obtenerCliente(DNI) #Obtiene el cliente de la base de datos, si lo encuentra
            if cliente is None: #Si no lo encuentra
                return {"message": f"No se encontró ningún cliente con DNI {DNI}"}, 404 #Error, no encontrado
            return {
                "nombre": cliente.nombre,
                "DNI":DNI,
                "email": cliente.email,
                "capital_solicitado": cliente.capital_solicitado
            }, 200 #Resultado satisfactorio
        except:
            return {"message": "Problema al obtener cliente"}, 500 #Error de servidor

#Clase de modificación de cliente
@ns.route("/modificarCliente")
class ModificarCliente(Resource):
    @ns.expect(cliente_model, validate=True)
    @ns.response(200,"Cliente modificado de la base de datos correctamente")
    @ns.response(400,"Error de validación en caso de que haya algún atributo incorrecto en el modelo de cliente")   
    @ns.response(404,"Cliente no encontrado con un determinado DNI")
    @ns.response(500,"Error del servidor")   
    def put(self):
        """Modifica los datos de un cliente a partir de un JSON. Comprobará si el DNI existe antes de modificar el cliente, cuyos field_validator comprobarán la validez de los campos"""
        try:
            cliente = Cliente(**api.payload)#Crea un objeto Cliente a partir del payload en formato JSON
            cliente_existente=DBHelper.obtenerCliente(cliente.DNI)#Llama a la base de datos para comprobar si el cliente existe
            if cliente_existente is None: #Si el cliente no existe
                return {"message": f"No se encontró ningún cliente con DNI {cliente.DNI}"},404 #Error no encontrado
            DBHelper.modificarCliente(cliente) #Modifica el cliente
            return {"message": "Cliente modificado correctamente"}, 200 #Resultado satisfactorio
        except ValidationError as e:
            errores=e.errors() #Lista de errores
            mensajes={} #Creación del json
            for error in errores: #Obtenemos la ubicación y mensaje de cada uno
                mensajes[error["loc"][0]]=error["msg"]
            return mensajes, 400 #Error de validación
        except:
            return {"message": "Problema al modificar cliente"}, 500 #Error de servidor

#Clase de eliminación de cliente
@ns.route("/eliminarCliente")
@ns.param("DNI", "El DNI del cliente a eliminar")
class EliminarCliente(Resource):
    @ns.response(200,"Cliente eliminado de la base de datos correctamente")
    @ns.response(400,"Error de validación en caso de DNI incorrecto")   
    @ns.response(404,"Cliente no encontrado con un determinado DNI")
    @ns.response(500,"Error del servidor") 
    def delete(self):
        """Elimina un cliente por su DNI, comprobando previamente la validez del DNI y si dicho cliente existe"""
        try:
            DNI = request.args.get("DNI") #Obtiene el DNI por parámetro
            if not DNI:#Si no se ha introducido DNI
                return {"message": "No se ha introducido un DNI"}, 400 #Error de validación
            if not Cliente.dni_es_verdadero(DNI): #Si el DNI es inválido
                return {"message":"El DNI introducido no es válido"}, 400 #Error de validación
            cliente=DBHelper.obtenerCliente(DNI) #Obtiene el cliente de la base de datos, si lo encuentra
            if cliente is None: #Si el cliente no existe
                return {"message": f"No se encontró ningún cliente con DNI {DNI}, no se puede eliminar"}, 404 #Error no encontrado
            DBHelper.eliminarCliente(DNI) #Elimina el cliente de la base de datos
            return {"message": "Cliente eliminado satisfactoriamente"}, 200 #Resultado satisfactorio
        except:
            return {"message": "Problema al eliminar cliente"}, 500 #Error de servidor

#Clase de cálculo de cuota
@ns.route("/calcularCuota")
@ns.param("DNI", "El DNI del cliente del que calcular la cuota mensual")
@ns.param("TAE", "Tasa Anual Equivalente en porcentaje. Debe tener un valor máximo de 100")
@ns.param("plazo_de_amortizacion", "Plazo de amortización en años")    
class CalcularCuota(Resource):
    @ns.response(200,"Cuota calculada correctamente")
    @ns.response(400,"Error de validación en caso de que alguno de los parámetros sea incorrecto")   
    @ns.response(404,"Cliente no encontrado con un determinado DNI")
    @ns.response(500,"Error del servidor") 
    def get(self):
        """Cálculo de cuota mensual de un cliente a partir del DNI de un cliente existente de la base de datos, un TAE y un plazo de amortización. Comprueba dichos parámetros antes de calcular la cuota mensual"""
        try:
            DNI = request.args.get("DNI") #Obtiene el DNI por parámetro
            TAE = request.args.get("TAE", type=float) #Obtiene la TAE por parámetro y la convierte a float
            plazo_de_amortizacion = request.args.get("plazo_de_amortizacion", type=int) #Obtiene el plazo de amortización por parámetro y lo convierte a entero
            if not DNI:#Si no se ha introducido DNI
                return {"message": "No se ha introducido un DNI"}, 400 #Error de validación
            if not Cliente.dni_es_verdadero(DNI): #Si el DNI es inválido
                return {"message": "El DNI introducido no es válido"}, 400 #Error de validación
            if TAE is None: #Si no se ha introducido TAE
                return {"message":"No se ha introducido TAE. Debe ser un número entre 0 y 100"},400 #Error de validación
            if TAE < 0 or TAE > 100: #Si la TAE no está entre 0 y 100
                return {"message":"El TAE introducido no es válido. Debe ser un número entre 0 y 100"},400 #Error de validación
            if plazo_de_amortizacion is None: #Si no se ha introducido plazo de amortización
                return {"message":"No se ha introducido plazo de amortización, debe ser un número mayor a 0"},400 #Error de validación
            if plazo_de_amortizacion<=0: #Si se ha introducido un plazo de amortización no positivo
                return {"message":"El plazo de amortización no es válido, debe ser un número mayor a 0"},400 #Error de validación
            cliente=DBHelper.obtenerCliente(DNI) #Obtenemos el cliente de la base de datos, si lo encuentra
            if cliente is None: #Si el cliente no existe
                return {"message":f"No existe cliente con el DNI {DNI}"}, 404 #Error no encontrado
            tipo_de_interes_mensual=TAE/100/12 #Cálculo del tipo de interés mensual a partir de la TAE
            num_meses_plazo_de_amortizacion=plazo_de_amortizacion*12 #Cálculo del número de meses de plazo de amortización a partir de los años
            cuota_mensual=(cliente.capital_solicitado*tipo_de_interes_mensual)/(1-(1+tipo_de_interes_mensual)**(-num_meses_plazo_de_amortizacion)) #Cálculo de la cuota mensual
            return {"message": f"El cliente {cliente.nombre} con un capital de {cliente.capital_solicitado} €, un TAE del {TAE} % y un plazo de amortización de {plazo_de_amortizacion} años, tiene una cuota mensual de es de {cuota_mensual} €"},200 #Resultado satisfactorio
        except:
            return {"message": "Problema al calcular la cuota"}, 500 #Error del servidor

# Iniciar la aplicación
if __name__ == "__main__":
    DBHelper.crearTabla()  # Crea la tabla si es necesario
    app.run() #Ejecuta el servidor