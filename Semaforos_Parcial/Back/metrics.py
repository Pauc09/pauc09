import math
import time
from collections import defaultdict, deque
import statistics

class MetricsCollector:
    def __init__(self):
        self.start_time = time.time()
        self.step_data = []
        self.vehicle_metrics = defaultdict(list)
        self.light_change_history = deque(maxlen=100)
        self.throughput_history = deque(maxlen=50)
        
        # Métricas acumulativas
        self.total_vehicles_processed = 0
        self.total_wait_time = 0
        self.congestion_events = 0
        
    def collect_step_data(self, system_state):
        """Recopila datos de un paso de simulación"""
        current_time = time.time()
        
        step_info = {
            'timestamp': current_time,
            'simulation_time': system_state['simulation_time'],
            'ns_light_state': system_state['ns_light'].state.value,
            'ew_light_state': system_state['ew_light'].state.value,
            'ns_time_in_state': system_state['ns_light'].time_in_state,
            'ew_time_in_state': system_state['ew_light'].time_in_state,
            'total_vehicles': len(system_state['vehicles']),
            'waiting_vehicles': len([v for v in system_state['vehicles'] if v.stopped]),
            'rule_applications': system_state['rule_applications'].copy()
        }
        
        self.step_data.append(step_info)
        
        # Calcular throughput
        if len(self.step_data) >= 2:
            prev_vehicles = self.step_data[-2]['total_vehicles']
            current_vehicles = step_info['total_vehicles']
            
            # Estimar vehículos que pasaron (simplificado)
            if prev_vehicles > current_vehicles:
                vehicles_passed = prev_vehicles - current_vehicles
                self.throughput_history.append(vehicles_passed)
            else:
                self.throughput_history.append(0)
        
        # Mantener solo los últimos 500 pasos
        if len(self.step_data) > 500:
            self.step_data = self.step_data[-250:]
    
    def get_current_stats(self):
        """Obtiene estadísticas actuales"""
        if not self.step_data:
            return self._empty_stats()
        
        latest = self.step_data[-1]
        
        # Calcular métricas derivadas
        avg_wait_time = self._calculate_average_wait_time()
        throughput = self._calculate_throughput()
        congestion_level = self._calculate_congestion_level()
        
        stats = {
            'simulation_time': latest['simulation_time'],
            'total_vehicles': latest['total_vehicles'],
            'waiting_vehicles': latest['waiting_vehicles'],
            'ns_light_state': latest['ns_light_state'],
            'ew_light_state': latest['ew_light_state'],
            'ns_changes': self._count_light_changes('ns'),
            'ew_changes': self._count_light_changes('ew'),
            'avg_wait_time': avg_wait_time,
            'throughput': throughput,
            'congestion_level': congestion_level,
        }
        
        # Agregar aplicaciones de reglas
        if self.step_data:
            for rule, count in latest['rule_applications'].items():
                stats[f'{rule}_applied'] = count
        
        return stats
    
    def get_chaos_analysis(self):
        """Obtiene análisis de caos del sistema"""
        if len(self.step_data) < 10:
            return {
                'entropy': 0.0,
                'variability': 0.0,
                'complexity_index': 0.0,
                'predictability': 1.0
            }
        
        # Calcular entropía basada en cambios de estado
        state_changes = []
        for i in range(1, len(self.step_data)):
            prev = self.step_data[i-1]
            curr = self.step_data[i]
            
            changes = 0
            if prev['ns_light_state'] != curr['ns_light_state']:
                changes += 1
            if prev['ew_light_state'] != curr['ew_light_state']:
                changes += 1
            
            state_changes.append(changes)
        
        entropy = self._calculate_entropy(state_changes)
        variability = self._calculate_variability()
        complexity_index = self._calculate_complexity_index()
        predictability = max(0.0, 1.0 - (entropy + variability) / 2)
        
        return {
            'entropy': entropy,
            'variability': variability,
            'complexity_index': complexity_index,
            'predictability': predictability
        }
    
    def _empty_stats(self):
        """Estadísticas vacías"""
        return {
            'simulation_time': 0,
            'total_vehicles': 0,
            'waiting_vehicles': 0,
            'ns_light_state': 'ROJO',
            'ew_light_state': 'ROJO',
            'ns_changes': 0,
            'ew_changes': 0,
            'avg_wait_time': 0.0,
            'throughput': 0.0,
            'congestion_level': 0.0,
            'rule1_applied': 0,
            'rule2_applied': 0,
            'rule3_applied': 0,
            'rule4_applied': 0,
            'rule5_applied': 0,
            'rule6_applied': 0,
        }
    
    def _calculate_average_wait_time(self):
        """Calcula tiempo promedio de espera"""
        if len(self.step_data) < 2:
            return 0.0
        
        wait_times = [step['waiting_vehicles'] for step in self.step_data[-10:]]
        return statistics.mean(wait_times) if wait_times else 0.0
    
    def _calculate_throughput(self):
        """Calcula throughput en vehículos por minuto"""
        if len(self.throughput_history) == 0:
            return 0.0
        
        return sum(self.throughput_history) * 6  # Aproximación a veh/min
    
    def _calculate_congestion_level(self):
        """Calcula nivel de congestión"""
        if not self.step_data:
            return 0.0
        
        latest = self.step_data[-1]
        total = latest['total_vehicles']
        waiting = latest['waiting_vehicles']
        
        if total == 0:
            return 0.0
        
        return min(1.0, waiting / max(1, total))
    
    def _count_light_changes(self, direction):
        """Cuenta cambios de semáforo"""
        if len(self.step_data) < 2:
            return 0
        
        changes = 0
        state_key = f'{direction}_light_state'
        
        for i in range(1, len(self.step_data)):
            if self.step_data[i-1][state_key] != self.step_data[i][state_key]:
                changes += 1
        
        return changes
    
    def _calculate_entropy(self, sequence):
        """Calcula entropía de una secuencia"""
        if not sequence:
            return 0.0
        
        # Contar frecuencias
        freq = {}
        for item in sequence:
            freq[item] = freq.get(item, 0) + 1
        
        # Calcular entropía de Shannon
        total = len(sequence)
        entropy = 0.0
        
        for count in freq.values():
            if count > 0:
                p = count / total
                entropy -= p * math.log2(p) if p > 0 else 0
        
        return min(1.0, entropy)
    
    def _calculate_variability(self):
        """Calcula variabilidad del sistema"""
        if len(self.step_data) < 5:
            return 0.0
        
        vehicle_counts = [step['total_vehicles'] for step in self.step_data[-20:]]
        
        if len(set(vehicle_counts)) <= 1:
            return 0.0
        
        mean_count = statistics.mean(vehicle_counts)
        variance = statistics.variance(vehicle_counts)
        
        return min(1.0, variance / (mean_count + 1))
    
    def _calculate_complexity_index(self):
        """Calcula índice de complejidad"""
        if len(self.step_data) < 10:
            return 0.0
        
        # Basado en la variación de aplicaciones de reglas
        rule_applications = []
        for step in self.step_data[-10:]:
            total_rules = sum(step['rule_applications'].values())
            rule_applications.append(total_rules)
        
        if not rule_applications or max(rule_applications) == 0:
            return 0.0
        
        normalized = [x / max(rule_applications) for x in rule_applications]
        return statistics.stdev(normalized) if len(set(normalized)) > 1 else 0.0
    
    def reset(self):
        """Reinicia las métricas"""
        self.start_time = time.time()
        self.step_data.clear()
        self.vehicle_metrics.clear()
        self.light_change_history.clear()
        self.throughput_history.clear()
        self.total_vehicles_processed = 0
        self.total_wait_time = 0
        self.congestion_events = 0