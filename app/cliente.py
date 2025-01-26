import re
from pydantic import BaseModel, EmailStr, field_validator

class Cliente(BaseModel):

    nombre:str
    DNI:str
    email:EmailStr
    capital_solicitado:float

    @field_validator("nombre")
    def comprobarNombre(cls,nombre):
        if not nombre:
            raise ValueError("El nombre está vacío")
        return nombre

    @field_validator("DNI")
    def comprobarDNI(cls,DNI):
        if not cls.dni_es_verdadero(DNI):
            raise ValueError("El DNI no es válido")
        return DNI
    
    @field_validator("capital_solicitado")
    def comprobarCapitalSolicitado(cls,capital_solicitado):
        if not capital_solicitado:
            raise ValueError("No se ha introducido un capital solicitado")
        elif capital_solicitado<=0:
            raise ValueError("El capital solicitado es incorrecto.")
        return capital_solicitado
        

    @staticmethod
    def dni_es_verdadero(DNI:str) -> bool:
        if re.match(r'^\d{8}[A-Z]$', DNI):
            letras="TRWAGMYFPDXBNJZSQVHLCKE"
            numeroDNI=int(DNI[:-1])
            letraDNI=DNI[-1]
            modulo=numeroDNI%23
            return letras[modulo]==letraDNI
        return False
    
    