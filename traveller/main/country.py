import pycountry


class Country:
    """Class used to maniuplate the initial query"""

    def get_list(self) -> list:
        """Method used to check if the country
        name exist"""
        all_countries = list(pycountry.countries)
        clist = []
        for i in all_countries:
            clist.append(i.name)
        return clist
