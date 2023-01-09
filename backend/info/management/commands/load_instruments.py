import csv

from django.core.management.base import BaseCommand
from pathlib import Path

from backend.settings import BASE_DIR
from info.models import Instrument, InstrumentCategory


data_file_path = Path('../data')


class Command(BaseCommand):
    """Instrument categories and instruments loading into Database."""

    def handle(self, **kwargs):
        data_path = BASE_DIR / 'data'

        with open(
            f'{data_path}/instrument_categories.csv', 'r', encoding='UTF-8'
        ) as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                title, slug = row
                InstrumentCategory.objects.get_or_create(
                    title=title,
                    slug=slug
                )
        
        with open(
            f'{data_path}/instruments.csv', 'r', encoding='UTF-8'
        ) as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                title, category = row
                category = InstrumentCategory.objects.get(title=category)
                Instrument.objects.get_or_create(
                    title=title,
                    category=category
                )

        self.stdout.write(self.style.SUCCESS('SUCCESS'))

