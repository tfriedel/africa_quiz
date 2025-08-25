# Specification: Africa Geography Quiz Game
1. Introduction
This document outlines the technical specification for a desktop application, the Africa Geography Quiz Game. The application is designed to be a simple and engaging educational tool for learning the locations of countries in Africa. Users are prompted with a country name and must click on its location on a borderless map of the continent. The application provides immediate visual feedback and continues indefinitely until closed.
This specification is intended for the development team and provides a comprehensive guide for implementation, testing, and architecture.
2. Requirements
2.1. Functional Requirements (Must-Have)
FR-1: Map Display: The application shall display a borderless outline of the African continent in a fixed-size window.
FR-2: Quiz Prompt: The application shall display the name of a randomly selected African country to the user.
FR-3: User Interaction: The user shall interact with the application by clicking a location on the map.
FR-4: Hit Detection: The application shall determine which country, if any, the user's click coordinates fall within.
FR-5: Correct Answer Feedback: If the clicked country matches the prompted country, the application shall fill that country's shape on the map with a solid green color.
FR-6: Incorrect Answer Feedback: If the clicked country does not match the prompted country, the application shall fill the correct (prompted) country's shape with a solid red color. The incorrectly clicked location will remain visually unchanged.
FR-7: Ocean Click Handling: A click outside of any country's polygon (e.g., in the ocean) shall be treated as an incorrect answer.
FR-8: Country Labeling: Upon being colored (either red or green), the country's name shall be displayed as a text label within its polygon.
FR-9: Cumulative Display: All correctly and incorrectly identified countries shall remain colored on the map for the duration of a round.
FR-10: Quiz Progression: The application shall cycle through all countries from the dataset once per round, without repetition.
FR-11: Round Reset: Once all countries have been prompted and colored, the application shall automatically clear the map and begin a new round with a reshuffled country list.
FR-12: Indefinite Play: The quiz shall continue with new rounds until the user manually closes the application window.
2.2. Non-Functional Requirements
NFR-1: Platform: The application shall be a desktop application built using Python.
NFR-2: GUI Framework: The graphical user interface shall be implemented using the tkinter library.
NFR-3: Testing Framework: Unit tests shall be written using the pytest framework.
NFR-4: Window Sizing: The main application window shall have a fixed, non-resizable size.
NFR-5: Data Dependency: The application shall rely on a local GeoJSON file for all geographical data.
3. Architecture
The application will be a monolithic desktop program with a clear separation between data processing, application logic, and presentation.
3.1. Key Components
Main Application (main.py):
Initializes the tkinter window and canvas.
Manages the main application loop.
Instantiates the QuizManager and CoordinateProjector.
Binds the user click event on the canvas to the appropriate handler function.
Quiz Manager (quiz.py):
A class (QuizManager) responsible for the core quiz logic.
Loads and holds the country data from the GeoJSON file.
Manages the list of countries for a round, ensuring no repetition.
Selects the next random country to prompt.
Processes user clicks, performs the point-in-polygon test using a geometry library, and determines if the answer is correct or incorrect.
Maintains the state of the current round (e.g., which countries have been guessed).
Coordinate Projector (projection.py):
A dedicated class (CoordinateProjector) responsible for converting GeoJSON geographic coordinates (latitude, longitude) into tkinter canvas pixel coordinates (x, y).
It will be initialized with the geographic bounding box of the entire dataset and the target canvas dimensions.
It will implement an equirectangular projection (linear scaling).
This component will be shared between the main application for rendering and the test suite for generating test data.
Data File (africa.geojson):
A GeoJSON file stored within the project repository.
It contains the feature collection of all African countries, including their names and polygon/multi-polygon geometries.
3.2. External Libraries
tkinter: For the GUI.
shapely: For robust geometric operations, specifically the point-in-polygon test.
pytest: For unit testing.
4. Data Handling
4.1. Data Source
A single africa.geojson file will be the sole source of geographic data. This file must be included in the application's source repository.
The application will load this file from a path relative to its execution context.
4.2. Data Loading and Processing
On startup, the QuizManager will load and parse the africa.geojson file.
The geometry data for each country will be converted into shapely Polygon/MultiPolygon objects for efficient geometric testing.
The CoordinateProjector will calculate the overall bounding box (min/max lat/lon) of all loaded geometries to establish the projection scale.
The application will transform all country geometries into canvas pixel coordinates and store them for rendering. This pre-calculation prevents redundant conversions during the quiz loop.
4.3. Data Structures
A list of Country objects (or simple dictionaries) will be maintained. Each object will store:
name (string): The country's common name.
geo_geometry (shapely object): The original geographic geometry.
canvas_geometry (list of pixel coordinates): The projected polygon(s) for drawing on the tkinter canvas.
5. API Design
Not applicable, as this is a standalone desktop application with no external APIs.
6. Error Handling
File Not Found: If africa.geojson is missing, the application shall display a fatal error message in a dialog box and terminate gracefully.
Invalid GeoJSON: If the GeoJSON file is corrupt or cannot be parsed, the application shall display a fatal error message and terminate.
7. Performance Considerations
All coordinate projection for rendering should be performed once at application startup to avoid performance degradation during user interaction.
The use of shapely for hit detection is expected to be highly performant and suitable for real-time feedback.
8. Security Measures
As a self-contained offline desktop application that does not connect to any network services, there are no significant security concerns. The application will only read from a local file packaged with it.
9. Testing Plan
9.1. Unit Testing Strategy
The primary focus of unit testing will be on the core logic components, ensuring they function correctly in isolation from the GUI.
9.2. Test Scenarios
Test Case 1: Point-in-Polygon Hit Detection
Objective: Verify that a given (x, y) coordinate is correctly mapped to the corresponding country.
Implementation (pytest):
Create a test fixture that loads the africa.geojson file and initializes the CoordinateProjector.
Write a test function that iterates through each country feature in the GeoJSON data.
For each country, calculate the geometric centroid of its polygon(s) using shapely. The centroid is guaranteed to be inside the shape.
Use the CoordinateProjector to transform the centroid's (lon, lat) coordinates into canvas (x, y) pixel coordinates.
Call the application's hit-detection method with these pixel coordinates.
Assert that the returned country name matches the name of the country from which the centroid was calculated.
Test Case 2: Multi-Polygon Handling
Objective: Ensure that clicks within any polygon of a multi-polygon country are correctly identified.
Implementation (pytest):
Extend the previous test case.
For countries with multi-polygon geometries, calculate the centroid for each individual polygon.
Run the assertion for each of these centroids, verifying that they all map back to the same parent country.
10. Implementation Timeline
This section is not applicable as no timeline was discussed.
11. Open Questions and Future Considerations
Text Label Overflow: The current specification for country labels is to use a small, fixed-size font. For very small countries or countries with long names, this text may overflow the colored boundaries. Future iterations could explore more sophisticated labeling strategies, such as dynamic font resizing, abbreviation, or placing the label outside the polygon with a leader line.
UI Styling: The visual styling (colors, fonts, window size) is defined but minimal. Future work could involve creating a more polished and configurable user interface.
Island Nations: The handling of very small island nations (e.g., São Tomé and Príncipe, Comoros) needs careful attention. Their small clickable area might pose a usability challenge.
