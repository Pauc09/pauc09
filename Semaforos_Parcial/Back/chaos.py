import random
import math

class ChaosEngine:
    def __init__(self):
        self.chaos_factor = 0.1
        self.lorenz_x = 1.0
        self.lorenz_y = 1.0
        self.lorenz_z = 1.0
        
        # Parámetros de Lorenz
        self.sigma = 10.0
        self.rho = 28.0
        self.beta = 8.0/3.0
        self.dt = 0.01
        
        self.history = []
        
    def set_chaos_factor(self, factor):
        """Establece el factor de caos (0.0 a 1.0)"""
        self.chaos_factor = max(0.0, min(1.0, factor))
    
    def update_lorenz(self):
        """Actualiza el sistema de Lorenz"""
        dx = self.sigma * (self.lorenz_y - self.lorenz_x) * self.dt
        dy = (self.lorenz_x * (self.rho - self.lorenz_z) - self.lorenz_y) * self.dt
        dz = (self.lorenz_x * self.lorenz_y - self.beta * self.lorenz_z) * self.dt
        
        self.lorenz_x += dx
        self.lorenz_y += dy
        self.lorenz_z += dz
        
        return self.lorenz_x, self.lorenz_y, self.lorenz_z
    
    def get_chaos_value(self):
        """Obtiene un valor caótico basado en Lorenz"""
        x, y, z = self.update_lorenz()
        
        # Normalizar el valor entre -1 y 1
        chaos_value = math.sin(x * 0.1) * self.chaos_factor
        return chaos_value
    
    def apply_chaos(self, controller):
        """Aplica caos al sistema de tráfico"""
        if self.chaos_factor <= 0:
            return
        
        chaos_val = self.get_chaos_value()
        
        # Aplicar perturbaciones aleatorias
        if abs(chaos_val) > 0.5:
            # Perturbación en la velocidad de vehículos
            for vehicle in controller.vehicle_queue.vehicles:
                if random.random() < self.chaos_factor:
                    vehicle.speed *= (1 + chaos_val * 0.3)
                    vehicle.speed = max(0.1, min(3.0, vehicle.speed))
            
            # Perturbación en los tiempos de los semáforos
            if random.random() < self.chaos_factor * 0.5:
                # Cambio caótico de semáforo
                if random.random() > 0.5:
                    controller._change_lights('NS' if random.random() > 0.5 else 'EW')
        
        # Guardar en historial para análisis
        self.history.append({
            'chaos_value': chaos_val,
            'lorenz_state': (self.lorenz_x, self.lorenz_y, self.lorenz_z),
            'vehicles_count': len(controller.vehicle_queue.vehicles)
        })
        
        # Limitar historial
        if len(self.history) > 1000:
            self.history = self.history[-500:]
    
    def get_entropy(self):
        """Calcula la entropía del sistema"""
        if len(self.history) < 10:
            return 0.0
        
        # Calcular entropía basada en variaciones del sistema
        values = [h['chaos_value'] for h in self.history[-50:]]
        
        # Discretizar valores
        bins = [-1, -0.5, 0, 0.5, 1]
        hist = [0] * (len(bins) - 1)
        
        for val in values:
            for i in range(len(bins) - 1):
                if bins[i] <= val < bins[i + 1]:
                    hist[i] += 1
                    break
        
        # Calcular entropía de Shannon
        total = sum(hist)
        if total == 0:
            return 0.0
        
        entropy = 0.0
        for count in hist:
            if count > 0:
                p = count / total
                entropy -= p * math.log2(p)
        
        return entropy
    
    def get_complexity_index(self):
        """Calcula un índice de complejidad del sistema"""
        if len(self.history) < 20:
            return 0.0
        
        # Variabilidad en el número de vehículos
        vehicle_counts = [h['vehicles_count'] for h in self.history[-20:]]
        if len(set(vehicle_counts)) == 1:
            return 0.0
        
        mean_vehicles = sum(vehicle_counts) / len(vehicle_counts)
        variance = sum((x - mean_vehicles)**2 for x in vehicle_counts) / len(vehicle_counts)
        
        return min(1.0, variance / (mean_vehicles + 1))