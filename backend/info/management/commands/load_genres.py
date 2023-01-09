import csv
import random

from django.core.management.base import BaseCommand
from pathlib import Path

from backend.settings import BASE_DIR
from info.models import Instrument, InstrumentCategory, Genre


data_file_path = Path('../data')

class Command(BaseCommand):
    """Genres loading into the Database."""

    def handle(self, **kwargs):
        data_path = BASE_DIR / 'data'

        with open(f'{data_path}/genres.csv', 'r', encoding='UTF-8') as file:
            reader = csv.reader(file)
            for row in reader:
                title = row[0]
                slug = '_'.join(title.lower().split())
                symbol_list = [
                    chr(i) for i in range(97, 123)
                    ] + [str(i) for i in range(1, 10)]
                color = '#'
                for i in range(6):
                    symbol = random.choice(symbol_list)
                    color += symbol
                Genre.objects.get_or_create(
                    title=title,
                    slug=slug,
                    color=color.upper()
                )
        
        self.stdout.write(self.style.SUCCESS('SUCCESS'))



        



# class Command(BaseCommand):
#     """Instrument categories and instruments loading into the Database."""

#     def handle(self, **kwargs):
#         data_path = BASE_DIR / 'data'

#         with open(
#             f'{data_path}/instrument_categories.csv', 'r', encoding='UTF-8'
#         ) as file:
#             reader = csv.reader(file, delimiter=',')
#             for row in reader:
#                 title, slug = row
#                 InstrumentCategory.objects.get_or_create(
#                     title=title,
#                     slug=slug
#                 )