import googlemaps
from datetime import datetime
import pprint
import os


class GeoMaps:
    """
    Class used for the API REST request to the googlemaps
    """

    def __init__(self, city, country):
        self.country = country
        self.city = city
        self.geocode_result = {}

    def get_geocode(self):
        """Method used to get the geocode coords"""
        api_key = os.environ.get("BACK_API_KEY")
        gmaps = googlemaps.Client(key=api_key)
        try:
            self.geocode_result = gmaps.geocode(
                f"{self.country},  {self.city}"
            )
            return self.geocode_result[0]["geometry"]["location"]
        except IndexError:
            return {"result": "no data found"}

    def __str__(self):
        return self.query, self.geocode_result
