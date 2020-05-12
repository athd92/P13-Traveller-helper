import pycountry


all_countries = list(pycountry.countries)
clist = []
for i in all_countries:
    clist.append(i.name)
print(clist)

for i in clist:
    if i == 'France':
        print('OK')
    else:
        pass