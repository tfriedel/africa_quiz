"""Coordinate projection module for Africa Geography Quiz Game."""

from typing import Tuple


class CoordinateProjector:
    """Projects geographic coordinates to canvas coordinates using equirectangular projection."""

    def __init__(
        self, bbox: tuple[float, float, float, float], canvas_width: int, canvas_height: int
    ) -> None:
        """Initialize projector with bounding box and canvas dimensions.

        Args:
            bbox: (min_lon, min_lat, max_lon, max_lat) geographic bounding box
            canvas_width: Target canvas width in pixels
            canvas_height: Target canvas height in pixels
        """
        self.min_lon, self.min_lat, self.max_lon, self.max_lat = bbox
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        # Calculate scale factors
        self.lon_range = self.max_lon - self.min_lon
        self.lat_range = self.max_lat - self.min_lat
        self.x_scale = canvas_width / self.lon_range
        self.y_scale = canvas_height / self.lat_range

    def geo_to_canvas(self, lon: float, lat: float) -> tuple[int, int]:
        """Convert geographic coordinates to canvas pixel coordinates.

        Args:
            lon: Longitude in degrees
            lat: Latitude in degrees

        Returns:
            Tuple of (x, y) canvas coordinates in pixels
        """
        x = int((lon - self.min_lon) * self.x_scale)
        y = int((self.max_lat - lat) * self.y_scale)  # Flip Y axis for canvas
        return (x, y)

    def canvas_to_geo(self, x: int, y: int) -> tuple[float, float]:
        lon = (x / self.x_scale) + self.min_lon
        lat = self.max_lat - (y / self.y_scale)  # Flip Y axis back
        return (lon, lat)

    @staticmethod
    def calculate_bbox(geojson_data):
        min_lon = min_lat = float("inf")
        max_lon = max_lat = float("-inf")

        for feature in geojson_data["features"]:
            geometry = feature["geometry"]
            coords = geometry["coordinates"]

            if geometry["type"] == "Polygon":
                for ring in coords:
                    for lon, lat in ring:
                        min_lon = min(min_lon, lon)
                        max_lon = max(max_lon, lon)
                        min_lat = min(min_lat, lat)
                        max_lat = max(max_lat, lat)
            elif geometry["type"] == "MultiPolygon":
                for polygon in coords:
                    for ring in polygon:
                        for lon, lat in ring:
                            min_lon = min(min_lon, lon)
                            max_lon = max(max_lon, lon)
                            min_lat = min(min_lat, lat)
                            max_lat = max(max_lat, lat)

        return (min_lon, min_lat, max_lon, max_lat)
