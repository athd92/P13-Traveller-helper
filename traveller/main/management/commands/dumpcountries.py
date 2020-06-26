from django.core.management.base import BaseCommand, CommandError
from django.db import models
from main.models import Country
import pycountry
from tqdm import tqdm
import wikipedia
import pandas as pd
from .temperatures import TempClass


class Command(BaseCommand):
    help = "Dump countries list"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Lancement du programme"))

        all_countries = list(pycountry.countries)
        clist = []
        temp_dict = TempClass()
        temp_dict = temp_dict.get_datas()
        print(temp_dict)
        for i in all_countries:
            clist.append(i)

        for country in tqdm(clist):            
            try:
                country_resume = wikipedia.summary(country.name, sentences=1)
            except:
                country_resume = "No resume avaible for now..."
            if country.alpha_3 in temp_dict:
                c = Country(
                    name=country.name,
                    alpha_2=country.alpha_2,
                    alpha_3=country.alpha_3,
                    temp_averges=temp_dict[country.alpha_3],
                    flag=f"../static/img/flags/flag-{country.alpha_2}.jpg",
                    resume=country_resume,
                )
                c.save()
        self.stdout.write(self.style.SUCCESS("Opération terminée: [OK]"))
