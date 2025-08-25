"""Tests for coordinate projection functionality."""

import json


def test_coordinate_projector_can_be_created():
    """Test that CoordinateProjector can be instantiated."""
    from africa_quiz.projection import CoordinateProjector

    bbox = (-20.0, -35.0, 55.0, 37.0)  # Example Africa bounding box
    projector = CoordinateProjector(bbox, 800, 600)

    assert projector is not None


def test_coordinate_projector_converts_geo_to_canvas():
    """Test that geographic coordinates can be converted to canvas coordinates."""
    from africa_quiz.projection import CoordinateProjector

    bbox = (-20.0, -35.0, 55.0, 37.0)  # (min_lon, min_lat, max_lon, max_lat)
    projector = CoordinateProjector(bbox, 800, 600)

    # Test corner coordinates
    x, y = projector.geo_to_canvas(-20.0, 37.0)  # Top-left corner
    assert x == 0
    assert y == 0


def test_calculate_bbox_from_africa_geojson():
    """Test that bounding box calculation works with actual Africa GeoJSON data."""
    from africa_quiz.projection import CoordinateProjector

    with open("africa.geojson") as f:
        africa_data = json.load(f)

    bbox = CoordinateProjector.calculate_bbox(africa_data)

    # Africa roughly spans these coordinates
    min_lon, min_lat, max_lon, max_lat = bbox
    assert min_lon < -10  # Western edge around Senegal
    assert max_lon > 50  # Eastern edge around Somalia
    assert min_lat < -30  # Southern edge around South Africa
    assert max_lat > 30  # Northern edge around Egypt


def test_calculate_bbox_with_simple_geojson():
    """Test bounding box calculation with a simple test case."""
    from africa_quiz.projection import CoordinateProjector

    test_data = {
        "features": [
            {
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [[0.0, 0.0], [10.0, 0.0], [10.0, 10.0], [0.0, 10.0], [0.0, 0.0]]
                    ],
                }
            }
        ]
    }

    bbox = CoordinateProjector.calculate_bbox(test_data)
    min_lon, min_lat, max_lon, max_lat = bbox

    assert min_lon == 0.0
    assert min_lat == 0.0
    assert max_lon == 10.0
    assert max_lat == 10.0


def test_calculate_bbox_with_multipolygon():
    """Test bounding box calculation with MultiPolygon geometry."""
    from africa_quiz.projection import CoordinateProjector

    test_data = {
        "features": [
            {
                "geometry": {
                    "type": "MultiPolygon",
                    "coordinates": [
                        [[[0.0, 0.0], [5.0, 0.0], [5.0, 5.0], [0.0, 5.0], [0.0, 0.0]]],
                        [[[10.0, 10.0], [15.0, 10.0], [15.0, 15.0], [10.0, 15.0], [10.0, 10.0]]],
                    ],
                }
            }
        ]
    }

    bbox = CoordinateProjector.calculate_bbox(test_data)
    min_lon, min_lat, max_lon, max_lat = bbox

    assert min_lon == 0.0
    assert min_lat == 0.0
    assert max_lon == 15.0
    assert max_lat == 15.0


def test_coordinate_projector_reverse_conversion():
    """Test that canvas coordinates can be converted back to geographic coordinates."""
    from africa_quiz.projection import CoordinateProjector

    bbox = (-20.0, -35.0, 55.0, 37.0)  # (min_lon, min_lat, max_lon, max_lat)
    projector = CoordinateProjector(bbox, 800, 600)

    # Test reverse conversion of corner coordinates
    lon, lat = projector.canvas_to_geo(0, 0)  # Should be top-left corner
    assert abs(lon - (-20.0)) < 0.1  # Allow small floating point error
    assert abs(lat - 37.0) < 0.1
