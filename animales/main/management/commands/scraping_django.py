from main.management.commands.scraping.scraping import extraer_datos_principal
from main.models import Animal
from django.core.management.base import BaseCommand, CommandError

import sys

# sys.path.append('/ruta/al/directorio/que/contiene/scraping')

def almacenar_datos():
    datos = extraer_datos_principal()
    for animal in datos:
        edad = animal[4]  
        if edad is not None:
            Animal.objects.create(
                nombre=animal[0],
                tipo=animal[1],
                genero=animal[2],
                raza=animal[3],
                edad=edad,
                tamano=animal[5],
                url_foto=animal[6],
                url_detalle=animal[7]
            )

class Command(BaseCommand):
    
    help = 'Populates the database with Animal data.'
    
    def handle(self, *args, **options):
        # print(sys.path[0])
        almacenar_datos()
        self.stdout.write(self.style.SUCCESS('Database populated successfully'))