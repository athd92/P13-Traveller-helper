from django.core.management.base import BaseCommand, CommandError
from django.db import models
from main.models import Country
import pycountry


class Command(BaseCommand):
    help = 'Dump countries list'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Lancement du programme'))

        all_countries = list(pycountry.countries)
        clist = []
        for i in all_countries:
            clist.append(i.name[0:])

        for country in clist:
            c = Country(name=country)
            c.save()
        self.stdout.write(self.style.SUCCESS('Opération terminée: [OK]'))