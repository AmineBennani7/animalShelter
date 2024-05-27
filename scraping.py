from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import sqlite3
import lxml
from datetime import datetime
# lineas para evitar error SSL                          
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context
    




def obtener_tamano(url_detalle):
    f_detalle = urllib.request.urlopen(url_detalle)
    s_detalle = BeautifulSoup(f_detalle, "lxml")
    
    # Buscar el tamaño en la página de detalle
    tamano_elemento = s_detalle.find('li', class_='ficha_tamanio')
    tamano = tamano_elemento.find('span').text.strip() if tamano_elemento else "N/A"
    
    return tamano

def extraer_datos_arcaDeNoe():
    dominio_base = "https://arcadenoe.org"
    res=[]

    url_principal_perros = "https://arcadenoe.org/listado_animales.php?id_seccion=25"
    url_principal_gatos = "https://arcadenoe.org/listado_animales.php?id_seccion=26"
    
    for url_principal, tipo_animal in [(url_principal_perros, "Perro"), (url_principal_gatos, "Gato")]:
        pagina = 1
        while True:
            url_pagina = f"{url_principal}&p={pagina}"
            f_perros = urllib.request.urlopen(url_pagina)
            s = BeautifulSoup(f_perros, "lxml")
            
    
            contenedor_principal = s.find('div', id='principal_contenidos')
            if "No se encontraron animales" in contenedor_principal.text:
                break

            tarjetas_perros1 = contenedor_principal.find_all('div', class_='card cuadro_listado cuad1 c-horizontal')
            tarjetas_perros2 = contenedor_principal.find_all('div', class_='card cuadro_listado cuad2 c-horizontal')
            tarjetas_perros = []
            for elemento1, elemento2 in zip(tarjetas_perros1, tarjetas_perros2):
                tarjetas_perros.append(elemento1)
                tarjetas_perros.append(elemento2)

            for tarjeta in tarjetas_perros:
                nombre = tarjeta.find('h3', class_='card-title').text.strip()
                
                raza = tarjeta.find('p', class_='car_listado-raza').strong.next_sibling.strip()
                #Si la raza es desconocida
                if raza == "" :
                     raza = "N/A"
                genero_raw = tarjeta.find('p', class_='car_listado-sexo').strong.next_sibling.strip()
                # Remover los símbolos de género y reemplazarlos con "Hembra" o "Macho"
                genero = genero_raw.replace("♂", "").replace("♀", "").strip()

                edad = tarjeta.find('p', class_='car_listado-edad').strong.next_sibling.strip()
                foto = tarjeta.find('img')['src']
                url_foto=urllib.parse.urljoin(dominio_base, foto)


                # Obtener URL del detalle
                enlace_detalle = tarjeta.find('a', href=True)['href']
                url_detalle = f"{enlace_detalle}"
                tamano = obtener_tamano(url_detalle)


                # print('Nombre:', nombre)
                # print('Tipo:', tipo_animal)
                # print('Género:', genero)
                # print('Raza :', raza)
                # print('Edad :', edad)
                # print('Tamaño :' , tamano)
                # print('URL de la foto :', url_foto)
                # print('URL de origen:', url_detalle)
                # print()
                res.append((nombre, tipo_animal, genero, raza, edad, tamano, url_foto, url_detalle))


            pagina += 1
    return res

#PAGINA 2: 
dominio_base2="https://www.ciudadanimal.org"
def extraer_datos_ciudadAnimal():
    lista_detalles=[]
    url_principal = "https://www.ciudadanimal.org/animales-en-adopcion.html"
    f = urllib.request.urlopen(url_principal)

    s = BeautifulSoup(f, "lxml")
    articulo = s.find('article', class_='item-page')
    enlaces = articulo.find_all('a')
    for enlace in enlaces[:-2]:
        url = enlace.get('href')
        url_completa = urllib.parse.urljoin(dominio_base2, url)
        
        #recorro las distintas paginas 
        pagina = 11
        extraer_mascotas(url_completa,lista_detalles)

        while True:
             pagina += 10
             url_pagina = f"{url_completa}?start={pagina}"
             if not extraer_mascotas(url_pagina,lista_detalles):
                break

             extraer_mascotas(url_pagina,lista_detalles)
    return lista_detalles
    

def extraer_mascotas(url,lista_detalles):
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f, "lxml")
    secciones_animales = s.find_all('div', class_='items-row')

    # Verificar si hay artículos en esta categoría (para las paginas)
    if "No hay artículos en esta categoría." in s.text :
        return False

    
    # Usar un conjunto para almacenar URLs únicas
    urls_unicas = set()
    
    # Extraer y almacenar las URLs de los enlaces "Leer más..."
    for seccion in secciones_animales:
        enlaces = seccion.find_all('a', href=True)
        for enlace in enlaces:
            url_animal = enlace['href']
            url_animal_completa = urllib.parse.urljoin(dominio_base2, url_animal)
            urls_unicas.add(url_animal_completa)
    
    # Imprimir las URLs únicas
    for url in list(urls_unicas)[:-2]:
        detalles_mascotas(url,lista_detalles)
    return True


def detalles_mascotas(url,lista_detalles):
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f, "lxml")
    secciones_animales = s.find_all('article', class_='item-page')

    
    for seccion in secciones_animales:
        detalles = seccion.find_all('span', style="color: #7f0200;")  # Buscar todas las etiquetas <span> con el estilo de color específico
        
        # Inicializar variables para almacenar los detalles de la mascota
        nombre = None
        sexo = None
        raza = None
        edad = None
        tamaño = None
        foto_url = None
        
        tipo = "Gato" if "gatos-en-adopcion-lista.html" in url else "Perro"

        for detalle in detalles:
            texto = detalle.get_text(strip=True)  # Obtener el texto sin espacios adicionales
            
            if texto.startswith("- NOMBRE:"):
                nombre = detalle.find_next('span', style="color: #000000;").get_text(strip=True)
            elif texto.startswith("- SEXO:"):
                sexo = detalle.find_next('span', style="color: #000000;").get_text(strip=True)
            elif texto.startswith("- RAZA:"):
                raza = detalle.find_next('span', style="color: #000000;").get_text(strip=True)
                if raza == "" :
                     raza = "N/A"
            elif texto.startswith("- FECHA DE NACIMIENTO:"):
                fecha_nacimiento = detalle.find_next('span', style="color: #000000;").get_text(strip=True)
                edad = calcular_edad(fecha_nacimiento)
                if edad == "" :
                     edad = "N/A"
               
            elif texto.startswith("- MEDIDAS"):
                tamaño = detalle.find_next('span', style="color: #000000;").get_text(strip=True)
                tamano_cm = obtener_tamano_cm(tamaño)
                tamano_categoria = clasificar_tamano(tamano_cm)  
            

        # Encontrar la etiqueta <img> que contiene la foto de la mascota y extraer la URL de la imagen
        foto_tag = seccion.find('img', src=True)
        if foto_tag:
            foto_url = foto_tag['src']
            foto_url_completa = urllib.parse.urljoin(dominio_base2, foto_url)
        
        #Si el nombre es None, descartar los datos
        if nombre is None:
            continue
        lista_detalles.append((nombre, tipo, sexo, raza, edad, tamano_categoria, foto_url_completa, url))
       
    
        return (lista_detalles)  # Devolver la lista con los detalles de las mascotas


    

        #Imprimir o almacenar los detalles extraídos
        # print("Nombre:", nombre)
        # print("Tipo:", tipo)
        # print("Género:", sexo)
        # print("Raza:", raza)
        # print("Edad:", edad)
        # print("Tamaño:", tamano_categoria)
        # print("URL de la foto:", foto_url_completa)
        # print("URL de origen:", url)
        # print()


def clasificar_tamano(tamano_cm):
   
    if tamano_cm <= 25:
        return "Mini"
    elif 25 < tamano_cm <= 40:
        return "Pequeño"
    elif 40 < tamano_cm <= 55:
        return "Mediano"
    elif 55 < tamano_cm <= 70:
        return "Grande"
    else:
        return "Gigante"
def obtener_tamano_cm(tamano):
    # Extraer el tamaño en centímetros del texto
  
    tamano = tamano.split(' ')[0]
    if (tamano == "cms") or (tamano == "   cms aprox a la cruz. ")  :
        return 45
    
    elif "-" in tamano:
        valores = tamano.split("-")
        valor_inferior = int(valores[0])
        valor_superior = int(valores[1])
        # Calcular la mitad del rango
        tamano_cm = (valor_inferior + valor_superior) // 2
        return int(tamano_cm)
    else:
        return int(tamano)



def calcular_edad(fecha_nacimiento):
    try:
        # Intenta analizar la fecha completa
        fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%d.%m.%Y')
    except ValueError:
        # Si falla, intenta analizar solo el año
        fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y')
        # Calcula la edad solo con el año
        años = datetime.now().year - fecha_nacimiento.year
        return f"{años} años"
    else:
        fecha_actual = datetime.now()
        diferencia = fecha_actual - fecha_nacimiento
        años = diferencia.days // 365
        meses = (diferencia.days % 365) // 30
        return f"{años} años y {meses} meses"



   
print(extraer_datos_arcaDeNoe())
#print(extraer_datos_ciudadAnimal())

        
   
# def almacenar_bd():
#     conn = sqlite3.connect('animales.db')
#     conn.text_factory = str
#     conn.execute("DROP TABLE IF EXISTS ANIMALES")
#     conn.execute('''CREATE TABLE ANIMALES
#         (NOMBRE TEXT NOT NULL,
#         TIPO TEXT,
#         GENERO TEXT,
#         RAZA TEXT,
#         EDAD TEXT,
#         TAMANO TEXT,
#         FOTO_URL TEXT,
#         URL_ORIGEN TEXT);''')

#     datos_arcaDeNoe = extraer_datos_arcaDeNoe()
#     datos_ciudadAnimal = extraer_datos_ciudadAnimal()
#     todos_datos = datos_arcaDeNoe + datos_ciudadAnimal

#     for animal in todos_datos:
#         conn.execute("""INSERT INTO ANIMALES (NOMBRE, TIPO, GENERO, RAZA, EDAD, TAMANO, FOTO_URL, URL_ORIGEN) VALUES (?,?,?,?,?,?,?,?)""",
#                      animal)
#     conn.commit()
    
#     cursor = conn.execute("SELECT COUNT(*) FROM ANIMALES")
#     messagebox.showinfo("Base Datos",
#                         "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " animales.")
#     conn.close()

# Ejecutar la función para extraer y almacenar los datos
# almacenar_bd()
   
  
    
    # #LINK PAGINA 2: 
# def extraer_datos_arcaSevilla():
#     url_principal = "https://arcasevilla.es/arca/"
#     req = urllib.request.Request(url_principal, headers={'User-Agent': 'Mozilla/5.0'})  #Al usar como agente mozilla deja 
#     f = urllib.request.urlopen(req)
#     s = BeautifulSoup(f, "lxml")

#     en_adopcion_item = s.find('li', {'id': 'menu-item-648'})
#     links = en_adopcion_item.find_all('a', href=True)[1:]  
#     descartes = ['machos', 'hembras', 'especiales','particulares']
#     for link in links:  ##SE HAN DESCARTADO PARTICULARES Y ESPECIALES
#         href = link['href']
#         if not any(palabra in href for palabra in descartes):
#             extraer_animales(href)

# def extraer_animales(enlace):
#     req = urllib.request.Request(enlace, headers={'User-Agent': 'Mozilla/5.0'})
#     f = urllib.request.urlopen(req)
#     s = BeautifulSoup(f, "lxml")
#     div_content = s.find('div', class_='entry-content-wrapper')
#     animales_divs = div_content.find_all('div', class_='flex_cell')  #col de izquierda y col de derecha 
#     for animal_div in animales_divs:
#         animales_img = animal_div.find_all('a', class_='grid-image')
#         for animal in animales_img:
#             nombre = animal['title']

#             print("Nombre: ", nombre)

#             enlace_url = animal['href']
            
#             detalles_animales(enlace_url)

# def detalles_animales(enlace):
#     req = urllib.request.Request(enlace, headers={'User-Agent': 'Mozilla/5.0'})
#     f = urllib.request.urlopen(req)
#     s = BeautifulSoup(f, "lxml")
    
#     detalles_div = s.find('div', class_='entry-content-wrapper clearfix')
#     detalles = detalles_div.find_all('li')
#     for detalle in detalles:
#         if 'Sexo' in detalle.text:
#             detalle.string.replace_with('Género: ' + detalle.text.split(': ')[1])
#         print(detalle.text.strip())           
# #extraer_datos_arcaSevilla()

        
   
# def almacenar_bd():
#     conn = sqlite3.connect('animales.db')
#     conn.text_factory = str
#     conn.execute("DROP TABLE IF EXISTS ANIMALES")
#     conn.execute('''CREATE TABLE ANIMALES
#         (NOMBRE TEXT NOT NULL,
#         TIPO TEXT,
#         GENERO TEXT,
#         RAZA TEXT,
#         EDAD TEXT,
#         TAMANO TEXT,
#         FOTO_URL TEXT,
#         URL_ORIGEN TEXT);''')

#     datos_arcaDeNoe = extraer_datos_arcaDeNoe()
#     datos_ciudadAnimal = extraer_datos_ciudadAnimal()
#     todos_datos = datos_arcaDeNoe + datos_ciudadAnimal

#     for animal in todos_datos:
#         conn.execute("""INSERT INTO ANIMALES (NOMBRE, TIPO, GENERO, RAZA, EDAD, TAMANO, FOTO_URL, URL_ORIGEN) VALUES (?,?,?,?,?,?,?,?)""",
#                      animal)
#     conn.commit()
    
#     cursor = conn.execute("SELECT COUNT(*) FROM ANIMALES")
#     messagebox.showinfo("Base Datos",
#                         "Base de datos creada correctamente \nHay " + str(cursor.fetchone()[0]) + " animales.")
#     conn.close()

# Ejecutar la función para extraer y almacenar los datos
# almacenar_bd()
   
  
    
    # #LINK PAGINA 2: 
# def extraer_datos_arcaSevilla():
#     url_principal = "https://arcasevilla.es/arca/"
#     req = urllib.request.Request(url_principal, headers={'User-Agent': 'Mozilla/5.0'})  #Al usar como agente mozilla deja 
#     f = urllib.request.urlopen(req)
#     s = BeautifulSoup(f, "lxml")

#     en_adopcion_item = s.find('li', {'id': 'menu-item-648'})
#     links = en_adopcion_item.find_all('a', href=True)[1:]  
#     descartes = ['machos', 'hembras', 'especiales','particulares']
#     for link in links:  ##SE HAN DESCARTADO PARTICULARES Y ESPECIALES
#         href = link['href']
#         if not any(palabra in href for palabra in descartes):
#             extraer_animales(href)

# def extraer_animales(enlace):
#     req = urllib.request.Request(enlace, headers={'User-Agent': 'Mozilla/5.0'})
#     f = urllib.request.urlopen(req)
#     s = BeautifulSoup(f, "lxml")
#     div_content = s.find('div', class_='entry-content-wrapper')
#     animales_divs = div_content.find_all('div', class_='flex_cell')  #col de izquierda y col de derecha 
#     for animal_div in animales_divs:
#         animales_img = animal_div.find_all('a', class_='grid-image')
#         for animal in animales_img:
#             nombre = animal['title']

#             print("Nombre: ", nombre)

#             enlace_url = animal['href']
            
#             detalles_animales(enlace_url)

# def detalles_animales(enlace):
#     req = urllib.request.Request(enlace, headers={'User-Agent': 'Mozilla/5.0'})
#     f = urllib.request.urlopen(req)
#     s = BeautifulSoup(f, "lxml")
    
#     detalles_div = s.find('div', class_='entry-content-wrapper clearfix')
#     detalles = detalles_div.find_all('li')
#     for detalle in detalles:
#         if 'Sexo' in detalle.text:
#             detalle.string.replace_with('Género: ' + detalle.text.split(': ')[1])
#         print(detalle.text.strip())           
# #extraer_datos_arcaSevilla()
