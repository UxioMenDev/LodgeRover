import random
import requests
import time
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.conf import settings
from reservation_app.models import Room


class Command(BaseCommand):
    help = "Crea 20 alojamientos con imágenes de Unsplash"

    def add_arguments(self, parser):
        parser.add_argument(
            '--access-key',
            type=str,
            help='Unsplash Access Key',
        )

    def get_unsplash_image(self, room_number, access_key):
        """Descarga una imagen de Unsplash para la habitación"""
        search_queries = [
            'hotel room', 'luxury hotel room', 'modern hotel room',
            'cozy bedroom', 'boutique hotel', 'hotel interior'
        ]
        
        query = random.choice(search_queries)
        url = "https://api.unsplash.com/photos/random"
        params = {
            'query': query,
            'orientation': 'landscape',
            'content_filter': 'high',
            'client_id': access_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                photo_data = response.json()
                image_url = photo_data['urls']['regular']
                photo_id = photo_data['id']
                
                # Descargar la imagen
                image_response = requests.get(image_url, timeout=30)
                
                if image_response.status_code == 200:
                    filename = f"room_{room_number}_{photo_id}.jpg"
                    return ContentFile(image_response.content), filename
        except:
            pass
        
        return None, None

    def handle(self, *args, **kwargs):
        if Room.objects.exists():
            self.stdout.write(
                self.style.WARNING(
                    "Los alojamientos ya existen. No se añadieron nuevos alojamientos."
                )
            )
            return

        access_key = kwargs.get('access_key') or getattr(settings, 'UNSPLASH_ACCESS_KEY', None)
        
        if not access_key:
            self.stdout.write(
                "⚠️ No se encontró Access Key de Unsplash. Las habitaciones se crearán sin imágenes."
            )
            self.stdout.write(
                "Para añadir imágenes, usa: --access-key TU_ACCESS_KEY"
            )

        self.stdout.write("Creando 10 habitaciones...")
        
        for i in range(1, 11):
            room = Room(
                number=i,
                description=f"Alojamiento {i}",
                price=random.randint(20, 100),
                capacity=random.randint(2, 4),
            )
            
            # Intentar añadir imagen de Unsplash
            if access_key:
                image_content, filename = self.get_unsplash_image(i, access_key)
                if image_content and filename:
                    room.photo.save(filename, image_content, save=False)
                    self.stdout.write(f"✓ Habitación {i} creada con imagen")
                else:
                    self.stdout.write(f"⚠ Habitación {i} creada sin imagen")
                
                # Pausa para respetar rate limits
                time.sleep(1.2)
            else:
                self.stdout.write(f"✓ Habitación {i} creada")
            
            room.save()

        self.stdout.write(self.style.SUCCESS("¡Todas las habitaciones creadas con éxito!"))
