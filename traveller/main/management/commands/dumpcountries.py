from django.core.management.base import BaseCommand, CommandError
from django.db import models
from main.models import Country
import pycountry
from tqdm import tqdm
import wikipedia
import pandas as pd
from .temperatures import TempClass
import time
import base64
import os
import requests
from django.core import files
from io import BytesIO


class Command(BaseCommand):
    """Dump datas for initial database"""

    help = "Dump countries list"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Lancement du programme"))
        self.key = key = os.environ.get("UNSPLASH_KEY")

        all_countries = list(pycountry.countries)
        clist = []
        temp_dict = TempClass()
        temp_dict = temp_dict.get_datas()
        for i in all_countries:
            clist.append(i)
        for country in tqdm(clist):
            time.sleep(3)

            try:
                country_resume = wikipedia.summary(country.name, sentences=1)
            except:
                country_resume = "No resume avaible for now..."
            try:
                query = country.name.lower()
                url = f"https://unsplash.com/napi/search?query={country.name}&xp=&per_page=1"
                headers = {"authorization": f"Client-ID {self.key}"}
                response = requests.get(url, headers=headers)
                urls = []
                resp = response.json()
                for img in resp["photos"]["results"]:
                    try:
                        urls.append((img.get("urls")["small"]))
                    except:
                        try:
                            urls.append((img.get("urls")["thumbnail"]))
                        except:
                            urls.append((img.get("urls")["raw"]))

                response = requests.get(urls[0])
                pic = (
                    "data:"
                    + response.headers["Content-Type"]
                    + ";"
                    + "base64,"
                    + base64.b64encode(response.content).decode("utf-8")
                )
            except:
                self.stdout.write(self.style.WARNING("WARNING NOT FOUND IMAGE"))
                pic = "No image found"

            if country.alpha_3 in temp_dict:
                c = Country(
                    name=country.name,
                    alpha_2=country.alpha_2,
                    alpha_3=country.alpha_3,
                    temp_averges=temp_dict[country.alpha_3],
                    flag=f"../static/img/flags/flag-{country.alpha_2}.jpg",
                    resume=country_resume,
                    picture=pic,
                )
                c.save()
                a = self.style.WARNING(f"{country.name}")
                b = self.style.SUCCESS(" [OK] ")
                self.stdout.write(a + b)
        self.stdout.write(self.style.SUCCESS("Opération terminée: [OK]"))
