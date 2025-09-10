import random
from enum import Enum

# Imports compatibles con ambas estructuras
try:
    from Back.config import Config
    from Back.queues import VehicleQueue, Vehicle
    from Back.chaos import ChaosEngine
except Exception:
    from .config import Config
    from .queues import VehicleQueue, Vehicle
    from .chaos import ChaosEngine


class LightState(Enum):
    RED = "ROJO"
    GREEN = "VERDE"
    YELLOW = "AMARILLO"


class TrafficLight:
    def __init__(self, axis_label: str):
        # axis_label: 'NS' o 'EW'
        self.axis = axis_label
        self.state = LightState.RED
        self.time_in_state = 0
        self.total_changes = 0

    def set_state(self, new_state: LightState):
        if self.state != new_state:
            self.state = new_state
            self.time_in_state = 0
            self.total_changes += 1
        else:
            # mismo estado, solo avanza tiempo
            self.time_in_state += 1

    def update_time(self):
        self.time_in_state += 1


class TrafficController:
    """
    Controlador principal: gestiona colas, semáforos, generación y movimiento
    de vehículos, reglas de autoorganización y métricas básicas.
    """

    def __init__(self, config: Config):
        self.config = config
        self.vehicle_queue = VehicleQueue()
        self.chaos_engine = ChaosEngine()

        # Semáforos por eje
        self.ns_light = TrafficLight("NS")
        self.ew_light = TrafficLight("EW")
        self.ns_light.set_state(LightState.GREEN)
        self.ew_light.set_state(LightState.RED)

        # Métricas simples
        self.simulation_time = 0
        self.passed_ns = 0
        self.passed_ew = 0

        # Parámetros visuales/lógicos para corrección: línea de pare
        self.STOP_OFFSET = getattr(self.config, "stop_offset", 25)   # píxeles antes del centro
        self.BRAKE_WINDOW = getattr(self.config, "brake_window", 35) # ventana de frenado
        
        # Distancias de spawn - CORREGIDAS para que aparezcan ANTES del semáforo
        self.SPAWN_DISTANCE = getattr(self.config, "spawn_distance", 150)  # Distancia desde el centro

    # --------------------------
    # Hooks/servicios utilitarios
    # --------------------------
    def update_config(self, new_config: Config):
        self.config = new_config
        # si el usuario cambia offsets en caliente
        self.STOP_OFFSET = getattr(self.config, "stop_offset", self.STOP_OFFSET)
        self.BRAKE_WINDOW = getattr(self.config, "brake_window", self.BRAKE_WINDOW)
        self.SPAWN_DISTANCE = getattr(self.config, "spawn_distance", self.SPAWN_DISTANCE)

    def get_stats(self):
        return {
            "sim_time": self.simulation_time,
            "queue": len(self.vehicle_queue.vehicles),
            "passed_ns": self.passed_ns,
            "passed_ew": self.passed_ew,
            "changes_ns": self.ns_light.total_changes,
            "changes_ew": self.ew_light.total_changes,
        }

    def get_current_state(self):
        """Obtiene el estado actual del sistema para métricas"""
        return {
            'simulation_time': self.simulation_time,
            'ns_light': self.ns_light,
            'ew_light': self.ew_light,
            'vehicles': self.vehicle_queue.vehicles,
            'rule_applications': {  # Placeholder para aplicaciones de reglas
                'rule1': 0,
                'rule2': 0,
                'rule3': 0,
                'rule4': 0,
                'rule5': 0,
                'rule6': 0,
            }
        }

    # --------------------------
    # Bucle de simulación
    # --------------------------
    def step(self):
        self.simulation_time += 1

        # Generar vehículos nuevos
        self._generate_vehicles()

        # Mover existentes (con línea de pare)
        self._move_vehicles()

        # Reglas autoorganizantes (tu lógica existente)
        self._apply_traffic_rules()

        # Avanzar reloj de semáforos
        self.ns_light.update_time()
        self.ew_light.update_time()
        
        # Aplicar caos si está habilitado
        if hasattr(self.chaos_engine, 'apply_chaos'):
            self.chaos_engine.apply_chaos(self)

    # --------------------------
    # Generación de vehículos CORREGIDA
    # --------------------------
    def _generate_vehicles(self):
        """Genera vehículos en posiciones correctas ANTES de los semáforos"""
        # Probabilidades configurables (0..100)
        p_ns = getattr(self.config, "spawn_ns_pct", 35)
        p_ew = getattr(self.config, "spawn_ew_pct", 35)

        cx, cy = self.config.intersection_x, self.config.intersection_y

        if random.randint(1, 100) <= p_ns:
            # Spawns en N o S al azar - CORREGIDOS
            if random.random() < 0.5:
                # Norte: spawn AL SUR del centro, avanzando hacia el norte (Y decrece)
                spawn_x = cx + random.randint(-20, 20)  # Variación lateral
                spawn_y = cy + self.SPAWN_DISTANCE  # AL SUR del centro
                self.vehicle_queue.add_vehicle(
                    Vehicle(spawn_x, spawn_y, "N", 
                           speed=random.uniform(self.config.vehicle_speed_min, self.config.vehicle_speed_max))
                )
            else:
                # Sur: spawn AL NORTE del centro, avanzando hacia el sur (Y crece)  
                spawn_x = cx + random.randint(-20, 20)  # Variación lateral
                spawn_y = cy - self.SPAWN_DISTANCE  # AL NORTE del centro
                self.vehicle_queue.add_vehicle(
                    Vehicle(spawn_x, spawn_y, "S", 
                           speed=random.uniform(self.config.vehicle_speed_min, self.config.vehicle_speed_max))
                )

        if random.randint(1, 100) <= p_ew:
            # Spawns en E o W al azar - CORREGIDOS
            if random.random() < 0.5:
                # Este: spawn AL OESTE del centro, avanzando hacia el este (X crece)
                spawn_x = cx - self.SPAWN_DISTANCE  # AL OESTE del centro
                spawn_y = cy + random.randint(-20, 20)  # Variación lateral
                self.vehicle_queue.add_vehicle(
                    Vehicle(spawn_x, spawn_y, "E", 
                           speed=random.uniform(self.config.vehicle_speed_min, self.config.vehicle_speed_max))
                )
            else:
                # Oeste: spawn AL ESTE del centro, avanzando hacia el oeste (X decrece)
                spawn_x = cx + self.SPAWN_DISTANCE  # AL ESTE del centro
                spawn_y = cy + random.randint(-20, 20)  # Variación lateral
                self.vehicle_queue.add_vehicle(
                    Vehicle(spawn_x, spawn_y, "W", 
                           speed=random.uniform(self.config.vehicle_speed_min, self.config.vehicle_speed_max))
                )

    # --------------------------
    # Movimiento con "línea de pare" MEJORADO
    # --------------------------
    def _move_vehicles(self):
        remove_list = []

        for v in self.vehicle_queue.vehicles:
            should_stop = self._should_vehicle_stop(v)
            v.stopped = should_stop

            if should_stop:
                # "Clamp" para no pasarse de la línea - MEJORADO
                cx, cy = self.config.intersection_x, self.config.intersection_y
                if v.direction == "N":
                    stop_y = cy + self.STOP_OFFSET
                    if v.y < stop_y:
                        v.y = stop_y
                elif v.direction == "S":
                    stop_y = cy - self.STOP_OFFSET
                    if v.y > stop_y:
                        v.y = stop_y
                elif v.direction == "E":
                    stop_x = cx - self.STOP_OFFSET
                    if v.x > stop_x:
                        v.x = stop_x
                elif v.direction == "W":
                    stop_x = cx + self.STOP_OFFSET
                    if v.x < stop_x:
                        v.x = stop_x
            else:
                # Avanza normalmente
                v.move()

            # Conteo de vehículos que completan cruce (para métricas)
            if self._has_crossed(v):
                if v.direction in ("N", "S"):
                    self.passed_ns += 1
                else:
                    self.passed_ew += 1

            # Sacar si se va del canvas (con margen ampliado)
            margin = 100  # Margen más amplio para spawns lejanos
            if (v.x < -margin or v.x > self.config.canvas_width + margin or
                v.y < -margin or v.y > self.config.canvas_height + margin):
                remove_list.append(v)

        for v in remove_list:
            self.vehicle_queue.remove_vehicle(v)

    def _should_vehicle_stop(self, v) -> bool:
        """
        Determina si el vehículo debe detenerse por rojo en una LÍNEA DE PARE
        antes del centro de la intersección.
        Utiliza proyección sobre el eje de avance y ventana de frenado.
        MEJORADO: mejor lógica de detección de proximidad
        """
        cx, cy = self.config.intersection_x, self.config.intersection_y

        if v.direction == "N":
            # Se acerca desde el sur, Y decrece hacia el centro
            stop_y = cy + self.STOP_OFFSET
            if self.ns_light.state == LightState.RED:
                # Está acercándose a la línea y en ventana de frenado
                if v.y > stop_y and (v.y - stop_y) <= self.BRAKE_WINDOW:
                    return True

        elif v.direction == "S":
            # Se acerca desde el norte, Y crece hacia el centro
            stop_y = cy - self.STOP_OFFSET
            if self.ns_light.state == LightState.RED:
                # Está acercándose a la línea y en ventana de frenado
                if v.y < stop_y and (stop_y - v.y) <= self.BRAKE_WINDOW:
                    return True

        elif v.direction == "E":
            # Se acerca desde el oeste, X crece hacia el centro
            stop_x = cx - self.STOP_OFFSET
            if self.ew_light.state == LightState.RED:
                # Está acercándose a la línea y en ventana de frenado
                if v.x < stop_x and (stop_x - v.x) <= self.BRAKE_WINDOW:
                    return True

        elif v.direction == "W":
            # Se acerca desde el este, X decrece hacia el centro
            stop_x = cx + self.STOP_OFFSET
            if self.ew_light.state == LightState.RED:
                # Está acercándose a la línea y en ventana de frenado
                if v.x > stop_x and (v.x - stop_x) <= self.BRAKE_WINDOW:
                    return True

        return False

    def _has_crossed(self, v) -> bool:
        """
        Señal sencilla para métricas: considera que cruzó cuando pasa
        2*STOP_OFFSET del centro hacia el lado opuesto de su dirección.
        """
        cx, cy = self.config.intersection_x, self.config.intersection_y
        crossing_threshold = 2 * self.STOP_OFFSET

        if v.direction == "N":
            return v.y < cy - crossing_threshold
        if v.direction == "S":
            return v.y > cy + crossing_threshold
        if v.direction == "E":
            return v.x > cx + crossing_threshold
        if v.direction == "W":
            return v.x < cx - crossing_threshold
        return False

    # --------------------------
    # Reglas autoorganizantes MEJORADAS
    # --------------------------
    def _apply_traffic_rules(self):
        """
        Aplica lógica SASO/autoorganización.
        Heurística mejorada para alternar por demanda y eficiencia.
        """
        # Conteos "cerca" para decidir cambios - usando distancias configurables
        approach_distance = getattr(self.config, "r_distance", 80)
        near_ns = self._count_approaching(axis="NS", radius=approach_distance)
        near_ew = self._count_approaching(axis="EW", radius=approach_distance)
        
        # Umbrales configurables
        threshold = getattr(self.config, "n_threshold", 4)
        need_ns = near_ns >= threshold
        need_ew = near_ew >= threshold

        # Tiempo mínimo en verde para evitar cambios excesivos
        min_green = getattr(self.config, "min_green_ticks", 18)  # ~0.5s si tick=30ms
        max_green = getattr(self.config, "max_green_ticks", 180)  # ~5s máximo en verde

        current_green_time = 0
        if self.ns_light.state == LightState.GREEN:
            current_green_time = self.ns_light.time_in_state
            
            # Cambiar a EW si:
            # 1. Ha estado verde el tiempo mínimo Y hay demanda en EW
            # 2. O ha estado verde demasiado tiempo (forzar cambio)
            # 3. Y no hay mucha demanda en NS
            if ((current_green_time >= min_green and need_ew and near_ns <= threshold//2) or
                current_green_time >= max_green):
                self._switch_to("EW")
                
        elif self.ew_light.state == LightState.GREEN:
            current_green_time = self.ew_light.time_in_state
            
            # Cambiar a NS con lógica similar
            if ((current_green_time >= min_green and need_ns and near_ew <= threshold//2) or
                current_green_time >= max_green):
                self._switch_to("NS")
        else:
            # Estado inicial o transición - decidir basado en demanda
            if need_ns and not need_ew:
                self._switch_to("NS")
            elif need_ew and not need_ns:
                self._switch_to("EW")
            elif near_ns > near_ew:
                self._switch_to("NS")
            elif near_ew > near_ns:
                self._switch_to("EW")

    def _switch_to(self, axis: str):
        """Cambia los semáforos al eje especificado"""
        if axis == "NS":
            self.ns_light.set_state(LightState.GREEN)
            self.ew_light.set_state(LightState.RED)
        else:
            self.ns_light.set_state(LightState.RED)
            self.ew_light.set_state(LightState.GREEN)

    # --------------------------
    # Utilidades de conteo MEJORADAS
    # --------------------------
    def _count_approaching(self, axis: str, radius: int) -> int:
        """
        Cuenta vehículos aproximándose al eje indicado en una franja
        de radio sobre el eje de avance.
        MEJORADO: mejor detección de vehículos relevantes
        """
        cx, cy = self.config.intersection_x, self.config.intersection_y
        cnt = 0
        
        for v in self.vehicle_queue.vehicles:
            if axis == "NS" and v.direction in ("N", "S"):
                if v.direction == "N":
                    # Vehículos al SUR del centro acercándose hacia el norte
                    if cy + self.STOP_OFFSET <= v.y <= cy + self.STOP_OFFSET + radius:
                        # Solo contar si están en el carril correcto (cerca del centro X)
                        if abs(v.x - cx) <= 30:  # Tolerancia de carril
                            cnt += 1
                else:  # S
                    # Vehículos al NORTE del centro acercándose hacia el sur
                    if cy - self.STOP_OFFSET - radius <= v.y <= cy - self.STOP_OFFSET:
                        if abs(v.x - cx) <= 30:  # Tolerancia de carril
                            cnt += 1
                            
            elif axis == "EW" and v.direction in ("E", "W"):
                if v.direction == "E":
                    # Vehículos al OESTE del centro acercándose hacia el este
                    if cx - self.STOP_OFFSET - radius <= v.x <= cx - self.STOP_OFFSET:
                        if abs(v.y - cy) <= 30:  # Tolerancia de carril
                            cnt += 1
                else:  # W
                    # Vehículos al ESTE del centro acercándose hacia el oeste
                    if cx + self.STOP_OFFSET <= v.x <= cx + self.STOP_OFFSET + radius:
                        if abs(v.y - cy) <= 30:  # Tolerancia de carril
                            cnt += 1
        return cnt

    # --------------------------
    # Método de cambio forzado (para interfaz)
    # --------------------------
    def _change_lights(self, axis: str):
        """Método para cambio manual desde la interfaz o caos"""
        self._switch_to(axis)