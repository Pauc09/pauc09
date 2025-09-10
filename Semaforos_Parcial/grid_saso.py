import tkinter as tk
import math


class TrafficGrid:
    """
    Clase para dibujar la simulación de tráfico en un canvas de Tkinter.
    Versión mejorada con mejor visualización y corrección de posiciones.
    """
    
    def __init__(self, controller, config, metrics=None):
        self.controller = controller
        self.config = config
        self.metrics = metrics
        
        # Colores mejorados
        self.colors = {
            'road': '#404040',
            'road_line': '#FFFFFF',
            'intersection': '#606060',
            'stop_line': '#FFFF00',
            'light_green': '#00FF00',
            'light_red': '#FF0000',
            'light_yellow': '#FFFF00',
            'light_frame': '#333333',
            'vehicle_moving': '#0066CC',
            'vehicle_stopped': '#CC0000',
            'vehicle_outline': '#000000',
            'background': '#FFFFFF',
            'grid': '#E0E0E0',
            'spawn_zone': '#CCFFCC',
            'detection_zone': '#FFCCCC'
        }
        
        # Configuraciones de dibujo
        self.vehicle_size = getattr(config, 'vehicle_size', 10)
        self.show_stop_lines = getattr(config, 'show_stop_lines', True)
        self.show_vehicle_ids = getattr(config, 'show_vehicle_ids', False)
        self.show_distances = getattr(config, 'show_distances', False)
        self.show_spawn_zones = False  # Para debugging
        
    def draw(self, canvas):
        """Dibuja toda la simulación en el canvas"""
        try:
            # Limpiar canvas
            canvas.delete("all")
            
            # Dibujar elementos en orden
            self._draw_background(canvas)
            if self.show_spawn_zones:
                self._draw_spawn_zones(canvas)
            if self.show_distances:
                self._draw_detection_zones(canvas)
            self._draw_roads(canvas)
            self._draw_intersection(canvas)
            if self.show_stop_lines:
                self._draw_stop_lines(canvas)
            self._draw_traffic_lights(canvas)
            self._draw_vehicles(canvas)
            self._draw_info_overlay(canvas)
            
        except Exception as e:
            print(f"Error en draw(): {e}")
            # Dibujar mensaje de error en el canvas
            canvas.create_text(
                self.config.canvas_width // 2,
                self.config.canvas_height // 2,
                text=f"Error de visualización: {str(e)[:50]}...",
                fill="red",
                font=("Arial", 12)
            )
    
    def _draw_background(self, canvas):
        """Dibuja el fondo"""
        canvas.create_rectangle(
            0, 0,
            self.config.canvas_width,
            self.config.canvas_height,
            fill=self.colors['background'],
            outline=""
        )
    
    def _draw_spawn_zones(self, canvas):
        """Dibuja las zonas de spawn para debugging"""
        cx, cy = self.config.intersection_x, self.config.intersection_y
        spawn_dist = getattr(self.config, 'spawn_distance', 150)
        zone_size = 40
        
        # Zonas de spawn
        zones = [
            (cx, cy + spawn_dist, "S→N"),  # Norte (spawn al sur)
            (cx, cy - spawn_dist, "N→S"),  # Sur (spawn al norte)
            (cx - spawn_dist, cy, "W→E"),  # Este (spawn al oeste)
            (cx + spawn_dist, cy, "E→W")   # Oeste (spawn al este)
        ]
        
        for x, y, label in zones:
            canvas.create_oval(
                x - zone_size//2, y - zone_size//2,
                x + zone_size//2, y + zone_size//2,
                fill=self.colors['spawn_zone'],
                outline=self.colors['vehicle_outline'],
                width=2
            )
            canvas.create_text(
                x, y,
                text=label,
                font=("Arial", 8),
                fill="black"
            )
    
    def _draw_detection_zones(self, canvas):
        """Dibuja las zonas de detección para debugging"""
        cx, cy = self.config.intersection_x, self.config.intersection_y
        r_dist = getattr(self.config, 'r_distance', 60)
        stop_offset = getattr(self.controller, 'STOP_OFFSET', 25)
        
        # Zonas de detección por dirección
        zones = [
            # Norte: desde línea de pare hacia el sur
            (cx - 15, cy + stop_offset, cx + 15, cy + stop_offset + r_dist),
            # Sur: desde línea de pare hacia el norte  
            (cx - 15, cy - stop_offset - r_dist, cx + 15, cy - stop_offset),
            # Este: desde línea de pare hacia el oeste
            (cx - stop_offset - r_dist, cy - 15, cx - stop_offset, cy + 15),
            # Oeste: desde línea de pare hacia el este
            (cx + stop_offset, cy - 15, cx + stop_offset + r_dist, cy + 15)
        ]
        
        for x1, y1, x2, y2 in zones:
            canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=self.colors['detection_zone'],
                stipple="gray25",
                outline=self.colors['vehicle_outline']
            )
    
    def _draw_roads(self, canvas):
        """Dibuja las carreteras"""
        cx, cy = self.config.intersection_x, self.config.intersection_y
        road_width = getattr(self.config, 'road_width', 60)
        
        # Carretera vertical (Norte-Sur)
        canvas.create_rectangle(
            cx - road_width//2, 0,
            cx + road_width//2, self.config.canvas_height,
            fill=self.colors['road'],
            outline=""
        )
        
        # Carretera horizontal (Este-Oeste)
        canvas.create_rectangle(
            0, cy - road_width//2,
            self.config.canvas_width, cy + road_width//2,
            fill=self.colors['road'],
            outline=""
        )
        
        # Líneas divisorias
        # Línea central vertical
        canvas.create_line(
            cx, 0, cx, self.config.canvas_height,
            fill=self.colors['road_line'],
            width=2,
            dash=(5, 5)
        )
        
        # Línea central horizontal
        canvas.create_line(
            0, cy, self.config.canvas_width, cy,
            fill=self.colors['road_line'],
            width=2,
            dash=(5, 5)
        )
    
    def _draw_intersection(self, canvas):
        """Dibuja la intersección central"""
        cx, cy = self.config.intersection_x, self.config.intersection_y
        intersection_size = getattr(self.config, 'intersection_size', 80)
        
        canvas.create_rectangle(
            cx - intersection_size//2, cy - intersection_size//2,
            cx + intersection_size//2, cy + intersection_size//2,
            fill=self.colors['intersection'],
            outline=self.colors['road_line'],
            width=2
        )
    
    def _draw_stop_lines(self, canvas):
        """Dibuja las líneas de pare"""
        cx, cy = self.config.intersection_x, self.config.intersection_y
        stop_offset = getattr(self.controller, 'STOP_OFFSET', 25)
        line_width = 30
        
        # Líneas de pare para cada dirección
        # Norte (vehículos vienen del sur)
        canvas.create_line(
            cx - line_width, cy + stop_offset,
            cx + line_width, cy + stop_offset,
            fill=self.colors['stop_line'],
            width=4
        )
        
        # Sur (vehículos vienen del norte)
        canvas.create_line(
            cx - line_width, cy - stop_offset,
            cx + line_width, cy - stop_offset,
            fill=self.colors['stop_line'],
            width=4
        )
        
        # Este (vehículos vienen del oeste)
        canvas.create_line(
            cx - stop_offset, cy - line_width,
            cx - stop_offset, cy + line_width,
            fill=self.colors['stop_line'],
            width=4
        )
        
        # Oeste (vehículos vienen del este)
        canvas.create_line(
            cx + stop_offset, cy - line_width,
            cx + stop_offset, cy + line_width,
            fill=self.colors['stop_line'],
            width=4
        )
    
    def _draw_traffic_lights(self, canvas):
        """Dibuja los semáforos"""
        cx, cy = self.config.intersection_x, self.config.intersection_y
        light_size = 15
        light_offset = 40
        
        # Obtener estados de los semáforos
        ns_state = self.controller.ns_light.state
        ew_state = self.controller.ew_light.state
        
        # Semáforos Norte-Sur
        positions_ns = [
            (cx - light_offset, cy - light_offset),  # Noroeste
            (cx + light_offset, cy + light_offset)   # Sureste
        ]
        
        # Semáforos Este-Oeste  
        positions_ew = [
            (cx - light_offset, cy + light_offset),  # Suroeste
            (cx + light_offset, cy - light_offset)   # Noreste
        ]
        
        # Dibujar semáforos NS
        color_ns = self.colors['light_green'] if ns_state.value == "VERDE" else self.colors['light_red']
        for x, y in positions_ns:
            self._draw_single_light(canvas, x, y, color_ns, light_size)
        
        # Dibujar semáforos EW
        color_ew = self.colors['light_green'] if ew_state.value == "VERDE" else self.colors['light_red']
        for x, y in positions_ew:
            self._draw_single_light(canvas, x, y, color_ew, light_size)
    
    def _draw_single_light(self, canvas, x, y, color, size):
        """Dibuja un semáforo individual"""
        # Marco del semáforo
        canvas.create_rectangle(
            x - size//2 - 2, y - size//2 - 2,
            x + size//2 + 2, y + size//2 + 2,
            fill=self.colors['light_frame'],
            outline="black"
        )
        
        # Luz del semáforo
        canvas.create_oval(
            x - size//2, y - size//2,
            x + size//2, y + size//2,
            fill=color,
            outline="black",
            width=2
        )
    
    def _draw_vehicles(self, canvas):
        """Dibuja todos los vehículos"""
        for vehicle in self.controller.vehicle_queue.vehicles:
            self._draw_vehicle(canvas, vehicle)
    
    def _draw_vehicle(self, canvas, vehicle):
        """Dibuja un vehículo individual"""
        x, y = vehicle.x, vehicle.y
        size = self.vehicle_size
        
        # Color según estado
        if vehicle.stopped:
            fill_color = self.colors['vehicle_stopped']
        else:
            fill_color = vehicle.color if hasattr(vehicle, 'color') else self.colors['vehicle_moving']
        
        # Forma del vehículo según dirección
        if vehicle.direction in ('N', 'S'):
            # Vehículo vertical
            points = [
                x - size//2, y - size,
                x + size//2, y - size,
                x + size//2, y + size,
                x - size//2, y + size
            ]
        else:
            # Vehículo horizontal
            points = [
                x - size, y - size//2,
                x + size, y - size//2,
                x + size, y + size//2,
                x - size, y + size//2
            ]
        
        # Dibujar vehículo
        canvas.create_polygon(
            points,
            fill=fill_color,
            outline=self.colors['vehicle_outline'],
            width=2
        )
        
        # Indicador de dirección (flecha pequeña)
        self._draw_direction_arrow(canvas, vehicle)
        
        # ID del vehículo si está habilitado
        if self.show_vehicle_ids:
            canvas.create_text(
                x, y,
                text=str(vehicle.id),
                font=("Arial", 6),
                fill="white"
            )
    
    def _draw_direction_arrow(self, canvas, vehicle):
        """Dibuja una flecha indicando la dirección del vehículo"""
        x, y = vehicle.x, vehicle.y
        arrow_size = 6
        
        # Calcular puntos de la flecha según la dirección
        if vehicle.direction == 'N':
            points = [x, y - arrow_size, x - 3, y, x + 3, y]
        elif vehicle.direction == 'S':
            points = [x, y + arrow_size, x - 3, y, x + 3, y]
        elif vehicle.direction == 'E':
            points = [x + arrow_size, y, x, y - 3, x, y + 3]
        elif vehicle.direction == 'W':
            points = [x - arrow_size, y, x, y - 3, x, y + 3]
        else:
            return
        
        canvas.create_polygon(
            points,
            fill="white",
            outline="black",
            width=1
        )
    
    def _draw_info_overlay(self, canvas):
        """Dibuja información superpuesta en el canvas"""
        # Información en la esquina superior izquierda
        info_text = []
        
        # Estadísticas básicas
        stats = self.controller.get_stats()
        info_text.append(f"Tiempo: {stats.get('sim_time', 0)}")
        info_text.append(f"Vehículos: {stats.get('queue', 0)}")
        
        # Estado de semáforos
        ns_state = "🟢" if self.controller.ns_light.state.value == "VERDE" else "🔴"
        ew_state = "🟢" if self.controller.ew_light.state.value == "VERDE" else "🔴"
        info_text.append(f"NS: {ns_state} EW: {ew_state}")
        
        # Dibujar el texto
        y_pos = 10
        for line in info_text:
            canvas.create_text(
                10, y_pos,
                text=line,
                anchor="nw",
                font=("Arial", 10, "bold"),
                fill="black"
            )
            y_pos += 15
        
        # Información en la esquina superior derecha
        corner_info = [
            f"Canvas: {self.config.canvas_width}x{self.config.canvas_height}",
            f"Centro: ({self.config.intersection_x}, {self.config.intersection_y})"
        ]
        
        y_pos = 10
        for line in corner_info:
            text_width = len(line) * 6  # Aproximación del ancho del texto
            canvas.create_text(
                self.config.canvas_width - 10, y_pos,
                text=line,
                anchor="ne",
                font=("Arial", 8),
                fill="gray"
            )
            y_pos += 12
    
    def toggle_debug_view(self):
        """Alterna la vista de debugging"""
        self.show_spawn_zones = not self.show_spawn_zones
        self.show_distances = not self.show_distances
        print(f"Vista debug: spawn_zones={self.show_spawn_zones}, distances={self.show_distances}")
    
    def update_config(self, new_config):
        """Actualiza la configuración"""
        self.config = new_config
        self.vehicle_size = getattr(new_config, 'vehicle_size', 10)
        self.show_stop_lines = getattr(new_config, 'show_stop_lines', True)
        self.show_vehicle_ids = getattr(new_config, 'show_vehicle_ids', False)