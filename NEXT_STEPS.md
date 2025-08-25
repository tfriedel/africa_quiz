# Next Steps - Africa Geography Quiz Game

Based on the comprehensive code review, here are the prioritized next steps to improve the project from B+ to A-grade quality.

## 🚨 Priority 1: Critical Issues (Immediate)

### 1. Fix Code Quality Issues
```bash
# Fix all linting and formatting issues
uv run --frozen ruff check . --fix
uv run --frozen ruff format .
```

**Expected Result:** Clean up 213 linting errors and 133 formatting violations

### 2. Add Missing Type Annotations
Add return type annotations to all functions:

```python
# In all test files
def test_quiz_manager_can_be_created() -> None:
def test_coordinate_projector_converts_geo_to_canvas() -> None:

# In main.py
def __init__(self) -> None:
def draw_map(self) -> None:
def on_click(self, event) -> None:

# Complete the missing one in projection.py
def canvas_to_geo(self, x: int, y: int) -> tuple[float, float]:
```

### 3. Implement Error Handling
Add robust error handling for file operations:

```python
# In quiz.py __init__ method
try:
    with open(geojson_path) as f:
        geojson_data = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError(f"GeoJSON file not found: {geojson_path}")
except json.JSONDecodeError as e:
    raise ValueError(f"Invalid GeoJSON format: {e}")

# Validate geometry data
for feature in geojson_data["features"]:
    if not feature.get("properties", {}).get("name"):
        continue  # Skip features without names
    if feature["geometry"]["type"] not in ["Polygon", "MultiPolygon"]:
        continue  # Skip unsupported geometry types
```

### 4. Fix Hard-coded Paths
Replace hard-coded file paths with configurable paths:

```python
from pathlib import Path

class AfricaQuizApp:
    def __init__(self, geojson_path: str = "africa.geojson"):
        self.geojson_path = Path(geojson_path)
        if not self.geojson_path.exists():
            raise FileNotFoundError(f"GeoJSON file not found: {geojson_path}")
```

## ⚡ Priority 2: Architecture Improvements (Next Sprint)

### 1. Refactor Large Init Method
Break down the 74-line `__init__` method in main.py:

```python
class AfricaQuizApp:
    def __init__(self):
        self.root = tk.Tk()
        self._setup_dimensions()
        self._setup_components()
        self._setup_ui()
        self._setup_event_handlers()
        self._initialize_game_data()
    
    def _setup_dimensions(self) -> None:
        # Canvas dimension calculation logic
        
    def _setup_components(self) -> None:
        # Create projector and quiz manager
        
    def _setup_ui(self) -> None:
        # Create UI elements
        
    def _setup_event_handlers(self) -> None:
        # Bind events
        
    def _initialize_game_data(self) -> None:
        # Pre-calculate geometries
```

### 2. Create Configuration System
Add a configuration file for game settings:

```python
# config.py
from dataclasses import dataclass

@dataclass
class GameConfig:
    canvas_base_width: int = 1000
    geojson_file: str = "africa.geojson"
    font_size: int = 16
    label_font_size: int = 8
    colors: dict = None
    
    def __post_init__(self):
        if self.colors is None:
            self.colors = {
                "correct": "green",
                "incorrect": "red",
                "background": "lightblue",
                "outline": "black"
            }
```

### 3. Add Comprehensive Logging
Implement logging for debugging and monitoring:

```python
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('africa_quiz.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Use in methods
logger.info(f"Loading GeoJSON file: {geojson_path}")
logger.debug(f"Calculated canvas dimensions: {self.canvas_width}x{self.canvas_height}")
```

### 4. Implement Resource Cleanup
Add proper cleanup for memory management:

```python
def __del__(self):
    """Cleanup geometric data when app closes."""
    self.canvas_geometries.clear()
    self.quiz_manager.country_data.clear()
    logger.info("Application resources cleaned up")
```

## 🎯 Priority 3: User Experience Enhancements (Future)

### 1. Add Accessibility Features
Implement keyboard navigation and screen reader support:

```python
def _setup_accessibility(self):
    # Keyboard shortcuts
    self.root.bind('<Return>', self.skip_country)
    self.root.bind('<Escape>', self.restart_round)
    self.root.bind('<h>', self.show_help)
    
    # High contrast mode
    self.root.bind('<Alt-h>', self.toggle_high_contrast)
```

### 2. Enhanced Educational Content
Add educational information about countries:

```python
# Add country facts to display
country_facts = {
    "Nigeria": {
        "capital": "Abuja",
        "population": "218 million",
        "fun_fact": "Most populous country in Africa"
    }
}

def show_country_info(self, country_name):
    facts = self.country_facts.get(country_name, {})
    info_text = f"Capital: {facts.get('capital', 'Unknown')}\n"
    info_text += f"Population: {facts.get('population', 'Unknown')}\n"
    info_text += f"Fact: {facts.get('fun_fact', 'No fact available')}"
    # Display in UI
```

### 3. Progress Tracking System
Add score and progress tracking:

```python
class GameStats:
    def __init__(self):
        self.correct_answers = 0
        self.total_attempts = 0
        self.current_streak = 0
        self.best_streak = 0
        self.round_number = 1
    
    def record_answer(self, is_correct: bool):
        self.total_attempts += 1
        if is_correct:
            self.correct_answers += 1
            self.current_streak += 1
            self.best_streak = max(self.best_streak, self.current_streak)
        else:
            self.current_streak = 0
    
    @property
    def accuracy(self) -> float:
        return self.correct_answers / self.total_attempts if self.total_attempts > 0 else 0
```

### 4. Difficulty Levels
Implement different difficulty modes:

```python
class DifficultyLevel(Enum):
    EASY = "easy"      # Show country outlines
    MEDIUM = "medium"  # Show continent outline only
    HARD = "hard"      # No visual hints

def set_difficulty(self, level: DifficultyLevel):
    self.difficulty = level
    if level == DifficultyLevel.EASY:
        self.show_country_outlines = True
    elif level == DifficultyLevel.HARD:
        self.show_hints = False
```

## 🧪 Testing Enhancements

### 1. Add Property-Based Testing
Use hypothesis for edge case testing:

```python
from hypothesis import given, strategies as st

@given(st.floats(min_value=-180, max_value=180), 
       st.floats(min_value=-90, max_value=90))
def test_coordinate_projection_boundaries(lon: float, lat: float) -> None:
    bbox = (-20.0, -35.0, 55.0, 37.0)
    projector = CoordinateProjector(bbox, 800, 600)
    
    # Should not crash with any valid coordinates
    canvas_x, canvas_y = projector.geo_to_canvas(lon, lat)
    assert isinstance(canvas_x, int)
    assert isinstance(canvas_y, int)
```

### 2. Add Performance Tests
Test memory usage and rendering performance:

```python
def test_memory_usage_under_load() -> None:
    """Test memory usage during extended gameplay."""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    app = AfricaQuizApp()
    # Simulate 1000 clicks
    for _ in range(1000):
        event = MockEvent(random.randint(0, 800), random.randint(0, 600))
        app.on_click(event)
    
    final_memory = process.memory_info().rss
    memory_growth = final_memory - initial_memory
    
    # Memory growth should be reasonable (< 50MB)
    assert memory_growth < 50 * 1024 * 1024
```

## 📊 Success Metrics

Track these metrics to measure improvement:

- **Code Quality**: Achieve 0 linting errors
- **Type Coverage**: 100% type annotation coverage
- **Test Coverage**: Maintain 100% passing tests
- **Performance**: < 2 second startup time
- **Memory Usage**: < 100MB memory footprint
- **User Experience**: Add 5+ accessibility features

## 🗓️ Implementation Timeline

**Week 1**: Priority 1 items (Critical fixes)
**Week 2**: Priority 2 items (Architecture improvements)
**Week 3**: Priority 3 items (UX enhancements)
**Week 4**: Testing enhancements and documentation updates

## 📝 Validation Checklist

Before considering improvements complete:

- [ ] All linting errors fixed (`uv run ruff check .` returns clean)
- [ ] All functions have return type annotations
- [ ] Error handling covers file operations and data validation
- [ ] Configuration system implemented
- [ ] Logging added to key operations
- [ ] Resource cleanup implemented
- [ ] At least 3 accessibility features added
- [ ] Performance tests added
- [ ] Documentation updated to reflect changes
- [ ] All existing tests still pass

## 🎖️ Target Grade: A (90+/100)

With these improvements, the project will demonstrate:
- **Professional code quality** with clean, well-typed, documented code
- **Robust architecture** with proper error handling and resource management
- **Excellent user experience** with accessibility and educational enhancements
- **Production readiness** with logging, configuration, and performance optimization

This comprehensive improvement plan will elevate the Africa Geography Quiz Game from a good educational project to an exemplary piece of software that demonstrates best practices in educational software development.