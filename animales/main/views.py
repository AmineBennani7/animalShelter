from django.db.models import Q
from .models import Animal
from django.shortcuts import render, redirect, get_object_or_404

def index(request):
    return render(request, 'animales/index.html')

def listar_todo(request):
    animales = Animal.objects.all()
    animales_unicos = eliminar_duplicados(animales)

    
    return render(request, 'animales/lista_animales.html', {'animales': animales_unicos})


def buscar_nombre_raza(request):
    query = request.GET.get('query')
    animales = Animal.objects.all()

    if query:
        animales = Animal.objects.filter(Q(nombre__icontains=query) | Q(raza__icontains=query))
    
    # Crear un diccionario para eliminar duplicados basados en url_detalle
    animales_unicos = {}
    for animal in animales:
        if animal.url_detalle not in animales_unicos:
            animales_unicos[animal.url_detalle] = animal

    # Convertir el diccionario de nuevo a una lista
    animales_unicos = list(animales_unicos.values())

    return render(request, 'animales/buscar_nombre_raza.html', {'animales': animales_unicos})



def eliminar_duplicados(animales):
    # Crear un diccionario para eliminar duplicados basados en url_detalle
    animales_unicos = {}
    for animal in animales:
        if animal.url_detalle not in animales_unicos:
            animales_unicos[animal.url_detalle] = animal

    # Convertir el diccionario de nuevo a una lista
    return list(animales_unicos.values())

def buscar_nombre_raza(request):
    query = request.GET.get('query')
    animales = Animal.objects.all()

    if query:
        animales = Animal.objects.filter(Q(nombre__icontains=query) | Q(raza__icontains=query))
    
    animales_unicos = eliminar_duplicados(animales)
    return render(request, 'animales/buscar_nombre_raza.html', {'animales': animales_unicos})

def buscar_genero(request):
    genero = request.GET.get('genero')
    if genero:
        animales = Animal.objects.filter(genero=genero)

    else:
        animales = Animal.objects.none()
    animales_unicos = eliminar_duplicados(animales)

    return render(request, 'animales/buscar_genero.html', {'animales': animales_unicos})


def buscar_tipo(request):
    tipo = request.GET.get('tipo')
    if tipo:
        animales = Animal.objects.filter(tipo=tipo)

    else:
        animales = Animal.objects.none()
    
    animales_unicos = eliminar_duplicados(animales)
    return render(request, 'animales/buscar_tipo.html', {'animales': animales_unicos})

def buscar_tamano(request):
    # Obtener todos los tamaños únicos de la base de datos
    tamanos = Animal.objects.values_list('tamano', flat=True).distinct()
    
    # Si se recibe un tamaño seleccionado en el formulario
    tamano_seleccionado = request.GET.get('tamano')
    if tamano_seleccionado:
        animales = Animal.objects.filter(tamano=tamano_seleccionado)
    else:
        animales = Animal.objects.none()
    animales_unicos = eliminar_duplicados(animales)

    
    return render(request, 'animales/buscar_tamano.html', {'animales': animales_unicos, 'tamanos': tamanos, 'tamano_seleccionado': tamano_seleccionado})

def buscar_tipo_tamano(request):
    # Obtener todos los tamaños únicos de la base de datos
    tamanos = Animal.objects.values_list('tamano', flat=True).distinct()
    
    tipo = request.GET.get('tipo')
    tamano = request.GET.get('tamano')
    if tipo and tamano:
        animales = Animal.objects.filter(tipo=tipo, tamano=tamano)
    else:
        animales = Animal.objects.none()
    animales_unicos = eliminar_duplicados(animales)

    return render(request, 'animales/buscar_tipo_tamano.html', {'animales': animales_unicos, 'tamanos': tamanos, 'tipo_seleccionado': tipo, 'tamano_seleccionado': tamano})

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
