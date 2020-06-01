from django.core.management.base import BaseCommand, CommandError
from django.db import models
from main.models import Country
import pycountry
from tqdm import tqdm
import wikipedia


class Command(BaseCommand):
    help = "Dump countries list"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Lancement du programme"))

        all_countries = list(pycountry.countries)
        clist = []

        for i in all_countries:
            clist.append(i)

        for country in tqdm(clist):
            try:
                country_resume = wikipedia.summary(country.name, sentences=1)
            except:
                country_resume = 'No resume avaible for now...'
                
            c = Country(
                name=country.name,
                alpha_2=country.alpha_2,
                flag=f"../static/img/flags/flag-{country.alpha_2}.jpg",
                resume=country_resume,
            )
            c.save()
        self.stdout.write(self.style.SUCCESS("Opération terminée: [OK]"))
