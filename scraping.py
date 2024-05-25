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
    print(tamano_elemento)
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
                genero = tarjeta.find('p', class_='car_listado-sexo').strong.next_sibling.strip()
                edad = tarjeta.find('p', class_='car_listado-edad').strong.next_sibling.strip()
                foto = tarjeta.find('img')['src']

                # Obtener URL del detalle
                enlace_detalle = tarjeta.find('a', href=True)['href']
                url_detalle = f"{enlace_detalle}"
                tamano = obtener_tamano(url_detalle)


                print('nombre :', nombre)
                print('tipo :', tipo_animal)
                print('raza :', raza)
                print('genero :', genero)
                print('Tamaño :' , tamano)
                print('edad :', edad)
                print('foto :', foto)
                print('--------------------------------------')
            pagina += 1

#extraer_datos_arcaDeNoe()


def extraer_datos_arcaSevilla():
    url_principal = "https://arcasevilla.es/arca/"
    req = urllib.request.Request(url_principal, headers={'User-Agent': 'Mozilla/5.0'})  #Al usar como agente mozilla deja 
    f = urllib.request.urlopen(req)
    s = BeautifulSoup(f, "lxml")

    en_adopcion_item = s.find('li', {'id': 'menu-item-648'})
    links = en_adopcion_item.find_all('a', href=True)[1:]  
    descartes = ['machos', 'hembras', 'especiales','particulares']
    for link in links:  ##SE HAN DESCARTADO PARTICULARES Y ESPECIALES
        href = link['href']
        if not any(palabra in href for palabra in descartes):
            print(href)
extraer_datos_arcaSevilla()






        
   
        

   
  
    
    
 

