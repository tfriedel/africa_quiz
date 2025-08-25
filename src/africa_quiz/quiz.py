import json
import random

from shapely.geometry import MultiPolygon, Point, Polygon


class QuizManager:
    def __init__(self, geojson_path, projector):
        self.projector = projector
        self.countries = []  # List of country names for quiz order
        self.country_data = {}  # Dict mapping country names to geometric data
        self.current_country_index = 0

        # Load countries from GeoJSON file
        with open(geojson_path) as f:
            geojson_data = json.load(f)

        for feature in geojson_data["features"]:
            country_name = feature["properties"]["name"]
            coords = feature["geometry"]["coordinates"]

            # Create shapely geometry
            if feature["geometry"]["type"] == "Polygon":
                geo_geometry = Polygon(coords[0])
            elif feature["geometry"]["type"] == "MultiPolygon":
                geo_geometry = MultiPolygon([Polygon(poly[0]) for poly in coords])
            else:
                continue  # Skip unsupported geometry types

            self.countries.append(country_name)
            self.country_data[country_name] = geo_geometry

        # Start with a shuffled list
        self.start_new_round()

    def get_current_country(self):
        if not self.countries:
            return "No countries loaded"
        return self.countries[self.current_country_index]

    def start_new_round(self):
        if self.countries:
            random.shuffle(self.countries)
            self.current_country_index = 0

    def handle_click(self, x, y):
        # Convert canvas coordinates to geographic coordinates
        lon, lat = self.projector.canvas_to_geo(x, y)
        point = Point(lon, lat)

        # Test against all countries
        for country_name, geo_geometry in self.country_data.items():
            if geo_geometry.contains(point):
                current_country = self.get_current_country()
                is_correct = country_name == current_country
                return (is_correct, country_name)

        return (False, None)  # Ocean click

    def is_round_complete(self):
        return self.current_country_index >= len(self.countries)
