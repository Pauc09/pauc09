class Config:
    def __init__(self):
        # Parámetros de las reglas de autoorganización
        self.d_distance = 50      # distancia lejana
        self.r_distance = 10      # distancia corta
        self.e_distance = 15      # distancia más allá
        self.n_threshold = 3      # umbral vehículos en rojo
        self.m_max = 2           # máximo vehículos cerca en verde
        self.u_time = 30         # tiempo mínimo en verde
        
        # Parámetros de simulación
        self.canvas_width = 600
        self.canvas_height = 400
        self.intersection_x = self.canvas_width // 2
        self.intersection_y = self.canvas_height // 2
        
        # Parámetros de vehículos
        self.vehicle_spawn_rate = 0.3
        self.vehicle_speed_min = 0.5
        self.vehicle_speed_max = 2.0
        self.vehicle_size = 10  # Tamaño visual del vehículo
        
        # Parámetros de spawn - NUEVOS
        self.spawn_ns_pct = 35    # Probabilidad de spawn Norte-Sur (%)
        self.spawn_ew_pct = 35    # Probabilidad de spawn Este-Oeste (%)
        self.spawn_distance = 150 # Distancia de spawn desde el centro
        
        # Parámetros de semáforos - NUEVOS/MEJORADOS
        self.stop_offset = 25        # Distancia de la línea de pare desde el centro
        self.brake_window = 35       # Ventana de frenado antes de la línea
        self.min_green_ticks = 18    # Tiempo mínimo en verde (ticks)
        self.max_green_ticks = 180   # Tiempo máximo en verde (ticks)
        
        # Parámetros de caos
        self.chaos_factor = 0.1
        
        # Parámetros de interfaz - NUEVOS
        self.tick_ms = 30            # Milisegundos por tick de simulación
        self.show_vehicle_ids = False # Mostrar IDs de vehículos
        self.show_distances = False   # Mostrar distancias de detección
        self.show_stop_lines = True   # Mostrar líneas de pare
        
        # Parámetros de visualización - NUEVOS
        self.road_width = 60         # Ancho de las carreteras
        self.lane_width = 25         # Ancho de carril
        self.intersection_size = 80  # Tamaño del área de intersección
        
        # Colores de la simulación - NUEVOS
        self.colors = {
            'road': '#404040',
            'intersection': '#606060',
            'stop_line': '#FFFF00',
            'light_green': '#00FF00',
            'light_red': '#FF0000',
            'light_yellow': '#FFFF00',
            'vehicle_default': '#0000FF',
            'vehicle_stopped': '#FF4444',
            'background': '#FFFFFF',
            'grid': '#E0E0E0'
        }
        
    def update_parameters(self, params):
        """Actualiza parámetros desde la interfaz"""
        for key, value in params.items():
            if hasattr(self, key):
                # Validaciones básicas
                if isinstance(value, (int, float)):
                    # Asegurar valores positivos para ciertos parámetros
                    if key in ['tick_ms', 'vehicle_speed_min', 'vehicle_speed_max', 
                              'spawn_distance', 'stop_offset', 'brake_window']:
                        value = max(1, value)
                    # Asegurar porcentajes válidos
                    elif key in ['spawn_ns_pct', 'spawn_ew_pct']:
                        value = max(0, min(100, value))
                    # Asegurar factor de caos válido
                    elif key == 'chaos_factor':
                        value = max(0.0, min(1.0, value))
                
                setattr(self, key, value)
        
        # Recalcular posición de intersección si cambian las dimensiones
        if hasattr(self, 'canvas_width') and hasattr(self, 'canvas_height'):
            self.intersection_x = self.canvas_width // 2
            self.intersection_y = self.canvas_height // 2
    
    def get_spawn_positions(self):
        """Obtiene las posiciones de spawn para cada dirección"""
        positions = {}
        cx, cy = self.intersection_x, self.intersection_y
        
        positions['N'] = (cx, cy + self.spawn_distance)  # Spawn al sur para ir al norte
        positions['S'] = (cx, cy - self.spawn_distance)  # Spawn al norte para ir al sur
        positions['E'] = (cx - self.spawn_distance, cy)  # Spawn al oeste para ir al este
        positions['W'] = (cx + self.spawn_distance, cy)  # Spawn al este para ir al oeste
        
        return positions
    
    def get_stop_lines(self):
        """Obtiene las posiciones de las líneas de pare"""
        cx, cy = self.intersection_x, self.intersection_y
        
        return {
            'N': cy + self.stop_offset,  # Línea para vehículos que van al norte
            'S': cy - self.stop_offset,  # Línea para vehículos que van al sur
            'E': cx - self.stop_offset,  # Línea para vehículos que van al este
            'W': cx + self.stop_offset   # Línea para vehículos que van al oeste
        }
    
    def validate_parameters(self):
        """Valida que todos los parámetros estén en rangos válidos"""
        # Validar dimensiones mínimas
        self.canvas_width = max(400, self.canvas_width)
        self.canvas_height = max(300, self.canvas_height)
        
        # Validar velocidades
        self.vehicle_speed_min = max(0.1, self.vehicle_speed_min)
        self.vehicle_speed_max = max(self.vehicle_speed_min, self.vehicle_speed_max)
        
        # Validar distancias
        self.spawn_distance = max(50, self.spawn_distance)
        self.stop_offset = max(10, self.stop_offset)
        self.brake_window = max(10, self.brake_window)
        
        # Validar tiempos de semáforo
        self.min_green_ticks = max(5, self.min_green_ticks)
        self.max_green_ticks = max(self.min_green_ticks * 2, self.max_green_ticks)
        
        # Validar porcentajes
        self.spawn_ns_pct = max(0, min(100, self.spawn_ns_pct))
        self.spawn_ew_pct = max(0, min(100, self.spawn_ew_pct))
        
        # Recalcular intersección
        self.intersection_x = self.canvas_width // 2
        self.intersection_y = self.canvas_height // 2
    
    def export_config(self):
        """Exporta la configuración como diccionario"""
        config_dict = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                config_dict[key] = value
        return config_dict
    
    def import_config(self, config_dict):
        """Importa configuración desde un diccionario"""
        self.update_parameters(config_dict)
        self.validate_parameters()
    
    def reset_to_defaults(self):
        """Resetea todos los parámetros a sus valores por defecto"""
        self.__init__()
    
    def get_description(self, parameter_name):
        """Obtiene descripción de un parámetro"""
        descriptions = {
            'spawn_ns_pct': 'Probabilidad de generar vehículos en eje Norte-Sur (%)',
            'spawn_ew_pct': 'Probabilidad de generar vehículos en eje Este-Oeste (%)',
            'spawn_distance': 'Distancia desde el centro donde aparecen los vehículos',
            'stop_offset': 'Distancia de la línea de pare desde el centro de la intersección',
            'brake_window': 'Distancia de frenado antes de la línea de pare',
            'n_threshold': 'Número de vehículos necesarios para considerar cambio de semáforo',
            'r_distance': 'Distancia de detección de vehículos acercándose',
            'd_distance': 'Distancia lejana para análisis de tráfico',
            'min_green_ticks': 'Tiempo mínimo que debe permanecer un semáforo en verde',
            'max_green_ticks': 'Tiempo máximo que puede permanecer un semáforo en verde',
            'vehicle_speed_min': 'Velocidad mínima de los vehículos',
            'vehicle_speed_max': 'Velocidad máxima de los vehículos',
            'chaos_factor': 'Factor de caos del sistema (0.0 = sin caos, 1.0 = máximo caos)',
            'tick_ms': 'Milisegundos por paso de simulación (menor = más rápido)'
        }
        return descriptions.get(parameter_name, f'Parámetro: {parameter_name}')
    
    def __str__(self):
        """Representación string de la configuración"""
        lines = ["=== Configuración del Sistema ==="]
        
        # Agrupar parámetros por categoría
        categories = {
            'Simulación': ['tick_ms', 'canvas_width', 'canvas_height'],
            'Vehículos': ['spawn_ns_pct', 'spawn_ew_pct', 'spawn_distance', 
                         'vehicle_speed_min', 'vehicle_speed_max', 'vehicle_size'],
            'Semáforos': ['stop_offset', 'brake_window', 'min_green_ticks', 'max_green_ticks'],
            'Detección': ['n_threshold', 'r_distance', 'd_distance'],
            'Caos': ['chaos_factor']
        }
        
        for category, params in categories.items():
            lines.append(f"\n{category}:")
            for param in params:
                if hasattr(self, param):
                    value = getattr(self, param)
                    lines.append(f"  {param}: {value}")
        
        return "\n".join(lines)