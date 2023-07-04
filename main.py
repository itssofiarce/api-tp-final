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

# Globales
# Acceso a los municipios


def get_provincias():     
    municipios= data["municipios"]
    provincias = {}
    for muni in municipios:
        provin = muni["provincia"]["nombre"]
        if provin not in provincias:
            provincias[provin] = []
    return provincias

def get_municipios(name=None): 
    municipios= data["municipios"]
    prov_muni = get_provincias()

    # Cargar datos
    for muni in municipios:
            provin = muni["provincia"]["nombre"]
            nombre_com = muni['nombre']
            prov_muni[provin].append(nombre_com)

    # Todos los municipios
    if name == None:
        return prov_muni
    
    # El nombre es de una provincia
    nombre = name
    if nombre in prov_muni:
        return prov_muni[nombre]
    # No es el nombre de una provincia sino de un municipio:
    else:   
        for clave, valor in prov_muni.items():
            if nombre in valor:
                return f"El municipio de {name} esta en la provincia: {clave}"

def ver_municipios():
    with open("municipios.json", "r", encoding='utf-8') as file:
        data_municipios = file.read()
    return data_municipios    

def get_categoria(cat = None):
    municipios= data["municipios"]
    categorias = {}
    for muni in municipios:
        categoria = muni["categoria"]
        if categoria not in categorias:
            categorias[categoria] = []

    if cat == None:
        return categorias

    for muni in municipios:
        categoria = muni["categoria"]
        categorias[categoria].append(muni["nombre"])
    
    # Es una categoria
    if cat in categorias.keys():
        return categorias[cat]
    
    # Es un municipio
    for clave, valor in categorias.items():
        if cat in valor:
            return f"El municipio de {cat} es de la categoría: {clave}"

    



# ENDPOINTS --> Get
@app.get('/')
def root():
    return {"Bienvenid@!"}

#Ver el json crudo
@app.get('/redes/tp/api/data')
async def municipios():
    return ver_municipios()

# Ver todos los datos de x municipio
@app.get('/redes/tp/api/data/{nombre}')
def municipo_info(nombre: str):
    municipios= data["municipios"]
    # Cargar datos
    for muni in municipios:
        if muni['nombre'] == nombre.capitalize():
            return muni


# Ver todas las provincias, sin municipios
@app.get('/redes/tp/api/data/provincias')
async def provincias():
    return get_provincias()


# Ver todos los municipios, separados por provincia
@app.get('/redes/tp/api/data/provincias/municipios')
def municipios():
    return get_municipios()

# Ver municipios segun categoría
@app.get('/redes/tp/api/data/provincias/municipios/categoria')
def categoria_all():
    return get_categoria()

# Ver municipios segun categoría
@app.get('/redes/tp/api/data/provincias/municipios/{categoria}')
async def categoria_por_nombre(categoria: str):
    cg = categoria.capitalize()
    return get_categoria(f"{cg}")

# Ver todos los municipios de x provincia 
@app.get('/redes/tp/api/data/provincias/municipios/{provincia}')
async def municipio_de_prov(provincia: str):
    pr = provincia.capitalize()
    return get_municipios(pr)

# Ver la provincia, dado un x municipio 
@app.get('/redes/tp/api/data/provincias/{municipio}')
async def municipios_por_nombre(nombre: str):
    return get_municipios(f"{municipio}")




# ENDPOINTS --> Put
 
# Cambiar nombre completo del municipio
@app.put('/redes/tp/api/data/provincias/{nombre}/{nombre_completo}')
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

@app.put('/redes/tp/api/data/provincias/{nombre}/cat/{categoria}')

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

# Agregar nuevo municipio

@app.post('/redes/tp/api/data/add')
async def agregar_municipio(mun: Municipio): 
    municipios= data["municipios"]
    municipios.append(mun)
    return mun
    
@app.delete('/redes/tp/api/data/remove')
async def del_municipio(nombre: str):
    municipios= data["municipios"]
    for mun in municipios:
        if mun["nombre"] == nombre.capitalize():
            municipios.pop(municipios.index(mun))
            return mun
  





            



                