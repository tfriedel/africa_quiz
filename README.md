# Africa Geography Quiz Game

An interactive educational desktop application for learning African geography. The game displays a borderless map of Africa and challenges users to identify countries by clicking on their locations. Built with Python, tkinter, and shapely using strict Test-Driven Development (TDD).

## Features

🗺️ **Interactive Map**: Borderless outline of Africa with accurate country boundaries  
🎯 **Point-and-Click Learning**: Click on countries to identify them  
✅ **Visual Feedback**: Green for correct answers, red for incorrect  
📍 **Country Labels**: Names appear on correctly identified countries  
🔄 **Progressive Learning**: Cycle through all 49 African countries  
🎮 **Endless Gameplay**: Automatic round reset with shuffled country order  
📏 **Accurate Proportions**: Proper aspect ratio matching Africa's geography  

## How to Play

1. **Launch the game**: Run `uv run python main.py`
2. **Read the prompt**: See which country to find (e.g., "Click on: Nigeria")
3. **Click on the map**: Try to click on the correct country
4. **Get feedback**: Countries turn green (correct) or red (incorrect)
5. **Learn and progress**: Continue through all 49 countries
6. **New rounds**: Game automatically starts fresh rounds indefinitely

## Technical Architecture

- **GUI Framework**: tkinter for cross-platform desktop interface
- **Geometric Operations**: shapely for accurate point-in-polygon hit detection
- **Data Source**: GeoJSON file with 49 African country boundaries
- **Coordinate System**: Equirectangular projection for geographic accuracy
- **Performance**: Pre-calculated canvas coordinates for smooth rendering

## Development Setup

After generating your project:

```bash
cd your-project-name

# Install dependencies
uv sync

# Install pre-commit hooks
uv run pre-commit install

# Run tests
uv run pytest

# Run formatting and linting (automatically runs on commit)
uv run ruff format .
uv run ruff check .
# Auto Fix
uv run ruff check . --fix
```

### Docker Development

The template includes a complete Docker setup:

```bash
# create uv.lock file
uv sync

# use the provided scripts
./docker/build.sh
./docker/run.sh # or./docker/run.sh (Command)

# Build and run with Docker Compose
docker compose build
docker compose up
```

### VS Code Devcontainer

Open the project in VS Code and use the "Reopen in Container" command for a fully configured development environment.
