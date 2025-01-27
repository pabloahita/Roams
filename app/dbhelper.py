import sqlite3
from cliente import Cliente

#Clase con métodos estáticos para realizar diferentes operaciones a la base de datos
class DBHelper:

    conexion=None #Conexión a la base de datos
    
    #Apertura de conexión
    @staticmethod
    def abrirConexion():
        DBHelper.conexion=sqlite3.connect("basededatos.db") #Llama al fichero basededatos.db
    
    #Creación de la tabla
    @staticmethod
    def crearTabla():
        DBHelper.abrirConexion() #Llama al método de apertura de conexión
        try:
            DBHelper.conexion.execute("""create table clientes (
                                    nombre text,
                                    DNI text primary key,
                                    email text,
                                    capital_solicitado real
                                )""") #Crea la tabla                 
        except sqlite3.OperationalError: #Si la tabla ya está creada, pasa de la excepción
            pass
        
        DBHelper.conexion.close() #Cierra la conexión

    #Inserción de un cliente en la base de datos
    @staticmethod
    def crearCliente(cliente: Cliente):
        DBHelper.abrirConexion() #Llama al método de apertura de conexión
        DBHelper.conexion.execute("insert into clientes(nombre,DNI,email,capital_solicitado) VALUES (?,?,?,?)",(cliente.nombre,cliente.DNI,cliente.email,cliente.capital_solicitado)) #Ejecuta el comando SQL
        DBHelper.conexion.commit() #Guarda los cambios
        DBHelper.conexion.close() #Cierra la conexión

    #Obtención de un cliente en la base de datos
    @staticmethod
    def obtenerCliente(dni:str):
        DBHelper.abrirConexion() #Llama al método de apertura de conexión
        cursor=DBHelper.conexion.execute("select nombre,email,capital_solicitado from clientes where DNI=?",(dni,))#Ejecuta el comando SQL
        fila=cursor.fetchone() #Obtiene el único resultado, si le hay
        DBHelper.conexion.close() #Cierra la conexión
        if fila is None:
            return None
        
        return Cliente(
            nombre=fila[0],
            DNI=dni,
            email=fila[1],
            capital_solicitado=fila[2]
        )
    
    #Modificación de un cliente en la base de datos
    @staticmethod
    def modificarCliente(cliente: Cliente):
        DBHelper.abrirConexion() #Llama al método de apertura de conexión
        DBHelper.conexion.execute("update clientes set nombre=?,DNI=?,email=?,capital_solicitado=? where DNI=?",(cliente.nombre,cliente.DNI,cliente.email,cliente.capital_solicitado,cliente.DNI)) #Ejecuta el comando SQL
        DBHelper.conexion.commit() #Guarda los cambios
        DBHelper.conexion.close() #Cierra la conexión

    #Eliminación de un cliente en la base de datos
    @staticmethod
    def eliminarCliente(dni:str):
        DBHelper.abrirConexion() #Llama al método de apertura de conexión
        DBHelper.conexion.execute("delete from clientes where DNI=?",(dni,))
        DBHelper.conexion.commit() #Guarda los cambios
        DBHelper.conexion.close() #Cierra la conexión
    