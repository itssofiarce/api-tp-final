import requests

# El código del cliente API que ya tienes aquí...

def ver_municipios():
    """Ver el JSON crudo con todos los municipios."""
    response = requests.get("http://localhost:8000/redes/tp/api/data")
    if response.status_code == 200:
        print(response.text)
    else:
        print(f"Error al obtener los municipios. Código de estado: {response.status_code}")

def municipo_info(nombre):
    """Ver los datos de un municipio específico."""
    response = requests.get(f"http://localhost:8000/redes/tp/api/data/{nombre}")
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error al obtener los datos del municipio. Código de estado: {response.status_code}")

def provincias():
    """Ver todas las provincias sin municipios."""
    response = requests.get("http://localhost:8000/redes/tp/api/data/provincias")
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error al obtener las provincias. Código de estado: {response.status_code}")

def municipios():
    """Ver todos los municipios separados por provincia."""
    response = requests.get("http://localhost:8000/redes/tp/api/data/provincias/municipios")
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error al obtener los municipios. Código de estado: {response.status_code}")

def categoria_all():
    """Ver municipios según categoría."""
    response = requests.get("http://localhost:8000/redes/tp/api/data/provincias/municipios/categoria")
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error al obtener las categorías. Código de estado: {response.status_code}")

def categoria_por_nombre(categoria):
    """Ver todos los municipios de una categoría específica."""
    response = requests.get(f"http://localhost:8000/redes/tp/api/data/provincias/municipios/{categoria}")
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error al obtener los municipios de la categoría. Código de estado: {response.status_code}")

def update_nombre_completo_municipio(nombre, nombre_completo):
    """Cambiar el nombre completo de un municipio."""
    data = {"nombre_completo": nombre_completo}
    response = requests.put(f"http://localhost:8000/redes/tp/api/data/provincias/{nombre}/{nombre_completo}", json=data)
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error al actualizar el nombre completo del municipio. Código de estado: {response.status_code}")

def update_municipio_categoria(nombre, categoria):
    """Cambiar la categoría de un municipio."""
    data = {"categoria": categoria}
    response = requests.put(f"http://localhost:8000/redes/tp/api/data/provincias/{nombre}/cat/{categoria}", json=data)
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error al actualizar la categoría del municipio. Código de estado: {response.status_code}")

def agregar_municipio(nombre, nombre_completo, categoria):
    """Agregar un nuevo municipio."""
    data = {"nombre": nombre, "nombre_completo": nombre_completo, "categoria": categoria}
    response = requests.post("http://localhost:8000/redes/tp/api/data/add", json=data)
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error al agregar el nuevo municipio. Código de estado: {response.status_code}")

def del_municipio(nombre):
    """Eliminar un municipio."""
    response = requests.delete(f"http://localhost:8000/redes/tp/api/data/remove?nombre={nombre}")
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Error al eliminar el municipio. Código de estado: {response.status_code}")

# Menú interactivo
while True:
    print("\n--- MENÚ INTERACTIVO ---")
    print("1. Ver JSON crudo con todos los municipios")
    print("2. Ver datos de un municipio específico")
    print("3. Ver todas las provincias sin municipios")
    print("4. Ver todos los municipios separados por provincia")
    print("5. Ver municipios según categoría")
    print("6. Ver todos los municipios de una categoría específica")
    print("7. Cambiar el nombre completo de un municipio")
    print("8. Cambiar la categoría de un municipio")
    print("9. Agregar un nuevo municipio")
    print("10. Eliminar un municipio")
    print("0. Salir")

    opcion = input("Ingrese el número de opción deseada: ")

    if opcion == "1":
        ver_municipios()
    elif opcion == "2":
        nombre = input("Ingrese el nombre del municipio: ")
        municipo_info(nombre)
    elif opcion == "3":
        provincias()
    elif opcion == "4":
        municipios()
    elif opcion == "5":
        categoria_all()
    elif opcion == "6":
        categoria = input("Ingrese el nombre de la categoría: ")
        categoria_por_nombre(categoria)
    elif opcion == "7":
        nombre = input("Ingrese el nombre del municipio: ")
        nombre_completo = input("Ingrese el nuevo nombre completo: ")
        update_nombre_completo_municipio(nombre, nombre_completo)
    elif opcion == "8":
        nombre = input("Ingrese el nombre del municipio: ")
        categoria = input("Ingrese el nuevo nombre de la categoría: ")
        update_municipio_categoria(nombre, categoria)
    elif opcion == "9":
        nombre = input("Ingrese el nombre del municipio: ")
        nombre_completo = input("Ingrese el nombre completo del municipio: ")
        categoria = input("Ingrese la categoría del municipio: ")
        agregar_municipio(nombre, nombre_completo, categoria)
    elif opcion == "10":
        nombre = input("Ingrese el nombre del municipio a eliminar: ")
        del_municipio(nombre)
    elif opcion == "0":
        print("¡Hasta luego!")
        break
    else:
        print("Opción inválida. Por favor, ingrese un número del menú.")

