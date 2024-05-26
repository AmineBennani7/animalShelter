from bs4 import BeautifulSoup
import urllib.request
from tkinter import *
from tkinter import messagebox
import sqlite3
import lxml
from datetime import datetime




# def cargar():
#    respuesta = messagebox.askyesno(title="Confirmar",message="Esta seguro que quiere recargar los datos. \nEsta operaciÃ³n puede ser lenta")
#    if respuesta:
#        almacenar_bd()
#         #almacenar_bd(titulo,titulo_original,paises,fecha_estreno,director,generos )

def obtener_tamano(url_detalle):
    f_detalle = urllib.request.urlopen(url_detalle)
    s_detalle = BeautifulSoup(f_detalle, "lxml")
    
    # Buscar el tamaño en la página de detalle
    tamano_elemento = s_detalle.find('li', class_='ficha_tamanio')
    tamano = tamano_elemento.find('span').text.strip() if tamano_elemento else "N/A"
    
    return tamano

def extraer_datos_arcaDeNoe():
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

                # Obtener URL del detalle
                enlace_detalle = tarjeta.find('a', href=True)['href']
                url_detalle = f"{enlace_detalle}"
                tamano = obtener_tamano(url_detalle)


                print('Nombre:', nombre)
                print('Tipo:', tipo_animal)
                print('Género:', genero)
                print('Raza :', raza)
                print('Edad :', edad)
                print('Tamaño :' , tamano)
                print('URL de la foto :', foto)
                print('URL de origen:', url_detalle)
                print()
            pagina += 1

#extraer_datos_arcaDeNoe()



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




#PAGINA 2: 
dominio_base="https://www.ciudadanimal.org"
def extraer_datos_ciudadAnimal():
    url_principal = "https://www.ciudadanimal.org/animales-en-adopcion.html"
    f = urllib.request.urlopen(url_principal)

    s = BeautifulSoup(f, "lxml")
    articulo = s.find('article', class_='item-page')
    enlaces = articulo.find_all('a')
    for enlace in enlaces:
        url = enlace.get('href')
        url_completa = urllib.parse.urljoin(dominio_base, url)

        extraer_mascotas(url_completa)
    

def extraer_mascotas(url):
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f, "lxml")
    secciones_animales = s.find_all('div', class_='items-row')
    
    # Usar un conjunto para almacenar URLs únicas
    urls_unicas = set()
    
    # Extraer y almacenar las URLs de los enlaces "Leer más..."
    for seccion in secciones_animales:
        enlaces = seccion.find_all('a', href=True)
        for enlace in enlaces:
            url_animal = enlace['href']
            url_animal_completa = urllib.parse.urljoin(dominio_base, url_animal)
            urls_unicas.add(url_animal_completa)
    
    # Imprimir las URLs únicas
    for url in list(urls_unicas)[:-1]:
        detalles_mascotas(url)

def detalles_mascotas(url):
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
            elif texto.startswith("- FECHA DE NACIMIENTO:"):
                fecha_nacimiento = detalle.find_next('span', style="color: #000000;").get_text(strip=True)
                edad = calcular_edad(fecha_nacimiento)
               
            elif texto.startswith("- MEDIDAS:"):
                tamaño = detalle.find_next('span', style="color: #000000;").get_text(strip=True)
                tamano_cm = obtener_tamano_cm(tamaño)
                tamano_categoria = clasificar_tamano(tamano_cm)           

        # Encontrar la etiqueta <img> que contiene la foto de la mascota y extraer la URL de la imagen
        foto_tag = seccion.find('img', src=True)
        if foto_tag:
            foto_url = foto_tag['src']

        # Imprimir o almacenar los detalles extraídos
        print("Nombre:", nombre)
        print("Tipo:", tipo)
        print("Género:", sexo)
        print("Raza:", raza)
        print("Edad:", edad)
        print("Tamaño:", tamano_categoria)
        print("URL de la foto:", foto_url)
        print("URL de origen:", url)
        print()


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
    if tamano == "cms" :
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



   



extraer_datos_ciudadAnimal()

        
   
        

   
  
    
    
 

#mini pequeño mediano grande gigante