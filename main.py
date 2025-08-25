import tkinter as tk

from africa_quiz.projection import CoordinateProjector
from africa_quiz.quiz import QuizManager


class AfricaQuizApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Africa Geography Quiz")
        
        # Calculate proper canvas dimensions based on actual Africa bounds
        import json
        with open("africa.geojson") as f:
            geojson_data = json.load(f)
        
        bbox = CoordinateProjector.calculate_bbox(geojson_data)
        
        # Calculate canvas dimensions maintaining Africa's aspect ratio
        # Start with a reasonable base size and scale to maintain proportions
        base_width = 1000  # Larger base size for better visibility
        geographic_ratio = (bbox[2] - bbox[0]) / (bbox[3] - bbox[1])  # lon_range / lat_range
        
        if geographic_ratio > 1:
            # Wider than tall
            self.canvas_width = base_width
            self.canvas_height = int(base_width / geographic_ratio)
        else:
            # Taller than wide (or square)
            self.canvas_height = base_width
            self.canvas_width = int(base_width * geographic_ratio)
        
        self.projector = CoordinateProjector(bbox, self.canvas_width, self.canvas_height)
        self.quiz_manager = QuizManager("africa.geojson", self.projector)
        
        # Create prompt label
        current_country = self.quiz_manager.get_current_country()
        self.prompt_label = tk.Label(self.root, text=f"Click on: {current_country}", font=("Arial", 16, "bold"))
        self.prompt_label.pack(pady=10)
        
        # Create canvas
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="lightblue")
        self.canvas.pack()
        
        # Create status label for feedback
        self.status_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.status_label.pack(pady=5)
        
        # Bind click events
        self.canvas.bind("<Button-1>", self.on_click)
        
        # Pre-calculate canvas geometries for all countries
        self.canvas_geometries = {}
        for country_name, geo_geometry in self.quiz_manager.country_data.items():
            canvas_coords = []
            if hasattr(geo_geometry, 'geoms'):  # MultiPolygon
                for polygon in geo_geometry.geoms:
                    poly_coords = []
                    for x, y in polygon.exterior.coords:
                        canvas_x, canvas_y = self.projector.geo_to_canvas(x, y)
                        poly_coords.extend([canvas_x, canvas_y])
                    canvas_coords.append(poly_coords)
            else:  # Polygon
                poly_coords = []
                for x, y in geo_geometry.exterior.coords:
                    canvas_x, canvas_y = self.projector.geo_to_canvas(x, y)
                    poly_coords.extend([canvas_x, canvas_y])
                canvas_coords.append(poly_coords)
            
            self.canvas_geometries[country_name] = canvas_coords
        
        # Track country colors for visual feedback
        self.country_colors = {}
    
    def draw_map(self):
        # Clear canvas
        self.canvas.delete("all")
        
        # Draw all countries
        for country_name, canvas_coords_list in self.canvas_geometries.items():
            color = self.country_colors.get(country_name, "")
            outline_color = "black"
            
            for canvas_coords in canvas_coords_list:
                if len(canvas_coords) >= 6:  # Need at least 3 points (6 coordinates)
                    if color:
                        self.canvas.create_polygon(
                            canvas_coords, 
                            fill=color, 
                            outline=outline_color,
                            tags=country_name
                        )
                    else:
                        self.canvas.create_polygon(
                            canvas_coords, 
                            fill="", 
                            outline=outline_color,
                            tags=country_name
                        )
        
        # Draw country labels for colored countries
        for country_name, color in self.country_colors.items():
            if color:
                # Find centroid of first polygon for label placement
                canvas_coords = self.canvas_geometries[country_name][0]
                if len(canvas_coords) >= 6:
                    # Simple centroid calculation
                    x_coords = canvas_coords[::2]
                    y_coords = canvas_coords[1::2]
                    center_x = sum(x_coords) / len(x_coords)
                    center_y = sum(y_coords) / len(y_coords)
                    
                    self.canvas.create_text(
                        center_x, center_y,
                        text=country_name,
                        font=("Arial", 8, "bold"),
                        fill="white" if color == "red" else "black"
                    )
    
    def on_click(self, event):
        x, y = event.x, event.y
        is_correct, clicked_country = self.quiz_manager.handle_click(x, y)
        current_country = self.quiz_manager.get_current_country()
        
        if clicked_country:
            if is_correct:
                self.country_colors[clicked_country] = "green"
                self.status_label.config(text=f"Correct! {clicked_country}")
            else:
                self.country_colors[current_country] = "red"
                self.status_label.config(text=f"Incorrect. You clicked {clicked_country}, correct answer: {current_country}")
        else:
            # Ocean click
            self.country_colors[current_country] = "red"
            self.status_label.config(text=f"Ocean click. Correct answer: {current_country}")
        
        # Redraw map with new colors
        self.draw_map()
        
        # Progress to next country
        self.quiz_manager.current_country_index += 1
        
        # Update prompt for next country (or reset round)
        if self.quiz_manager.is_round_complete():
            # Show completion message and start new round
            total_countries = len(self.quiz_manager.countries)
            self.status_label.config(text=f"Round complete! You've identified all {total_countries} African countries. Starting new round...")
            self.country_colors.clear()
            self.quiz_manager.start_new_round()
            self.draw_map()  # Redraw to clear labels
            next_country = self.quiz_manager.get_current_country()
            self.prompt_label.config(text=f"Click on: {next_country}")
        else:
            next_country = self.quiz_manager.get_current_country()
            self.prompt_label.config(text=f"Click on: {next_country}")


def main() -> None:
    app = AfricaQuizApp()
    app.draw_map()  # Draw the initial map
    app.root.mainloop()


if __name__ == "__main__":
    main()
