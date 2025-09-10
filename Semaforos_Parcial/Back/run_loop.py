
import time
import threading
from .controller import TrafficController
from .metrics import MetricsCollector

class SimulationLoop:
    def __init__(self, controller, metrics, update_callback=None):
        self.controller = controller
        self.metrics = metrics
        self.update_callback = update_callback
        
        self.running = False
        self.thread = None
        self.step_delay = 0.1  # 100ms entre pasos
        
    def start(self):
        """Inicia el loop de simulación"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run_loop, daemon=True)
            self.thread.start()
    
    def stop(self):
        """Detiene el loop de simulación"""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)
    
    def set_speed(self, delay):
        """Establece la velocidad de simulación (delay entre pasos)"""
        self.step_delay = max(0.01, delay)
    
    def _run_loop(self):
        """Loop principal de simulación"""
        while self.running:
            try:
                # Ejecutar un paso
                self.controller.step()
                
                # Recopilar métricas
                system_state = self.controller.get_current_state()
                self.metrics.collect_step_data(system_state)
                
                # Callback para actualizar UI
                if self.update_callback:
                    self.update_callback(system_state)
                
                # Pausa entre pasos
                time.sleep(self.step_delay)
                
            except Exception as e:
                print(f"Error en simulación: {e}")
                self.running = False
                break