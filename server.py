from fastapi import FastAPI, HTTPException
from typing import List
from modelos import Municipio  
import requests
import json

app = FastAPI()

# Obtener los datos de la fuente: 
url = "https://infra.datos.gob.ar/catalog/modernizacion/dataset/7/distribution/7.4/download/municipios.json"
response = requests.get(url)

if response.status_code != 200:
    print(f"There was an error {response.status_code}")

# Guardarlos en un archivo json --> municipios.json
data = json.loads(response.text)
open("municipios.json", "wb").write(response.content)
municipios = data['municipios']
# Acceso a los municipios

def get_provincias():     
    municipios= data["municipios"]
    provincias = {}
    for muni in municipios:
        provin = muni["provincia"]["nombre"]
        if provin not in provincias:
            provincias[provin] = []
    return provincias


def ver_municipios():
    with open("municipios.json", "r", encoding='utf-8') as file:
        data_municipios = file.read()
    return data_municipios    


# ENDPOINTS --> Get

# Nop parameters
@app.get('/')
def root():
    return {"Bienvenid@!"}

#Ver el json crudo
@app.get('/api/data')
def municipios():
    return ver_municipios()

# Ver todas las provincias, sin municipios y a que pprov pertenece el muni
@app.get('/api/data/provincias')
def provincias(nombre = None):
    prov_muni = get_provincias()
    municipios = data['municipios']

    
    # Todos los municipios
    if nombre == None:
        return prov_muni
    

    # Cargar datos
    for muni in municipios:
            provin = muni["provincia"]["nombre"]
            nombre_com = muni['nombre']
            prov_muni[provin].append(nombre_com)

    # El nombre es de una provincia
    if nombre in prov_muni:
        return prov_muni[nombre]
    # No es el nombre de una provincia sino de un municipio:
    else:   
        for clave, valor in prov_muni.items():
            if nombre in valor:
                return f"El municipio de {nombre} esta en la provincia: {clave}"
    

# Ver todos los municipios, separados por provincia
@app.get('/api/data/municipios/')
def municipios(nombre = None):
    municipios= data["municipios"]
    prov_muni = get_provincias()

    # Cargar datos
    for muni in municipios:
            provin = muni["provincia"]["nombre"]
            nombre_com = muni['nombre']
            prov_muni[provin].append(nombre_com)
    
    if nombre == None:
        return prov_muni
    else:

        for muni in municipios:
            muni = dict(muni)
            if muni['nombre'].lower() == nombre.lower():
                return muni

# Ver todas las categorías
@app.get('/api/data/provincias/municipios/categoria')
def categoria_all(nombre = None):
    municipios= data["municipios"]
    categorias = {}
    for muni in municipios:
        categoria = muni["categoria"]
        if categoria not in categorias:
            categorias[categoria] = []

    if nombre == None:
        return categorias

    for muni in municipios:
        categoria = muni["categoria"]
        categorias[categoria].append(muni["nombre"])
    
    # Es una categoria
    todas_cat = list(categorias.keys())
    if nombre in todas_cat:
        return categorias[nombre]
    # Es un municipio
    for clave, valor in categorias.items():
        if nombre in list(valor):
            return f"El municipio de {nombre} es de la categoría: {clave}"


# ENDPOINTS --> Put
# Cambiar nombre completo del municipio
@app.put('/api/data/provincias/{nombre}/{nombre_completo}')
def update_nombre_completo_municipio(nombre: str, nombre_completo: str):
    municipios= data["municipios"]
    for municipio in municipios:
        if municipio['nombre'] == nombre.capitalize():
            municipio['nombre_completo'] = nombre_completo.capitalize()
            return {"Mensaje": f"Nombre de {municipio['nombre']} actualizado."}

    raise HTTPException(
        status_code=404,
        detail=f"No se pudo actualizar el nombre completo de {nombre}. Municipio no encontrado."
    )    


@app.put('/api/data/provincias/{nombre}/cat/{categoria}')
def update_municipio_categoria(nombre: str, categoria: str):
    municipios= data["municipios"]
    for municipio in municipios:
        if municipio['nombre'] == nombre.capitalize():
            municipio['categoria'] = categoria.capitalize()
            return {"Mensaje": f"Categoria de {nombre} actualizada."}

    raise HTTPException(
        status_code=404,
        detail=f"No se pudo actualizar la categoría de {nombre}. Municipio no encontrado."
    )   


# ENDPOINTS --> Post
# Agregar nuevo municipio
@app.post('/api/data/add')
async def agregar_municipio(mun: Municipio): 
    municipios= data["municipios"]
    municipio_nuevo = mun
    municipios.append(municipio_nuevo)
    return dict(municipio_nuevo)
    
# ENDPOINTS --> Delete
#El nombre a agregar tiene que estar en minuscula. 
@app.delete('/api/data/remove')
async def del_municipio(nombre: str):
    municipios= data["municipios"]
    for mun in municipios:
        mun = dict(mun)
        if mun["nombre"] == nombre.lower():
            indice = municipios.index(mun)
            municipios.pop(indice)
            return mun
