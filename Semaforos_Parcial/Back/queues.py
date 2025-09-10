import math
import random

class Vehicle:
    def __init__(self, x, y, direction, speed=1.0):
        self.x = x
        self.y = y
        self.direction = direction  # 'N', 'S', 'E', 'W'
        self.speed = speed
        self.stopped = False
        self.wait_time = 0
        self.id = random.randint(1000, 9999)
        self.color = random.choice(['blue', 'red', 'green', 'orange', 'purple', 'brown', 'pink'])
        
        # Métricas adicionales
        self.spawn_time = 0  # Se establecerá cuando se agregue a la simulación
        self.total_distance = 0.0
        self.stops_count = 0
        self.last_stopped_state = False
    
    def move(self):
        """Mueve el vehículo según su dirección"""
        if not self.stopped:
            old_x, old_y = self.x, self.y
            
            if self.direction == 'N':
                self.y -= self.speed
            elif self.direction == 'S':
                self.y += self.speed
            elif self.direction == 'E':
                self.x += self.speed
            elif self.direction == 'W':
                self.x -= self.speed
            
            # Calcular distancia recorrida
            distance_moved = math.sqrt((self.x - old_x)**2 + (self.y - old_y)**2)
            self.total_distance += distance_moved
        else:
            self.wait_time += 1
            # Contar paradas
            if not self.last_stopped_state:
                self.stops_count += 1
        
        self.last_stopped_state = self.stopped
    
    def distance_to_intersection(self, intersection_x, intersection_y):
        """Calcula la distancia euclidiana a la intersección"""
        return math.sqrt((self.x - intersection_x)**2 + (self.y - intersection_y)**2)
    
    def distance_to_intersection_axis(self, intersection_x, intersection_y):
        """Calcula la distancia sobre el eje de movimiento a la intersección"""
        if self.direction == 'N':
            return max(0, self.y - intersection_y)
        elif self.direction == 'S':
            return max(0, intersection_y - self.y)
        elif self.direction == 'E':
            return max(0, intersection_x - self.x)
        elif self.direction == 'W':
            return max(0, self.x - intersection_x)
        return 0
    
    def is_in_lane(self, intersection_x, intersection_y, lane_width=30):
        """Verifica si el vehículo está en el carril correcto"""
        if self.direction in ('N', 'S'):
            return abs(self.x - intersection_x) <= lane_width
        else:  # E, W
            return abs(self.y - intersection_y) <= lane_width
    
    def get_stats(self):
        """Obtiene estadísticas del vehículo"""
        return {
            'id': self.id,
            'direction': self.direction,
            'position': (self.x, self.y),
            'speed': self.speed,
            'stopped': self.stopped,
            'wait_time': self.wait_time,
            'total_distance': self.total_distance,
            'stops_count': self.stops_count
        }
    
    def __repr__(self):
        return f"Vehicle({self.id}, {self.direction}, {self.x:.1f}, {self.y:.1f}, stopped={self.stopped})"

class VehicleQueue:
    def __init__(self):
        self.vehicles = []
        self.next_vehicle_id = 1000
        self.total_spawned = 0
        self.total_removed = 0
    
    def add_vehicle(self, vehicle):
        """Añade un vehículo a la cola"""
        if vehicle not in self.vehicles:
            vehicle.spawn_time = len(self.vehicles)  # Timestamp aproximado
            self.vehicles.append(vehicle)
            self.total_spawned += 1
    
    def spawn_vehicle(self, direction, config=None):
        """
        Crea y añade un vehículo en la posición correcta según su dirección
        CORREGIDO: Los vehículos aparecen ANTES de llegar al semáforo
        """
        if config is None:
            # Valores por defecto si no se proporciona config
            canvas_width = 600
            canvas_height = 400
            intersection_x = canvas_width // 2
            intersection_y = canvas_height // 2
            spawn_distance = 150
            speed_min = 0.5
            speed_max = 2.0
        else:
            canvas_width = config.canvas_width
            canvas_height = config.canvas_height
            intersection_x = config.intersection_x
            intersection_y = config.intersection_y
            spawn_distance = getattr(config, 'spawn_distance', 150)
            speed_min = getattr(config, 'vehicle_speed_min', 0.5)
            speed_max = getattr(config, 'vehicle_speed_max', 2.0)

        # Variación lateral para simular múltiples carriles
        lateral_variation = random.randint(-25, 25)
        speed = random.uniform(speed_min, speed_max)

        # Posiciones de spawn CORREGIDAS
        if direction == 'N':
            # Norte: spawn AL SUR del centro, avanzando hacia arriba (Y decrece)
            x = intersection_x + lateral_variation
            y = intersection_y + spawn_distance
        elif direction == 'S':
            # Sur: spawn AL NORTE del centro, avanzando hacia abajo (Y crece)
            x = intersection_x + lateral_variation
            y = intersection_y - spawn_distance
        elif direction == 'E':
            # Este: spawn AL OESTE del centro, avanzando hacia la derecha (X crece)
            x = intersection_x - spawn_distance
            y = intersection_y + lateral_variation
        elif direction == 'W':
            # Oeste: spawn AL ESTE del centro, avanzando hacia la izquierda (X decrece)
            x = intersection_x + spawn_distance
            y = intersection_y + lateral_variation
        else:
            raise ValueError(f"Dirección inválida: {direction}")

        # Asegurar que está dentro del canvas (con margen)
        margin = 50
        x = max(margin, min(canvas_width - margin, x))
        y = max(margin, min(canvas_height - margin, y))

        # Crear y añadir vehículo
        vehicle = Vehicle(x, y, direction, speed)
        vehicle.id = self.next_vehicle_id
        self.next_vehicle_id += 1
        
        self.add_vehicle(vehicle)
        return vehicle
    
    def remove_vehicle(self, vehicle):
        """Remueve un vehículo de la cola"""
        if vehicle in self.vehicles:
            self.vehicles.remove(vehicle)
            self.total_removed += 1
    
    def get_vehicles_by_direction(self, direction):
        """Obtiene vehículos por dirección"""
        return [v for v in self.vehicles if v.direction == direction]
    
    def get_vehicles_by_axis(self, axis):
        """Obtiene vehículos por eje (NS o EW)"""
        if axis == 'NS':
            return [v for v in self.vehicles if v.direction in ('N', 'S')]
        elif axis == 'EW':
            return [v for v in self.vehicles if v.direction in ('E', 'W')]
        return []
    
    def get_waiting_vehicles(self):
        """Obtiene vehículos que están esperando"""
        return [v for v in self.vehicles if v.stopped]
    
    def get_moving_vehicles(self):
        """Obtiene vehículos que se están moviendo"""
        return [v for v in self.vehicles if not v.stopped]
    
    def get_vehicles_near_intersection(self, intersection_x, intersection_y, radius=100):
        """Obtiene vehículos cerca de la intersección"""
        near_vehicles = []
        for v in self.vehicles:
            if v.distance_to_intersection(intersection_x, intersection_y) <= radius:
                near_vehicles.append(v)
        return near_vehicles
    
    def get_total_wait_time(self):
        """Obtiene el tiempo total de espera de todos los vehículos"""
        return sum(v.wait_time for v in self.vehicles)
    
    def get_average_wait_time(self):
        """Obtiene el tiempo promedio de espera"""
        if not self.vehicles:
            return 0.0
        return self.get_total_wait_time() / len(self.vehicles)
    
    def get_queue_stats(self):
        """Obtiene estadísticas completas de la cola"""
        if not self.vehicles:
            return {
                'total_vehicles': 0,
                'waiting_vehicles': 0,
                'moving_vehicles': 0,
                'total_wait_time': 0,
                'average_wait_time': 0.0,
                'by_direction': {'N': 0, 'S': 0, 'E': 0, 'W': 0},
                'total_spawned': self.total_spawned,
                'total_removed': self.total_removed
            }
        
        waiting = self.get_waiting_vehicles()
        moving = self.get_moving_vehicles()
        
        direction_counts = {}
        for direction in ['N', 'S', 'E', 'W']:
            direction_counts[direction] = len(self.get_vehicles_by_direction(direction))
        
        return {
            'total_vehicles': len(self.vehicles),
            'waiting_vehicles': len(waiting),
            'moving_vehicles': len(moving),
            'total_wait_time': self.get_total_wait_time(),
            'average_wait_time': self.get_average_wait_time(),
            'by_direction': direction_counts,
            'total_spawned': self.total_spawned,
            'total_removed': self.total_removed
        }
    
    def clear(self):
        """Limpia la cola"""
        self.vehicles.clear()
        self.total_spawned = 0
        self.total_removed = 0
    
    def __len__(self):
        return len(self.vehicles)
    
    def __iter__(self):
        return iter(self.vehicles)
    
    def __getitem__(self, index):
        return self.vehicles[index]