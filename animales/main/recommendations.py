from math import sqrt

from .models import Animal

# animals = [
#     ('SIMBA', 'Perro', 'Macho', 'Mestizo', 9, 'Mediano', 'https://arcadenoe.org/imas/animales/_579/thumbnail_square.jpg?id=1838', 'https://arcadenoe.org/ficha-579'),
#     ('THOR', 'Perro', 'Macho', 'Mestizo Labrador y Border Collie', 8, 'Mediano', 'https://arcadenoe.org/imas/animales/_662/thumbnail_square.jpg?id=2113', 'https://arcadenoe.org/ficha-662'),
#     ('TRUFO', 'Perro', 'Macho', 'Mestizo Labrador y Border Collie', 8, 'Mediano', 'https://arcadenoe.org/imas/animales/_661/thumbnail_square.jpg?id=2110', 'https://arcadenoe.org/ficha-661')
# ]


# # Función de similitud de Jaccard ajustada para múltiples atributos
# #https://jackfiallos.com/similitud-coseno-y-jaccard-midiendo-semejanzas-en-python
# def sim_jaccard(prefs, animal1, animal2):
#     # Asumimos que los atributos relevantes son: Tipo, Género, Raza, Tamaño
#     attrs_animal1 = set(prefs[animal1][1:4])  # Tipo, Género, Raza
#     attrs_animal2 = set(prefs[animal2][1:4])  # Tipo, Género, Raza
    
#     # Considerar también el tamaño como un atributo adicional
#     attrs_animal1.add(prefs[animal1][5])
#     attrs_animal2.add(prefs[animal2][5])
    
#     intersection = len(attrs_animal1 & attrs_animal2)
#     union = len(attrs_animal1 | attrs_animal2)
    
#     return intersection / union

# # Función para encontrar los mejores matches
# def topMatches(prefs, animal, n=3, similarity=sim_jaccard):
#     scores = [(similarity(prefs, animal, other), other) 
#                 for other in prefs if other != animal]
#     scores.sort(reverse=True)
#     return scores[0:n]

# # Función para recomendar animales
# def recomendar_animales(prefs, animal, similarity=sim_jaccard, n=3):
#     return topMatches(prefs, animal, n=n, similarity=similarity)

# # Convertir la lista de animales en un diccionario para mejor manejo
# animals_dict = {animal[0]: animal for animal in animals}



# #En tu aplicación PetPal, estos resultados pueden usarse para recomendar a los
# #usuarios mascotas que sean más similares a las que ya les gustan o han visto:
# print(recomendar_animales(animals_dict, 'THOR'))
# # devuelve[(1.0, 'TRUFO'), (0.6, 'SIMBA')]
# #'Trufo' ' es es más similar a  con una similitud del 1%

# ######################################################
# # Función para calcular la similitud entre perros basada en tipo, raza y tamaño
# def sim_perros(prefs, perro1, perro2):
#     # Obtener los atributos relevantes para la similitud
#     attrs_perro1 = set(prefs[perro1][1:4])  # Tipo, Raza, Tamaño
#     attrs_perro2 = set(prefs[perro2][1:4])  # Tipo, Raza, Tamaño

#     # Calcular la intersección y la unión de los conjuntos de atributos
#     intersection = len(attrs_perro1 & attrs_perro2)
#     union = len(attrs_perro1 | attrs_perro2)
    
#     # Calcular la similitud de Jaccard
#     if union == 0:
#         return 0
#     else:
#         return intersection / union

# # Función para encontrar los perros más similares a un perro dado
# def topPerros(prefs, perro, n=5, similarity=sim_perros):
#     scores = [(similarity(prefs, perro, otro), otro) for otro in prefs if otro != perro]
#     scores.sort(reverse=True)
#     return scores[0:n]

# # Función para recomendar perros similares a un perro dado
# def recomendar_perros(prefs, perro, similarity=sim_perros, n=3):
#     return topPerros(prefs, perro, n=n, similarity=similarity)

# # Ahora puedes usar esta función para recomendar perros según tipo, raza y tamaño
# perros = {
#     'SIMBA': ('Perro', 'Macho', 'Mestizo', 'Mediano'),
#     'THOR': ('Perro', 'Macho', 'Labrador', 'Mediano'),
#     'TRUFO': ('Perro', 'Macho', 'Border Collie', 'Grande'),
#     'BELLA': ('Perro', 'Hembra', 'Labrador', 'Mediano'),
#     'LUPI': ('Perro', 'Macho', 'Mestizo', 'Pequeño'),
#     'LUNA': ('Perro', 'Hembra', 'Border Collie', 'Grande')
# }

# # Llama a la función recomendar_perros para obtener recomendaciones para un perro específico
# perro_de_interes = 'SIMBA'
# recomendaciones = recomendar_perros(perros, perro_de_interes)

# # Imprime las recomendaciones
# print("Recomendaciones para", perro_de_interes, ":")
# for similitud, perro in recomendaciones:
#     print(f"Perro: {perro}, Similitud: {similitud}")

# #toma un perro de referencia (en este caso, "SIMBA") y 
# #encuentra los perros más similares a él en base a sus atributos de tipo, raza y tamaño. 

# #Perro: THOR, Similitud: 0.5
# #Perro: LUPI, Similitud: 0.5
# #Perro: TRUFO, Similitud: 0.2



# ##SON LO MISMO, OSEA el usuario le gusta simba, a partir de ello, busca algun animal similar a ello 



def sim_jaccard(animal1, animal2):
    attrs_animal1 = {animal1.tipo, animal1.genero, animal1.raza, animal1.tamano}
    attrs_animal2 = {animal2.tipo, animal2.genero, animal2.raza, animal2.tamano}
    
    intersection = len(attrs_animal1 & attrs_animal2)
    union = len(attrs_animal1 | attrs_animal2)
    
    return intersection / union if union != 0 else 0

def obtener_datos_animales_desde_bd():
    return Animal.objects.all()

def recomendar_animales(animal_seleccionado):
    animales = obtener_datos_animales_desde_bd()
    recomendaciones = []
    
    for animal in animales:
        if animal_seleccionado.id != animal.id:
            similitud = sim_jaccard(animal_seleccionado, animal)
            recomendaciones.append((animal, similitud))
    
    recomendaciones.sort(key=lambda x: x[1], reverse=True)
    return [recomendacion[0] for recomendacion in recomendaciones[:5]]