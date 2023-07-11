from pydantic import BaseModel

class Provincia(BaseModel):
    nombre: str 
    id: int
    interseccion: float

class Centroide(BaseModel):
    lat: float 
    lon: float

class Municipio(BaseModel):
    nombre_completo: str
    fuente: str 
    nombre: str 
    id: int 
    provincia: Provincia
    categoria: str
    centroide: Centroide