
import requests
import pycountry
from tqdm import tqdm

all_countries = list(pycountry.countries)
clist = []
for i in all_countries:
    clist.append(i.alpha_2)

for i in tqdm(clist):
    image_url = f"https://www.countryflags.io/{i}/flat/64.png"
    img_data = requests.get(image_url).content
    with open(f'flag-{i}.jpg', 'wb') as handler:
        handler.write(img_data)