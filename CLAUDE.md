# Development Guidelines

This document contains critical information about working with this codebase.
Follow these guidelines precisely with a focus on test-driven development for the Africa Geography Quiz Game.

## Core Development Principles

### Fundamental Philosophy
- **Business behavior first**: Focus on what the quiz does for users (correct country identification, visual feedback)
- **Emergent design**: Let architecture evolve based on real needs from geometric calculations and UI requirements
- **Simplicity over complexity**: Choose the simplest solution that delivers educational value
- **Clear boundaries**: Separate quiz logic, coordinate projection, and UI rendering

## Rules

1. Package Management
   - ONLY use uv, NEVER pip
   - Installation: `uv add package`
   - Upgrading: `uv add --dev package --upgrade-package package`
   - FORBIDDEN: `uv pip install`, `@latest` syntax

2. Code Quality
   - Type hints required for all code
   - Follow existing patterns exactly
   - Use Google style for docstring
   - Business-focused naming: Names should describe quiz behavior, not technical details

3. Testing Requirements
   - Framework: `uv run --frozen pytest`
   - Coverage: test edge cases and errors
   - New features require tests
   - Bug fixes require regression tests
   - **Geometric testing priority**: Point-in-polygon detection and coordinate projection are critical

4. Git
   - Follow the Conventional Commits style on commit messages.

## Test-Driven Development (TDD)

### The TDD Mindset for Geographic Applications
- **Red-Green-Refactor cycle**: Write failing test → Make it pass → Improve the code
- **Tests define behavior**: Each test documents a specific quiz requirement
- **Design emergence**: Let the tests guide you to discover the right geometric abstractions
- **Refactor when valuable**: Actively look for opportunities to improve coordinate calculations and hit detection

### Critical TDD Rules
- **ONE TEST AT A TIME**: Add only a single test, see it fail (RED), implement minimal code to pass (GREEN), refactor (REFACTOR), repeat
- **MINIMAL IMPLEMENTATION**: Fix only the immediate test failure - do not implement complete functionality until tests demand it
- **NO BULK TEST ADDITION**: Never add multiple tests simultaneously - TDD Guard will block this
- **FAIL FIRST**: Always run the new test to confirm it fails before writing implementation code
- **INCREMENTAL PROGRESS**: Each test should drive one small increment of functionality

### Geographic Testing Best Practices
- **Shared geometric utilities**: Import projection logic from production code, never duplicate in tests
- **Centroid-based testing**: Use shapely centroids for reliable point-in-polygon tests as specified in DESIGN.md
- **Multi-polygon handling**: Test each polygon in multi-polygon countries separately
- **Boundary testing**: Test edge cases like ocean clicks and country borders
- **Test data from GeoJSON**: Use actual africa.geojson data for realistic geometric tests

### Refactoring Triggers for Quiz Logic
After each green test, look for:
- **Coordinate calculation duplication**: Shared projection logic that can be centralized
- **Complex hit detection**: Break down point-in-polygon logic into clear steps
- **Emerging geometric patterns**: Abstractions suggested by repeated coordinate transformations
- **Quiz state management**: Centralize round progression and country selection logic

## Code Formatting and Linting

1. Ruff
   - Format: `uv run --frozen ruff format .`
   - Check: `uv run --frozen ruff check .`
   - Fix: `uv run --frozen ruff check . --fix`
2. Pre-commit
   - Config: `.pre-commit-config.yaml`
   - Runs: on git commit
   - Tools: Ruff (Python)
