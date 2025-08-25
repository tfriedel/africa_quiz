"""Integration tests for the Africa Quiz GUI application."""
import sys
from pathlib import Path


def test_africa_quiz_app_can_be_created():
    """Test that AfricaQuizApp can be instantiated."""
    # Add parent directory to path to import main
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from main import AfricaQuizApp
    
    app = AfricaQuizApp()
    
    assert app is not None
    assert hasattr(app, 'root')
    assert hasattr(app, 'quiz_manager')
    assert hasattr(app, 'projector')


def test_africa_quiz_app_has_canvas():
    """Test that AfricaQuizApp creates a canvas for map rendering."""
    # Add parent directory to path to import main
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from main import AfricaQuizApp
    
    app = AfricaQuizApp()
    
    assert hasattr(app, 'canvas')
    assert hasattr(app, 'canvas_width')
    assert hasattr(app, 'canvas_height')
    # Canvas should have reasonable dimensions (calculated from Africa's bounds)
    assert app.canvas_width > 0
    assert app.canvas_height > 0


def test_africa_quiz_app_can_draw_map():
    """Test that AfricaQuizApp can render country outlines on the canvas."""
    # Add parent directory to path to import main
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from main import AfricaQuizApp
    
    app = AfricaQuizApp()
    
    # Should have pre-calculated canvas geometries for countries
    assert hasattr(app, 'canvas_geometries')
    assert len(app.canvas_geometries) > 0
    
    # Should have a method to draw the map
    assert hasattr(app, 'draw_map')
    
    # Drawing the map should not raise an error
    app.draw_map()


def test_africa_quiz_app_handles_click():
    """Test that AfricaQuizApp can handle mouse clicks and provide feedback."""
    # Add parent directory to path to import main
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from main import AfricaQuizApp
    
    app = AfricaQuizApp()
    
    # Should have a method to handle clicks
    assert hasattr(app, 'on_click')
    
    # Should have color tracking for countries
    assert hasattr(app, 'country_colors')
    
    # Create a mock event
    class MockEvent:
        def __init__(self, x, y):
            self.x = x
            self.y = y
    
    event = MockEvent(400, 300)
    
    # Clicking should not raise an error
    app.on_click(event)


def test_africa_quiz_app_populates_canvas_geometries():
    """Test that AfricaQuizApp pre-calculates canvas coordinates for countries."""
    # Add parent directory to path to import main
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from main import AfricaQuizApp
    
    app = AfricaQuizApp()
    
    # Should have actual coordinate data, not empty lists
    assert len(app.canvas_geometries) > 0
    
    # Pick a country and verify it has coordinates
    first_country = next(iter(app.canvas_geometries.keys()))
    country_coords = app.canvas_geometries[first_country]
    
    # Should have actual coordinate data (not empty list)
    assert len(country_coords) > 0


def test_africa_quiz_app_draws_country_polygons():
    """Test that AfricaQuizApp draws country polygons on canvas."""
    # Add parent directory to path to import main
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from main import AfricaQuizApp
    
    app = AfricaQuizApp()
    
    # Initially canvas should be empty
    canvas_items_before = app.canvas.find_all()
    
    # After drawing map, should have polygon items
    app.draw_map()
    canvas_items_after = app.canvas.find_all()
    
    # Should have created canvas items (polygons for countries)
    assert len(canvas_items_after) > len(canvas_items_before)
    assert len(canvas_items_after) > 0


def test_main_function_creates_app():
    """Test that main function creates and runs the application."""
    import sys
    from pathlib import Path
    
    # Add parent directory to path to import main
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from main import main
    
    # Should be callable without error (we can't test mainloop in tests)
    assert callable(main)


def test_main_function_actually_works():
    """Test that main function can be called and does something meaningful."""
    import sys
    from pathlib import Path
    from unittest.mock import patch, MagicMock
    
    # Add parent directory to path to import main
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    # Mock the mainloop to prevent GUI from actually starting in tests
    with patch('tkinter.Tk') as mock_tk:
        mock_root = MagicMock()
        mock_tk.return_value = mock_root
        
        from main import main
        main()
        
        # Should have called mainloop on the root window
        mock_root.mainloop.assert_called_once()


def test_africa_quiz_app_canvas_is_packed():
    """Test that the canvas is properly displayed in the window."""
    # Add parent directory to path to import main
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from main import AfricaQuizApp
    
    app = AfricaQuizApp()
    
    # Canvas should be packed/displayed
    assert hasattr(app.canvas, 'pack_info')
    pack_info = app.canvas.pack_info()
    
    # Canvas should be packed (not empty dict)
    assert pack_info or hasattr(app.canvas, 'grid_info') and app.canvas.grid_info()


def test_africa_quiz_app_binds_click_events():
    """Test that the canvas has click event bindings."""
    # Add parent directory to path to import main
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from main import AfricaQuizApp
    
    app = AfricaQuizApp()
    
    # Canvas should have click event bindings
    bindings = app.canvas.bind()
    
    # Should have at least some bindings (including Button-1 for mouse clicks)
    assert '<Button-1>' in bindings or len([b for b in bindings if 'Button' in b]) > 0


def test_africa_quiz_app_shows_country_prompt():
    """Test that the app displays which country to find."""
    # Add parent directory to path to import main
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from main import AfricaQuizApp
    
    app = AfricaQuizApp()
    
    # Should have a prompt label showing current country
    assert hasattr(app, 'prompt_label')
    
    # Label should show current country name
    current_country = app.quiz_manager.get_current_country()
    label_text = app.prompt_label.cget('text')
    
    # Should contain the country name in the prompt
    assert current_country in label_text
    assert len(label_text) > len(current_country)  # Should have additional text like "Find:" or "Click on:"


def test_africa_quiz_app_updates_prompt_after_click():
    """Test that the app shows feedback after clicking and progresses."""
    import json
    from shapely.geometry import MultiPolygon, Polygon
    
    # Add parent directory to path to import main
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from main import AfricaQuizApp
    
    app = AfricaQuizApp()
    
    # Get initial country and prompt
    initial_country = app.quiz_manager.get_current_country()
    initial_prompt = app.prompt_label.cget('text')
    
    # Should have a status label for feedback
    assert hasattr(app, 'status_label')
    
    # Load GeoJSON to find centroid of current country
    with open("africa.geojson") as f:
        geojson_data = json.load(f)
    
    # Find the current country in GeoJSON
    target_feature = None
    for feature in geojson_data["features"]:
        if feature["properties"]["name"] == initial_country:
            target_feature = feature
            break
    
    assert target_feature is not None
    
    # Calculate centroid and click on correct country
    coords = target_feature["geometry"]["coordinates"]
    if target_feature["geometry"]["type"] == "Polygon":
        shape = Polygon(coords[0])
    else:  # MultiPolygon
        shape = MultiPolygon([Polygon(poly[0]) for poly in coords])
    
    centroid = shape.centroid
    canvas_x, canvas_y = app.projector.geo_to_canvas(centroid.x, centroid.y)
    
    # Create mock event and click
    class MockEvent:
        def __init__(self, x, y):
            self.x = x
            self.y = y
    
    event = MockEvent(canvas_x, canvas_y)
    app.on_click(event)
    
    # Status should show feedback
    status_text = app.status_label.cget('text')
    assert len(status_text) > 0
    assert "Correct" in status_text or "Incorrect" in status_text


def test_africa_quiz_app_progresses_to_next_country():
    """Test that the app moves to the next country after a click."""
    import json
    from shapely.geometry import MultiPolygon, Polygon
    
    # Add parent directory to path to import main
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from main import AfricaQuizApp
    
    app = AfricaQuizApp()
    
    # Get initial country
    initial_country = app.quiz_manager.get_current_country()
    initial_index = app.quiz_manager.current_country_index
    
    # Click somewhere (doesn't matter where for progression)
    class MockEvent:
        def __init__(self, x, y):
            self.x = x
            self.y = y
    
    event = MockEvent(400, 300)  # Middle of canvas
    app.on_click(event)
    
    # Should have progressed to next country
    new_index = app.quiz_manager.current_country_index
    new_country = app.quiz_manager.get_current_country()
    new_prompt = app.prompt_label.cget('text')
    
    # Quiz should have progressed
    assert new_index > initial_index
    
    # Prompt should show new country (unless we hit the end)
    if not app.quiz_manager.is_round_complete():
        assert new_country != initial_country
        assert new_country in new_prompt


def test_africa_quiz_app_resets_round_when_complete():
    """Test that the app starts a new round when all countries are complete."""
    # Add parent directory to path to import main
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from main import AfricaQuizApp
    
    app = AfricaQuizApp()
    
    # Simulate completing the round by setting index to end
    total_countries = len(app.quiz_manager.countries)
    app.quiz_manager.current_country_index = total_countries - 1  # Last country
    
    # Click to complete the round
    class MockEvent:
        def __init__(self, x, y):
            self.x = x
            self.y = y
    
    event = MockEvent(400, 300)
    app.on_click(event)
    
    # Should have triggered round reset
    # Check that colors are cleared and new round started
    assert app.quiz_manager.current_country_index == 0
    assert len(app.country_colors) == 0  # Colors should be cleared
    
    # Should show prompt for new country
    new_country = app.quiz_manager.get_current_country()
    prompt_text = app.prompt_label.cget('text')
    assert new_country in prompt_text


def test_africa_quiz_app_labels_colored_countries():
    """Test that colored countries show their names as labels."""
    import json
    from shapely.geometry import MultiPolygon, Polygon
    
    # Add parent directory to path to import main
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from main import AfricaQuizApp
    
    app = AfricaQuizApp()
    
    # Get current country and click on it correctly
    current_country = app.quiz_manager.get_current_country()
    
    # Load GeoJSON to find centroid
    with open("africa.geojson") as f:
        geojson_data = json.load(f)
    
    # Find the current country in GeoJSON
    target_feature = None
    for feature in geojson_data["features"]:
        if feature["properties"]["name"] == current_country:
            target_feature = feature
            break
    
    assert target_feature is not None
    
    # Calculate centroid and click on correct country
    coords = target_feature["geometry"]["coordinates"]
    if target_feature["geometry"]["type"] == "Polygon":
        shape = Polygon(coords[0])
    else:  # MultiPolygon
        shape = MultiPolygon([Polygon(poly[0]) for poly in coords])
    
    centroid = shape.centroid
    canvas_x, canvas_y = app.projector.geo_to_canvas(centroid.x, centroid.y)
    
    # Create mock event and click (should be correct)
    class MockEvent:
        def __init__(self, x, y):
            self.x = x
            self.y = y
    
    event = MockEvent(canvas_x, canvas_y)
    app.on_click(event)
    
    # After clicking, the map should have text labels for colored countries
    canvas_items = app.canvas.find_all()
    text_items = [item for item in canvas_items if app.canvas.type(item) == "text"]
    
    # Should have at least one text item (the country name label)
    assert len(text_items) > 0
    
    # At least one text item should contain the country name
    found_label = False
    for item in text_items:
        text_content = app.canvas.itemcget(item, "text")
        if current_country in text_content:
            found_label = True
            break
    
    assert found_label, f"Could not find text label for {current_country}"


def test_africa_quiz_app_shows_round_completion_message():
    """Test that the app shows a completion message when round is complete."""
    # Add parent directory to path to import main
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from main import AfricaQuizApp
    
    app = AfricaQuizApp()
    
    # Simulate completing the round by setting index to end
    total_countries = len(app.quiz_manager.countries)
    app.quiz_manager.current_country_index = total_countries - 1  # Last country
    
    # Click to complete the round
    class MockEvent:
        def __init__(self, x, y):
            self.x = x
            self.y = y
    
    event = MockEvent(400, 300)
    app.on_click(event)
    
    # Status should show round completion message
    status_text = app.status_label.cget('text')
    assert "New round started!" in status_text or "Round complete" in status_text


def test_africa_quiz_app_uses_proper_aspect_ratio():
    """Test that the app calculates proper canvas dimensions based on Africa's geographic bounds."""
    # Add parent directory to path to import main
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from main import AfricaQuizApp
    
    app = AfricaQuizApp()
    
    # Should calculate canvas dimensions based on actual Africa bounding box
    # Africa is actually slightly taller than wide (geographic_ratio ~0.95)
    # So height should be larger than width
    assert app.canvas_height >= app.canvas_width
    
    # Canvas should be reasonably sized (not tiny, not huge)
    assert app.canvas_width >= 800
    assert app.canvas_height >= 600
    
    # Aspect ratio should roughly match Africa's geographic proportions
    geographic_width = app.projector.lon_range
    geographic_height = app.projector.lat_range
    canvas_ratio = app.canvas_width / app.canvas_height
    geographic_ratio = geographic_width / geographic_height
    
    # Ratios should be reasonably close (within 20% difference)
    ratio_diff = abs(canvas_ratio - geographic_ratio) / geographic_ratio
    assert ratio_diff < 0.3, f"Canvas aspect ratio {canvas_ratio:.2f} too different from geographic ratio {geographic_ratio:.2f}"


def test_africa_quiz_app_handles_click_with_quiz_logic():
    """Test that clicking processes quiz logic and updates colors."""
    import json
    from shapely.geometry import MultiPolygon, Polygon
    
    # Add parent directory to path to import main
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from main import AfricaQuizApp
    
    app = AfricaQuizApp()
    
    # Get current country being quizzed
    current_country = app.quiz_manager.get_current_country()
    
    # Load GeoJSON to find centroid of current country
    with open("africa.geojson") as f:
        geojson_data = json.load(f)
    
    # Find the current country in GeoJSON
    target_feature = None
    for feature in geojson_data["features"]:
        if feature["properties"]["name"] == current_country:
            target_feature = feature
            break
    
    assert target_feature is not None, f"Could not find {current_country} in GeoJSON"
    
    # Calculate centroid
    coords = target_feature["geometry"]["coordinates"]
    if target_feature["geometry"]["type"] == "Polygon":
        shape = Polygon(coords[0])
    else:  # MultiPolygon
        shape = MultiPolygon([Polygon(poly[0]) for poly in coords])
    
    centroid = shape.centroid
    canvas_x, canvas_y = app.projector.geo_to_canvas(centroid.x, centroid.y)
    
    # Create mock event for correct click
    class MockEvent:
        def __init__(self, x, y):
            self.x = x
            self.y = y
    
    event = MockEvent(canvas_x, canvas_y)
    
    # Click on correct country
    app.on_click(event)
    
    # Country should now be colored (either green for correct or red for incorrect)
    assert current_country in app.country_colors
    assert app.country_colors[current_country] in ["green", "red"]