# Africa Geography Quiz Game - Implementation Plan

This document provides a detailed implementation plan for the Africa Geography Quiz Game as specified in DESIGN.md.

## Project Overview

A desktop quiz application built with Python/tkinter where users identify African countries by clicking on a borderless map. The game provides immediate visual feedback, tracks progress through all countries, and runs indefinitely with new rounds.

## Implementation Phases

### Phase 1: Project Setup (30 minutes)

#### 1.1 Environment Setup
- Initialize Python project using `uv`
- Install core dependencies:
  - `uv add tkinter` (GUI framework)
  - `uv add shapely` (geometric operations)
  - `uv add pytest` (testing framework)
- Configure development tools:
  - Set up ruff for formatting and linting
  - Configure pytest for unit testing

#### 1.2 Project Structure
```
africa_quiz/
├── main.py              # Application entry point
├── quiz.py              # QuizManager class
├── projection.py        # CoordinateProjector class
├── africa.geojson       # Geographic data
├── tests/
│   ├── __init__.py
│   ├── test_projection.py
│   ├── test_quiz.py
│   └── test_integration.py
├── pyproject.toml       # Project configuration
└── CLAUDE.md           # Development guidelines
```

#### 1.3 Data Acquisition
- Source africa.geojson file containing African country polygons
- Validate GeoJSON format and completeness
- Place in project root directory

### Phase 2: Coordinate Projection System (1 hour)

#### 2.1 CoordinateProjector Class (`projection.py`)
Core component for converting geographic coordinates to screen coordinates.

**Key Methods:**
- `__init__(bbox: tuple, canvas_width: int, canvas_height: int)`
- `geo_to_canvas(lon: float, lat: float) -> tuple[int, int]`
- `project_polygon(coords: list) -> list[tuple[int, int]]`
- `calculate_bbox(geojson_data: dict) -> tuple[float, float, float, float]`

**Implementation Details:**
- Use equirectangular projection (linear scaling)
- Calculate scale factors based on bounding box
- Handle coordinate system conversion (lon/lat to x/y)
- Maintain aspect ratio of geographic data

#### 2.2 Testing Strategy
- Test projection accuracy with known coordinates
- Verify bounding box calculations
- Test edge cases (poles, date line)
- Validate coordinate transformation reversibility

### Phase 3: Data Loading & Processing (1 hour)

#### 3.1 Country Data Structure
```python
@dataclass
class Country:
    name: str
    geo_geometry: Union[Polygon, MultiPolygon]
    canvas_geometry: list[list[tuple[int, int]]]
    is_colored: bool = False
    color: str = ""
```

#### 3.2 GeoJSON Processing
- Load and parse africa.geojson file
- Extract country names and geometries
- Convert to shapely geometric objects
- Pre-calculate all canvas coordinates
- Handle MultiPolygon countries (island nations)

#### 3.3 Error Handling
- Graceful handling of missing/corrupt GeoJSON
- Validation of required properties
- User-friendly error messages
- Application termination for fatal errors

### Phase 4: Quiz Logic (2 hours)

#### 4.1 QuizManager Class (`quiz.py`)
Central component managing quiz state and logic.

**Core Methods:**
- `__init__(geojson_path: str, projector: CoordinateProjector)`
- `start_new_round() -> None`
- `get_current_country() -> str`
- `handle_click(x: int, y: int) -> tuple[bool, str]`
- `is_round_complete() -> bool`
- `reset_round() -> None`

#### 4.2 Quiz State Management
- Maintain list of countries for current round
- Track which countries have been guessed
- Shuffle country order for each round
- Prevent repetition within rounds

#### 4.3 Hit Detection Logic
- Use shapely's `contains()` for point-in-polygon testing
- Handle MultiPolygon countries correctly
- Distinguish between country hits and ocean clicks
- Return hit country name or None

#### 4.4 Answer Processing
- Compare clicked country with target country
- Update country visual state (color, label)
- Progress to next country automatically
- Handle round completion and reset

### Phase 5: GUI Implementation (2 hours)

#### 5.1 Main Application Window (`main.py`)
- Create fixed-size tkinter window (non-resizable)
- Initialize canvas for map rendering
- Set up event bindings for mouse clicks
- Manage main application loop

#### 5.2 Map Rendering
- Draw country outlines using canvas polygons
- Render countries in default state (outline only)
- Handle polygon filling for correct/incorrect answers
- Display country names within colored regions

#### 5.3 Visual Feedback System
- **Correct Answer**: Fill country with solid green (#00FF00)
- **Incorrect Answer**: Fill target country with solid red (#FF0000)
- **Country Labels**: Display country names in colored regions
- **Cumulative Display**: Maintain all colors throughout round

#### 5.4 User Interface Flow
```
1. Display map with country outlines
2. Show country name prompt
3. Wait for user click
4. Process click coordinates
5. Provide visual feedback
6. Update country display
7. Progress to next country or reset round
8. Repeat indefinitely
```

### Phase 6: Testing & Polish (1 hour)

#### 6.1 Comprehensive Test Suite

**Test Categories:**
1. **Geometric Tests** (`test_projection.py`)
   - Coordinate projection accuracy
   - Bounding box calculations
   - Edge case handling

2. **Quiz Logic Tests** (`test_quiz.py`)
   - Country selection randomization
   - Hit detection accuracy
   - Round progression logic
   - State management

3. **Integration Tests** (`test_integration.py`)
   - End-to-end click processing
   - GeoJSON loading and parsing
   - Complete round simulation

#### 6.2 Test Implementation Strategy
- Use pytest fixtures for shared test data
- Import CoordinateProjector from production code
- Test with actual africa.geojson data
- Use shapely centroids for reliable hit testing
- Test multi-polygon countries separately

#### 6.3 Performance Optimization
- Pre-calculate all coordinate projections at startup
- Cache geometric objects in memory
- Optimize canvas drawing operations
- Profile hit detection performance

## Technical Specifications

### Dependencies
```toml
[dependencies]
python = "^3.11"
shapely = "^2.0.0"

[dev-dependencies]
pytest = "^7.0.0"
ruff = "^0.1.0"
```

### Canvas Specifications
- Fixed window size (to be determined based on Africa's aspect ratio)
- Non-resizable window
- Canvas coordinates matching CoordinateProjector output

### File Handling
- Relative path loading for africa.geojson
- Graceful error handling for missing files
- JSON parsing with appropriate error messages

### Color Scheme
- Default country outline: Black (#000000)
- Correct answer: Green fill (#00FF00)
- Incorrect answer: Red fill (#FF0000)
- Country labels: Black text on colored background

## Development Workflow

### Test-Driven Development
1. Write failing test for specific functionality
2. Implement minimal code to pass test
3. Refactor for clarity and performance
4. Repeat for next feature

### Quality Assurance
- Run `uv run --frozen pytest` for all tests
- Use `uv run --frozen ruff format .` for code formatting
- Execute `uv run --frozen ruff check .` for linting
- Maintain >90% test coverage for core logic

### Critical Testing Points
- Point-in-polygon accuracy with centroids
- Multi-polygon country handling
- Coordinate projection precision
- Round progression and reset logic
- Error handling for corrupt data

## Success Criteria

### Functional Requirements Met
- ✅ Display borderless Africa map
- ✅ Random country prompting
- ✅ Click-based user interaction
- ✅ Accurate hit detection
- ✅ Visual feedback (green/red coloring)
- ✅ Country name labeling
- ✅ Cumulative round display
- ✅ Complete country coverage per round
- ✅ Automatic round reset
- ✅ Indefinite gameplay

### Technical Quality
- Comprehensive test suite with geometric validation
- Clean separation of concerns (projection, quiz logic, GUI)
- Robust error handling and user feedback
- Optimal performance for real-time interaction
- Maintainable, well-documented code

This implementation plan provides a structured approach to building the Africa Geography Quiz Game while adhering to the test-driven development principles outlined in CLAUDE.md.