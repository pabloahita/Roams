import re
from pydantic import BaseModel, EmailStr, field_validator

#Clase cliente basada en BaseModel de PyDantic, sin necesidad de constructor explícito
class Cliente(BaseModel):

    nombre:str #Nombre del cliente
    DNI:str #DNI del cliente
    email:EmailStr #Email del cliente. EmailStr comprueba la validez implícitamente, por eso no hay validador explícito
    capital_solicitado:float #Capital solicitado

    #Validador del nombre
    @field_validator("nombre")
    def comprobarNombre(cls,nombre):
        if not nombre: #Si no se ha escrito nombre, lanza la excepción
            raise ValueError("No se ha introducido el nombre")
        return nombre

    #Validador del DNI
    @field_validator("DNI")
    def comprobarDNI(cls,DNI):
        if not DNI:
            raise ValueError("No se ha introducido el DNI")
        if not cls.dni_es_verdadero(DNI): #Si el DNI es incorrecto, lanza la excepción
            raise ValueError("El DNI no es válido")
        return DNI
    
    #Validador del capital solicitado
    @field_validator("capital_solicitado")
    def comprobarCapitalSolicitado(cls,capital_solicitado):
        if capital_solicitado is None: #Si no se ha escrito capital solicitado, lanza la excepción
            raise ValueError("No se ha introducido un capital solicitado")
        elif capital_solicitado<=0:#Si no se ha escrito un capital solicitado positivo, lanza la excepción
            raise ValueError("El capital solicitado es incorrecto.")
        return capital_solicitado
        
    #Algoritmo oficial de comprobación de DNI
    @staticmethod
    def dni_es_verdadero(DNI:str) -> bool:
        if re.match(r'^\d{8}[A-Z]$', DNI): #Comprueba el formato de 8 dígitos y 1 letra con re
            letras="TRWAGMYFPDXBNJZSQVHLCKE" #Conjunto de letras en orden
            numeroDNI=int(DNI[:-1]) #Extrae los 8 dígitos del DNI y los convierte a entero
            letraDNI=DNI[-1] #Extrae la letra del DNI
            modulo=numeroDNI%23 #El módulo establece la posición de la letra correspondiente
            return letras[modulo]==letraDNI #Si la letra de la lista de letras y la letra proporcionada son iguales, el DNI es verdadero
        return False #DNI falso
    
    