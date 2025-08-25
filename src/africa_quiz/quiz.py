import json
import random

from shapely.geometry import MultiPolygon, Point, Polygon

from .projection import CoordinateProjector


class QuizManager:
    def __init__(self, geojson_path: str, projector: CoordinateProjector) -> None:
        self.projector = projector
        self.countries = []  # List of country names for quiz order
        self.country_data = {}  # Dict mapping country names to geometric data
        self.current_country_index = 0

        # Load countries from GeoJSON file with comprehensive error handling
        try:
            with open(geojson_path) as f:
                geojson_data = json.load(f)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"GeoJSON file not found: {geojson_path}") from e
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid GeoJSON format: {e}") from e
        except PermissionError as e:
            raise PermissionError(
                f"Permission denied accessing GeoJSON file: {geojson_path}"
            ) from e
        except Exception as e:
            raise RuntimeError(f"Unexpected error loading GeoJSON file {geojson_path}: {e}") from e

        # Validate GeoJSON structure
        if not isinstance(geojson_data, dict) or "features" not in geojson_data:
            raise ValueError("Invalid GeoJSON format: missing 'features' key")

        if not isinstance(geojson_data["features"], list):
            raise ValueError("Invalid GeoJSON format: 'features' must be a list")

        for feature in geojson_data["features"]:
            # Validate feature structure
            if not isinstance(feature, dict):
                continue  # Skip malformed features

            properties = feature.get("properties", {})
            geometry = feature.get("geometry", {})

            # Skip features without required properties
            if not properties.get("name"):
                continue  # Skip features without names

            country_name = properties["name"]
            coords = geometry.get("coordinates")
            geometry_type = geometry.get("type")

            if not coords or geometry_type not in ["Polygon", "MultiPolygon"]:
                continue  # Skip unsupported or malformed geometry types

            try:
                # Create shapely geometry
                if geometry_type == "Polygon":
                    geo_geometry = Polygon(coords[0])
                elif geometry_type == "MultiPolygon":
                    geo_geometry = MultiPolygon([Polygon(poly[0]) for poly in coords])

                # Validate geometry
                if not geo_geometry.is_valid:
                    continue  # Skip invalid geometries

                self.countries.append(country_name)
                self.country_data[country_name] = geo_geometry

            except Exception:
                # Skip countries with geometry processing errors
                continue

        # Validate that we loaded some countries
        if not self.countries:
            raise ValueError(f"No valid countries found in GeoJSON file: {geojson_path}")

        # Start with a shuffled list
        self.start_new_round()

    def get_current_country(self) -> str:
        if not self.countries:
            return "No countries loaded"
        return self.countries[self.current_country_index]

    def start_new_round(self) -> None:
        if self.countries:
            random.shuffle(self.countries)
            self.current_country_index = 0

    def handle_click(self, x: int, y: int) -> tuple[bool, str | None]:
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

    def is_round_complete(self) -> bool:
        return self.current_country_index >= len(self.countries)
