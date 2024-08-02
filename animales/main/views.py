from django.db.models import Q
from django.http import HttpResponse

from .management.commands.scraping_django import almacenar_datos
from .models import Animal
from django.shortcuts import render, redirect, get_object_or_404
from whoosh.index import open_dir
from whoosh.qparser import MultifieldParser
from whoosh.qparser import QueryParser
from whoosh.index import open_dir




def load_data(request):
    if request.method == 'POST':
        almacenar_datos()
        return HttpResponse("Datos cargados exitosamente")
    return render(request, 'animales/load_data.html')

def index(request):
    return render(request, 'animales/index.html')



def listar_todo(request):
    if request.method == "GET":
        ix = open_dir("Index")
        
        # Obtener todos los documentos indexados
        with ix.searcher() as searcher:
            # Obtener todas las URLs de los documentos indexados
            animales_urls = [doc['url_detalle'] for doc in searcher.documents()]


        # Filtrar los animales de Django basados en las URLs obtenidas
        animales = Animal.objects.filter(url_detalle__in=animales_urls)
        animales_unicos = eliminar_duplicados(animales)



        return render(request, 'animales/lista_animales.html', {'animales': animales_unicos})
    else:
        return render(request, 'animales/lista_animales.html', {'animales': []})


def buscar_nombre_raza(request):
    if request.method == "GET":
        query = request.GET.get('query')
        
        if query:
            ix = open_dir("Index")
            
            # Parsear la consulta de búsqueda
            animal_query = MultifieldParser(["nombre", "raza"], ix.schema).parse(query)
            
            with ix.searcher() as searcher:
                # Realizar la búsqueda
                results = searcher.search(animal_query, limit=None)
                
                # Convertir los resultados de la búsqueda de Whoosh en URLs de animales
                animales_urls = [hit['url_detalle'] for hit in results]
            
            # Filtrar los animales de Django basados en las URLs obtenidas
            animales = Animal.objects.filter(url_detalle__in=animales_urls)
            
            animales_unicos = eliminar_duplicados(animales)

            return render(request, 'animales/buscar_nombre_raza.html', {'animales': animales_unicos})
        else:
            return render(request, 'animales/buscar_nombre_raza.html', {'animales': []})

    return render(request, 'animales/buscar_nombre_raza.html', {'animales': []})



def eliminar_duplicados(animales):
    # Crear un diccionario para eliminar duplicados basados en url_detalle
    animales_unicos = {}
    for animal in animales:
        if animal.url_detalle not in animales_unicos:
            animales_unicos[animal.url_detalle] = animal

    # Convertir el diccionario de nuevo a una lista
    return list(animales_unicos.values())



def buscar_genero(request):
    genero = request.GET.get('genero')
    if genero:
        ix = open_dir("Index")
        with ix.searcher() as searcher:
            query = QueryParser('genero', ix.schema).parse(genero)
            results = searcher.search(query, limit=None)
            animales_urls = [hit['url_detalle'] for hit in results]
        animales = Animal.objects.filter(url_detalle__in=animales_urls)
        animales_unicos = eliminar_duplicados(animales)
    else:
        animales_unicos = []

    return render(request, 'animales/buscar_genero.html', {'animales': animales_unicos})


def buscar_tipo(request):
    tipo = request.GET.get('tipo')
    if tipo:
        ix = open_dir("Index")
        with ix.searcher() as searcher:
            query = QueryParser('tipo', ix.schema).parse(tipo)
            results = searcher.search(query, limit=None)
            animales_urls = [hit['url_detalle'] for hit in results]
        animales = Animal.objects.filter(url_detalle__in=animales_urls)
        animales_unicos = eliminar_duplicados(animales)
    else:
        animales_unicos = []

    return render(request, 'animales/buscar_tipo.html', {'animales': animales_unicos})

def buscar_tamano(request):
    # Obtener todos los tamaños únicos disponibles en la base de datos de Whoosh
    ix = open_dir("Index")
    with ix.searcher() as searcher:
        unique_sizes = [size.decode('utf-8') for size in searcher.lexicon('tamano')]

    tamano = request.GET.get('tamano')
    animales_unicos = []

    if tamano:
        with ix.searcher() as searcher:
            query = QueryParser('tamano', ix.schema).parse(tamano)
            results = searcher.search(query, limit=None)
            animales_urls = [hit['url_detalle'] for hit in results]
            animales = Animal.objects.filter(url_detalle__in=animales_urls)
            animales_unicos = eliminar_duplicados(animales)

    return render(request, 'animales/buscar_tamano.html', {'animales': animales_unicos, 'tamanos': unique_sizes})


def buscar_tipo_tamano(request):
    tipo = request.GET.get('tipo')
    tamano = request.GET.get('tamano')
    if tipo and tamano:
        ix = open_dir("Index")
        with ix.searcher() as searcher:
            query_tipo = QueryParser('tipo', ix.schema).parse(tipo)
            results_tipo = searcher.search(query_tipo, limit=None)
            query_tamano = QueryParser('tamano', ix.schema).parse(tamano)
            results_tamano = searcher.search(query_tamano, limit=None)
            animales_urls = [hit['url_detalle'] for hit in results_tipo if hit['url_detalle'] in [hit['url_detalle'] for hit in results_tamano]]
        animales = Animal.objects.filter(url_detalle__in=animales_urls)
        animales_unicos = eliminar_duplicados(animales)
    else:
        animales_unicos = []

    return render(request, 'animales/buscar_tipo_tamano.html', {'animales': animales_unicos})

def buscar_rango_edades(request):
    edad_min = request.GET.get('edad_min')
    edad_max = request.GET.get('edad_max')
    if edad_min is not None and edad_max is not None:
        animales = Animal.objects.filter(edad__gte=edad_min, edad__lte=edad_max)
    else:
        animales = Animal.objects.none()
    
    animales_unicos = eliminar_duplicados(animales)
    return render(request, 'animales/buscar_rango_edades.html', {'animales': animales_unicos})

def buscar_avanzado(request):
    if request.method == 'GET':
        # Obtener los parámetros de la solicitud GET
        tipo = request.GET.get('tipo', '')
        genero = request.GET.get('genero', '')
        tamano = request.GET.get('tamano', '')
        edad_min = request.GET.get('edad_min', '')
        edad_max = request.GET.get('edad_max', '')

        # Filtrar los animales según los parámetros proporcionados
        animales = Animal.objects.all()
        if tipo:
            animales = animales.filter(tipo=tipo)
        if genero:
            animales = animales.filter(genero=genero)
        if tamano:
            animales = animales.filter(tamano=tamano)
        if edad_min:
            animales = animales.filter(edad__gte=edad_min)
        if edad_max:
            animales = animales.filter(edad__lte=edad_max)
        
        animales_unicos = eliminar_duplicados(animales)

        # Obtener todos los tamaños únicos de la base de datos
        tamanos = Animal.objects.values_list('tamano', flat=True).distinct()

        # Renderizar el template con los resultados de la búsqueda y los tamaños únicos
        return render(request, 'animales/buscar_avanzado.html', {'animales': animales_unicos, 'tamanos': tamanos})
    else:
        # Si no es una solicitud GET, simplemente mostrar el formulario de búsqueda
        return render(request, 'animales/buscar_avanzado.html')
