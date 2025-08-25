"""Tests for quiz management functionality."""


def test_quiz_manager_can_be_created() -> None:
    """Test that QuizManager can be instantiated."""
    from africa_quiz.projection import CoordinateProjector
    from africa_quiz.quiz import QuizManager

    bbox = (-20.0, -35.0, 55.0, 37.0)
    projector = CoordinateProjector(bbox, 800, 600)
    quiz_manager = QuizManager("africa.geojson", projector)

    assert quiz_manager is not None


def test_quiz_manager_loads_countries_and_provides_current() -> None:
    """Test that QuizManager loads countries and provides current country to guess."""
    from africa_quiz.projection import CoordinateProjector
    from africa_quiz.quiz import QuizManager

    bbox = (-20.0, -35.0, 55.0, 37.0)
    projector = CoordinateProjector(bbox, 800, 600)
    quiz_manager = QuizManager("africa.geojson", projector)

    current_country = quiz_manager.get_current_country()

    # Should return a non-empty string (country name)
    assert isinstance(current_country, str)
    assert len(current_country) > 0


def test_quiz_manager_loads_actual_african_countries() -> None:
    """Test that QuizManager loads actual countries from the africa.geojson file."""
    from africa_quiz.projection import CoordinateProjector
    from africa_quiz.quiz import QuizManager

    bbox = (-20.0, -35.0, 55.0, 37.0)
    projector = CoordinateProjector(bbox, 800, 600)
    quiz_manager = QuizManager("africa.geojson", projector)

    # Get multiple countries to ensure they're from the actual data
    countries = set()
    for _ in range(10):  # Try to get different countries
        quiz_manager.start_new_round()  # This should reset and potentially change country
        country = quiz_manager.get_current_country()
        countries.add(country)

    # Should have loaded actual African countries, not just hardcoded ones
    assert len(countries) > 1  # Should get different countries due to randomization

    # Check that we loaded a reasonable number of countries (Africa has 49 in our dataset)
    total_countries = len(quiz_manager.countries)
    assert total_countries >= 40  # Should have loaded most African countries

    # Countries should be real African countries (check a few that we know are in the file)
    all_loaded_countries = set(quiz_manager.countries)
    expected_countries = {"Angola", "Egypt", "Nigeria", "South Africa", "Kenya"}
    assert len(all_loaded_countries.intersection(expected_countries)) >= 3


def test_quiz_manager_handles_click() -> None:
    """Test that QuizManager can handle click coordinates and determine correctness."""
    from africa_quiz.projection import CoordinateProjector
    from africa_quiz.quiz import QuizManager

    bbox = (-20.0, -35.0, 55.0, 37.0)
    projector = CoordinateProjector(bbox, 800, 600)
    quiz_manager = QuizManager("africa.geojson", projector)

    # Handle a click - should return (is_correct, country_clicked)
    is_correct, clicked_country = quiz_manager.handle_click(400, 300)

    assert isinstance(is_correct, bool)
    assert isinstance(clicked_country, str) or clicked_country is None


def test_quiz_manager_hit_detection_with_centroids() -> None:
    """Test hit detection using shapely centroids for reliable geometric testing."""
    import json

    from shapely.geometry import MultiPolygon, Polygon

    from africa_quiz.projection import CoordinateProjector
    from africa_quiz.quiz import QuizManager

    # Load the actual geojson to test with real data
    with open("africa.geojson") as f:
        geojson_data = json.load(f)

    bbox = CoordinateProjector.calculate_bbox(geojson_data)
    projector = CoordinateProjector(bbox, 800, 600)
    quiz_manager = QuizManager("africa.geojson", projector)

    # Test the first country with its centroid
    first_feature = geojson_data["features"][0]
    country_name = first_feature["properties"]["name"]
    coords = first_feature["geometry"]["coordinates"]

    # Create shapely geometry
    if first_feature["geometry"]["type"] == "Polygon":
        shape = Polygon(coords[0])
    else:  # MultiPolygon
        shape = MultiPolygon([Polygon(poly[0]) for poly in coords])

    # Get centroid and convert to canvas coordinates
    centroid = shape.centroid
    canvas_x, canvas_y = projector.geo_to_canvas(centroid.x, centroid.y)

    # Click on the centroid should detect this country
    is_correct, clicked_country = quiz_manager.handle_click(canvas_x, canvas_y)

    assert clicked_country == country_name
    # Whether it's correct depends on if this is the current quiz country
    assert isinstance(is_correct, bool)


def test_quiz_manager_detects_multiple_countries() -> None:
    """Test that hit detection works for multiple different countries."""
    import json

    from shapely.geometry import MultiPolygon, Polygon

    from africa_quiz.projection import CoordinateProjector
    from africa_quiz.quiz import QuizManager

    # Load the actual geojson to test with real data
    with open("africa.geojson") as f:
        geojson_data = json.load(f)

    bbox = CoordinateProjector.calculate_bbox(geojson_data)
    projector = CoordinateProjector(bbox, 800, 600)
    quiz_manager = QuizManager("africa.geojson", projector)

    # Test first three countries to ensure we're not hardcoded to just Angola
    detected_countries = set()
    for feature in geojson_data["features"][:3]:  # Test first 3
        country_name = feature["properties"]["name"]
        coords = feature["geometry"]["coordinates"]

        # Create shapely geometry
        if feature["geometry"]["type"] == "Polygon":
            shape = Polygon(coords[0])
        else:  # MultiPolygon
            shape = MultiPolygon([Polygon(poly[0]) for poly in coords])

        # Get centroid and convert to canvas coordinates
        centroid = shape.centroid
        canvas_x, canvas_y = projector.geo_to_canvas(centroid.x, centroid.y)

        # Click on the centroid should detect this country
        _is_correct, clicked_country = quiz_manager.handle_click(canvas_x, canvas_y)

        detected_countries.add(clicked_country)
        assert clicked_country == country_name

    # Should have detected 3 different countries, not all "Angola"
    assert len(detected_countries) == 3


def test_quiz_manager_round_completion() -> None:
    """Test that QuizManager can detect when a round is complete."""
    from africa_quiz.projection import CoordinateProjector
    from africa_quiz.quiz import QuizManager

    bbox = (-20.0, -35.0, 55.0, 37.0)
    projector = CoordinateProjector(bbox, 800, 600)
    quiz_manager = QuizManager("africa.geojson", projector)

    # Initially should not be complete
    assert not quiz_manager.is_round_complete()

    # After going through all countries, should be complete
    total_countries = len(quiz_manager.countries)
    quiz_manager.current_country_index = total_countries

    assert quiz_manager.is_round_complete()
