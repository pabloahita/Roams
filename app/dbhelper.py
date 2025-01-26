import sqlite3
from cliente import Cliente
class DBHelper:

    conexion=None
    
    @staticmethod
    def abrirConexion():
        DBHelper.conexion=sqlite3.connect("basededatos.db")
    
    @staticmethod
    def crearTabla():
        DBHelper.abrirConexion()
        try:
            DBHelper.conexion.execute("""create table clientes (
                                    nombre text,
                                    DNI text primary key,
                                    email text,
                                    capital_solicitado real
                                )""")                  
        except sqlite3.OperationalError:
            pass
        
        DBHelper.conexion.close()

    @staticmethod
    def crearCliente(cliente: Cliente):
        DBHelper.abrirConexion()
        DBHelper.conexion.execute("insert into clientes(nombre,DNI,email,capital_solicitado) VALUES (?,?,?,?)",(cliente.nombre,cliente.DNI,cliente.email,cliente.capital_solicitado))
        DBHelper.conexion.commit()
        DBHelper.conexion.close()

    @staticmethod
    def obtenerCliente(dni:str):
        DBHelper.abrirConexion()
        cursor=DBHelper.conexion.execute("select nombre,email,capital_solicitado from clientes where DNI=?",(dni,))
        fila=cursor.fetchone()
        DBHelper.conexion.close()
        if fila is None:
            return None
        
        return Cliente(
            nombre=fila[0],
            DNI=dni,
            email=fila[1],
            capital_solicitado=fila[2]
        )
    
    @staticmethod
    def modificarCliente(cliente: Cliente,dni:str):
        DBHelper.abrirConexion()
        DBHelper.conexion.execute("update clientes set nombre=?,DNI=?,email=?,capital_solicitado=? where DNI=?",(cliente.nombre,cliente.DNI,cliente.email,cliente.capital_solicitado,dni))
        DBHelper.conexion.commit()
        DBHelper.conexion.close()

    @staticmethod
    def eliminarCliente(dni:str):
        DBHelper.abrirConexion()
        DBHelper.conexion.execute("delete from clientes where DNI=?",(dni,))
        DBHelper.conexion.commit()
        DBHelper.conexion.close()
    